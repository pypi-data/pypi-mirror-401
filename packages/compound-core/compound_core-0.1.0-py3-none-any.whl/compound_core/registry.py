"""
Centralized registry for LLM models and fallback logic.
Used by parallel_agents.py and evaluation_core.py to ensure consistent model selection and resilience.
"""
import copy
import os
import random
from typing import Optional


# Map friendly names to LiteLLM provider format
MODEL_MAP = {
    # Mistral (Mistral 3 Family - Released Dec 2025)
    "mistral-large": "mistral/mistral-large-latest",     # Maps to Mistral Large 3
    
    # Cerebras (Ultra-fast Inference Llama 3.3)
    "cerebras-llama3.3-70b": "cerebras/llama-3.3-70b",
    "cerebras-llama3-70b": "cerebras/llama-3.3-70b", # Intentionally mapping generic 70b to latest 3.3
    "cerebras-llama3-8b": "cerebras/llama-3.1-8b",
    
    # Cerebras Preview/Other
    "cerebras-glm4": "cerebras/zai-glm-4.6",
    "cerebras-gpt-oss": "cerebras/gpt-oss-120b",
    "cerebras-qwen-32b": "cerebras/qwen-3-32b",
    "cerebras-qwen-user-235b": "cerebras/qwen-3-235b-a22b-instruct-2507",
    
    # Cloudflare Workers AI
    "cf-llama-3.1-8b": "cloudflare/@cf/meta/llama-3.1-8b-instruct",
    "cf-llama-3.3-70b": "cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    "cf-llama-4-scout": "cloudflare/@cf/meta/llama-4-scout-17b-16e-instruct", # Preview/New
    "cf-llama-3.1-8b-fast": "cloudflare/@cf/meta/llama-3.1-8b-instruct-fast", # Optimized
    # "cf-qwen-3-30b": "cloudflare/@cf/qwen/qwen3-30b-a3b-fp8", # Parse Error (KeyError: 'response')
    "cf-qwen-2.5-coder-32b": "cloudflare/@cf/qwen/qwen2.5-coder-32b-instruct", # SOTA Coding
    "cf-mistral-small-24b": "cloudflare/@cf/mistralai/mistral-small-3.1-24b-instruct", # Vision/Text, Strong
    "cf-gemma-3-12b": "cloudflare/@cf/google/gemma-3-12b-it", # Multimodal
    "cf-qwq-32b": "cloudflare/@cf/qwen/qwq-32b",
    
    # GitHub Models (Free Tier / Prototyping)
    "gh-gpt-4o": "github/gpt-4o", # Validated Working!
    "gh-gpt-4o-mini": "github/gpt-4o-mini", # Validated Working!
    "gh-mistral-nemo": "github/Mistral-Nemo", # 12B, Fast, 128k context
    "gh-llama-3.2-11b": "github/Llama-3.2-11B-Vision-Instruct", # Vision
    "gh-llama-3.2-90b": "github/Llama-3.2-90B-Vision-Instruct", # Vision, Strong
    
    # Microsoft Phi-4 (Validated Jan 2025)
    "gh-phi-4": "github/Phi-4", # 14B Strong Reasoning
    "gh-phi-4-multimodal": "github/Phi-4-multimodal-instruct", # 3-modality input
    
    # "gh-o1-mini": "github/o1-mini", # Restricted/Unknown
    # "gh-phi-3-mini": "github/Phi-3-mini-4k-instruct", # Failed (Unknown model)
    # "gh-phi-3-medium": "github/Phi-3-medium-128k-instruct", # Failed
    # "gh-mistral-large": "github/Mistral-large-2407", # Failed
    # "gh-cohere-command-r-plus": "github/Cohere-command-r-plus", # Failed
    
    # "cf-gpt-oss-120b": "cloudflare/@cf/openai/gpt-oss-120b", # Schema Error
    # "cf-deepseek-r1": "cloudflare/@cf/deepseek/deepseek-r1-distill-qwen-32b", # Route Error
    
    
    # Mistral Official
    "mistral-small": "mistral/mistral-small-latest",
    "codestral": "mistral/codestral-2501",           # Jan 2025 Model!
    "pixtral-large": "mistral/pixtral-large-2411",   # Vision Large
    "ministral-8b": "mistral/ministral-8b-latest",   # Edge efficient
    # "mistral-ocr": "mistral/mistral-ocr-latest",   # Invalid model error
    
    # Mistral Open Weights (MoE)
    "mixtral-8x7b": "mistral/open-mixtral-8x7b",     # The Classic
    "mixtral-8x22b": "mistral/open-mixtral-8x22b",   # The Beast (176B params)
    "mistral-saba": "mistral/mistral-saba-latest",   # Mid-tier (Feb 2025)
    
    # Cohere (Command Series 2026)
    "command-r-plus": "cohere/command-r-plus-08-2024",
    "command-r": "cohere/command-r-08-2024",
    "command-a": "cohere/command-a-03-2025",       # Flagship (March 2025)
    
    # Groq (Llama 4, Qwen 3, GPT-OSS)
    "groq-llama-4-maverick": "groq/meta-llama/llama-4-maverick-17b-128e-instruct", # 17B, 128 experts?
    "groq-llama-4-scout": "groq/meta-llama/llama-4-scout-17b-16e-instruct",
    "groq-qwen-3-32b": "groq/qwen/qwen3-32b", 
    "groq-gpt-oss-120b": "groq/openai/gpt-oss-120b",
    
    "llama3-instant": "groq/llama-3.1-8b-instant", 
    "qwen": "groq/qwen-2.5-coder-32b",             # (Qwen 3 is rolling out)
    
    # Groq OpenAI-Compatible/Specialty
    "gpt-oss": "groq/openai/gpt-oss-120b",         # Matches GPT-5.1 class
    "kimi": "groq/moonshotai/kimi-k2-instruct-0905",
    
    # Google (Gemini) - Verified Jan 2026 via User Screenshot & API List
    "gemini": "gemini/gemini-2.5-pro",                   # Stable Workhorse
    "gemini-flash": "gemini/gemini-3-flash-preview",     # High-speed (Preview)
    "gemini-lite": "gemini/gemini-2.5-flash-lite",       # Ultra-efficient
    "gemini-experimental": "gemini/gemini-robotics-er-1.5-preview", # Specialized
    
    # Gemma 3 Family (Open Weights)
    "gemma-27b": "gemini/gemma-3-27b-it",                # Strongest local-class (Instruct)
    "gemma-small": "gemini/gemma-3-4b-it",               # Edge logic (Instruct)
    
    # Legacy/Extras
    "compound": "groq/llama-3.3-70b-versatile",
    
    # --- NEW SOTA ADDITIONS (Jan 2026) ---
    # DeepSeek R1 (Reasoning SOTA)
    "cf-deepseek-r1": "cloudflare/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
    
    # Groq (Llama 4 & Moonshot)
    "groq-llama-4-maverick": "groq/llama-4-maverick-17b-128e-instruct", # 128-Expert MoE
    "groq-llama-4-scout": "groq/llama-4-scout-17b-16e-instruct",       # Multimodal
    "groq-kimi-k2": "groq/moonshotai/kimi-k2-instruct-0905",           # 256k Context
    "gh-phi-4": "github/Phi-4",
    
    # Braintrust Proxy (Requires upstream configuration)
    "bt-claude-3.5-sonnet": "braintrust/claude-3-5-sonnet-latest",

    # --- LLM Gateway (Free Tier) ---
    # SOTA Models available via llmgateway.io
    "llm-gateway-deepseek-r1": "openai/deepseek-r1t2-chimera-free",
    "llm-gateway-llama-4-maverick": "openai/llama-4-maverick-free",
    "llm-gateway-llama-4-scout": "openai/llama-4-scout-free",
    "llm-gateway-kimi-k2": "openai/kimi-k2-0905-free",
    "llm-gateway-gpt-oss-20b": "openai/gpt-oss-20b-free",
    "llm-gateway-glm-4.5": "openai/glm-4.5-air-free",
    
    # --- RouteWay.ai (Free Tier) ---
    # Premium models available via routeway.ai (OpenAI-compatible)
    "routeway-deepseek-r1": "openai/deepseek-r1",
    "routeway-deepseek-r1-0528": "openai/deepseek-r1-0528",
    "routeway-deepseek-v31": "openai/deepseek-v31",
    "routeway-llama-3.3-70b": "openai/llama-3.3-70b-instruct",
    "routeway-llama-3.2-3b": "openai/llama-3.2-3b-instruct",
    "routeway-llama-3.1-8b": "openai/llama-3.1-8b-instruct",
    "routeway-gpt-oss-120b": "openai/gpt-oss-120b",
    "routeway-mistral-nemo": "openai/mistral-nemo-instruct",
    "routeway-devstral-2-2512": "openai/devstral-2-2512",
    "routeway-r1-distill-qwen-32b": "openai/r1-distill-qwen-32b",
    "routeway-nemotron-nano-9b": "openai/nemotron-nano-9b-v2",
    "routeway-kimi-k2": "openai/kimi-k2-0905",

    # --- OpenRouter (Aggregation Layer - Free Tier) ---
    "openrouter-gemini-2.0-flash": "openrouter/google/gemini-2.0-flash-exp:free",
    "openrouter-llama-3.1-405b": "openrouter/meta-llama/llama-3.1-405b-instruct:free",
    "openrouter-llama-3.3-70b": "openrouter/meta-llama/llama-3.3-70b-instruct:free",
    "openrouter-qwen3-coder": "openrouter/qwen/qwen3-coder:free",
    "openrouter-deepseek-r1": "openrouter/deepseek/deepseek-r1-0528:free",
    "openrouter-kat-coder": "openrouter/kwaipilot/kat-coder-pro:free",
    "openrouter-mistral-small-24b": "openrouter/mistralai/mistral-small-3.1-24b-instruct:free",
    "openrouter-gemma-3-27b": "openrouter/google/gemma-3-27b-it:free",
    "openrouter-qwen-2.5-vl-7b": "openrouter/qwen/qwen-2.5-vl-7b-instruct:free",
    
    "llm7-default": "openai/default",
    "llm7-fast": "openai/fast",
    "llm7-gpt-4-nano": "openai/gpt-4.1-nano-2025-04-14",
    # "llm7-pro": "openai/pro", # 402 Payment Required
    # "llm7-mistral-small": "openai/mistral-small-3.1-24b-instruct-2503", # 402 Payment Required

    # --- ElectronHub.ai (TRULY FREE Models - pricing: $0) ---
    
    # OpenAI GPT-5 Mini FREE (Successor to o4-mini)
    "eh-gpt-5-mini-free": "openai/gpt-5-mini:free",  # GPT-5 Mini FREE! Vision + Reasoning
    
    # OpenAI O-Series (Verified FREE)
    "eh-o3-mini": "openai/o3-mini",  # FREE
    "eh-o3": "openai/o3",  # FREE (5.29s) ✅
    "eh-o3-high": "openai/o3-high",  # FREE (5.09s) ✅
    
    # ZhipuAI GLM 4.7 FREE (Latest flagship)
    "eh-glm-4.7-free": "openai/glm-4.7:free",  # GLM 4.7 FREE! Programming + Reasoning
    
    # MoonshotAI Kimi K2 Thinking FREE (Trillion-param MoE, 256k context)
    "eh-kimi-k2-thinking-free": "openai/kimi-k2-thinking:free",  # Kimi K2 Thinking FREE! 256k context
    
    # Meta Llama 4 (LMArena Leaders - FREE)
    "eh-llama-4-maverick-free": "openai/llama-4-maverick-17b-128e-instruct:free",  # 128-Expert MoE (Jan 2026 ELO Leader)
    "eh-llama-4-scout-free": "openai/llama-4-scout-17b-16e-instruct:free",  # Multimodal Expert
    
    # Nvidia Nemotron Ultra (Verified - LARGEST!)
    "eh-nemotron-ultra-253b": "openai/llama-3.1-nemotron-ultra-253b-v1",  # 253B params (1.76s) ✅
    
    # X.AI Grok (Verified)
    "eh-grok-4-fast": "openai/grok-4-fast:free",  # Grok FREE (33.97s) ✅
    
    # Xiaomi (Verified)
    "eh-mimo-v2-flash": "openai/mimo-v2-flash",  # Fast Chinese (1.61s) ✅
    
    # --- NON-PREMIUM PAID Models (use with $1 budget) ---
    # Note: Some may not work via ElectronHub's OpenAI-compatible endpoint
    "eh-o4-mini": "openai/o4-mini",  # O4 Mini ($1.1/M) - May not be supported
    "eh-gpt-5-nano": "openai/gpt-5-nano",  # GPT-5 Nano ($0.05/M) - May not be supported
    "eh-gpt-5-mini-paid": "openai/gpt-5-mini",  # GPT-5 Mini ($0.25/M) - May not be supported  
    "eh-nova-micro-paid": "openai/nova-micro-v1",  # Nova Micro ($0.035/M) - May not be supported
    
    # Excluded (not truly free / failed verification):
    # "eh-claude-haiku-4.5": "openai/claude-haiku-4-5-20251001:free",  # Timeout
    # "eh-codex-mini-high": "openai/codex-mini-latest-high",  # 402 Payment
    # "eh-glm-4": "openai/glm-4",  # 402 Payment (use glm-4.7:free instead)
    # "eh-nova-micro": "openai/nova-micro-v1",  # Timeout
}

