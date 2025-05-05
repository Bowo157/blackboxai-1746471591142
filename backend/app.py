import streamlit as st
import os
from pathlib import Path
from streamlit_lottie import st_lottie
import requests
import json

# Set page config
st.set_page_config(
    page_title="D-ISO Hybrid System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Beranda"

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def header():
    """Display header with modern logo and title"""
    col1, col2 = st.columns([1, 4])
    with col1:
        # Modern abstract logo animation
        lottie_url = "https://assets2.lottiefiles.com/packages/lf20_kkflmtur.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=100, key="logo")
        else:
            # Professional fallback image
            st.image("https://img.icons8.com/fluency/96/000000/workflow.png", width=100)
    
    with col2:
        st.title("D-ISO Hybrid System")
        st.markdown("""
        <div class='custom-box'>
            <h3 style='margin:0; color: #334155;'>
                Platform Digital Interaktif untuk Sistem Manajemen ISO
            </h3>
            <p style='margin:0.5rem 0 0 0; color: #64748b; font-size: 0.9rem;'>
                Solusi modern untuk implementasi ISO 9001, 14001, dan 45001
            </p>
        </div>
        """, unsafe_allow_html=True)

def footer():
    """Display footer with copyright information"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
                © 2024 D-ISO Hybrid System. All rights reserved.<br>
                <small>Powered by Streamlit & Hugging Face AI</small>
            </div>
            """,
            unsafe_allow_html=True
        )

def sidebar_navigation():
    """Create modern sidebar navigation"""
    with st.sidebar:
        st.sidebar.title("Menu Navigasi")
        
        # Navigation menu with icons
        with st.container():
            st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
            pages = {
                "Beranda": "🏠",
                "Form ISO": "📝",
                "Dashboard": "📊",
                "AI Assistant": "🤖"
            }
            
            # Create radio buttons with icons
            selected = st.radio(
                "",
                list(pages.keys()),
                format_func=lambda x: f"{pages[x]} {x}"
            )
            st.session_state.current_page = selected
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced system status
        with st.expander("System Status"):
            # Check if data directory exists
            data_status = "active" if Path("data/uploads").exists() else "inactive"
            # Check if .env exists for AI service
            ai_status = "active" if Path(".env").exists() else "inactive"
            
            st.markdown(f"""
                <div class='status-indicator status-{data_status}'>
                    {'✓' if data_status == 'active' else '×'} Database: {data_status.title()}
                </div>
                <br>
                <div class='status-indicator status-{data_status}'>
                    {'✓' if data_status == 'active' else '×'} File Storage: {data_status.title()}
                </div>
                <br>
                <div class='status-indicator status-{ai_status}'>
                    {'✓' if ai_status == 'active' else '×'} AI Service: {ai_status.title()}
                </div>
            """, unsafe_allow_html=True)

