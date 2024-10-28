import streamlit as st
import pandas as pd
import altair as alt
from utils.token_counter import count_tokens, analyze_text_sections, get_token_distribution
from utils.file_processors import process_file

def display_token_analysis(text: str):
    """Display detailed token analysis for the given text"""
    analysis = analyze_text_sections(text)
    distribution = get_token_distribution(text)
    
    # Display total statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tokens", f"{analysis['total_tokens']:,}")
    with col2:
        st.metric("Total Paragraphs", analysis['total_paragraphs'])
    with col3:
        st.metric("Avg Tokens/Paragraph", f"{analysis['average_tokens_per_paragraph']:.1f}")
    
    # Token distribution chart
    st.subheader("Token Distribution")
    dist_df = pd.DataFrame(distribution, columns=['Category', 'Count'])
    chart = alt.Chart(dist_df).mark_bar().encode(
        x='Category',
        y='Count',
        color=alt.value("#FF4B4B")
    ).properties(height=200)
    st.altair_chart(chart, use_container_width=True)
    
    # Paragraph breakdown
    st.subheader("Paragraph Analysis")
    for para in analysis['paragraphs']:
        with st.expander(f"Paragraph {para['paragraph_number']} ({para['total_tokens']} tokens)"):
            st.text(para['text'])
            
            # Create sentence analysis table
            sentences_df = pd.DataFrame([
                {'Sentence': s['text'], 'Tokens': s['tokens']}
                for s in para['sentences']
            ])
            st.dataframe(
                sentences_df,
                column_config={
                    "Tokens": st.column_config.NumberColumn(format=",")
                },
                hide_index=True
            )

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
        .file-summary {
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            background-color: #f8f9fa;
            margin: 5px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("🔤 Token Calculator")
    st.markdown("""
        Calculate the number of tokens in your text or documents.
        Support for TXT, PDF, DOCX, CSV, XLSX, RTF, EPUB, JSON, and YAML files.
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
                display_token_analysis(text_input)
            except Exception as e:
                st.error(f"Error analyzing text: {str(e)}")
    
    with tab2:
        # Multiple file upload
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['txt', 'pdf', 'docx', 'csv', 'xlsx', 'rtf', 'epub', 'json', 'yaml', 'yml'],
            accept_multiple_files=True,
            help="Supported formats: TXT, PDF, DOCX, CSV, XLSX, RTF, EPUB, JSON, YAML"
        )
        
        if uploaded_files:
            total_tokens = 0
            file_results = []
            
            with st.spinner('Processing files...'):
                for uploaded_file in uploaded_files:
                    try:
                        # Process each file
                        text_content = process_file(uploaded_file)
                        analysis = analyze_text_sections(text_content)
                        total_tokens += analysis['total_tokens']
                        
                        file_results.append({
                            'File Name': uploaded_file.name,
                            'File Type': uploaded_file.type,
                            'Token Count': analysis['total_tokens'],
                            'Paragraphs': analysis['total_paragraphs'],
                            'Avg Tokens/Paragraph': analysis['average_tokens_per_paragraph'],
                            'Content': text_content,
                            'Analysis': analysis
                        })
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                if file_results:
                    # Display total token count
                    st.markdown(f"""
                        <div class="token-count">
                            Total Tokens: {total_tokens:,}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a DataFrame for file summary
                    summary_df = pd.DataFrame([{
                        'File Name': result['File Name'],
                        'File Type': result['File Type'],
                        'Token Count': result['Token Count'],
                        'Paragraphs': result['Paragraphs'],
                        'Avg Tokens/Paragraph': result['Avg Tokens/Paragraph']
                    } for result in file_results])
                    
                    # Display file summary
                    st.subheader("File Summary")
                    st.dataframe(
                        summary_df,
                        column_config={
                            "Token Count": st.column_config.NumberColumn(format=","),
                            "Avg Tokens/Paragraph": st.column_config.NumberColumn(format="%.1f")
                        }
                    )
                    
                    # File content expanders
                    st.subheader("File Analysis")
                    for result in file_results:
                        with st.expander(f"Analyze {result['File Name']}"):
                            display_token_analysis(result['Content'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            Made with ❤️ using Streamlit
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
