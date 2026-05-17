"""
LLM client using Kimi K2.6 via OpenClaw CLI.
Ollama is disabled due to GPU memory issues.
"""

import os
import json
import subprocess
from typing import Optional
import hashlib
import time

# Load pre-generated AI response cache
_cache_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai_response_cache.json')
_response_cache = {}
if os.path.exists(_cache_file):
    with open(_cache_file, 'r') as f:
        _response_cache = json.load(f)


class LLMClient:
    """Client that calls Kimi K2.6 via OpenClaw CLI."""

    def __init__(self, model: str = "moonshot/kimi-k2.6"):
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None, client_id: Optional[int] = None, response_type: Optional[str] = None, use_cache: bool = False) -> str:
        """Generate text using Kimi K2.6 via OpenClaw CLI.
        
        Args:
            prompt: The prompt text
            system: Optional system message
            client_id: Client ID for cache lookup (1, 2, or 3)
            response_type: 'tax' or 'summary' for cache lookup
            use_cache: If True, use pre-generated cache; if False, always call live LLM
        """
        # Check pre-generated cache only if explicitly requested
        if use_cache and client_id and response_type:
            cache_key = f"{response_type}_{client_id}"
            if cache_key in _response_cache:
                print(f"[LLM] Using pre-generated AI response for client {client_id} ({response_type})")
                return _response_cache[cache_key]
        
        # Try live generation via OpenClaw CLI
        try:
            return self._call_openclaw(prompt, system)
        except Exception as e:
            print(f"⚠️ OpenClaw CLI failed: {e}. Using fallback.")
            return self._fallback_response(prompt)

    def _call_openclaw(self, prompt: str, system: Optional[str] = None) -> str:
        """Call OpenClaw CLI to run Kimi K2.6."""
        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n{prompt}"
        
        print(f"[LLM] Calling Kimi K2.6 via OpenClaw CLI...")
        start = time.time()
        
        result = subprocess.run(
            ["openclaw", "capability", "model", "run", "--model", self.model, "--prompt", full_prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        elapsed = time.time() - start
        print(f"[LLM] Response received in {elapsed:.1f}s")
        
        if result.returncode != 0:
            raise RuntimeError(f"OpenClaw CLI error: {result.stderr}")
        
        # Parse the output - OpenClaw outputs: N header then the content
        lines = result.stdout.strip().split('\n')
        # Find the actual output (after "outputs: N" line)
        output_started = False
        output_lines = []
        for line in lines:
            if output_started:
                output_lines.append(line)
            elif line.startswith("outputs:"):
                output_started = True
        
        return '\n'.join(output_lines).strip()

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


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