def home_page():
    """Display modern home page with enhanced animations"""
    # Welcome section with animation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class='custom-box'>
            <h1 style='color: #1e293b; margin-bottom: 1rem;'>
                Selamat Datang di D-ISO Hybrid System
            </h1>
            <p style='color: #475569; font-size: 1.1rem; line-height: 1.6;'>
                Platform digital interaktif untuk membantu organisasi dalam menerapkan 
                sistem manajemen ISO secara efektif dan efisien.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced feature highlights with modern styling
        st.markdown("""
        <div class='custom-box'>
            <h3 style='color: #1e293b; margin-bottom: 1rem;'>
                Sistem Manajemen yang Didukung:
            </h3>
            
            <div class='feature-card'>
                <h4 style='color: #0f766e; margin: 0;'>
                    🏆 ISO 9001 - Sistem Manajemen Mutu
                </h4>
                <ul style='color: #475569; margin: 0.5rem 0;'>
                    <li>Standarisasi proses bisnis</li>
                    <li>Peningkatan kepuasan pelanggan</li>
                    <li>Dokumentasi yang terstruktur</li>
                </ul>
            </div>
            
            <div class='feature-card'>
                <h4 style='color: #15803d; margin: 0;'>
                    🌿 ISO 14001 - Sistem Manajemen Lingkungan
                </h4>
                <ul style='color: #475569; margin: 0.5rem 0;'>
                    <li>Pengelolaan dampak lingkungan</li>
                    <li>Kepatuhan regulasi</li>
                    <li>Efisiensi sumber daya</li>
                </ul>
            </div>
            
            <div class='feature-card'>
                <h4 style='color: #9333ea; margin: 0;'>
                    🛡️ ISO 45001 - Sistem Manajemen K3
                </h4>
                <ul style='color: #475569; margin: 0.5rem 0;'>
                    <li>Keselamatan kerja</li>
                    <li>Kesehatan karyawan</li>
                    <li>Manajemen risiko</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Add workspace animation
        workspace_url = "https://lottie.host/c99f1d8d-4691-4d35-a2c2-d99c8e5259e0/Ht9yJq9bQs.json"
        workspace_animation = load_lottie_url(workspace_url)
        if workspace_animation:
            st_lottie(workspace_animation, key="workspace")
    
    # Main features section
    st.markdown("---")
    st.subheader("Fitur Utama")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📝 Form ISO Interaktif
        - Input data terstruktur
        - Validasi otomatis
        - Upload dokumen pendukung
        - AI-powered suggestions
        """)
        
    with col2:
        st.markdown("""
        ### 📊 Dashboard Evaluasi
        - Visualisasi real-time
        - Analisis tren
        - Filter data interaktif
        - Export laporan
        """)
        
    with col3:
        st.markdown("""
        ### 🤖 AI Assistant
        - Bantuan 24/7
        - Jawaban kontekstual
        - Pembelajaran adaptif
        - Multi-bahasa support
        """)
    
    # Quick start guide
    st.markdown("---")
    with st.expander("🚀 Quick Start Guide"):
        st.markdown("""
        1. **Form ISO**: Mulai dengan mengisi form sesuai kebutuhan Anda
        2. **Dashboard**: Pantau progress dan analisis data
        3. **AI Assistant**: Dapatkan bantuan untuk pertanyaan seputar ISO
        
        Butuh bantuan? Gunakan fitur AI Assistant atau hubungi support team kami.
        """)

def main():
    """Main function to run the application"""
    # Create required directories if they don't exist
    Path("data/uploads").mkdir(parents=True, exist_ok=True)
    
    # Apply custom CSS for modern styling
    st.markdown("""
        <style>
        /* Main app container */
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Typography */
        .st-emotion-cache-16txtl3 h1 {
            font-weight: 600;
            color: #1f1f1f;
            margin-bottom: 1rem;
        }
        .st-emotion-cache-16txtl3 h2 {
            font-weight: 500;
            color: #2c3e50;
            margin-bottom: 0.75rem;
        }
        .st-emotion-cache-16txtl3 h3 {
            font-weight: 500;
            color: #34495e;
            margin-bottom: 0.5rem;
        }
        
        /* Custom containers */
        .custom-box {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Sidebar styling */
        .sidebar-nav {
            background-color: #f8fafc;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid #e2e8f0;
        }
        
        /* Button styling */
        .stButton button {
            border-radius: 0.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        .status-active {
            background-color: #dcfce7;
            color: #166534;
        }
        .status-inactive {
            background-color: #fee2e2;
            color: #991b1b;
        }
        
        /* Feature card */
        .feature-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 0.5rem 0;
            transition: all 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display header
    header()
    
    # Setup navigation
    sidebar_navigation()
    
    # Route to appropriate page based on selection
    if st.session_state.current_page == "Beranda":
        home_page()
    elif st.session_state.current_page == "Form ISO":
        from pages.form_iso import render_page as render_form
        render_form()
    elif st.session_state.current_page == "Dashboard":
        from pages.dashboard import render_page as render_dashboard
        render_dashboard()
    elif st.session_state.current_page == "AI Assistant":
        from pages.assistant import render_page as render_assistant
        render_assistant()
    
    # Display footer
    footer()

if __name__ == "__main__":
    main()
