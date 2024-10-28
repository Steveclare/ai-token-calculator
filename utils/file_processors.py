import PyPDF2
from docx import Document
import pandas as pd
from io import BytesIO, StringIO
import streamlit as st
import json
import yaml
from striprtf.striprtf import rtf_to_text
import ebooklib
from ebooklib import epub
import html2text

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

def process_xlsx(file_content: bytes) -> str:
    """Process XLSX files - handles multiple sheets."""
    try:
        excel_file = pd.ExcelFile(BytesIO(file_content))
        all_sheets = []
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            all_sheets.append(f'Sheet: {sheet_name}\n{df.to_string()}')
        return '\n\n'.join(all_sheets)
    except Exception as e:
        raise Exception(f'Error processing XLSX: {str(e)}')

def process_rtf(file_content: bytes) -> str:
    """Process RTF files."""
    try:
        rtf_text = file_content.decode('utf-8', errors='ignore')
        return rtf_to_text(rtf_text)
    except Exception as e:
        raise Exception(f"Error processing RTF: {str(e)}")

def process_epub(file_content: bytes) -> str:
    """Process EPUB files."""
    try:
        book = epub.read_epub(BytesIO(file_content))
        text = []
        h = html2text.HTML2Text()
        h.ignore_links = True
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8')
                text.append(h.handle(content))
        
        return "\n".join(text)
    except Exception as e:
        raise Exception(f"Error processing EPUB: {str(e)}")

def process_json(file_content: bytes) -> str:
    """Process JSON files."""
    try:
        json_data = json.loads(file_content.decode('utf-8'))
        return json.dumps(json_data, indent=2)
    except Exception as e:
        raise Exception(f"Error processing JSON: {str(e)}")

def process_yaml(file_content: bytes) -> str:
    """Process YAML files."""
    try:
        yaml_data = yaml.safe_load(file_content.decode('utf-8'))
        return yaml.dump(yaml_data, sort_keys=False, allow_unicode=True)
    except Exception as e:
        raise Exception(f"Error processing YAML: {str(e)}")

def process_file(uploaded_file) -> str:
    """
    Process different file types and return their text content
    """
    # Get the file type
    file_type = uploaded_file.type
    
    # Read the file content and seek back to start
    file_content = uploaded_file.getvalue()
    uploaded_file.seek(0)  # Reset file pointer to beginning
    
    processors = {
        'text/plain': process_txt,
        'application/pdf': process_pdf,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': process_docx,
        'text/csv': process_csv,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': process_xlsx,
        'application/rtf': process_rtf,
        'application/epub+zip': process_epub,
        'application/json': process_json,
        'application/x-yaml': process_yaml,
        'text/yaml': process_yaml
    }
    
    if file_type in processors:
        return processors[file_type](file_content)
    else:
        raise Exception(f"Unsupported file type: {file_type}")
