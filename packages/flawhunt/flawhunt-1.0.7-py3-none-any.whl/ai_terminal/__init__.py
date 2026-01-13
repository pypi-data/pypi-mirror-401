"""
FlawHunt CLI - The smart CLI for cybersecurity professionals and ethical hackers.

A safe-by-default AI assistant that uses Groq (primary) + LangChain ReAct agent
to convert natural language into safe shell actions. Gemini is supported as an
optional provider.
"""

__version__ = "1.0.1"
__author__ = "FlawHunt CLI"
__description__ = "Natural language to shell with explanations & confirmations"

from .llm import LLM
from .agent import AgentHarness
from .persistence import load_state, save_state, VectorStore
from .conversation_history import ConversationHistoryManager
from .vector_store import ConversationVectorStore
from .utils import get_platform_info, run_subprocess
from .tools import *
from .safety import looks_dangerous, DANGEROUS_PATTERNS

__all__ = [
    "LLM",
    "ConversationHistoryManager",
    "ConversationVectorStore",
    "AgentHarness", 
    "load_state",
    "save_state", 
    "VectorStore",
    "get_platform_info",
    "run_subprocess",
    "looks_dangerous",
    "DANGEROUS_PATTERNS"
]
