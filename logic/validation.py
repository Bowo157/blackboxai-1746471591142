import re
from pathlib import Path

class FormValidator:
    def __init__(self):
        self.allowed_file_types = ['.pdf']
        self.max_file_size = 5 * 1024 * 1024  # 5MB

    def validate_required_fields(self, form_data, required_fields):
        """
        Validate that all required fields are present and not empty
        Returns (is_valid, error_message)
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in form_data or not str(form_data[field]).strip():
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Field berikut harus diisi: {', '.join(missing_fields)}"
        
        return True, ""

    def validate_file(self, uploaded_file):
        """
        Validate uploaded file
        Returns (is_valid, error_message)
        """
        if not uploaded_file:
            return False, "File belum diunggah"

        # Check file extension
        file_ext = Path(uploaded_file.name).suffix.lower()
        if file_ext not in self.allowed_file_types:
            return False, f"Format file tidak valid. Format yang diizinkan: {', '.join(self.allowed_file_types)}"

        # Check file size
        if uploaded_file.size > self.max_file_size:
            return False, f"Ukuran file terlalu besar. Maksimum: {self.max_file_size/1024/1024}MB"

        return True, ""

    def validate_email(self, email):
        """
        Validate email format
        Returns (is_valid, error_message)
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Format email tidak valid"
        return True, ""

    def validate_date(self, date_str):
        """
        Validate date format (YYYY-MM-DD)
        Returns (is_valid, error_message)
        """
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, date_str):
            return False, "Format tanggal harus YYYY-MM-DD"
        return True, ""

    def validate_sop_form(self, form_data, uploaded_file=None):
        """
        Validate SOP Production form
        Returns (is_valid, error_messages)
        """
        required_fields = [
            'nomor_sop',
            'judul_sop',
            'departemen',
            'tanggal_efektif',
            'penyusun',
            'reviewer',
            'approver'
        ]
        
        is_valid, error_message = self.validate_required_fields(form_data, required_fields)
        if not is_valid:
            return False, error_message

        # Validate date format
        is_valid, error_message = self.validate_date(form_data['tanggal_efektif'])
        if not is_valid:
            return False, error_message

        # Validate file if provided
        if uploaded_file:
            is_valid, error_message = self.validate_file(uploaded_file)
            if not is_valid:
                return False, error_message

        return True, ""

    def validate_hirarc_form(self, form_data, uploaded_file=None):
        """
        Validate HIRARC form
        Returns (is_valid, error_messages)
        """
        required_fields = [
            'area_kerja',
            'aktivitas',
            'bahaya',
            'risiko',
            'tingkat_risiko',
            'pengendalian',
            'pic',
            'deadline'
        ]
        
        is_valid, error_message = self.validate_required_fields(form_data, required_fields)
        if not is_valid:
            return False, error_message

        # Validate risk level
        valid_risk_levels = ['Rendah', 'Sedang', 'Tinggi']
        if form_data['tingkat_risiko'] not in valid_risk_levels:
            return False, "Tingkat risiko tidak valid"

        # Validate deadline date
        is_valid, error_message = self.validate_date(form_data['deadline'])
        if not is_valid:
            return False, error_message

        # Validate file if provided
        if uploaded_file:
            is_valid, error_message = self.validate_file(uploaded_file)
            if not is_valid:
                return False, error_message

        return True, ""

    def validate_audit_form(self, form_data, uploaded_file=None):
        """
        Validate Internal Audit form
        Returns (is_valid, error_messages)
        """
        required_fields = [
            'nomor_audit',
            'tanggal_audit',
            'departemen',
            'auditor',
            'auditee',
            'temuan',
            'kategori_temuan',
            'tindakan_perbaikan',
            'deadline'
        ]
        
        is_valid, error_message = self.validate_required_fields(form_data, required_fields)
        if not is_valid:
            return False, error_message

        # Validate dates
        for date_field in ['tanggal_audit', 'deadline']:
            is_valid, error_message = self.validate_date(form_data[date_field])
            if not is_valid:
                return False, f"Field {date_field}: {error_message}"

        # Validate finding category
        valid_categories = ['Major', 'Minor', 'Observasi']
        if form_data['kategori_temuan'] not in valid_categories:
            return False, "Kategori temuan tidak valid"

        # Validate file if provided
        if uploaded_file:
            is_valid, error_message = self.validate_file(uploaded_file)
            if not is_valid:
                return False, error_message

        return True, ""
