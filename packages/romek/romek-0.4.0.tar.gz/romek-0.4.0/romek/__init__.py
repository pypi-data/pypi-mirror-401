import warnings
warnings.filterwarnings("ignore")

import os
os.environ["PYTHONWARNINGS"] = "ignore"

"""Romek - Identity and session management for AI Agents."""

from .identity import Agent
from .client import RomekClient
from .vault import Vault

__version__ = "0.1.0"

__all__ = ["Agent", "RomekClient", "Vault"]

# Optional LangChain integration
try:
    from .langchain import get_romek_tools, AuthenticatedRequestTool, GetSessionTool
    __all__.extend(["get_romek_tools", "AuthenticatedRequestTool", "GetSessionTool"])
except ImportError:
    # LangChain not installed
    pass
