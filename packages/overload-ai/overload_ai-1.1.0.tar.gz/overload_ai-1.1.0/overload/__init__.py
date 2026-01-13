"""
Overload - AI-powered Python bug identification client
"""

from .client import analyze_code
from .exceptions import OverloadError

__version__ = "1.1.0"

# Only these names are public
__all__ = ["analyze_code", "OverloadError"]
