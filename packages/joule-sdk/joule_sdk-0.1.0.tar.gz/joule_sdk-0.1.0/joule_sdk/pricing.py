"""
Model pricing data for cost calculations.

Prices are in dollars per 1K tokens.
Updated January 2025.
"""

# OpenAI pricing (per 1K tokens)
OPENAI_PRICING = {
    # GPT-4o
    "gpt-4o": {"prompt": 0.0025, "completion": 0.01},
    "gpt-4o-2024-11-20": {"prompt": 0.0025, "completion": 0.01},
    "gpt-4o-2024-08-06": {"prompt": 0.0025, "completion": 0.01},
    "gpt-4o-2024-05-13": {"prompt": 0.005, "completion": 0.015},
    # GPT-4o mini
    "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
    "gpt-4o-mini-2024-07-18": {"prompt": 0.00015, "completion": 0.0006},
    # GPT-4 Turbo
    "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
    "gpt-4-turbo-2024-04-09": {"prompt": 0.01, "completion": 0.03},
    "gpt-4-turbo-preview": {"prompt": 0.01, "completion": 0.03},
    # GPT-4
    "gpt-4": {"prompt": 0.03, "completion": 0.06},
    "gpt-4-0613": {"prompt": 0.03, "completion": 0.06},
    "gpt-4-32k": {"prompt": 0.06, "completion": 0.12},
    # GPT-3.5 Turbo
    "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
    "gpt-3.5-turbo-0125": {"prompt": 0.0005, "completion": 0.0015},
    "gpt-3.5-turbo-1106": {"prompt": 0.001, "completion": 0.002},
    # o1 models
    "o1": {"prompt": 0.015, "completion": 0.06},
    "o1-2024-12-17": {"prompt": 0.015, "completion": 0.06},
    "o1-preview": {"prompt": 0.015, "completion": 0.06},
    "o1-mini": {"prompt": 0.003, "completion": 0.012},
    "o1-mini-2024-09-12": {"prompt": 0.003, "completion": 0.012},
    # Embeddings
    "text-embedding-3-small": {"prompt": 0.00002, "completion": 0},
    "text-embedding-3-large": {"prompt": 0.00013, "completion": 0},
    "text-embedding-ada-002": {"prompt": 0.0001, "completion": 0},
}

# Anthropic pricing (per 1K tokens)
ANTHROPIC_PRICING = {
    # Claude 4
    "claude-sonnet-4-20250514": {"prompt": 0.003, "completion": 0.015},
    "claude-sonnet-4": {"prompt": 0.003, "completion": 0.015},
    # Claude 3.5
    "claude-3-5-sonnet-20241022": {"prompt": 0.003, "completion": 0.015},
    "claude-3-5-sonnet-20240620": {"prompt": 0.003, "completion": 0.015},
    "claude-3-5-sonnet": {"prompt": 0.003, "completion": 0.015},
    "claude-3-5-haiku-20241022": {"prompt": 0.0008, "completion": 0.004},
    "claude-3-5-haiku": {"prompt": 0.0008, "completion": 0.004},
    # Claude 3
    "claude-3-opus-20240229": {"prompt": 0.015, "completion": 0.075},
    "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
    "claude-3-sonnet-20240229": {"prompt": 0.003, "completion": 0.015},
    "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
    "claude-3-haiku-20240307": {"prompt": 0.00025, "completion": 0.00125},
    "claude-3-haiku": {"prompt": 0.00025, "completion": 0.00125},
    # Legacy
    "claude-2.1": {"prompt": 0.008, "completion": 0.024},
    "claude-2.0": {"prompt": 0.008, "completion": 0.024},
    "claude-instant-1.2": {"prompt": 0.0008, "completion": 0.0024},
}

# Cache pricing multipliers for Anthropic
ANTHROPIC_CACHE_WRITE_MULTIPLIER = 1.25  # 25% more for cache writes
ANTHROPIC_CACHE_READ_MULTIPLIER = 0.1    # 90% discount for cache reads


def get_openai_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculate cost in cents for an OpenAI API call.

    Args:
        model: Model name
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens

    Returns:
        Cost in cents
    """
    pricing = OPENAI_PRICING.get(model)

    if not pricing:
        # Try to match partial model name
        for key, value in OPENAI_PRICING.items():
            if key in model or model in key:
                pricing = value
                break

    if not pricing:
        # Default to GPT-4 pricing as fallback
        pricing = OPENAI_PRICING["gpt-4"]

    prompt_cost = (prompt_tokens / 1000) * pricing["prompt"]
    completion_cost = (completion_tokens / 1000) * pricing["completion"]

    # Convert to cents
    return (prompt_cost + completion_cost) * 100


def get_anthropic_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0,
    cache_creation_tokens: int = 0
) -> float:
    """
    Calculate cost in cents for an Anthropic API call.

    Args:
        model: Model name
        input_tokens: Number of input tokens (excluding cache)
        output_tokens: Number of output tokens
        cache_read_tokens: Number of tokens read from cache
        cache_creation_tokens: Number of tokens written to cache

    Returns:
        Cost in cents
    """
    pricing = ANTHROPIC_PRICING.get(model)

    if not pricing:
        # Try to match partial model name
        for key, value in ANTHROPIC_PRICING.items():
            if key in model or model in key:
                pricing = value
                break

    if not pricing:
        # Default to Claude 3.5 Sonnet pricing as fallback
        pricing = ANTHROPIC_PRICING["claude-3-5-sonnet"]

    # Regular tokens
    regular_input_tokens = input_tokens - cache_read_tokens - cache_creation_tokens
    input_cost = (regular_input_tokens / 1000) * pricing["prompt"]
    output_cost = (output_tokens / 1000) * pricing["completion"]

    # Cache tokens
    cache_read_cost = (cache_read_tokens / 1000) * pricing["prompt"] * ANTHROPIC_CACHE_READ_MULTIPLIER
    cache_write_cost = (cache_creation_tokens / 1000) * pricing["prompt"] * ANTHROPIC_CACHE_WRITE_MULTIPLIER

    total_dollars = input_cost + output_cost + cache_read_cost + cache_write_cost

    # Convert to cents
    return total_dollars * 100
