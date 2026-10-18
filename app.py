import os
import subprocess
import streamlit as st

# Page configuration
st.set_page_config(page_title="Word to PDF Converter", page_icon="📄", layout="centered")

st.title("📄 Word to PDF Converter")
st.write("Easily convert your Word documents (.docx) into PDF format.")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload your .docx file", type=["docx"])

if uploaded_file is not None:
    # Save the uploaded file locally
    input_path = "temp_input.docx"
    output_path = "temp_input.pdf"  # LibreOffice automatically names output after input stem
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.info(f"Loaded: **{uploaded_file.name}**")
    
    if st.button("Convert to PDF"):
        with st.spinner("Converting document... please wait."):
            try:
                # Use LibreOffice in headless mode
                process = subprocess.run(
                    ["libreoffice", "--headless", "--convert-to", "pdf", input_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                if process.returncode == 0 and os.path.exists(output_path):
                    st.success("Conversion complete!")
                    
                    # Read the converted PDF
                    with open(output_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Converted PDF",
                            data=pdf_file,
                            file_name=uploaded_file.name.replace(".docx", ".pdf"),
                            mime="application/pdf"
                        )
                else:
                    st.error(f"Conversion failed. Error: {process.stderr.decode('utf-8')}")
                    
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
            finally:
                # Cleanup temporary files
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)

st.markdown("---")
st.caption("Powered by Streamlit & LibreOffice")
