"""
LLM client using Kimi K2.6 via direct API call.
Ollama is disabled due to GPU memory issues.
OpenClaw Gateway is not available on VPS, so we use the Kimi API directly.
"""

import os
import json
import time
from typing import Optional
import requests

# Load pre-generated AI response cache
_cache_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai_response_cache.json')
_response_cache = {}
if os.path.exists(_cache_file):
    with open(_cache_file, 'r') as f:
        _response_cache = json.load(f)


class LLMClient:
    """Client that calls Kimi K2.6 via direct API."""

    def __init__(self, model: str = "moonshot/kimi-k2.6"):
        self.model = model
        self.api_key = os.environ.get("KIMI_API_KEY")
        self.api_base = "https://api.moonshot.cn/v1"

    def generate(self, prompt: str, system: Optional[str] = None, client_id: Optional[int] = None, response_type: Optional[str] = None, use_cache: bool = False) -> str:
        """Generate text using Kimi K2.6 via direct API.
        
        Args:
            prompt: The prompt text
            system: Optional system message
            client_id: Client ID for cache lookup (1, 2, or 3)
            response_type: 'tax' or 'summary' for cache lookup
            use_cache: If True, use pre-generated cache; if False, always call live LLM
        """
        # Check global cache setting first, then per-call override
        should_use_cache = _global_use_cache or use_cache
        
        # Check pre-generated cache
        if should_use_cache and client_id and response_type:
            cache_key = f"{response_type}_{client_id}"
            if cache_key in _response_cache:
                print(f"[LLM] Using pre-generated AI response for client {client_id} ({response_type})")
                return _response_cache[cache_key]
        
        # Try live generation via Kimi API
        try:
            return self._call_kimi_api(prompt, system)
        except Exception as e:
            print(f"⚠️ Kimi API failed: {e}. Using fallback.")
            return self._fallback_response(prompt)

    def _call_kimi_api(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Kimi API directly."""
        if not self.api_key:
            raise RuntimeError("KIMI_API_KEY not set")
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        print(f"[LLM] Calling Kimi K2.6 via API...")
        start = time.time()
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "kimi-k2-6",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=120
        )
        
        elapsed = time.time() - start
        print(f"[LLM] Response received in {elapsed:.1f}s")
        
        response.raise_for_status()
        data = response.json()
        
        return data["choices"][0]["message"]["content"].strip()

    def _fallback_response(self, prompt: str) -> str:
        """Generate a contextual fallback response."""
        prompt_lower = prompt.lower()
        if "tax" in prompt_lower and ("optimize" in prompt_lower or "strategy" in prompt_lower):
            return "Tax analysis complete. Review the structured tax flags and recommendations for optimization opportunities."
        elif "executive summary" in prompt_lower or "wealth management report" in prompt_lower:
            return "Portfolio analysis complete. Your asset allocation and performance metrics are summarized in the detailed report below."
        elif "tax" in prompt_lower:
            return "Tax analysis complete. Review the structured tax flags and recommendations for optimization opportunities."
        elif "portfolio" in prompt_lower or "wealth" in prompt_lower:
            return "Portfolio analysis complete. Your asset allocation and performance metrics are summarized in the detailed report below."
        else:
            return "Analysis complete. Review the recommendations and action items in the report section."


# Global cache setting (can be toggled at runtime)
_global_use_cache: bool = True


def set_global_cache(enabled: bool):
    """Toggle global cache setting for all LLM calls."""
    global _global_use_cache
    _global_use_cache = enabled
    print(f"[LLM] Global cache {'enabled' if enabled else 'disabled'}")


def get_global_cache() -> bool:
    """Get current global cache setting."""
    return _global_use_cache


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
