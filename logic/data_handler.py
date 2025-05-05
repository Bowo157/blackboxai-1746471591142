import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

class DataHandler:
    def __init__(self):
        self.base_path = Path("data/uploads")
        self.forms_data_file = self.base_path / "forms_data.json"
        self.initialize_storage()

    def initialize_storage(self):
        """Initialize storage directories and files"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        if not self.forms_data_file.exists():
            self.save_forms_data([])

    def save_forms_data(self, data):
        """Save forms data to JSON file"""
        with open(self.forms_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    def load_forms_data(self):
        """Load forms data from JSON file"""
        if self.forms_data_file.exists():
            with open(self.forms_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_form_entry(self, form_data, uploaded_file=None):
        """Save a new form entry and its associated file"""
        # Add timestamp to form data
        form_data['timestamp'] = datetime.now().isoformat()
        
        # Handle file upload if present
        if uploaded_file:
            file_path = self.save_uploaded_file(uploaded_file, form_data['jenis_form'])
            form_data['file_path'] = str(file_path)

        # Load existing data
        existing_data = self.load_forms_data()
        
        # Add new entry
        existing_data.append(form_data)
        
        # Save updated data
        self.save_forms_data(existing_data)
        
        return form_data

    def save_uploaded_file(self, uploaded_file, form_type):
        """Save uploaded file to appropriate directory"""
        # Create directory for form type if it doesn't exist
        form_dir = self.base_path / form_type
        form_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = form_dir / filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path

    def get_dashboard_data(self, start_date=None, end_date=None, form_type=None, department=None):
        """Get filtered data for dashboard"""
        data = self.load_forms_data()
        df = pd.DataFrame(data)
        
        if not data:
            return pd.DataFrame()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Apply filters
        if start_date:
            df = df[df['timestamp'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['timestamp'] <= pd.to_datetime(end_date)]
        if form_type:
            df = df[df['jenis_form'] == form_type]
        if department:
            df = df[df['departemen'] == department]
            
        return df

    def get_form_types_count(self):
        """Get count of forms by type"""
        df = pd.DataFrame(self.load_forms_data())
        if df.empty:
            return pd.Series()
        return df['jenis_form'].value_counts()

    def get_risk_levels_by_department(self):
        """Get risk levels count by department"""
        df = pd.DataFrame(self.load_forms_data())
        if df.empty:
            return pd.DataFrame()
        return pd.crosstab(df['departemen'], df['tingkat_risiko'])

    def get_submissions_trend(self):
        """Get trend of form submissions over time"""
        df = pd.DataFrame(self.load_forms_data())
        if df.empty:
            return pd.Series()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.resample('D', on='timestamp').size()