# --- Capability-Based Abstractions (The "Long Term" Auto-Selection Layer) ---
# Agents request a capability, not a specific model. Check here for current SOTA.
CAPABILITY_MAP = {
    # For complex reasoning, hypothesis generation, RCA (Slow but smart)
    "complex_reasoning": "eh-kimi-k2-thinking-free", # Kimi K2 Thinking FREE (256k context, SOTA Reasoning)
    
    # For architectural decisions, security audits, large context
    "architectural_review": "cerebras-qwen-user-235b", # Qwen 3 235B (Massive Scale)
    
    # For coding tasks, refactoring, implementation  
    "coding_specialist": "eh-glm-4.7-free", # GLM 4.7 FREE (SOTA Agentic Coding: 73.8% SWE-bench)
    
    # For fast/simple tasks, classification, routing data
    "fast_routing": "eh-llama-4-maverick-free", # Llama 4 Maverick (128-Expert MoE, Ultra-Fast)
    
    # Good balance of speed/cost/intelligence (Default)
    "balanced": "eh-llama-4-maverick-free", # Llama 4 Maverick (Jan 2026 LMArena ELO Leader)
    
    # For general purpose agent work
    "auto": "eh-llama-4-maverick-free",
    
    # New: Vision/Multimodal specifically
    "vision": "eh-llama-4-scout-free", # Llama 4 Scout (Multimodal Expert)
    
    # New: Long Context Processing
    "long_context": "eh-kimi-k2-thinking-free", # Kimi K2 FREE (256k Context, SOTA Tool-Use)
}

