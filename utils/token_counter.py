import tiktoken

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
