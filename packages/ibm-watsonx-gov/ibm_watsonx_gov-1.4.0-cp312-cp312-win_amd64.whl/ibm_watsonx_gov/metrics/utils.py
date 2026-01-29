# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Dict, List, Optional

import pandas as pd


def mapping_to_df(mapping_data: Dict, execution_count: Optional[int] = 0) -> pd.DataFrame:
    """
    Convert mapping data into a pandas DataFrame.
    If execution_count is given, construct dataframe with values w.r.t to execution count
    """
    def generate_rows():
        row = {}
        for span, lvl1 in mapping_data.items():
            if not isinstance(lvl1, dict):
                row[span] = lvl1
                continue

            for attr, lvl2 in lvl1.items():
                if not isinstance(lvl2, dict):
                    col = f"{span}->{attr}"
                    row[col] = _get_list_value(lvl2, execution_count)
                    continue

                for path, value in lvl2.items():
                    col = f"{span}->{attr}->{path}"
                    row[col] = _get_list_value(value, execution_count)
        yield row

    return pd.DataFrame(generate_rows())


def _get_list_value(value, execution_count):
    """Helper function to safely get value from list"""
    if isinstance(value, list):
        if execution_count < len(value):
            return value[execution_count]
        return value[0] if value else None
    return value


TARGETED_USAGE_TRACE_NAMES = [
    # openAI
    "openai.embeddings",
    "ChatOpenAI.chat",
    "OpenAI.completion",
    # IBM
    "ChatWatsonx.chat",
    "WatsonxLLM.completion",
    "WatsonxChatModel.chat",  # wxo span
    # Azure
    "AzureChatOpenAI.chat",
    "AzureOpenAI.completion",
    # AWS
    "ChatBedrock.chat",
    "ChatBedrockConverse.chat",
    # Google
    "ChatVertexAI.chat",
    "VertexAI.completion",
    # Anthropic
    "ChatAnthropic.chat",
    "ChatAnthropicMessages.chat",
    # TODO: Add attributes for other frameworks as well.
]
ONE_M = 1000000

LAST_UPDATED = "2025-01-21"  # Date when pricing was last verified

