"""
AuthGuard Python SDK

A Python implementation of the AuthGuard v2 API client with NaCl box encryption.
"""

from .client import AuthGuardClient, Result, AuthGuardError

__version__ = "1.0.0"
__all__ = ["AuthGuardClient", "Result", "AuthGuardError"]
