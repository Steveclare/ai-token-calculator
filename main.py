import streamlit as st
from utils.token_counter import count_tokens
from utils.file_processors import process_file

def main():
    # Page config
    st.set_page_config(
        page_title="Token Calculator",
        page_icon="assets/icon.svg",
        layout="centered"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stTextArea textarea {
            font-size: 16px;
        }
        .token-count {
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("🔤 Token Calculator")
    st.markdown("""
        Calculate the number of tokens in your text or documents.
        Support for TXT, PDF, DOCX, and CSV files.
    """)
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])
    
    with tab1:
        # Text input area
        text_input = st.text_area(
            "Enter your text here:",
            height=200,
            placeholder="Paste your text here to calculate tokens..."
        )
        
        if text_input:
            try:
                token_count = count_tokens(text_input)
                st.markdown(f"""
                    <div class="token-count">
                        Token Count: {token_count:,}
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error counting tokens: {str(e)}")
    
    with tab2:
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'docx', 'csv'],
            help="Supported formats: TXT, PDF, DOCX, CSV"
        )
        
        if uploaded_file:
            try:
                with st.spinner('Processing file...'):
                    # Process the file
                    text_content = process_file(uploaded_file)
                    token_count = count_tokens(text_content)
                    
                    # Display results
                    st.markdown(f"""
                        <div class="token-count">
                            Token Count: {token_count:,}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Extracted Text"):
                        st.text_area(
                            "Extracted Text",
                            text_content,
                            height=200,
                            disabled=True
                        )
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            Made with ❤️ using Streamlit
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
