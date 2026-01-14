"""
Usefy Client - Main SDK Implementation
"""

import os
import time
import json
import logging
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
import httpx

from .exceptions import (
    UsefyError,
    UsefyAuthError,
    UsefyBudgetExceeded,
    UsefyRateLimited,
    UsefyProviderError,
    UsefyTimeoutError
)

logger = logging.getLogger("usefy")


@dataclass
class UsefyConfig:
    """Configuration for Usefy client."""
    api_key: str = None
    base_url: str = "https://api.usefy.ai"
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    fail_open: bool = False  # If True, bypass Usefy on errors
    fail_open_timeout: float = 2.0  # Timeout before triggering fail-open
    log_level: str = "WARNING"
    
    def __post_init__(self):
        # Try to get API key from environment
        if not self.api_key:
            self.api_key = os.getenv("USEFY_API_KEY")
        
        # Configure logging
        logging.basicConfig(level=getattr(logging, self.log_level.upper()))


class ChatCompletions:
    """OpenAI-compatible chat completions interface."""
    
    def __init__(self, client: "Usefy"):
        self._client = client
    
    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        provider: str = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a chat completion.
        
        Args:
            model: Model name (e.g., "gpt-4", "claude-3-opus")
            messages: List of message dicts with role and content
            provider: AI provider (auto-detected from model if not specified)
            stream: Enable streaming (default: False)
            **kwargs: Additional parameters passed to provider
            
        Returns:
            Chat completion response from provider
        """
        # Auto-detect provider from model name
        if not provider:
            provider = self._detect_provider(model)
        
        body = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        return self._client._proxy_request(provider, body, stream=stream)
    
    def _detect_provider(self, model: str) -> str:
        """Detect provider from model name."""
        model_lower = model.lower()
        
        if any(x in model_lower for x in ["gpt", "o1", "o3", "davinci", "curie"]):
            return "openai"
        elif any(x in model_lower for x in ["claude"]):
            return "anthropic"
        elif any(x in model_lower for x in ["gemini"]):
            return "google"
        elif any(x in model_lower for x in ["mistral", "mixtral"]):
            return "mistral"
        elif any(x in model_lower for x in ["command"]):
            return "cohere"
        elif any(x in model_lower for x in ["deepseek"]):
            return "deepseek"
        elif any(x in model_lower for x in ["llama", "groq"]):
            return "groq"
        elif any(x in model_lower for x in ["grok"]):
            return "xai"
        else:
            return "openai"  # Default


class Chat:
    """OpenAI-compatible chat interface."""
    
    def __init__(self, client: "Usefy"):
        self.completions = ChatCompletions(client)


class Usefy:
    """
    Usefy client for AI cost control and budget management.
    
    Usage:
        from usefy import Usefy
        
        client = Usefy(api_key="us_live_xxx")
        
        # OpenAI-compatible interface
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        
        # Or with explicit provider
        response = client.chat.completions.create(
            model="claude-3-opus",
            provider="anthropic",
            messages=[{"role": "user", "content": "Hello!"}]
        )
    """
    
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        timeout: float = None,
        max_retries: int = None,
        fail_open: bool = None,
        config: UsefyConfig = None
    ):
        """
        Initialize Usefy client.
        
        Args:
            api_key: Usefy API key (starts with 'us_live_')
            base_url: API base URL (default: https://api.usefy.ai)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Max retry attempts (default: 3)
            fail_open: If True, bypass Usefy on connection errors
            config: UsefyConfig object (overrides other params)
        """
        # Use config or create from params
        if config:
            self.config = config
        else:
            self.config = UsefyConfig(
                api_key=api_key,
                base_url=base_url or "https://api.usefy.ai",
                timeout=timeout or 30.0,
                max_retries=max_retries or 3,
                fail_open=fail_open or False
            )
        
        # Validate API key
        if not self.config.api_key:
            raise UsefyAuthError(
                "API key is required. Pass api_key parameter or set USEFY_API_KEY environment variable."
            )
        
        if not self.config.api_key.startswith("us_live_"):
            logger.warning("API key does not start with 'us_live_'. Make sure you're using a valid Usefy API key.")
        
        # Initialize HTTP client
        self._http_client = httpx.Client(
            timeout=self.config.timeout,
            headers={
                "X-API-Key": self.config.api_key,
                "Content-Type": "application/json",
                "User-Agent": "usefy-python/0.1.0"
            }
        )
        
        # OpenAI-compatible interface
        self.chat = Chat(self)
        
        # Track fail-open state
        self._fail_open_active = False
    
    def _proxy_request(
        self,
        provider: str,
        body: Dict[str, Any],
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send request through Usefy proxy.
        
        Args:
            provider: AI provider name
            body: Request body
            stream: Enable streaming
            
        Returns:
            Provider response
        """
        # Build endpoint URL based on provider
        endpoint_map = {
            "openai": "/v1/proxy/openai/chat/completions",
            "anthropic": "/v1/proxy/anthropic/messages",
            "google": "/v1/proxy/google/generateContent",
            "mistral": "/v1/proxy/mistral/chat/completions",
            "cohere": "/v1/proxy/cohere/chat",
            "deepseek": "/v1/proxy/deepseek/chat/completions",
            "groq": "/v1/proxy/groq/chat/completions",
            "together": "/v1/proxy/together/chat/completions",
            "xai": "/v1/proxy/xai/chat/completions"
        }
        
        endpoint = endpoint_map.get(provider)
        if not endpoint:
            raise UsefyError(f"Unsupported provider: {provider}")
        
        url = f"{self.config.base_url}{endpoint}"
        
        # Try request with retries
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                # Use shorter timeout for fail-open check
                timeout = self.config.fail_open_timeout if self.config.fail_open else self.config.timeout
                
                response = self._http_client.post(
                    url,
                    json=body,
                    timeout=timeout
                )
                
                # Reset fail-open state on success
                self._fail_open_active = False
                
                # Handle errors
                if response.status_code == 401:
                    raise UsefyAuthError("Invalid API key", status_code=401)
                
                elif response.status_code == 429:
                    error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                    
                    if "budget" in str(error_data).lower():
                        raise UsefyBudgetExceeded(
                            error_data.get("detail", "Budget limit exceeded"),
                            budget_info=error_data.get("plan_info", {})
                        )
                    else:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        raise UsefyRateLimited(
                            error_data.get("detail", "Rate limit exceeded"),
                            retry_after=retry_after
                        )
                
                elif response.status_code >= 400:
                    try:
                        error_data = response.json()
                    except:
                        error_data = {"detail": response.text}
                    
                    raise UsefyProviderError(
                        error_data.get("detail", "Provider error"),
                        provider=provider,
                        status_code=response.status_code
                    )
                
                # Success
                return response.json()
            
            except httpx.TimeoutException as e:
                last_error = UsefyTimeoutError(f"Request timed out: {e}")
                
                # Fail-open: log and continue
                if self.config.fail_open:
                    logger.warning(f"Usefy timeout, fail-open mode active. Consider direct provider call.")
                    self._fail_open_active = True
                    # Note: In fail-open, caller should handle fallback to direct provider
                    raise last_error
                
            except httpx.ConnectError as e:
                last_error = UsefyError(f"Connection error: {e}")
                
                if self.config.fail_open:
                    logger.warning(f"Usefy connection error, fail-open mode active.")
                    self._fail_open_active = True
                    raise last_error
                
            except (UsefyAuthError, UsefyBudgetExceeded):
                # Don't retry auth or budget errors
                raise
                
            except UsefyRateLimited as e:
                # Wait before retry
                wait_time = min(e.retry_after or (self.config.retry_delay * (2 ** attempt)), 60)
                logger.info(f"Rate limited, waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                last_error = e
                
            except Exception as e:
                last_error = e
                
                # Exponential backoff
                if attempt < self.config.max_retries - 1:
                    wait_time = self.config.retry_delay * (2 ** attempt)
                    logger.debug(f"Request failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
        
        # All retries exhausted
        if last_error:
            raise last_error
        raise UsefyError("Request failed after all retries")
    
    def check(
        self,
        provider: str,
        model: str,
        estimated_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Pre-flight check: verify if request would be allowed.
        
        Args:
            provider: AI provider name
            model: Model name
            estimated_tokens: Estimated input tokens
            
        Returns:
            Dict with 'allowed', 'reason', 'remaining_budget'
        """
        url = f"{self.config.base_url}/v1/check"
        
        response = self._http_client.post(
            url,
            json={
                "provider": provider,
                "model": model,
                "estimated_input_tokens": estimated_tokens
            }
        )
        
        if response.status_code != 200:
            raise UsefyError(f"Check failed: {response.text}")
        
        return response.json()
    
    def get_usage(self) -> Dict[str, Any]:
        """
        Get current usage and limits.
        
        Returns:
            Dict with usage info (requests_used, requests_limit, etc.)
        """
        url = f"{self.config.base_url}/v1/usage/limits"
        
        response = self._http_client.get(url)
        
        if response.status_code != 200:
            raise UsefyError(f"Failed to get usage: {response.text}")
        
        return response.json()
    
    @property
    def is_fail_open_active(self) -> bool:
        """Check if fail-open mode is currently active due to Usefy issues."""
        return self._fail_open_active
    
    def close(self):
        """Close HTTP client."""
        self._http_client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
