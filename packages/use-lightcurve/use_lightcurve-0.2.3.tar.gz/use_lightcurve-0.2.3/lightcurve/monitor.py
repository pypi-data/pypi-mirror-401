
import sys
import importlib
from typing import List, Optional
from .client import Lightcurve

# Global client instance for auto-instrumentation
_global_client = None

def monitor(api_key: Optional[str] = None, base_url: Optional[str] = None, agent_id: str = "default-agent", integrations: Optional[List[str]] = None):
    """
    Enables auto-instrumentation for supported libraries.
    
    Args:
        api_key: Lightcurve API Key.
        base_url: Lightcurve API URL.
        agent_id: The Agent ID to associate runs with.
        integrations: List of specific integrations to enable (e.g. ['openai']). 
                      If None, auto-detects installed libraries.
    """
    global _global_client
    
    # Initialize singleton client
    if _global_client is None:
        _global_client = Lightcurve(api_key=api_key, base_url=base_url)
    
    # Store agent_id in client for easy access by patchers
    _global_client.default_agent_id = agent_id

    # Detect and Apply Integrations
    enabled_integrations = []
    
    # 1. OpenAI
    if not integrations or 'openai' in integrations:
        if 'openai' in sys.modules or importlib.util.find_spec('openai'):
            try:
                from .integrations.openai import OpenAIIntegration
                OpenAIIntegration.patch(_global_client)
                enabled_integrations.append('openai')
            except Exception as e:
                print(f"[Lightcurve] Failed to patch OpenAI: {e}")

    # 2. Anthropic
    if not integrations or 'anthropic' in integrations:
        if 'anthropic' in sys.modules or importlib.util.find_spec('anthropic'):
            try:
                from .integrations.anthropic import AnthropicIntegration
                AnthropicIntegration.patch(_global_client)
                enabled_integrations.append('anthropic')
            except Exception as e:
                print(f"[Lightcurve] Failed to patch Anthropic: {e}")

    # 3. LangChain
    if not integrations or 'langchain' in integrations:
        if 'langchain' in sys.modules or importlib.util.find_spec('langchain'):
            try:
                from .integrations.langchain import LangChainIntegration
                LangChainIntegration.patch(_global_client)
                enabled_integrations.append('langchain')
            except Exception as e:
                print(f"[Lightcurve] Failed to patch LangChain: {e}")

    # 4. LiteLLM
    if not integrations or 'litellm' in integrations:
        if 'litellm' in sys.modules or importlib.util.find_spec('litellm'):
            try:
                from .integrations.litellm import LiteLLMIntegration
                LiteLLMIntegration.patch(_global_client)
                enabled_integrations.append('litellm')
            except Exception as e:
                print(f"[Lightcurve] Failed to patch LiteLLM: {e}")

    # 5. Gemini (google-generativeai)
    if not integrations or 'gemini' in integrations:
        if 'google.generativeai' in sys.modules or importlib.util.find_spec('google.generativeai'):
            try:
                from .integrations.gemini import GeminiIntegration
                GeminiIntegration.patch(_global_client)
                enabled_integrations.append('gemini')
            except Exception as e:
                print(f"[Lightcurve] Failed to patch Gemini: {e}")

    print(f"[Lightcurve] Auto-instrumentation enabled for: {', '.join(enabled_integrations)}")

def get_global_client():
    return _global_client
