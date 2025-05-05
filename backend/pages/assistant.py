import streamlit as st
from ai.huggingface_api import HuggingFaceAPI
import time
from datetime import datetime

class AIAssistantPage:
    def __init__(self):
        self.ai = HuggingFaceAPI()

    def render(self):
        st.header("AI Assistant ISO 24/7")
        
        # Add description with styling
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            🤖 Asisten AI yang siap membantu Anda dengan pertanyaan seputar:
            - Sistem Manajemen ISO (9001, 14001, 45001)
            - Prosedur Operasi Standar (SOP)
            - HIRARC (Hazard Identification, Risk Assessment & Risk Control)
            - Audit Internal
        </div>
        """, unsafe_allow_html=True)

        # Initialize chat history in session state if not exists
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Add suggested questions
        with st.expander("💡 Contoh Pertanyaan", expanded=len(st.session_state.chat_history) == 0):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **ISO 9001:**
                - Apa itu sistem manajemen mutu?
                - Bagaimana cara mengimplementasi ISO 9001?
                - Apa saja dokumen wajib ISO 9001?
                
                **SOP:**
                - Bagaimana menulis SOP yang baik?
                - Apa saja elemen wajib dalam SOP?
                - Tips review dan approval SOP?
                """)
            with col2:
                st.markdown("""
                **HIRARC:**
                - Cara mengidentifikasi bahaya?
                - Metode penilaian risiko?
                - Hierarki pengendalian risiko?
                
                **Audit:**
                - Persiapan audit internal?
                - Cara menulis temuan audit?
                - Tindak lanjut hasil audit?
                """)

        # Display chat history with timestamps
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    # For assistant messages, show timestamp and model info
                    st.markdown(message["content"])
                    st.caption(f"🕒 {message['timestamp']} | 🤖 {message['model']}")
                else:
                    # For user messages, just show the content
                    st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Tanyakan sesuatu tentang ISO...", key="chat_input"):
            # Add user message to chat history with timestamp
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response with loading spinner
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                with st.spinner("AI Assistant sedang menyiapkan jawaban..."):
                    try:
                        response, model = self.ai.get_response(prompt)
                        
                        if response:
                            # Simulate typing effect
                            for chunk in response.split():
                                full_response += chunk + " "
                                time.sleep(0.05)  # Adjust speed as needed
                                message_placeholder.markdown(full_response + "▌")
                            
                            # Format the final response
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            formatted_response = f"{response}\n\n---\n*Response generated using {model}*"
                            
                            # Add to chat history
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": formatted_response,
                                "timestamp": timestamp,
                                "model": model
                            })
                            
                            # Display final response
                            message_placeholder.markdown(formatted_response)
                            
                        else:
                            error_message = """
                            Maaf, saya mengalami kesulitan dalam memproses permintaan Anda.
                            Silakan coba lagi atau ajukan pertanyaan yang berbeda.
                            """
                            message_placeholder.error(error_message)
                            
                    except Exception as e:
                        error_message = f"""
                        Terjadi kesalahan dalam memproses permintaan Anda.
                        Detail: {str(e)}
                        """
                        message_placeholder.error(error_message)

        # Sidebar controls
        with st.sidebar:
            st.markdown("### 🛠️ Pengaturan Chat")
            
            # Clear chat history button with confirmation
            if st.session_state.chat_history:
                if st.button("🗑️ Hapus Riwayat Chat"):
                    if st.session_state.chat_history:  # Double check to prevent race conditions
                        confirm = st.button("⚠️ Konfirmasi Hapus")
                        if confirm:
                            st.session_state.chat_history = []
                            st.experimental_rerun()
            
            # Export chat history
            if st.session_state.chat_history:
                if st.button("📥 Ekspor Riwayat Chat"):
                    # Convert chat history to markdown
                    chat_export = "# Riwayat Chat D-ISO AI Assistant\n\n"
                    for msg in st.session_state.chat_history:
                        chat_export += f"## {msg['role'].title()} ({msg['timestamp']})\n"
                        chat_export += f"{msg['content']}\n\n"
                    
                    # Create download link
                    st.download_button(
                        "💾 Download Markdown",
                        chat_export,
                        "chat_history.md",
                        "text/markdown"
                    )
            
            # Display model information
            st.markdown("### ℹ️ Informasi Model")
            model_info = self.ai.get_model_info()
            st.write(f"🤖 Model Utama: {model_info['primary_model']}")
            st.write(f"🔄 Model Cadangan: {model_info['fallback_model']}")
            st.write(f"📡 Status API: {model_info['api_status']}")
            if 'context_length' in model_info:
                st.write(f"💭 Konteks: {model_info['context_length']} pesan")

def render_page():
    assistant = AIAssistantPage()
    assistant.render()

if __name__ == "__main__":
    render_page()
