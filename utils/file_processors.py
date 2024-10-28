import PyPDF2
from docx import Document
import pandas as pd
from io import BytesIO
import streamlit as st

def process_txt(file_content: bytes) -> str:
    """Process text files."""
    return file_content.decode('utf-8')

def process_pdf(file_content: bytes) -> str:
    """Process PDF files."""
    text = ""
    try:
        pdf = PyPDF2.PdfReader(BytesIO(file_content))
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def process_docx(file_content: bytes) -> str:
    """Process DOCX files."""
    try:
        doc = Document(BytesIO(file_content))
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise Exception(f"Error processing DOCX: {str(e)}")

def process_csv(file_content: bytes) -> str:
    """Process CSV files."""
    try:
        df = pd.read_csv(BytesIO(file_content))
        return df.to_string()
    except Exception as e:
        raise Exception(f"Error processing CSV: {str(e)}")

def process_file(uploaded_file) -> str:
    """
    Process different file types and return their text content
    """
    file_type = uploaded_file.type
    file_content = uploaded_file.read()
    
    processors = {
        'text/plain': process_txt,
        'application/pdf': process_pdf,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': process_docx,
        'text/csv': process_csv
    }
    
    if file_type in processors:
        return processors[file_type](file_content)
    else:
        raise Exception(f"Unsupported file type: {file_type}")