# ref: https://platform.openai.com/docs/pricing
OPENAI_COSTS = {  # Costs per 1M tokens
    # GPT-5 Series
    "gpt-5": {"input": 2.50, "output": 20.0},
    "gpt-5.1": {"input": 2.50, "output": 20.0},
    "gpt-5-mini": {"input": 0.45, "output": 3.60},
    "gpt-5-nano": {"input": 0.05, "output": 0.40},
    "gpt-5-pro": {"input": 15.0, "output": 120.0},

    # GPT-4.1 Series
    "gpt-4.1": {"input": 3.50, "output": 14.0},
    "gpt-4.1-mini": {"input": 0.70, "output": 2.80},
    "gpt-4.1-nano": {"input": 0.20, "output": 0.80},

    # GPT-4o Series
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-2024-05-13": {"input": 5.0, "output": 15.0},
    "gpt-4o-2024-08-06": {"input": 3.75, "output": 15.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini-2024-07-18": {"input": 0.30, "output": 1.20},
    "chatgpt-4o-latest": {"input": 5.0, "output": 15.0},

    # GPT-4 Series (Legacy)
    "gpt-4": {"input": 30.0, "output": 60.0},
    "gpt-4-turbo": {"input": 10.0, "output": 30.0},
    "gpt-4-turbo-2024-04-09": {"input": 10.0, "output": 30.0},
    "gpt-4-0125-preview": {"input": 10.0, "output": 30.0},
    "gpt-4-1106-preview": {"input": 10.0, "output": 30.0},
    "gpt-4-0613": {"input": 30.0, "output": 60.0},
    "gpt-4-32k": {"input": 60.0, "output": 120.0},

    # O-Series (Reasoning)
    "o1": {"input": 15.0, "output": 60.0},
    "o1-pro": {"input": 150.0, "output": 600.0},
    "o1-mini": {"input": 1.10, "output": 4.40},
    "o3": {"input": 3.50, "output": 14.0},
    "o3-pro": {"input": 20.0, "output": 80.0},
    "o3-mini": {"input": 1.10, "output": 4.40},
    "o4-mini": {"input": 2.0, "output": 8.0},
    "o3-deep-research": {"input": 10.0, "output": 40.0},
    "o4-mini-deep-research": {"input": 2.0, "output": 8.0},

    # GPT-3.5 Series
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-3.5-turbo-0125": {"input": 0.50, "output": 1.50},
    "gpt-3.5-turbo-1106": {"input": 1.0, "output": 2.0},
    "gpt-3.5-turbo-instruct": {"input": 1.50, "output": 2.0},

    # Base Models
    "davinci-002": {"input": 2.0, "output": 2.0},
    "babbage-002": {"input": 0.40, "output": 0.40},

    # Embeddings
    "text-embedding-3-large": {"input": 0.13, "output": 0.0},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    "text-embedding-ada-002": {"input": 0.10, "output": 0.0},
}

# ref: https://docs.anthropic.com/en/docs/about-claude/models/overview#model-pricing
ANTHROPIC_COSTS = {  # Costs per 1M tokens
    # Opus 4 Series
    "claude-opus-4-1": {"input": 15.0, "output": 75.0},
    "claude-opus-4-0": {"input": 15.0, "output": 75.0},
    "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
    "anthropic.claude-opus-4-20250514-v1:0": {"input": 15.0, "output": 75.0},
    "claude-opus-4@20250514": {"input": 15.0, "output": 75.0},

    # Sonnet 4.5 Series (tiered pricing based on prompt size)
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0},  # ≤200K tokens
    "claude-sonnet-4-5-large": {"input": 6.0, "output": 22.50},  # >200K tokens

    # Sonnet 4 Series
    "claude-sonnet-4-0": {"input": 3.0, "output": 15.0},
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
    "anthropic.claude-sonnet-4-20250514-v1:0": {"input": 3.0, "output": 15.0},
    "claude-sonnet-4@20250514": {"input": 3.0, "output": 15.0},

    # Sonnet 3.7 Series
    "claude-3-7-sonnet-latest": {"input": 3.0, "output": 15.0},
    "claude-3-7-sonnet-20250219": {"input": 3.0, "output": 15.0},
    "anthropic.claude-3-7-sonnet-20250219-v1:0": {"input": 3.0, "output": 15.0},
    "claude-3-7-sonnet@20250219": {"input": 3.0, "output": 15.0},

    # Sonnet 3.5 Series
    "claude-3-5-sonnet-latest": {"input": 3.0, "output": 15.0},
    "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
    "anthropic.claude-3-5-sonnet-20241022-v2:0": {"input": 3.0, "output": 15.0},
    "claude-3-5-sonnet-v2@20241022": {"input": 3.0, "output": 15.0},

    # Haiku 4.5 Series
    "claude-haiku-4-5": {"input": 1.0, "output": 5.0},

    # Haiku 3.5 Series
    "claude-3-5-haiku-latest": {"input": 0.80, "output": 4.0},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.0},
    "anthropic.claude-3-5-haiku-20241022-v1:0": {"input": 0.80, "output": 4.0},
    "claude-3-5-haiku@20241022": {"input": 0.80, "output": 4.0},

    # Haiku 3 Series
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.25, "output": 1.25},
    "claude-3-haiku@20240307": {"input": 0.25, "output": 1.25},
}

# ref: https://cloud.google.com/vertex-ai/generative-ai/pricing
GOOGLE_COSTS = {  # Costs per 1M tokens
    # Gemini 3 Series
    "gemini-3-pro-preview": {"input": 2.0, "output": 12.0},  # ≤200K tokens
    # >200K tokens
    "gemini-3-pro-preview-large": {"input": 4.0, "output": 18.0},

    # Gemini 2.5 Series
    "gemini-2.5-pro": {"input": 1.25, "output": 10.0},  # ≤200K tokens
    "gemini-2.5-pro-large": {"input": 2.50, "output": 15.0},  # >200K tokens
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "gemini-2.5-flash-lite": {"input": 0.1, "output": 0.4},

    # Gemini 2.0 Series
    "gemini-2.0-flash-001": {"input": 0.15, "output": 0.6},
    "gemini-2.0-flash-lite-001": {"input": 0.075, "output": 0.3},
}