# --- Fallback Chains (Resilience Layer) ---
# Ordered lists of models to try when the primary fails.
# Context-aware chains prioritize different capability profiles.
# OPTIMIZATION (2026-01-06): OpenRouter models moved to END (404 issues), added unused models
FALLBACK_CHAINS = {
    # Reasoning/Logic: For complex problem solving, planning, and RCA
    # ORDERING STRATEGY: Quality First (SOTA Reasoning) > Reliable Anchors > Speed
    "reasoning": [
        "eh-kimi-k2-thinking-free", # 1. Quality FREE (256k context)
        "cf-deepseek-r1",           # 2. Quality SOTA (Tier 2 Platform)
        "routeway-deepseek-r1",     # 3. Quality SOTA (Tier 3 Proxy)
        "cerebras-qwen-user-235b",  # 4. Reliability Anchor (Tier 1 Native)
        "llm-gateway-deepseek-r1",  # 5. Quality Backup (Tier 3)
        "groq-llama-4-maverick",    # 6. Speed Anchor (Tier 1)
        "gh-phi-4",                 # 7. Reasoning SOTA (Tier 2 Protocol)
        "gemini",                   # 8. Reliability Anchor (Tier 2)
        "mistral-large",            # 9. Quality Anchor (Tier 1)
        "gh-gpt-4o",                # 10. Quality Anchor (Tier 2)
        "mixtral-8x22b",
        "cf-qwq-32b",
        "routeway-r1-distill-qwen-32b",
        "llm-gateway-llama-4-maverick",
        "openrouter-deepseek-r1",
    ],
    
    # Coding: For implementation, refactoring, and code review
    # ORDERING STRATEGY: Quality First (SOTA Coding) > Specialist Models > Speed
    "code": [
        "eh-glm-4.7-free",          # 1. Quality FREE (GLM 4.7 Programming)
        "cerebras-glm4",            # 2. Quality SOTA (Tier 1 Native)
        "codestral",                # 3. Specialist SOTA (Tier 1 Native)
        "cf-qwen-2.5-coder-32b",    # 4. Quality SOTA (Tier 2 Platform)
        "routeway-devstral-2-2512", # 5. Quality Fallback (Tier 3 Proxy)
        "groq-qwen-3-32b",          # 6. Speed Anchor (Tier 1)
        "gh-gpt-4o",                # 7. Quality Anchor (Tier 2)
        "routeway-deepseek-v31",    # 8. SOTA Coding (Tier 3 Proxy)
        "groq-kimi-k2",
        "groq-llama-4-maverick",
        "llm-gateway-glm-4.5",
        "llm-gateway-kimi-k2",
        "openrouter-qwen3-coder",
        "openrouter-kat-coder",
    ],
    
    # Long Context: For processing massive documents or entire codebases
    # ORDERING STRATEGY: Context Quality (256k+) > Reliability > Speed
    "long_context": [
        "eh-kimi-k2-thinking-free", # 1. Quality FREE (256k, ElectronHub)
        "groq-kimi-k2",             # 2. Tier 1
        "cf-llama-4-scout",         # 3. Tier 2
        "cerebras-qwen-user-235b",  # 4. Tier 1
        "gemini",                   # 5. Reliability Anchor (Tier 2)
        "gh-gpt-4o",                # 6. Tier 2
        "gh-mistral-nemo",          # 7. Tier 2
        "llm-gateway-kimi-k2",      # 8. Tier 3
        "llm-gateway-llama-4-scout",# 9. Tier 3
        "gemini-flash",             # 10. Tier 2
        "mixtral-8x22b",            # 11. Large MoE
    ],
    
    # Speed: For classification, routing, and ultra-fast iterations
    # ORDERING STRATEGY: Throughput/Latency (Fastest First) > Reliability
    "speed": [
        "eh-llama-4-maverick-free", # 1. SOTA Fast (128-Expert MoE)
        "cerebras-llama3.3-70b",    # 2. Tier 1 (2500 t/s)
        "cerebras-llama3-8b",       # 3. Tier 1
        "cf-llama-3.1-8b-fast",     # 4. Tier 2
        "gh-gpt-4o-mini",           # 5. Tier 2 (Reliable)
        "ministral-8b",             # 6. Tier 1 Native
        "gemini-lite",              # 7. Tier 2
        "groq-llama-4-scout",       # 8. Tier 1
        "gh-mistral-nemo",          # 9. Tier 2
        "routeway-llama-3.3-70b",   # 10. Tier 3
        "routeway-llama-3.1-8b",    # 11. Tier 3
        "llm-gateway-gpt-oss-20b",  # 12. Tier 3
        "llm7-fast",                # 13. New Fast Option
    ],
    
    # Vision/Multimodal: For image, diagram, and UI analysis
    # ORDERING STRATEGY: Vision Accuracy (Multimodal Experts) > General Anchors
    "vision": [
        "eh-llama-4-scout-free",    # 1. Multimodal Expert (Llama 4 Scout)
        "groq-llama-4-scout",       # 2. Tier 1 (verified)
        "gh-gpt-4o",                # 3. Tier 2
        "gemini",                   # 4. Quality Anchor (Tier 2)
        "cf-mistral-small-24b",     # 5. Tier 2
        "gh-phi-4-multimodal",      # 6. Tier 2
        "gh-llama-3.2-90b",         # 7. Tier 2
        "gh-llama-3.2-11b",         # 8. Tier 2
        "pixtral-large",            # 9. Tier 1 Native
        "cf-gemma-3-12b",           # 10. Tier 2
        "llm-gateway-llama-4-scout",# 11. Tier 3
        "gemini-experimental",      # 12. Specialized (Tier 2)
        "openrouter-gemini-2.0-flash",
        "openrouter-qwen-2.5-vl-7b",
    ],
    
    # Balanced (default): General purpose agent logic
    # ORDERING STRATEGY: ELO/Quality Leader > Native Anchors > Platform Anchors
    "balanced": [
        "eh-llama-4-maverick-free", # 1. Jan 2026 ELO Leader
        "groq-llama-4-maverick",    # 2. Quality/Speed Native Anchor (Tier 1)
        "gemini",                   # 3. Quality Platform Anchor (Tier 2)
        "cerebras-qwen-user-235b",  # 4. Reasoning Quality Anchor (Tier 1)
        "routeway-deepseek-r1",     # 5. Reasoning Quality Fallback (Tier 3)
        "mistral-large",            # 6. Quality Anchor (Tier 1)
        "gh-gpt-4o",                # 7. Quality Anchor (Tier 2)
        "groq-kimi-k2",
        "cf-llama-3.3-70b",
        "cerebras-llama3.3-70b",
        "routeway-llama-3.3-70b",
        "llm-gateway-llama-4-maverick",
        "openrouter-llama-3.1-405b",
        "openrouter-gemini-2.0-flash",
        "llm7-default",             # 15. Quality Fallback
    ],
}

