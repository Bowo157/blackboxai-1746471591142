import streamlit as st
from datetime import datetime
import pandas as pd
from logic.data_handler import DataHandler
from logic.validation import FormValidator
from logic.file_storage import FileStorage
from ai.huggingface_api import HuggingFaceAPI

class FormISOPage:
    def __init__(self):
        self.data_handler = DataHandler()
        self.validator = FormValidator()
        self.file_storage = FileStorage()
        self.ai_assistant = HuggingFaceAPI()
        
    def get_field_suggestion(self, field_name: str, form_type: str) -> str:
        """Get AI suggestion for form field"""
        return self.ai_assistant.get_field_suggestion(field_name, form_type)
        
    def render(self):
        # Add custom CSS for form styling
        st.markdown("""
        <style>
        /* Form field styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.375rem;
            transition: all 0.2s ease;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Character counter styling */
        .character-counter {
            color: #64748b;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        
        /* Form section styling */
        .form-section {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background-color: #3b82f6;
        }
        
        /* Validation message styling */
        .validation-message {
            display: flex;
            align-items: center;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 0.375rem;
            font-size: 0.875rem;
        }
        .validation-error {
            background-color: #fee2e2;
            border: 1px solid #fecaca;
            color: #991b1b;
        }
        .validation-warning {
            background-color: #fffbeb;
            border: 1px solid #fef3c7;
            color: #92400e;
        }
        </style>
        """, unsafe_allow_html=True)

        st.header("Form ISO Interaktif")
        
        # Add help text with modern styling
        st.markdown("""
        <div class='custom-box'>
            <h3 style='margin:0; color: #334155;'>
                📝 Form ISO Interaktif
            </h3>
            <p style='margin:0.5rem 0 0 0; color: #64748b; font-size: 0.9rem;'>
                Isi formulir sesuai dengan jenis dokumen ISO yang dibutuhkan. 
                Gunakan fitur AI suggestion untuk bantuan pengisian.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form type selection with icons
        form_types = {
            "SOP Produksi": "📋",
            "HIRARC": "⚠️",
            "Audit Internal": "🔍"
        }
        
        selected_type = st.selectbox(
            "Pilih Jenis Formulir",
            list(form_types.keys()),
            format_func=lambda x: f"{form_types[x]} {x}"
        )
        
        # Display appropriate form based on selection
        if selected_type == "SOP Produksi":
            self.render_sop_form()
        elif selected_type == "HIRARC":
            self.render_hirarc_form()
        elif selected_type == "Audit Internal":
            self.render_audit_form()

    def create_help_text(self, field_name: str, form_type: str) -> None:
        """Create help text with enhanced AI suggestion button"""
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button(
                f"💡 Contoh {field_name}",
                key=f"suggest_{field_name}",
                help="Klik untuk mendapatkan contoh dari AI"
            ):
                with st.spinner("Memuat saran AI..."):
                    suggestion = self.get_field_suggestion(field_name, form_type)
                    st.markdown(f"""
                    <div class='custom-box' style='background-color: #f0f9ff; border-color: #93c5fd;'>
                        <p style='margin:0; color: #1e40af; font-size: 0.9rem;'>
                            <strong>AI Suggestion:</strong><br>
                            {suggestion}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    def render_sop_form(self):
        """Render SOP Production form"""
        with st.form("sop_form", clear_on_submit=True):
            st.markdown("""
            <div class='form-section'>
                <h3 style='color: #1e293b; margin-bottom: 1rem;'>Form SOP Produksi</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Add progress indicator with custom styling
            progress = st.progress(0)
            
            # Form fields in styled columns
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                nomor_sop = st.text_input(
                    "Nomor SOP", 
                    key="sop_number",
                    help="Format: DEP-SOP-XXX",
                    placeholder="Contoh: PRD-SOP-001"
                )
                self.create_help_text("Nomor SOP", "SOP Produksi")
                
                departemen = st.selectbox(
                    "Departemen",
                    ["Produksi", "Quality Control", "Engineering", "Safety", "Maintenance"],
                    help="Pilih departemen terkait"
                )
                
                penyusun = st.text_input(
                    "Penyusun", 
                    key="sop_author",
                    help="Nama lengkap penyusun SOP"
                )
                
            with col2:
                judul_sop = st.text_input(
                    "Judul SOP", 
                    key="sop_title",
                    help="Judul yang menggambarkan prosedur"
                )
                self.create_help_text("Judul SOP", "SOP Produksi")
                
                tanggal_efektif = st.date_input(
                    "Tanggal Efektif",
                    key="sop_date",
                    help="Tanggal SOP mulai berlaku"
                )
                
                reviewer = st.text_input(
                    "Reviewer",
                    key="sop_reviewer",
                    help="Nama lengkap reviewer"
                )
            
            # Update progress
            progress.progress(0.4)
            
            approver = st.text_input(
                "Approver",
                key="sop_approver",
                help="Nama lengkap dan jabatan approver"
            )
            
            # Description with character counter
            max_chars = 500
            deskripsi = st.text_area(
                "Deskripsi SOP",
                height=100,
                key="sop_description",
                help=f"Maksimum {max_chars} karakter",
                max_chars=max_chars
            )
            chars_remaining = max_chars - len(deskripsi)
            st.caption(f"{chars_remaining} karakter tersisa")
            
            # Enhanced file upload with preview
            uploaded_file = st.file_uploader(
                "Unggah Dokumen SOP (PDF)",
                type=['pdf'],
                help="Maksimum 5MB"
            )
            
            if uploaded_file:
                st.markdown(f"""
                <div class='custom-box' style='background-color: #f0fdf4; border-color: #86efac;'>
                    <p style='margin:0; color: #166534;'>
                        <i class="fas fa-file-pdf"></i> 
                        <strong>{uploaded_file.name}</strong> ({uploaded_file.size/1024/1024:.1f} MB)
                    </p>
                    <small style='color: #166534;'>File siap untuk diunggah</small>
                </div>
                """, unsafe_allow_html=True)
                
            # Update progress
            progress.progress(0.8)
            
            # Submit button with loading state
            submit_button = st.form_submit_button(
                "Submit",
                use_container_width=True,
                type="primary"
            )
            
            if submit_button:
                with st.spinner("Menyimpan data..."):
                    form_data = {
                        "jenis_form": "SOP Produksi",
                        "nomor_sop": nomor_sop,
                        "judul_sop": judul_sop,
                        "departemen": departemen,
                        "tanggal_efektif": str(tanggal_efektif),
                        "penyusun": penyusun,
                        "reviewer": reviewer,
                        "approver": approver,
                        "deskripsi": deskripsi
                    }
                    
                    # Validate form
                    is_valid, error_message = self.validator.validate_sop_form(form_data, uploaded_file)
                    
                    if is_valid:
                        # Save form data and file
                        saved_data = self.data_handler.save_form_entry(form_data, uploaded_file)
                        progress.progress(1.0)
                        st.success("✅ Form SOP berhasil disimpan!")
                        
                        # Enhanced preview of saved data
                        with st.expander("Lihat Data Tersimpan"):
                            st.markdown("""
                            <div class='custom-box' style='background-color: #f0fdf4; border-color: #86efac;'>
                                <h4 style='margin:0 0 0.5rem 0; color: #166534;'>
                                    ✅ Data Berhasil Disimpan
                                </h4>
                            """, unsafe_allow_html=True)
                            st.json(saved_data)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='validation-message validation-error'>
                            ❌ {error_message}
                        </div>
                        """, unsafe_allow_html=True)
                        progress.progress(0)
                        
            st.markdown("</div>", unsafe_allow_html=True)

    def render_hirarc_form(self):
        """Render HIRARC form"""
        with st.form("hirarc_form", clear_on_submit=True):
            st.markdown("""
            <div class='form-section'>
                <h3 style='color: #1e293b; margin-bottom: 1rem;'>
                    Form HIRARC
                </h3>
                <p style='color: #64748b; margin: 0;'>
                    Hazard Identification, Risk Assessment & Risk Control
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add progress indicator with custom styling
            progress = st.progress(0)
            
            # Form fields in styled columns
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                area_kerja = st.text_input(
                    "Area Kerja",
                    key="hirarc_area",
                    help="Lokasi atau area spesifik"
                )
                self.create_help_text("Area Kerja", "HIRARC")
                
                # Text areas with character counters
                max_chars = 500
                
                bahaya = st.text_area(
                    "Identifikasi Bahaya",
                    height=100,
                    key="hirarc_hazard",
                    help="Deskripsi potensi bahaya",
                    max_chars=max_chars
                )
                chars_remaining = max_chars - len(bahaya)
                st.caption(f"{chars_remaining} karakter tersisa")
                self.create_help_text("Identifikasi Bahaya", "HIRARC")
                
                tingkat_risiko = st.selectbox(
                    "Tingkat Risiko",
                    ["Rendah", "Sedang", "Tinggi"],
                    key="hirarc_risk_level",
                    help="Pilih tingkat risiko sesuai analisis"
                )
                
            with col2:
                aktivitas = st.text_area(
                    "Aktivitas",
                    height=100,
                    key="hirarc_activity",
                    help="Deskripsi aktivitas yang dilakukan",
                    max_chars=max_chars
                )
                chars_remaining = max_chars - len(aktivitas)
                st.caption(f"{chars_remaining} karakter tersisa")
                
                risiko = st.text_area(
                    "Risiko",
                    height=100,
                    key="hirarc_risk",
                    help="Dampak potensial dari bahaya",
                    max_chars=max_chars
                )
                chars_remaining = max_chars - len(risiko)
                st.caption(f"{chars_remaining} karakter tersisa")
                
                pic = st.text_input(
                    "PIC",
                    key="hirarc_pic",
                    help="Penanggung jawab pengendalian"
                )
            
            # Update progress
            progress.progress(0.5)
            
            pengendalian = st.text_area(
                "Pengendalian yang Diusulkan",
                height=100,
                key="hirarc_control",
                help="Langkah-langkah pengendalian risiko",
                max_chars=max_chars
            )
            chars_remaining = max_chars - len(pengendalian)
            st.caption(f"{chars_remaining} karakter tersisa")
            self.create_help_text("Pengendalian", "HIRARC")
            
            # Real-time validation feedback
            if len(bahaya.strip()) == 0 or len(aktivitas.strip()) == 0 or len(risiko.strip()) == 0:
                st.warning("⚠️ Semua field deskripsi harus diisi")
            
            deadline = st.date_input(
                "Deadline Implementasi",
                key="hirarc_deadline",
                help="Target waktu implementasi"
            )
            
            uploaded_file = st.file_uploader(
                "Unggah Dokumen Pendukung (PDF)",
                type=['pdf'],
                help="Maksimum 5MB"
            )
            
                if uploaded_file:
                    st.markdown(f"""
                    <div class='validation-message' style='background-color: #f0fdf4; border-color: #86efac; color: #166534;'>
                        <i class="fas fa-check-circle"></i>&nbsp;
                        File <strong>{uploaded_file.name}</strong> ({uploaded_file.size/1024/1024:.1f} MB) siap diupload
                    </div>
                    """, unsafe_allow_html=True)
            
            # Update progress
            progress.progress(0.8)
            
            submitted = st.form_submit_button(
                "Submit",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                with st.spinner("Menyimpan data..."):
                    form_data = {
                        "jenis_form": "HIRARC",
                        "area_kerja": area_kerja,
                        "aktivitas": aktivitas,
                        "bahaya": bahaya,
                        "risiko": risiko,
                        "tingkat_risiko": tingkat_risiko,
                        "pengendalian": pengendalian,
                        "pic": pic,
                        "deadline": str(deadline)
                    }
                    
                    # Validate form
                    is_valid, error_message = self.validator.validate_hirarc_form(form_data, uploaded_file)
                    
                    if is_valid:
                        # Save form data and file
                        saved_data = self.data_handler.save_form_entry(form_data, uploaded_file)
                        progress.progress(1.0)
                        st.success("✅ Form HIRARC berhasil disimpan!")
                        
                        # Enhanced preview of saved data
                        with st.expander("Lihat Data Tersimpan"):
                            st.markdown("""
                            <div class='custom-box' style='background-color: #f0fdf4; border-color: #86efac;'>
                                <h4 style='margin:0 0 0.5rem 0; color: #166534;'>
                                    ✅ Data Berhasil Disimpan
                                </h4>
                            """, unsafe_allow_html=True)
                            st.json(saved_data)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='validation-message validation-error'>
                            ❌ {error_message}
                        </div>
                        """, unsafe_allow_html=True)
                        progress.progress(0)
            
            st.markdown("</div>", unsafe_allow_html=True)

    def render_audit_form(self):
        """Render Internal Audit form"""
        with st.form("audit_form", clear_on_submit=True):
            st.markdown("""
            <div class='form-section'>
                <h3 style='color: #1e293b; margin-bottom: 1rem;'>
                    Form Audit Internal
                </h3>
                <p style='color: #64748b; margin: 0;'>
                    Internal Quality Management System Audit
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add progress indicator with custom styling
            progress = st.progress(0)
            
            # Form fields in styled columns
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                nomor_audit = st.text_input(
                    "Nomor Audit",
                    key="audit_number",
                    help="Format: AUD-YYYY-XXX"
                )
                self.create_help_text("Nomor Audit", "Audit Internal")
                
                departemen = st.selectbox(
                    "Departemen",
                    ["Produksi", "Quality Control", "Engineering", "Safety", "Maintenance"],
                    help="Departemen yang diaudit"
                )
                
                auditee = st.text_input(
                    "Auditee",
                    key="audit_auditee",
                    help="Nama dan jabatan auditee"
                )
                
            with col2:
                tanggal_audit = st.date_input(
                    "Tanggal Audit",
                    key="audit_date",
                    help="Tanggal pelaksanaan audit"
                )
                
                auditor = st.text_input(
                    "Auditor",
                    key="audit_auditor",
                    help="Nama dan kualifikasi auditor"
                )
                
                kategori_temuan = st.selectbox(
                    "Kategori Temuan",
                    ["Major", "Minor", "Observasi"],
                    key="audit_category",
                    help="Klasifikasi temuan audit"
                )
            
            # Update progress
            progress.progress(0.4)
            
            # Text areas with character counters
            max_chars = 500
            
            temuan = st.text_area(
                "Temuan Audit",
                height=100,
                key="audit_finding",
                help="Deskripsi detail temuan",
                max_chars=max_chars
            )
            chars_remaining = max_chars - len(temuan)
            st.caption(f"{chars_remaining} karakter tersisa")
            self.create_help_text("Temuan Audit", "Audit Internal")
            
            tindakan_perbaikan = st.text_area(
                "Tindakan Perbaikan",
                height=100,
                key="audit_action",
                help="Rencana tindakan perbaikan",
                max_chars=max_chars
            )
            chars_remaining = max_chars - len(tindakan_perbaikan)
            st.caption(f"{chars_remaining} karakter tersisa")
            self.create_help_text("Tindakan Perbaikan", "Audit Internal")
            
            # Real-time validation feedback
            if len(temuan.strip()) == 0 or len(tindakan_perbaikan.strip()) == 0:
                st.warning("⚠️ Deskripsi temuan dan tindakan perbaikan harus diisi")
            
            deadline = st.date_input(
                "Deadline Perbaikan",
                key="audit_deadline",
                help="Target waktu penyelesaian"
            )
            
            uploaded_file = st.file_uploader(
                "Unggah Dokumen Audit (PDF)",
                type=['pdf'],
                help="Maksimum 5MB"
            )
            
            if uploaded_file:
                st.markdown(f"""
                <div class='validation-message' style='background-color: #f0fdf4; border-color: #86efac; color: #166534;'>
                    <i class="fas fa-check-circle"></i>&nbsp;
                    File <strong>{uploaded_file.name}</strong> ({uploaded_file.size/1024/1024:.1f} MB) siap diupload
                </div>
                """, unsafe_allow_html=True)
            
            # Update progress
            progress.progress(0.8)
            
            submitted = st.form_submit_button(
                "Submit",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                with st.spinner("Menyimpan data..."):
                    form_data = {
                        "jenis_form": "Audit Internal",
                        "nomor_audit": nomor_audit,
                        "tanggal_audit": str(tanggal_audit),
                        "departemen": departemen,
                        "auditor": auditor,
                        "auditee": auditee,
                        "temuan": temuan,
                        "kategori_temuan": kategori_temuan,
                        "tindakan_perbaikan": tindakan_perbaikan,
                        "deadline": str(deadline)
                    }
                    
                    # Validate form
                    is_valid, error_message = self.validator.validate_audit_form(form_data, uploaded_file)
                    
                    if is_valid:
                        # Save form data and file
                        saved_data = self.data_handler.save_form_entry(form_data, uploaded_file)
                        progress.progress(1.0)
                        st.success("✅ Form Audit Internal berhasil disimpan!")
                        
                        # Enhanced preview of saved data
                        with st.expander("Lihat Data Tersimpan"):
                            st.markdown("""
                            <div class='custom-box' style='background-color: #f0fdf4; border-color: #86efac;'>
                                <h4 style='margin:0 0 0.5rem 0; color: #166534;'>
                                    ✅ Data Berhasil Disimpan
                                </h4>
                            """, unsafe_allow_html=True)
                            st.json(saved_data)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='validation-message validation-error'>
                            ❌ {error_message}
                        </div>
                        """, unsafe_allow_html=True)
                        progress.progress(0)
            
            st.markdown("</div>", unsafe_allow_html=True)

def render_page():
    form_page = FormISOPage()
    form_page.render()

if __name__ == "__main__":
    render_page()
