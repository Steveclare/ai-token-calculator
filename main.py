import streamlit as st
import pandas as pd
import altair as alt
from utils.token_counter import count_tokens, analyze_text_sections, get_token_distribution
from utils.file_processors import process_file
from utils.cost_calculator import calculate_costs, get_context_window_info, MODEL_CONFIGS

def format_model_name(model: str) -> str:
    """Format model name with context window and CPM information"""
    config = MODEL_CONFIGS[model]
    context_k = config['context_window'] // 1000
    input_cpm = config['input_cost'] * 1000  # Convert to cost per million
    output_cpm = config['output_cost'] * 1000  # Convert to cost per million
    return f"{model} (Context: {context_k}K, CPM: ${input_cpm:.2f} / ${output_cpm:.2f})"

def display_cost_analysis(token_count: int, selected_model: str):
    """Display cost analysis for the given token count and model"""
    costs = calculate_costs(token_count, selected_model)
    context_window, fits_context = get_context_window_info(token_count, selected_model)
    
    # Display context window info
    st.info(
        f"Context Window: {context_window:,} tokens\n\n" +
        ("✅ Text fits within context window" if fits_context else "⚠️ Text exceeds context window")
    )
    
    # Create cost breakdown table
    cost_df = pd.DataFrame([
        {"Scenario": "Input Only", "Cost ($)": costs['input_only']},
        {"Scenario": "Output Only", "Cost ($)": costs['output_only']},
        {"Scenario": "Equal Input/Output", "Cost ($)": costs['input_output_equal']}
    ])
    
    st.subheader("Estimated Costs")
    st.dataframe(
        cost_df,
        column_config={
            "Cost ($)": st.column_config.NumberColumn(format="$%.4f")
        },
        hide_index=True
    )

def display_token_analysis(text: str, selected_model: str):
    """Display simplified token analysis for the given text"""
    analysis = analyze_text_sections(text, selected_model)
    distribution = get_token_distribution(text, selected_model)
    
    # Display total statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tokens", f"{analysis['total_tokens']:,}")
    with col2:
        st.metric("Total Paragraphs", analysis['total_paragraphs'])
    
    # Display cost analysis
    display_cost_analysis(analysis['total_tokens'], selected_model)
    
    # Token distribution chart
    st.subheader("Token Distribution")
    dist_df = pd.DataFrame(distribution, columns=['Category', 'Count'])
    
    # Create the chart with explicit scale
    chart = alt.Chart(dist_df).mark_bar().encode(
        x=alt.X('Category:N', sort='-y'),
        y=alt.Y('Count:Q', scale=alt.Scale(zero=True)),  # Ensure scale starts at zero
        color=alt.value("#FF4B4B")
    ).properties(height=200)
    
    st.altair_chart(chart, use_container_width=True)

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
        Calculate the number of tokens and estimated costs for different AI models.
        Support for TXT, PDF, DOCX, CSV, XLSX, RTF, EPUB, JSON, and YAML files.
    """)
    
    # Model selection
    col1, col2 = st.columns(2)
    with col1:
        openai_models = [m for m in MODEL_CONFIGS.keys() if m.startswith(('gpt-', 'o1-'))]
        selected_openai = st.selectbox("OpenAI Models", options=openai_models, format_func=format_model_name)

    with col2:
        anthropic_models = [m for m in MODEL_CONFIGS.keys() if m.startswith('claude-')]
        selected_anthropic = st.selectbox("Anthropic Models", options=anthropic_models, format_func=format_model_name)

    # Use the selected model from either dropdown
    selected_model = selected_anthropic if selected_anthropic else selected_openai
    
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
                display_token_analysis(text_input, selected_model)
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
                        analysis = analyze_text_sections(text_content, selected_model)
                        total_tokens += analysis['total_tokens']
                        
                        file_results.append({
                            'File Name': uploaded_file.name,
                            'File Type': uploaded_file.type,
                            'File Size (KB)': round(len(uploaded_file.getvalue()) / 1024, 1),
                            'Token Count': analysis['total_tokens'],
                            'Paragraphs': analysis['total_paragraphs'],
                            'Content': text_content
                        })
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                if file_results:
                    # Display total token count and cost analysis
                    st.markdown(f"""
                        <div class="token-count">
                            Total Tokens: {total_tokens:,}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display cost analysis for total tokens
                    display_cost_analysis(total_tokens, selected_model)
                    
                    # Create a DataFrame for file summary
                    summary_df = pd.DataFrame([{
                        'File Name': result['File Name'],
                        'File Type': result['File Type'],
                        'File Size (KB)': result['File Size (KB)'],
                        'Token Count': result['Token Count'],
                        'Paragraphs': result['Paragraphs']
                    } for result in file_results])
                    
                    # Display file summary
                    st.subheader("File Summary")
                    st.dataframe(
                        summary_df,
                        column_config={
                            "Token Count": st.column_config.NumberColumn(format=","),
                            "File Size (KB)": st.column_config.NumberColumn(format="%.1f")
                        },
                        hide_index=True
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            Made with ❤️ using Streamlit
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