# Legacy Compatibility (links to balanced chain)
FALLBACK_ORDER = FALLBACK_CHAINS["balanced"]

# --- Validation Layer ---
def validate_capability(capability: str) -> bool:
    """Ensure capability exists in CAPABILITY_MAP."""
    if capability not in CAPABILITY_MAP:
        raise ValueError(f"Invalid capability: {capability}. Valid options: {list(CAPABILITY_MAP.keys())}")
    return True

def get_litellm_model(friendly_name: str) -> str:
    """
    Returns the LiteLLM model string for a given friendly name or capability alias.
    Resolves recursive aliases (e.g. 'auto' -> 'llama3' -> 'groq/...').
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # 1. Resolve capability alias if present
    resolved_name = CAPABILITY_MAP.get(friendly_name, friendly_name)
    
    # Log capability resolution
    if resolved_name != friendly_name:
        logger.debug(f"🔀 Capability '{friendly_name}' → '{resolved_name}'")
    
    # 2. Resolve final model name to LiteLLM string
    final_model = MODEL_MAP.get(resolved_name, resolved_name)
    
    if final_model != resolved_name:
        logger.debug(f"🎯 Model '{resolved_name}' → '{final_model}'")
    
    return final_model

def get_fallback_chain(capability_or_model: str, strategy: str = "balanced") -> list[str]:
    """
    Returns a list of LiteLLM model strings to try, starting with the primary model.
    New context-aware logic prioritizes chains based on 'strategy' arg.
    
    Strategies: 'reasoning', 'code', 'speed', 'long_context', 'vision', 'balanced'.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Determine which fallback chain to use as base
    # Correct invalid strategies to "balanced"
    target_strategy = strategy if strategy in FALLBACK_CHAINS else "balanced"
    if strategy not in FALLBACK_CHAINS:
        logger.warning(f"⚠️ Unknown strategy '{strategy}', defaulting to 'balanced'")

    base_chain_friendly = FALLBACK_CHAINS[target_strategy]
    
    # Convert base chain to LiteLLM strings
    base_chain_litellm = []
    for m in base_chain_friendly:
        if m in MODEL_MAP:
            base_chain_litellm.append(MODEL_MAP[m])

    # 1. Try Capability Map (Preferred)
    if capability_or_model in CAPABILITY_MAP:
        primary_friendly = CAPABILITY_MAP[capability_or_model]
        primary_litellm = get_litellm_model(primary_friendly)
        
        if primary_litellm in base_chain_litellm:
             # Order Preservation: Try primary, then fallback to global order (excluding primary)
             remaining = [m for m in base_chain_litellm if m != primary_litellm]
             return [primary_litellm] + remaining
        
        # Prepend primary if not in chain
        return [primary_litellm] + base_chain_litellm

    # 2. Try Model Map (Known Friendly Name)
    if capability_or_model in MODEL_MAP:
        primary_litellm = MODEL_MAP[capability_or_model]
        
        if primary_litellm in base_chain_litellm:
             # Order Preservation
             remaining = [m for m in base_chain_litellm if m != primary_litellm]
             return [primary_litellm] + remaining
            
        return [primary_litellm] + base_chain_litellm

    # 3. Direct LiteLLM string or Unknown
    if "/" in capability_or_model:
        return [capability_or_model]

    # 4. Unknown Capability - Fallback to Default (Safety Net)
    logger.error(f"❌ Unknown capability/model '{capability_or_model}'. Using '{target_strategy}' chain.")
    return base_chain_litellm

