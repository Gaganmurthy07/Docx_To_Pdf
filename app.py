import os
import streamlit as st
from docx2pdf import convert

# Page config
st.set_page_config(page_title="Word to PDF Converter", page_icon="📄", layout="centered")

st.title("📄 Word to PDF Converter")
st.write("Convert your Microsoft Word documents (.docx) into PDF format instantly.")

# Divider for clean UI look
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload your .docx file", type=["docx"])

if uploaded_file is not None:
    # Set up temp paths
    input_path = "temp_input.docx"
    output_path = "temp_output.pdf"
    
    # Save uploaded file locally
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.info(f"File uploaded: **{uploaded_file.name}**")
    
    # Conversion trigger button
    if st.button("Convert File"):
        with st.spinner("Converting document to PDF..."):
            try:
                # Perform the conversion using docx2pdf
                convert(input_path, output_path)
                
                st.success("Conversion successful!")
                
                # Read the resulting PDF for download
                with open(output_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name=uploaded_file.name.replace(".docx", ".pdf"),
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error during conversion: {e}")
            finally:
                # Cleanup input file if needed
                if os.path.exists(input_path):
                    os.remove(input_path)

# Simple footer
st.markdown("---")
st.caption("Built with Streamlit & docx2pdf")
