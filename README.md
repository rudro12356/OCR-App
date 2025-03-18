# 📝 PDF Text Extractor - Streamlit OCR App

This is a **Dockerized Streamlit app** that allows users to **upload a PDF**, extract text using **PyMuPDF or Unstructured**, and download the extracted text.

## 🚀 Features
- 📂 **Upload a PDF file**
- 📝 **Extract text** using:
  - PyMuPDF (`pymupdf`)
  - Unstructured library (`unstructured`)
- 📥 **Download extracted text** as a `.txt` file
- 🌐 **Streamlit-based web interface**
- 🐳 **Containerized using Docker for easy deployment**

---

## 📦 Pull and Run the Docker Image

Your friend can **pull and run the Docker container** with the following steps:

### 1️⃣ **Pull the Docker Image**
```bash
docker pull riokomoo12356/ocr_app:latest
```

### 2️⃣ **Run the Docker Container**
```bash
docker run -p 8501:8501 riokomoo12356/ocr_app:latest
```

### 3️⃣ **Access the App**
Open http://localhost:8501 in a web browser.

📜 Dependencies

This app uses:  
	•	streamlit  
	•	pymupdf (PyMuPDF)  
	•	unstructured  

These dependencies are installed inside the Docker container.