import os

def get_api_keys_for_provider(model_name: str) -> list[str]:
    """
    Returns a list of API keys to try for a given model.
    Dynamically scans env for {PREFIX}_API_KEY, {PREFIX}_API_KEY_SECONDARY, 
    and {PREFIX}_API_KEY_2 through 10.
    """
    keys = []
    prefix = ""
    
    # Identify Provider Prefix
    if "openrouter" in model_name:
        prefix = "OPENROUTER"
    elif "routeway" in model_name:
        prefix = "ROUTEWAY"
    elif "llm-gateway" in model_name or "llmgateway" in model_name:
        prefix = "LLMGATEWAY"
    elif "openai/" in model_name and "free" in model_name: 
        # Heuristic for LLM Gateway Free models mapped as openai/
        prefix = "LLMGATEWAY"
    elif "gemini" in model_name:
        prefix = "GEMINI"
    elif "groq" in model_name:
        prefix = "GROQ"
    elif "claude" in model_name or "anthropic" in model_name:
        prefix = "ANTHROPIC"
    elif "command" in model_name or "cohere" in model_name:
        prefix = "COHERE"
    elif "mistral" in model_name or "codestral" in model_name or "mixtral" in model_name:
        prefix = "MISTRAL"
    elif "cerebras" in model_name:
        prefix = "CEREBRAS"
    elif "cloudflare" in model_name or "@cf/" in model_name or "cf-" in model_name:
        prefix = "CLOUDFLARE"
    elif "github" in model_name:
        prefix = "GITHUB"
    elif "braintrust" in model_name or "bt-" in model_name:
        prefix = "BRAINTRUST"
    elif "llm7" in model_name:
        prefix = "LLM7"
    elif "electronhub" in model_name or model_name.startswith("eh-"):
        prefix = "ELECTRONHUB"
        
    if prefix:
        # Debug logging for troubleshooting
        # print(f"DEBUG: Identifying keys for {prefix} (Model: {model_name})")
        
        # 1. Base Key
        env_key = f"{prefix}_API_KEY"
        # Special case for Cloudflare which uses TOKEN
        if prefix == "CLOUDFLARE":
            env_key = "CLOUDFLARE_API_TOKEN"
        # Special case for GitHub which uses TOKEN per conventions (sometimes GITHUB_access_token)
        if prefix == "GITHUB":
            env_key = "GITHUB_TOKEN"
            
        val = os.getenv(env_key)
        if val:
            keys.append(val)
        
        # Special Handling for Providers needing Custom Base
        api_base = None
        if prefix == "GROQ":
            # Groq doesn't use api_base for standard models, but some might
            pass
        if prefix == "BRAINTRUST":
            # Braintrust uses custom base
            pass
        if prefix == "LLMGATEWAY":
            api_base = "https://api.llmgateway.io/v1"
            
        # 2. Search for keys in environment
        # Pattern: {PREFIX}_API_KEY, {PREFIX}_API_KEY_2, etc.
        
        # 2. Explicit Secondary (Legacy/User Request)
        secondary = os.getenv(f"{prefix}_API_KEY_SECONDARY")
        if secondary: keys.append(secondary)
        
        # Numbered Keys (Scalable: _2 to _10)
        for i in range(2, 11):
            # Check for regular numbering: {PREFIX}_API_KEY_{i}
            k = os.getenv(f"{prefix}_API_KEY_{i}")
            if k: keys.append(k)
            
            # Special caseNumbered keys for Cloudflare/GitHub
            if prefix == "CLOUDFLARE":
                k_cf = os.getenv(f"CLOUDFLARE_API_TOKEN_{i}")
                if k_cf: keys.append(k_cf)
            elif prefix == "GITHUB":
                k_gh = os.getenv(f"GITHUB_TOKEN_{i}")
                if k_gh: keys.append(k_gh)

    # If we identified a prefix but found NO keys in ENV, 
    # we should NOT return [None] because LiteLLM will then 
    # try to use the ENV default which we already know is missing.
    # Instead, we return an empty list so the caller knows this provider is dead.
    
    # Load Balancing: Shuffle keys to distribute rate limits
    if len(keys) > 1:
        # Cloudflare logic note preserved from original
        random.shuffle(keys)
        
    return keys

