import os
from pathlib import Path
from datetime import datetime
import shutil

class FileStorage:
    def __init__(self):
        self.base_path = Path("data/uploads")
        self.initialize_storage()

    def initialize_storage(self):
        """Initialize storage directories"""
        # Create base directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different form types
        form_types = ['SOP_Produksi', 'HIRARC', 'Audit_Internal']
        for form_type in form_types:
            (self.base_path / form_type).mkdir(exist_ok=True)

    def save_file(self, uploaded_file, form_type, identifier):
        """
        Save uploaded file with proper naming and organization
        Returns the relative path to the saved file
        """
        if not uploaded_file:
            return None

        # Clean form type string for directory name
        form_dir = self.base_path / form_type.replace(" ", "_")
        form_dir.mkdir(exist_ok=True)

        # Generate unique filename with timestamp and identifier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_filename = uploaded_file.name.replace(" ", "_")
        filename = f"{timestamp}_{identifier}_{clean_filename}"
        file_path = form_dir / filename

        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Return relative path from base_path
        return str(file_path.relative_to(self.base_path))

    def get_file_path(self, relative_path):
        """Get absolute file path from relative path"""
        return self.base_path / relative_path

    def delete_file(self, relative_path):
        """Delete file by relative path"""
        file_path = self.base_path / relative_path
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def list_files(self, form_type=None):
        """
        List all files or files for specific form type
        Returns list of relative paths
        """
        if form_type:
            search_path = self.base_path / form_type.replace(" ", "_")
        else:
            search_path = self.base_path

        files = []
        if search_path.exists():
            for file_path in search_path.rglob("*"):
                if file_path.is_file():
                    files.append(str(file_path.relative_to(self.base_path)))
        return files

    def get_file_info(self, relative_path):
        """
        Get file information
        Returns dict with file details
        """
        file_path = self.base_path / relative_path
        if not file_path.exists():
            return None

        return {
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'created': datetime.fromtimestamp(file_path.stat().st_ctime),
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
            'path': str(relative_path)
        }

    def move_file(self, relative_path, new_form_type):
        """
        Move file to different form type directory
        Returns new relative path
        """
        current_path = self.base_path / relative_path
        if not current_path.exists():
            return None

        new_dir = self.base_path / new_form_type.replace(" ", "_")
        new_dir.mkdir(exist_ok=True)
        new_path = new_dir / current_path.name

        shutil.move(str(current_path), str(new_path))
        return str(new_path.relative_to(self.base_path))

    def cleanup_old_files(self, days_old=30):
        """
        Remove files older than specified days
        Returns number of files removed
        """
        cutoff = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        count = 0

        for file_path in self.base_path.rglob("*"):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff:
                file_path.unlink()
                count += 1

        return count
