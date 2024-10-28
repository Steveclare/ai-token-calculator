import tiktoken
import re
from typing import Dict, List, Tuple

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a text string using tiktoken
    
    Args:
        text (str): The input text to count tokens for
        model (str): The model to use for token counting
        
    Returns:
        int: Number of tokens in the text
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        raise Exception(f"Error counting tokens: {str(e)}")

def analyze_text_sections(text: str, model: str = "gpt-3.5-turbo") -> Dict:
    """
    Analyze text and provide detailed token breakdown by sections
    
    Args:
        text (str): The input text to analyze
        model (str): The model to use for token counting
        
    Returns:
        Dict: Detailed breakdown of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        
        # Split text into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Analyze paragraphs
        paragraph_analysis = []
        for i, para in enumerate(paragraphs, 1):
            tokens = encoding.encode(para)
            sentences = [s.strip() for s in re.split('[.!?]+', para) if s.strip()]
            sentence_analysis = []
            
            for sentence in sentences:
                sentence_tokens = encoding.encode(sentence)
                sentence_analysis.append({
                    'text': sentence,
                    'tokens': len(sentence_tokens)
                })
            
            paragraph_analysis.append({
                'paragraph_number': i,
                'text': para,
                'total_tokens': len(tokens),
                'sentences': sentence_analysis
            })
        
        # Calculate statistics
        total_tokens = sum(p['total_tokens'] for p in paragraph_analysis)
        avg_tokens_per_paragraph = total_tokens / len(paragraphs) if paragraphs else 0
        
        return {
            'total_tokens': total_tokens,
            'total_paragraphs': len(paragraphs),
            'average_tokens_per_paragraph': round(avg_tokens_per_paragraph, 2),
            'paragraphs': paragraph_analysis
        }
        
    except Exception as e:
        raise Exception(f"Error analyzing text: {str(e)}")

def get_token_distribution(text: str, model: str = "gpt-3.5-turbo") -> List[Tuple[str, int]]:
    """
    Get token distribution by character type
    
    Args:
        text (str): The input text to analyze
        model (str): The model to use for token counting
        
    Returns:
        List[Tuple[str, int]]: List of (category, count) tuples
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(text)
        
        # Analyze character types in the text
        categories = {
            'Alphanumeric': len(re.findall(r'[a-zA-Z0-9]+', text)),
            'Punctuation': len(re.findall(r'[^\w\s]', text)),
            'Whitespace': len(re.findall(r'\s+', text)),
            'Special Characters': len(re.findall(r'[^a-zA-Z0-9\s\W]', text))
        }
        
        return list(categories.items())
        
    except Exception as e:
        raise Exception(f"Error getting token distribution: {str(e)}")
