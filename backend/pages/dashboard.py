import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from logic.data_handler import DataHandler
import io
import base64

class DashboardPage:
    def __init__(self):
        self.data_handler = DataHandler()

    def render(self):
        st.header("Dashboard Evaluasi Mutu")
        
        # Add description with styling
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            📊 Visualisasi dan analisis data implementasi ISO. Gunakan filter untuk menyesuaikan tampilan data.
        </div>
        """, unsafe_allow_html=True)

        # Load data
        data = self.data_handler.load_forms_data()
        if not data:
            st.info("🔍 Belum ada data tersimpan. Silakan isi form terlebih dahulu.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Filters
        self.render_filters(df)

        # Summary metrics
        self.render_summary_metrics(df)

        # Display metrics and charts in tabs
        tab1, tab2, tab3 = st.tabs(["📊 Distribusi", "📈 Tren", "📋 Detail Data"])
        
        with tab1:
            self.render_distribution_charts(df)
        
        with tab2:
            self.render_trend_charts(df)
            
        with tab3:
            self.render_detailed_data(df)

    def render_filters(self, df):
        """Render filter controls"""
        with st.expander("🔍 Filter Data", expanded=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                # Date range filter
                min_date = df['timestamp'].min().date()
                max_date = df['timestamp'].max().date()
                
                start_date = st.date_input(
                    "Dari Tanggal",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="dashboard_start_date"
                )

            with col2:
                end_date = st.date_input(
                    "Sampai Tanggal",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="dashboard_end_date"
                )

            with col3:
                # Department filter
                departments = df['departemen'].unique().tolist()
                selected_dept = st.multiselect(
                    "Departemen",
                    departments,
                    key="dashboard_department"
                )

            # Form type filter
            form_types = df['jenis_form'].unique().tolist()
            selected_forms = st.multiselect(
                "Jenis Formulir",
                form_types,
                key="dashboard_form_type"
            )

            # Apply filters
            filtered_df = df.copy()
            
            if start_date:
                filtered_df = filtered_df[filtered_df['timestamp'].dt.date >= start_date]
            if end_date:
                filtered_df = filtered_df[filtered_df['timestamp'].dt.date <= end_date]
            if selected_dept:
                filtered_df = filtered_df[filtered_df['departemen'].isin(selected_dept)]
            if selected_forms:
                filtered_df = filtered_df[filtered_df['jenis_form'].isin(selected_forms)]

            # Update session state with filtered data
            st.session_state.filtered_df = filtered_df

    def render_summary_metrics(self, df):
        """Render summary metrics"""
        if 'filtered_df' in st.session_state:
            df = st.session_state.filtered_df

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Form",
                len(df),
                f"{len(df) - len(df[df['timestamp'].dt.date < datetime.now().date()])} hari ini"
            )
            
        with col2:
            dept_count = df['departemen'].nunique()
            st.metric(
                "Departemen Aktif",
                dept_count,
                f"{dept_count}/{len(df['departemen'].unique())} total"
            )
            
        with col3:
            risk_high = len(df[df['tingkat_risiko'] == 'Tinggi']) if 'tingkat_risiko' in df.columns else 0
            st.metric(
                "Risiko Tinggi",
                risk_high,
                "Perlu perhatian" if risk_high > 0 else "Aman"
            )
            
        with col4:
            completion_rate = (
                len(df[df['status'] == 'Completed']) / len(df) * 100
                if 'status' in df.columns else 100
            )
            st.metric(
                "Tingkat Penyelesaian",
                f"{completion_rate:.1f}%",
                "On track" if completion_rate >= 80 else "Needs attention"
            )

    def render_distribution_charts(self, df):
        """Render distribution charts"""
        if 'filtered_df' in st.session_state:
            df = st.session_state.filtered_df

        col1, col2 = st.columns(2)
        
        with col1:
            # Form type distribution
            st.subheader("Distribusi Jenis Formulir")
            form_counts = df['jenis_form'].value_counts()
            st.pie_chart(form_counts)
            
            # Show counts in a table
            st.markdown("##### Detail Jumlah per Jenis")
            count_df = pd.DataFrame({
                'Jenis Formulir': form_counts.index,
                'Jumlah': form_counts.values
            })
            st.dataframe(count_df, hide_index=True)
            
        with col2:
            # Department distribution
            st.subheader("Distribusi per Departemen")
            dept_counts = df['departemen'].value_counts()
            st.bar_chart(dept_counts)
            
            # Risk levels by department (if HIRARC data exists)
            if 'tingkat_risiko' in df.columns:
                st.markdown("##### Tingkat Risiko per Departemen")
                risk_by_dept = pd.crosstab(
                    df['departemen'],
                    df['tingkat_risiko']
                )
                st.bar_chart(risk_by_dept)

    def render_trend_charts(self, df):
        """Render trend charts"""
        if 'filtered_df' in st.session_state:
            df = st.session_state.filtered_df

        st.subheader("Tren Pengisian Form")
        
        # Daily submissions trend
        daily_submissions = df.groupby(df['timestamp'].dt.date).size()
        st.line_chart(daily_submissions)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly trend
            weekly_submissions = df.groupby(df['timestamp'].dt.isocalendar().week).size()
            st.markdown("##### Tren Mingguan")
            st.line_chart(weekly_submissions)
            
        with col2:
            # Department activity trend
            dept_weekly = pd.crosstab(
                df['timestamp'].dt.isocalendar().week,
                df['departemen']
            )
            st.markdown("##### Aktivitas Departemen")
            st.line_chart(dept_weekly)

    def render_detailed_data(self, df):
        """Render detailed data view with export options"""
        if 'filtered_df' in st.session_state:
            df = st.session_state.filtered_data

        st.subheader("Data Detail")
        
        # Export buttons
        col1, col2 = st.columns([1, 4])
        with col1:
            export_format = st.selectbox(
                "Format Export",
                ["CSV", "Excel", "JSON"]
            )
            
            if st.button("📥 Export Data"):
                if export_format == "CSV":
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="iso_data.csv">Download CSV</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                elif export_format == "Excel":
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    b64 = base64.b64encode(output.getvalue()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="iso_data.xlsx">Download Excel</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                else:  # JSON
                    json_str = df.to_json(orient='records', date_format='iso')
                    b64 = base64.b64encode(json_str.encode()).decode()
                    href = f'<a href="data:file/json;base64,{b64}" download="iso_data.json">Download JSON</a>'
                    st.markdown(href, unsafe_allow_html=True)

        # Data table with search and sort
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "timestamp": st.column_config.DatetimeColumn(
                    "Timestamp",
                    format="DD-MM-YYYY HH:mm"
                )
            }
        )

def render_page():
    dashboard = DashboardPage()
    dashboard.render()

if __name__ == "__main__":
    render_page()
