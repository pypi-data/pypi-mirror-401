"""
waygrounddocgen - Documentation generator using Cursor AI

A language-agnostic CLI tool that leverages Cursor AI to automatically discover
modules in any codebase and generate comprehensive documentation.
"""

__version__ = "0.1.0"
__author__ = "Gaurav Madan"

from .cli import main

__all__ = ["main", "__version__"]

