import streamlit as st
import pymupdf
import io

import tempfile

# Import for unstructured extraction
from unstructured.partition.auto import partition

# Set page configuration for wide layout and title
st.set_page_config(page_title="PDF Text Extractor", layout="wide")

# Inject custom CSS for light blue background
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: lightblue;
    }
    .sidebar .sidebar-content {
        background-color: lightblue;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create two columns: left for description, right for app functionality
left_column, right_column = st.columns([1, 2])

with left_column:
    st.header("About this App")
    st.write("""
    **PDF Text Extractor App**  
    This application allows you to extract text from PDF files using two different methods:

    1. **PyMuPDF:** A robust library for PDF processing.
    2. **Unstructured:** A library that partitions the content into elements.

    Upload your PDF file on the right, choose your preferred extraction method, and download the output as a text file.
    """)

with right_column:
    st.header("Extract PDF Text")

    # Option for the user to select the extraction method
    extraction_method = st.radio("Choose extraction method:", ("PyMuPDF", "Unstructured"))

    # File uploader for PDF
    uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_pdf is not None:
        pdf_bytes = uploaded_pdf.read()

        if extraction_method == "PyMuPDF":
            # Use PyMuPDF to extract text
            doc = pymupdf.open("pdf", pdf_bytes)
            output_buffer = io.BytesIO()
            for page in doc:
                # Get the text from the page, encode it to UTF-8, and add a page delimiter
                text = page.get_text("text").encode("utf-8")
                output_buffer.write(text)
                output_buffer.write(bytes((12,)))  # form feed as page delimiter
            doc.close()
            output_buffer.seek(0)
            extraction_text = output_buffer.read().decode("utf-8")

        else:  # Unstructured method
            # Write the uploaded PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_file.flush()
                tmp_path = tmp_file.name

            # Partition the PDF using the unstructured library
            elements = partition(tmp_path)
            # Concatenate extracted elements into one string
            extraction_text = "\n\n".join([str(el) for el in elements])

        st.success("Text extraction complete!")

        # Provide a download button for the extracted text
        st.download_button(
            label="Download Extracted Text",
            data=extraction_text,
            file_name="output.txt",
            mime="text/plain"
        )

        # Optional: display a preview of the extracted text
        st.text_area("Extracted Text Preview", extraction_text, height=300)