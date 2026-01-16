"""
Output presenters for roar CLI.

Implements different output formats (console, JSON, etc.)
following the Strategy pattern.
"""

from .console import ConsolePresenter

__all__ = ["ConsolePresenter"]