# --- Performance Optimization: O(1) Reverse Lookup ---
# Map: litellm_string -> List[friendly_name]
# Needed because multiple friendly names can map to one litellm string
REVERSE_MODEL_MAP: dict[str, list[str]] = {}
for friendly, litellm in MODEL_MAP.items():
    if litellm not in REVERSE_MODEL_MAP:
        REVERSE_MODEL_MAP[litellm] = []
    REVERSE_MODEL_MAP[litellm].append(friendly)

# --- Architecture: Provider Identification Patterns ---
# Tuple: (Provider, Heuristic Type, Value)
# Types: 'contains', 'startswith', 'suffix', 'exact'
PROVIDER_PATTERNS = [
    # Heuristics on the resolved LiteLLM string itself
    ('ELECTRONHUB', 'contains', ':free'),
    ('ELECTRONHUB', 'startswith', 'eh-'),
    ('OPENAI', 'startswith', 'openai/'),
    ('OPENROUTER', 'contains', 'openrouter'),
    ('ROUTEWAY', 'contains', 'routeway'),
    ('LLMGATEWAY', 'contains', 'llm-gateway'),
    ('LLMGATEWAY', 'contains', 'llmgateway'),
    ('GEMINI', 'contains', 'gemini'),
    ('GROQ', 'contains', 'groq'),
    ('ANTHROPIC', 'contains', 'claude'),
    ('ANTHROPIC', 'contains', 'anthropic'),
    ('COHERE', 'contains', 'command'),
    ('COHERE', 'contains', 'cohere'),
    ('MISTRAL', 'contains', 'mistral'),
    ('MISTRAL', 'contains', 'codestral'),
    ('MISTRAL', 'contains', 'mixtral'),
    ('CEREBRAS', 'contains', 'cerebras'),
    ('CLOUDFLARE', 'contains', 'cloudflare'),
    ('CLOUDFLARE', 'contains', '@cf/'),
    ('CLOUDFLARE', 'contains', 'cf-'),
    ('GITHUB', 'contains', 'github'),
    ('BRAINTRUST', 'contains', 'braintrust'),
    ('LLM7', 'contains', 'llm7'),
]

