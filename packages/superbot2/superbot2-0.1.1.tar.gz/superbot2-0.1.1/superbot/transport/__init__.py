"""
Unified transport interface for local and remote policy servers/clients
Automatically switches between local and remote modes based on parameters
"""

from .client import PolicyClient
from .server import PolicyServer

__all__ = ['PolicyClient', 'PolicyServer']