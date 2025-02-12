# AI Token Calculator

A modern web application that calculates tokens and estimates costs for various AI language models. Built with Streamlit, this tool supports multiple file formats and provides detailed token analysis with beautiful visualizations.

## Features

- 🔤 Token counting for multiple AI models (OpenAI GPT series, Anthropic Claude)
- 📊 Detailed token analysis and distribution visualization
- 💰 Cost estimation for different usage scenarios
- 📁 Support for multiple file formats:
  - TXT, PDF, DOCX
  - CSV, XLSX
  - RTF, EPUB
  - JSON, YAML
- ✨ Modern, responsive UI with custom styling
- 📏 Context window compatibility checking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/token-calculator.git
cd token-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run main.py
```

The application will open in your default web browser. You can:
1. Choose between OpenAI and Anthropic models
2. Input text directly or upload supported files
3. View token counts, cost estimates, and visualizations
4. Analyze multiple files simultaneously

## Requirements

See `requirements.txt` for a complete list of dependencies.

## License

MIT License - See LICENSE file for details 