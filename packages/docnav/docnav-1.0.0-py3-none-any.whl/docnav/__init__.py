"""
DocNav: Local-first document navigation with AI-powered queries and citations.
"""

from .core import DocCorpus, Answer, QueryResult, ask
from .cli import main as cli_main

__version__ = "1.0.0"
__all__ = ["DocCorpus", "Answer", "QueryResult", "cli_main", "ask"]
