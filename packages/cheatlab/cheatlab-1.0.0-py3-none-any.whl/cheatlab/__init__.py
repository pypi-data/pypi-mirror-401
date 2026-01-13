"""
CheatLab Python Client
~~~~~~~~~~~~~~~~~~~~~

A Python client for the CheatLab API - Quick command reference storage and retrieval.

Basic usage:
    >>> from cheatlab import Cheat
    >>> cheat = Cheat("username", "auth_key")
    >>> cheat.post("Hello World", key="greeting")
    >>> cheat.get("greeting")
    'Hello World'
"""

from .client import Cheat, CheatLabError, AuthenticationError, APIError

__version__ = "1.0.0"
__all__ = ["Cheat", "CheatLabError", "AuthenticationError", "APIError"]
