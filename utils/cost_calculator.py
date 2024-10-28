from typing import Dict, Tuple

MODEL_CONFIGS = {
    # OpenAI Models
    'gpt-4o': {
        'input_cost': 0.0025,  # $2.50 per 1M tokens
        'output_cost': 0.01,   # $10.00 per 1M tokens
        'context_window': 128000
    },
    'gpt-4o-2024-08-06': {
        'input_cost': 0.0025,
        'output_cost': 0.01,
        'context_window': 128000
    },
    'gpt-4o-2024-05-13': {
        'input_cost': 0.005,
        'output_cost': 0.015,
        'context_window': 128000
    },
    'gpt-4o-mini': {
        'input_cost': 0.00015,
        'output_cost': 0.0006,
        'context_window': 128000
    },
    'gpt-4o-mini-2024-07-18': {
        'input_cost': 0.00015,
        'output_cost': 0.0006,
        'context_window': 128000
    },
    'o1-preview': {
        'input_cost': 0.015,
        'output_cost': 0.06,
        'context_window': 128000
    },
    'o1-mini': {
        'input_cost': 0.003,
        'output_cost': 0.012,
        'context_window': 128000
    },
    # Anthropic Models
    'claude-3-haiku': {
        'input_cost': 0.00025,  # $0.25 per 1M tokens
        'output_cost': 0.00125, # $1.25 per 1M tokens
        'context_window': 200000
    },
    'claude-3-sonnet': {
        'input_cost': 0.003,    # $3.00 per 1M tokens
        'output_cost': 0.015,   # $15.00 per 1M tokens
        'context_window': 200000
    },
    'claude-3-opus': {
        'input_cost': 0.015,    # $15.00 per 1M tokens
        'output_cost': 0.075,   # $75.00 per 1M tokens
        'context_window': 200000
    },
    'claude-3.5-sonnet': {
        'input_cost': 0.003,    # $3.00 per 1M tokens
        'output_cost': 0.015,   # $15.00 per 1M tokens
        'context_window': 200000
    }
}

def calculate_costs(token_count: int, model: str = 'gpt-4o') -> Dict[str, float]:
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
    
    # Calculate different scenarios with sum for input/output equal
    costs = {
        'input_only': round(tokens_in_thousands * config['input_cost'], 4),
        'output_only': round(tokens_in_thousands * config['output_cost'], 4),
        'input_output_equal': round(tokens_in_thousands * (config['input_cost'] + config['output_cost']), 4)
    }
    
    return costs

def get_context_window_info(token_count: int, model: str = 'gpt-4o') -> Tuple[int, bool]:
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