# Patterns for Friendly Names (from Reverse Lookup)
FRIENDLY_NAME_PATTERNS = [
    ('ELECTRONHUB', 'startswith', 'eh-'),
    ('ELECTRONHUB', 'contains', 'electronhub'),
    ('ROUTEWAY', 'startswith', 'routeway-'),
    ('ROUTEWAY', 'contains', 'routeway'),
    ('LLMGATEWAY', 'startswith', 'llm-gateway'),
    ('LLMGATEWAY', 'contains', 'llmgateway'),
    ('BRAINTRUST', 'startswith', 'bt-'),
    ('BRAINTRUST', 'contains', 'braintrust'),
    ('GITHUB', 'startswith', 'gh-'),
    ('GITHUB', 'contains', 'github'),
    ('CLOUDFLARE', 'startswith', 'cf-'),
    ('CLOUDFLARE', 'contains', 'cloudflare'),
    ('GROQ', 'startswith', 'groq-'),
    ('GROQ', 'contains', 'groq'),
    ('GEMINI', 'startswith', 'gemini'),
]

def _infer_provider_prefix(model_name: str) -> list[str]:
    """
    Infers the provider prefixes (e.g., 'ELECTRONHUB', 'OPENAI') for a given model string.
    
    Strategy:
    1. Check heuristics on the model string itself using PROVIDER_PATTERNS.
    2. Perform O(1) REVERSE LOOKUP in REVERSE_MODEL_MAP to find friendly names.
    3. Check friendly names against FRIENDLY_NAME_PATTERNS.
    
    Returns a list of unique prefixes found.
    """
    prefixes = set()
    
    # 1. Direct Heuristics on LiteLLM string
    for provider, match_type, val in PROVIDER_PATTERNS:
        if match_type == 'contains' and val in model_name:
            prefixes.add(provider)
        elif match_type == 'startswith' and model_name.startswith(val):
            prefixes.add(provider)
        elif match_type == 'suffix' and model_name.endswith(val):
            prefixes.add(provider)
            
    # 2. Reverse Lookup via Precomputed Map (O(1))
    friendly_names = REVERSE_MODEL_MAP.get(model_name, [])
    
    for friendly in friendly_names:
        for provider, match_type, val in FRIENDLY_NAME_PATTERNS:
             if match_type == 'contains' and val in friendly:
                 prefixes.add(provider)
             elif match_type == 'startswith' and friendly.startswith(val):
                 prefixes.add(provider)
             elif match_type == 'suffix' and friendly.endswith(val):
                 prefixes.add(provider)
    
    return list(prefixes)

