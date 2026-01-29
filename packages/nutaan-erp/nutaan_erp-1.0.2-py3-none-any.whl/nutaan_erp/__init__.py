"""Nutaan ERP AI Agent SDK - Public API

Autonomous AI agent for ERPNext/Frappe automation.
Powered by Google Gemini and LangChain.
"""

__version__ = "1.0.2"
__author__ = "Nutaan AI (Tecosys)"
__license__ = "MIT"

from .core.agent import AgentManager
from .core.config import AgentConfig
from .core.tracker import ActionTracker, SessionData

__all__ = [
    "AgentManager",
    "AgentConfig",
    "ActionTracker",
    "SessionData",
    "__version__",
    "__author__",
    "__license__"
]
