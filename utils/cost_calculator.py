from typing import Dict, Tuple

MODEL_CONFIGS = {
    'claude-instant': {
        'input_cost': 0.0008,  # per 1K tokens
        'output_cost': 0.0024,  # per 1K tokens
        'context_window': 200000
    },
    'claude-2': {
        'input_cost': 0.008,  # per 1K tokens
        'output_cost': 0.024,  # per 1K tokens
        'context_window': 200000
    },
    'claude-2.1': {
        'input_cost': 0.008,  # per 1K tokens
        'output_cost': 0.024,  # per 1K tokens
        'context_window': 200000
    },
    'claude-3-haiku': {
        'input_cost': 0.00025,  # per 1K tokens
        'output_cost': 0.00125,  # per 1K tokens
        'context_window': 200000
    },
    'claude-3-sonnet': {
        'input_cost': 0.003,  # per 1K tokens
        'output_cost': 0.015,  # per 1K tokens
        'context_window': 200000
    },
    'claude-3-opus': {
        'input_cost': 0.015,  # per 1K tokens
        'output_cost': 0.075,  # per 1K tokens
        'context_window': 200000
    },
    'claude-3.5-sonnet': {
        'input_cost': 0.003,  # per 1K tokens
        'output_cost': 0.015,  # per 1K tokens
        'context_window': 200000
    }
}

def calculate_costs(token_count: int, model: str = 'claude-3-sonnet') -> Dict[str, float]:
    """
    Calculate estimated costs for input and output tokens for different scenarios
    
    Args:
        token_count (int): Number of tokens to calculate costs for
        model (str): The model to use for cost calculation
        
    Returns:
        Dict[str, float]: Dictionary containing various cost estimates
    """
    if model not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model}")
        
    config = MODEL_CONFIGS[model]
    tokens_in_thousands = token_count / 1000
    
    # Calculate different scenarios
    costs = {
        'input_only': round(tokens_in_thousands * config['input_cost'], 4),
        'output_only': round(tokens_in_thousands * config['output_cost'], 4),
        'input_output_equal': round(tokens_in_thousands * (config['input_cost'] + config['output_cost']) / 2, 4),
    }
    
    return costs

def get_context_window_info(token_count: int, model: str = 'claude-3-sonnet') -> Tuple[int, bool]:
    """
    Get information about context window for the given token count and model
    
    Args:
        token_count (int): Number of tokens
        model (str): The model to check against
        
    Returns:
        Tuple[int, bool]: (context window size, whether tokens fit in context)
    """
    if model not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model}")
        
    context_window = MODEL_CONFIGS[model]['context_window']
    fits_context = token_count <= context_window
    
    return context_window, fits_context