# ref: https://mistral.ai/pricing#api-pricing
# ref: https://aws.amazon.com/bedrock/pricing
# ref: https://cloud.google.com/vertex-ai/generative-ai/pricing
MISTRAL_COSTS = {  # Costs per 1M tokens
    # Pixtral Series (Vision)
    "pixtral-large-latest": {"input": 2.0, "output": 6.0},
    "mistral.pixtral-large-2502-v1:0": {"input": 2.0, "output": 6.0},
    "pixtral-12b": {"input": 0.15, "output": 0.15},

    # Mistral Large Series
    "mistral-large-latest": {"input": 2.0, "output": 6.0},
    "mistral.mistral-large-2407-v1:0": {"input": 2.0, "output": 6.0},
    "mistralai/mistral-large-2411@001": {"input": 2.0, "output": 6.0},
    "mistral.mistral-large-2402-v1:0": {"input": 4.0, "output": 12.0},

    # Mistral Medium Series
    "mistral-medium-3": {"input": 0.4, "output": 2.0},
    "mistral-medium-latest": {"input": 0.4, "output": 2.0},

    # Mistral Small Series
    "mistral-small-3-2": {"input": 0.1, "output": 0.3},
    "mistral-small-latest": {"input": 0.1, "output": 0.3},
    "mistralai/mistral-small-2503@001": {"input": 0.1, "output": 0.3},
    "mistral.mistral-small-2402-v1:0": {"input": 1.0, "output": 3.0},

    # Magistral Series (Reasoning)
    "magistral-medium-latest": {"input": 2.0, "output": 5.0},
    "magistral-small-latest": {"input": 0.5, "output": 1.5},

    # Devstral Series (Coding)
    "devstral-medium-2507": {"input": 0.4, "output": 2.0},
    "devstral-small-2507": {"input": 0.1, "output": 0.3},

    # Codestral Series
    "codestral-latest": {"input": 0.3, "output": 0.9},

    # Ministral Series (Edge)
    "ministral-8b-latest": {"input": 0.1, "output": 0.1},
    "ministral-3b-latest": {"input": 0.04, "output": 0.04},

    # Open Mistral Series
    "open-mistral-7b": {"input": 0.25, "output": 0.25},
    "mistral.mistral-7b-instruct-v0:2": {"input": 0.15, "output": 0.2},
    "open-mistral-nemo": {"input": 0.15, "output": 0.15},

    # Open Mixtral Series
    "open-mixtral-8x7b": {"input": 0.7, "output": 0.7},
    "mistral.mixtral-8x7b-instruct-v0:1": {"input": 0.45, "output": 0.7},
    "open-mixtral-8x22b": {"input": 2.0, "output": 6.0},

    # Embeddings
    "mistral-embed": {"input": 0.1, "output": 0.0},
    "codestral-embed-2505": {"input": 0.15, "output": 0.0},
}

# ref: https://aws.amazon.com/bedrock/pricing
COHERE_COSTS = {  # Costs per 1M tokens
    "command-r": {"input": 0.5, "output": 1.5},
    "cohere.command-r-v1:0": {"input": 0.5, "output": 1.5},
    "command-r-plus": {"input": 3.0, "output": 15},
    "cohere.command-r-plus-v1:0": {"input": 3.0, "output": 15},
    "command-light": {"input": 0.3, "output": 0.6},
    "cohere.command-light-text-v14": {"input": 0.3, "output": 0.6},
    "command": {"input": 1.0, "output": 2.0},
    "cohere.command-text-v14": {"input": 1.0, "output": 2.0},
}

