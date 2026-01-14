# In a real-world scenario, this would be more sophisticated.
# For example, it could be a class that fetches the latest pricing from a remote server.
# For now, we'll hardcode the pricing for a few popular models.

# Prices are per 1,000 tokens
MODEL_PRICING = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-3.5-turbo-0125": {"input": 0.0005, "output": 0.0015},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
}

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculate the cost of a request given the model and the number of input and output tokens.
    """
    if model not in MODEL_PRICING:
        return 0.0
    
    pricing = MODEL_PRICING[model]
    input_cost = (prompt_tokens / 1_000) * pricing["input"]
    output_cost = (completion_tokens / 1_000) * pricing["output"]
    
    return input_cost + output_cost
