import os
from dotenv import load_dotenv
import requests
from typing import Optional, Tuple
from tenacity import retry, stop_after_attempt, wait_exponential

class HuggingFaceAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.primary_model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.fallback_model = "google/flan-t5-base"
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.context = []  # Store conversation context

    def _get_headers(self) -> dict:
        """Get headers for API request"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _format_prompt(self, query: str) -> str:
        """Format the prompt for the model with context"""
        # Include recent context in the prompt
        context_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.context[-3:]])
        
        return f"""<s>[INST] You are an ISO Management System expert assistant. 
        Previous conversation:
        {context_str}
        
        Current question about ISO standards, SOPs, HIRARC, or Auditing:
        {query}
        
        Please provide a professional, detailed, and contextually relevant response. [/INST]</s>"""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _query_model(self, model: str, query: str) -> Tuple[Optional[str], str]:
        """
        Query specific model with retry logic
        Returns tuple of (response_text or None, model_name)
        """
        try:
            url = f"{self.api_url}{model}"
            headers = self._get_headers()
            formatted_prompt = self._format_prompt(query)
            
            response = requests.post(
                url,
                headers=headers,
                json={"inputs": formatted_prompt, "parameters": {"max_length": 500}}
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract generated text based on model response format
                if model == self.primary_model:
                    generated_text = result[0]['generated_text']
                    # Clean up the response by removing the prompt
                    response_text = generated_text.split("[/INST]")[-1].strip()
                    return response_text, model
                else:
                    return result[0]['summary_text'], model
                    
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Retrying...")
            else:
                raise Exception(f"API request failed with status code: {response.status_code}")
                
            return None, model
            
        except Exception as e:
            print(f"Error querying {model}: {str(e)}")
            return None, model

    async def get_response(self, query: str) -> Tuple[str, str]:
        """
        Get response from Hugging Face model with fallback
        Returns tuple of (response_text, model_used)
        """
        # Try primary model first
        response, model = await self._query_model(self.primary_model, query)
        
        # If primary model fails, try fallback model
        if not response:
            response, model = await self._query_model(self.fallback_model, query)
            
        # Update conversation context if we got a response
        if response:
            self.context.append((query, response))
            # Keep only last 5 conversations in context
            self.context = self.context[-5:]
            
        return response or "I apologize, but I'm unable to process your request at the moment. Please try again later.", model

    def get_model_info(self) -> dict:
        """Get information about currently used models and API status"""
        api_status = "active" if self.api_key else "inactive"
        if api_status == "active":
            try:
                # Test API connection
                response = requests.get(
                    f"{self.api_url}{self.primary_model}",
                    headers=self._get_headers()
                )
                if response.status_code == 200:
                    api_status = "connected"
                else:
                    api_status = f"error (status: {response.status_code})"
            except Exception as e:
                api_status = f"error ({str(e)})"

        return {
            "primary_model": self.primary_model,
            "fallback_model": self.fallback_model,
            "api_status": api_status,
            "context_length": len(self.context)
        }

    def clear_context(self):
        """Clear conversation context"""
        self.context = []
        return True

    def get_field_suggestion(self, field_name: str, form_type: str) -> str:
        """
        Get AI suggestion for form fields
        Returns suggested text for the field
        """
        prompt = f"""Please provide a professional example or suggestion for the {field_name} field 
        in a {form_type} form. Keep it concise and relevant to ISO management systems."""
        
        try:
            response, _ = await self._query_model(self.fallback_model, prompt)
            return response or f"Example {field_name}"
        except:
            return f"Example {field_name}"