def _get_keys_for_prefix(prefix: str, model_name: str) -> list[str]:
    """Helper to get keys for a specific identified prefix."""
    keys = []
    
    # 1. Base Key
    env_key = f"{prefix}_API_KEY"
    # Special case for Cloudflare which uses TOKEN
    if prefix == "CLOUDFLARE":
        env_key = "CLOUDFLARE_API_TOKEN"
    # Special case for GitHub which uses TOKEN per conventions
    if prefix == "GITHUB":
        env_key = "GITHUB_TOKEN"
        
    val = os.getenv(env_key)
    if val:
        keys.append(val)
    
    # 2. Secondary
    secondary = os.getenv(f"{prefix}_API_KEY_SECONDARY")
    if secondary: keys.append(secondary)
    
    # 3. Numbered Keys (Scalable: _2 to _10)
    for i in range(2, 11):
        k = os.getenv(f"{prefix}_API_KEY_{i}")
        if k: keys.append(k)
        
        # Special case Numbered keys for Cloudflare/GitHub
        if prefix == "CLOUDFLARE":
            k_cf = os.getenv(f"CLOUDFLARE_API_TOKEN_{i}")
            if k_cf: keys.append(k_cf)
        elif prefix == "GITHUB":
            k_gh = os.getenv(f"GITHUB_TOKEN_{i}")
            if k_gh: keys.append(k_gh)
            
    return keys

def get_api_keys_for_provider(model_name: str) -> list[str]:
    """
    Returns a list of API keys to try for a given model.
    Dynamically scans env for keys based on inferred provider(s).
    Supports multiple providers mapping to the same model string resilience.
    """
    keys = []
    prefixes = _infer_provider_prefix(model_name)
    
    if not prefixes:
        # Fallback to simple string check if inference failed completely
        # (Preserves legacy behavior if needed, though _infer covers basic string checks too)
        # Assuming inference is comprehensive.
        pass
        
    for prefix in prefixes:
        provider_keys = _get_keys_for_prefix(prefix, model_name)
        keys.extend(provider_keys)
        
    # Load Balancing: Shuffle keys to distribute rate limits
    if len(keys) > 1:
        # Cloudflare Note: shuffle is risky if accounts differ, handled in parallel_agents
        random.shuffle(keys)
        
    return keys

def get_cloudflare_account_id(api_token: str) -> str:
    """
    Returns the Account ID corresponding to a specific Cloudflare API Token.
    Searches env vars to find which index the token belongs to.
    """
    # 1. Check primary
    if api_token == os.getenv("CLOUDFLARE_API_TOKEN"):
        return os.getenv("CLOUDFLARE_ACCOUNT_ID")
        
    # 2. Check secondary/numbered
    for i in range(2, 11):
        if api_token == os.getenv(f"CLOUDFLARE_API_TOKEN_{i}") or \
           api_token == os.getenv(f"CLOUDFLARE_API_KEY_{i}"):
            # Check for matching Account ID
            acc_id = os.getenv(f"CLOUDFLARE_ACCOUNT_ID_{i}")
            if acc_id:
                return acc_id
                
    # Fallback: Return primary Account ID if no match found (mostly for legacy)
    return os.getenv("CLOUDFLARE_ACCOUNT_ID")

def get_api_base(model_name: str) -> Optional[str]:
    """
    Returns the custom api_base URL for a given model if required.
    Crucial for proxies like LLM Gateway or Braintrust.
    
    Conflict Resolution:
    If a model maps to multiple providers (e.g. ELECTRONHUB and ROUTEWAY),
    we enforce a strict PRIORITY to prefer Free/Cheap options.
    """
    prefixes = _infer_provider_prefix(model_name)
    
    # Priority List: Free/Cheap > Paid Proxy > Native
    PRIORITY = ['ELECTRONHUB', 'ROUTEWAY', 'LLMGATEWAY', 'BRAINTRUST', 'OPENAI', 'GROQ', 'MISTRAL', 'CLOUDFLARE']
    
    # Find the best prefix present in both the inferred list and priority list
    selected_prefix = None
    for p in PRIORITY:
        if p in prefixes:
            selected_prefix = p
            break
            
    # If no priority match found, take the first one (arbitrary but deterministic from list)
    if not selected_prefix and prefixes:
        selected_prefix = prefixes[0]
        
    if not selected_prefix:
        return None

    # Return base for the selected prefix
    if selected_prefix == "LLMGATEWAY":
        return "https://api.llmgateway.io/v1"
    elif selected_prefix == "ROUTEWAY":
        return "https://api.routeway.ai/v1"
    elif selected_prefix == "BRAINTRUST":
        return "https://api.braintrust.dev/v1/proxy"
    elif selected_prefix == "LLM7":
        return "https://api.llm7.io/v1"
    elif selected_prefix == "ELECTRONHUB":
        return "https://api.electronhub.ai/v1/"
    elif selected_prefix == "OPENROUTER":
        # OpenRouter usually handled via litellm provider 'openrouter/', 
        # but if using openai/ format, it needs base:
        return "https://openrouter.ai/api/v1"
        
    return None