# ref: https://www.ai21.com/pricing
# ref: https://aws.amazon.com/bedrock/pricing
# ref: https://cloud.google.com/vertex-ai/generative-ai/pricing
AI21_COSTS = {  # Costs per 1M tokens
    "jamba-large": {"input": 2.0, "output": 8.0},
    "ai21.jamba-1-5-large-v1:0": {"input": 2.0, "output": 8.0},
    "ai21/jamba-1.5-large@001": {"input": 2.0, "output": 8.0},
    "jamba-mini": {"input": 0.2, "output": 0.4},
    "ai21.jamba-1-5-mini-v1:0": {"input": 0.2, "output": 0.4},
    "ai21/jamba-1.5-mini@001": {"input": 0.2, "output": 0.4},
}

# ref: https://www.ibm.com/products/watsonx-ai/pricing
IBM_WATSONX_COSTS = {  # Costs per 1M tokens
    # IBM Granite Series
    "ibm/granite-4-h-small": {"input": 0.06, "output": 0.25},
    "ibm/granite-vision-3-2-2b": {"input": 0.10, "output": 0.10},
    "ibm/granite-3-2b-instruct": {"input": 0.10, "output": 0.10},
    "ibm/granite-3-8b-instruct": {"input": 0.20, "output": 0.20},
    "ibm/granite-guardian-3-8b": {"input": 0.20, "output": 0.20},
    "ibm/granite-8b-code-instruct": {"input": 0.20, "output": 0.20},
    "ibm/granite-8b-japanese": {"input": 0.60, "output": 0.60},
    "ibm/granite-3-2-8b-instruct": {"input": 0.20, "output": 0.20},
    "ibm/granite-timeseries-ttm-r2": {"input": 0.38, "output": 0.38},

    # Meta Llama Series
    "meta-llama/llama-3-2-1b-instruct": {"input": 0.1, "output": 0.1},
    "meta-llama/llama-3-2-3b-instruct": {"input": 0.15, "output": 0.15},
    "meta-llama/llama-3-2-11b-vision-instruct": {"input": 0.35, "output": 0.35},
    "meta-llama/llama-3-2-90b-vision-instruct": {"input": 2.0, "output": 2.0},
    "meta-llama/llama-3-3-70b-instruct": {"input": 0.71, "output": 0.71},
    "meta-llama/llama-3-405b-instruct": {"input": 5.0, "output": 16.0},
    "meta-llama/llama-4-maverick-17b-128e-instruct-fp": {"input": 0.35, "output": 1.4},
    "meta-llama/llama-guard-3-11b-vision": {"input": 0.35, "output": 0.35},

    # Mistral Series on Watsonx
    "mistralai/mistral-small-3-1-24b-instruct-2503": {"input": 0.1, "output": 0.3},
    "mistralai/mistral-medium-2505": {"input": 3.0, "output": 10.0},

    # Other Models
    "core42/jais-13b-chat": {"input": 1.8, "output": 1.8},
    "sdaia/allam-1-13b-instruct": {"input": 1.8, "output": 1.8},

    # IBM Granite Embeddings
    "ibm/granite-embedding-107m-multilingual": {"input": 0.10, "output": 0.0},
    "ibm/granite-embedding-278m-multilingual": {"input": 0.10, "output": 0.0},

    # IBM Slate Retrieval Models
    "ibm/slate-125m-english-rtrvr": {"input": 0.10, "output": 0.0},
    "ibm/slate-125m-english-rtrvr-v2": {"input": 0.10, "output": 0.0},
    "ibm/slate-30m-english-rtrvr": {"input": 0.10, "output": 0.0},
    "ibm/slate-30m-english-rtrvr-v2": {"input": 0.10, "output": 0.0},

    # Third-Party Embeddings
    "intfloat/multilingual-e5-large": {"input": 0.10, "output": 0.0},
    "sentence-transformers/all-minilm-l12-v2": {"input": 0.10, "output": 0.0},
    "sentence-transformers/all-minilm-l6-v2": {"input": 0.10, "output": 0.0},

    # OpenAI
    "openai/gpt-oss-120b": {"input": 0.15, "output": 0.60}
}

# ref: https://aws.amazon.com/bedrock/pricing/ (DeepSeek tab)
DEEPSEEK_COSTS = {  # Costs per 1M tokens
    # DeepSeek models (Standard Tier - AWS Bedrock)
    "deepseek-r1": {"input": 1.35, "output": 5.40},
    "deepseek-v3.1": {"input": 0.58, "output": 1.68},
}

