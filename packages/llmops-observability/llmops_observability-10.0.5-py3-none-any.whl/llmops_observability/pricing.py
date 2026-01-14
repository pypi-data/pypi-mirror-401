# pricing.py
"""
AWS Bedrock pricing calculator for token-based cost estimation.
Prices as of 2024 - update as needed.
"""
from typing import Dict, Optional

# AWS Bedrock pricing per 1K tokens (USD)
# https://aws.amazon.com/bedrock/pricing/
BEDROCK_PRICING = {
    # Claude 3.5 Sonnet
    "anthropic.claude-3-5-sonnet-20240620-v1:0": {
        "input": 0.003,  # $3 per 1M tokens
        "output": 0.015,  # $15 per 1M tokens
    },
    "anthropic.claude-3-5-sonnet-20241022-v2:0": {
        "input": 0.003,
        "output": 0.015,
    },
    # Claude 4 Sonnet (Cross-region inference)
    "us.anthropic.claude-sonnet-4-20250514-v1:0": {
        "input": 0.003,  # $3 per 1M tokens
        "output": 0.015,  # $15 per 1M tokens
    },
    "us.anthropic.claude-sonnet-4-5-20250929-v1:0": {
        "input": 0.003,  # $3 per 1M tokens
        "output": 0.015,  # $15 per 1M tokens
    },
    # Claude 3 Sonnet
    "anthropic.claude-3-sonnet-20240229-v1:0": {
        "input": 0.003,  # $3 per 1M tokens
        "output": 0.015,  # $15 per 1M tokens
    },
    # Claude 3 Haiku
    "anthropic.claude-3-haiku-20240307-v1:0": {
        "input": 0.00025,  # $0.25 per 1M tokens
        "output": 0.00125,  # $1.25 per 1M tokens
    },
    # Claude 3 Opus
    "anthropic.claude-3-opus-20240229-v1:0": {
        "input": 0.015,  # $15 per 1M tokens
        "output": 0.075,  # $75 per 1M tokens
    },
    # Claude 2.1
    "anthropic.claude-v2:1": {
        "input": 0.008,  # $8 per 1M tokens
        "output": 0.024,  # $24 per 1M tokens
    },
    # Claude 2.0
    "anthropic.claude-v2": {
        "input": 0.008,
        "output": 0.024,
    },
    # Claude Instant
    "anthropic.claude-instant-v1": {
        "input": 0.0008,  # $0.80 per 1M tokens
        "output": 0.0024,  # $2.40 per 1M tokens
    },
    # Amazon Titan Text models
    "amazon.titan-text-express-v1": {
        "input": 0.0002,  # $0.20 per 1M tokens
        "output": 0.0006,  # $0.60 per 1M tokens
    },
    "amazon.titan-text-lite-v1": {
        "input": 0.00015,  # $0.15 per 1M tokens
        "output": 0.0002,  # $0.20 per 1M tokens
    },
    # Cohere Command
    "cohere.command-text-v14": {
        "input": 0.0015,  # $1.50 per 1M tokens
        "output": 0.002,  # $2 per 1M tokens
    },
    "cohere.command-light-text-v14": {
        "input": 0.0003,  # $0.30 per 1M tokens
        "output": 0.0006,  # $0.60 per 1M tokens
    },
    # AI21 Jurassic
    "ai21.j2-ultra-v1": {
        "input": 0.0125,  # $12.50 per 1M tokens
        "output": 0.0125,
    },
    "ai21.j2-mid-v1": {
        "input": 0.0188,  # $18.80 per 1M tokens (per 1K)
        "output": 0.0188,
    },
    # Meta Llama models
    "meta.llama2-13b-chat-v1": {
        "input": 0.00075,  # $0.75 per 1M tokens
        "output": 0.001,  # $1 per 1M tokens
    },
    "meta.llama2-70b-chat-v1": {
        "input": 0.00195,  # $1.95 per 1M tokens
        "output": 0.00256,  # $2.56 per 1M tokens
    },
    "meta.llama3-8b-instruct-v1:0": {
        "input": 0.0003,  # $0.30 per 1M tokens
        "output": 0.0006,  # $0.60 per 1M tokens
    },
    "meta.llama3-70b-instruct-v1:0": {
        "input": 0.00265,  # $2.65 per 1M tokens
        "output": 0.0035,  # $3.50 per 1M tokens
    },
}


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model_id: Optional[str] = None
) -> Dict[str, float]:
    """
    Calculate cost based on token counts and model.
    
    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model_id: AWS Bedrock model ID
        
    Returns:
        Dict with input, output, and total cost
    """
    if not model_id or model_id not in BEDROCK_PRICING:
        # Unknown model - return zeros
        return {
            "input": 0.0,
            "output": 0.0,
            "total": 0.0,
        }
    
    pricing = BEDROCK_PRICING[model_id]
    
    # Prices are per 1K tokens, so divide by 1000
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    total_cost = input_cost + output_cost
    
    return {
        "input": round(input_cost, 6),
        "output": round(output_cost, 6),
        "total": round(total_cost, 6),
    }
