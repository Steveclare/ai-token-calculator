import streamlit as st
import pandas as pd
import altair as alt
from utils.token_counter import count_tokens, analyze_text_sections, get_token_distribution
from utils.file_processors import process_file
from utils.cost_calculator import calculate_costs, get_context_window_info, MODEL_CONFIGS

def format_model_name(model: str) -> str:
    """Format model name with context window"""
    config = MODEL_CONFIGS[model]
    context_k = config['context_window'] // 1000
    return f"{model} (Context: {context_k}K)"

def display_model_pricing(model: str):
    """Display model pricing information prominently"""
    config = MODEL_CONFIGS[model]
    input_cost = config['input_cost'] * 1000  # Convert to per million tokens
    output_cost = config['output_cost'] * 1000
    
    st.markdown("""
        <style>
        .pricing-info {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-left: 4px solid #FF4B4B;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .pricing-header {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #262730;
        }
        .pricing-detail {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        .pricing-detail:last-child {
            border-bottom: none;
        }
        </style>
        
        <div class="pricing-info">
            <div class="pricing-header">Current Model Pricing</div>
            <div class="pricing-detail">
                <span>Input Cost:</span>
                <span><strong>${input_cost:.2f}</strong> / 1M tokens</span>
            </div>
            <div class="pricing-detail">
                <span>Output Cost:</span>
                <span><strong>${output_cost:.2f}</strong> / 1M tokens</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_cost_analysis(token_count: int, selected_model: str):
    """Display cost analysis for the given token count and model"""
    costs = calculate_costs(token_count, selected_model)
    context_window, fits_context = get_context_window_info(token_count, selected_model)
    
    st.markdown(
        f"""
        <div class="context-info {'context-warning' if not fits_context else ''}">
            <h4>Context Window: {context_window:,} tokens</h4>
            <p>{'✅ Text fits within context window' if fits_context else '⚠️ Text exceeds context window'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    cost_df = pd.DataFrame([
        {"Scenario": "Input Only", "Cost ($)": costs['input_only']},
        {"Scenario": "Output Only", "Cost ($)": costs['output_only']},
        {"Scenario": "Input + Output", "Cost ($)": costs['input_output_equal']}
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
    """Display token analysis with improved styling"""
    analysis = analyze_text_sections(text, selected_model)
    distribution = get_token_distribution(text, selected_model)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tokens", f"{analysis['total_tokens']:,}")
    with col2:
        st.metric("Total Paragraphs", analysis['total_paragraphs'])
    
    display_cost_analysis(analysis['total_tokens'], selected_model)
    
    st.subheader("Token Distribution")
    dist_df = pd.DataFrame(distribution)
    dist_df.columns = ['Category', 'Count']
    
    chart = alt.Chart(dist_df).mark_bar().encode(
        x=alt.X('Category:N', sort='-y'),
        y=alt.Y('Count:Q'),
        color=alt.value("#FF4B4B")
    ).properties(height=200)
    
    st.altair_chart(chart, use_container_width=True)

def main():
    st.set_page_config(
        page_title="Token Calculator",
        page_icon="assets/icon.svg",
        layout="centered"
    )
    
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        }
        .main {
            padding: 2rem;
        }
        .token-count {
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
        }
        .token-count:hover {
            transform: translateY(-2px);
        }
        .stDataFrame {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin: 1rem 0;
        }
        .stMetric {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s;
        }
        .stMetric:hover {
            transform: translateY(-2px);
        }
        .context-info {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin: 1rem 0;
            text-align: center;
        }
        .context-warning {
            border-left: 4px solid #ff4b4b;
        }
        .stTextArea textarea {
            font-size: 16px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            padding: 1rem;
            transition: border-color 0.2s;
        }
        .stTextArea textarea:focus {
            border-color: #ff4b4b;
            box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.1);
        }
        .file-summary {
            font-size: 16px;
            padding: 1rem;
            border-radius: 10px;
            background-color: white;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔤 Token Calculator")
    st.markdown("""
        Calculate the number of tokens and estimated costs for different AI models.
        Support for TXT, PDF, DOCX, CSV, XLSX, RTF, EPUB, JSON, and YAML files.
    """)
    
    # Model selection
    col1, col2 = st.columns([1, 3])
    with col1:
        company = st.selectbox("Company", ["OpenAI", "Anthropic"])

    with col2:
        available_models = [
            m for m in MODEL_CONFIGS.keys() 
            if (company == "OpenAI" and m.startswith(('gpt-', 'o1-'))) or 
               (company == "Anthropic" and m.startswith('claude-'))
        ]
        selected_model = st.selectbox("Model", options=available_models, format_func=format_model_name)
    
    # Display prominent pricing information
    display_model_pricing(selected_model)
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])
    
    with tab1:
        text_input = st.text_area(
            "Enter your text here:",
            height=200,
            placeholder="Paste your text here to calculate tokens..."
        )
        
        if text_input:
            try:
                with st.spinner('Analyzing text...'):
                    display_token_analysis(text_input, selected_model)
            except Exception as e:
                st.error(f"Error analyzing text: {str(e)}")
    
    with tab2:
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
                    st.markdown(f"""
                        <div class="token-count">
                            Total Tokens: {total_tokens:,}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    display_cost_analysis(total_tokens, selected_model)
                    
                    summary_df = pd.DataFrame([{
                        'File Name': result['File Name'],
                        'File Type': result['File Type'],
                        'File Size (KB)': result['File Size (KB)'],
                        'Token Count': result['Token Count'],
                        'Paragraphs': result['Paragraphs']
                    } for result in file_results])
                    
                    st.subheader("File Summary")
                    st.dataframe(
                        summary_df,
                        column_config={
                            "Token Count": st.column_config.NumberColumn(format=","),
                            "File Size (KB)": st.column_config.NumberColumn(format="%.1f")
                        },
                        hide_index=True
                    )
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            Made with ❤️ using Streamlit
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