# ref: https://docs.x.ai/docs/models
XAI_COSTS = {  # Costs per 1M tokens
    # Grok 4.1 Series
    "grok-4-1-fast-reasoning": {"input": 0.20, "output": 0.50},
    "grok-4-1-fast-non-reasoning": {"input": 0.20, "output": 0.50},

    # Grok 4 Series
    "grok-4-fast-reasoning": {"input": 0.20, "output": 0.50},
    "grok-4-fast-non-reasoning": {"input": 0.20, "output": 0.50},
    "grok-4-0709": {"input": 3.0, "output": 15.0},

    # Grok 3 Series
    "grok-3": {"input": 3.0, "output": 15.0},
    "grok-3-mini": {"input": 0.30, "output": 0.50},

    # Grok 2 Series
    # Both us-east-1 and eu-west-1
    "grok-2-vision-1212": {"input": 2.0, "output": 10.0},

    # Grok Code
    "grok-code-fast-1": {"input": 0.20, "output": 1.50},

    # Image Generation (per image)
    "grok-2-image-1212": {"input": 0.0, "output": 0.07},  # $0.07 per image
}

# ref: https://docs.perplexity.ai/getting-started/pricing
PERPLEXITY_COSTS = {  # Costs per 1M tokens
    # Sonar Models
    "sonar": {"input": 1.0, "output": 1.0},
    "sonar-pro": {"input": 3.0, "output": 15.0},
    "sonar-reasoning": {"input": 1.0, "output": 5.0},
    "sonar-reasoning-pro": {"input": 2.0, "output": 8.0},
    # Plus $2/1M citation tokens, $5/1K search queries, $3/1M reasoning tokens
    "sonar-deep-research": {"input": 2.0, "output": 8.0},
}

# ref: https://groq.com/pricing
GROQ_COSTS = {  # Costs per 1M tokens
    # GPT OSS Series
    "gpt-oss-20b": {"input": 0.075, "output": 0.30},
    "gpt-oss-safeguard-20b": {"input": 0.075, "output": 0.30},
    "gpt-oss-120b": {"input": 0.15, "output": 0.60},

    # Kimi Series
    "kimi-k2-0905-1t": {"input": 1.0, "output": 3.0},

    # Llama 4 Series
    "llama-4-scout-17b-16e": {"input": 0.11, "output": 0.34},
    "llama-4-maverick-17b-128e": {"input": 0.20, "output": 0.60},
    "llama-guard-4-12b": {"input": 0.20, "output": 0.20},

    # Qwen Series
    "qwen3-32b": {"input": 0.29, "output": 0.59},

    # Llama 3.3 Series
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},

    # Llama 3.1 Series
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
}

# Combined metadata for backward compatibility
COST_METADATA = {
    **OPENAI_COSTS,
    **ANTHROPIC_COSTS,
    **GOOGLE_COSTS,
    **MISTRAL_COSTS,
    **COHERE_COSTS,
    **AI21_COSTS,
    **IBM_WATSONX_COSTS,
    **DEEPSEEK_COSTS,
    **XAI_COSTS,
    **PERPLEXITY_COSTS,
    **GROQ_COSTS,
}


def calculate_cost(usage_data: List[dict]) -> float:
    """Calculate cost for given list of usage.
    [
        {"model": ..., "total_prompt_tokens": ...,  "total_completion_tokens": ...},
        ...
    ]
    """
    total_cost = 0.0

    for data in usage_data:
        model = data["model"].lower()

        try:
            model_pricing = COST_METADATA[model]
        except KeyError:
            return 0
            # raise ValueError(
            #     f"Pricing not available for {model}")

        # Calculate costs (per 1M tokens)
        input_cost = (data.get("total_prompt_tokens", 0) /
                      ONE_M) * model_pricing["input"]
        output_cost = (data.get("total_completion_tokens", 0) / ONE_M) * model_pricing[
            "output"
        ]
        total_cost += input_cost + output_cost

    return round(total_cost, 4)
