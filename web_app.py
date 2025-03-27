import streamlit as st
import pymupdf
import io
import pandas as pd

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

                # Partition the PDF using the unstructured library with hi_res strategy
                elements = partition(filename=tmp_path, strategy='hi_res', infer_table_structure=True)

                # Separate text and tables
                text_elements = [el for el in elements if el.category != "Table"]
                table_elements = [el for el in elements if el.category == "Table"]

                # Combine text elements
                extracted_text = "\n\n".join(str(el) for el in text_elements)

                # Display extracted text
                if extracted_text:
                    st.success("Text extraction complete!")
                    st.download_button(
                        label="Download Extracted Text",
                        data=extracted_text,
                        file_name="output.txt",
                        mime="text/plain"
                    )
                    st.text_area("Extracted Text Preview", extracted_text, height=300)
                else:
                    st.warning("No text found in the document.")

                # Display extracted tables
                if table_elements:
                    st.success(f"Extracted {len(table_elements)} table(s) from the document.")
                    for i, table in enumerate(table_elements):
                        try:
                            df = pd.read_html(table.metadata.text_as_html, flavor='bs4')[0]
                            st.write(f"Table {i + 1}:")
                            st.dataframe(df)

                            # Provide download button for CSV
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label=f"Download Table {i + 1} as CSV",
                                data=csv,
                                file_name=f'table_{i + 1}.csv',
                                mime='text/csv',
                            )
                        except Exception as e:
                            st.error(f"Error processing Table {i + 1}: {e}")
                else:
                    st.warning("No tables found in the document.")