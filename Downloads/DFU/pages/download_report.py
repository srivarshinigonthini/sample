import streamlit as st
import os

st.set_page_config(
    page_title="Download Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Download Medical Report")

st.write("Download your generated Diabetic Foot Ulcer report.")

report_folder = "reports"

if not os.path.exists(report_folder):
    st.warning("No reports folder found.")
else:

    pdf_files = [f for f in os.listdir(report_folder) if f.endswith(".pdf")]

    if len(pdf_files) == 0:
        st.info("No PDF reports available.")
    else:

        selected_pdf = st.selectbox(
            "Select Report",
            pdf_files
        )

        pdf_path = os.path.join(report_folder, selected_pdf)

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="⬇ Download Report",
                data=file,
                file_name=selected_pdf,
                mime="application/pdf"
            )

        st.success("Report is ready for download.")