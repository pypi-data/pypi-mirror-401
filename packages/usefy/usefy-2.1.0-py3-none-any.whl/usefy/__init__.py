"""
Usefy Python SDK
================

Official Python SDK for Usefy - AI Cost Control & Budget Management.

Features:
- Drop-in replacement for OpenAI client
- Automatic cost tracking and budget enforcement
- Fail-open mode for maximum reliability
- Built-in retry with exponential backoff

Usage:
    from usefy import Usefy
    
    client = Usefy(api_key="us_live_xxx")
    
    # Use like OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
"""

from .client import Usefy, UsefyConfig
from .exceptions import UsefyError, UsefyAuthError, UsefyBudgetExceeded, UsefyRateLimited

__version__ = "2.1.0"
__all__ = [
    "Usefy",
    "UsefyConfig", 
    "UsefyError",
    "UsefyAuthError",
    "UsefyBudgetExceeded",
    "UsefyRateLimited"
]
