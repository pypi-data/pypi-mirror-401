"""
Command handlers for roar CLI.

Each command is implemented as a class inheriting from BaseCommand,
following the Command pattern for consistent handling.
"""

from .auth import AuthCommand
from .base import BaseCommand
from .build import BuildCommand
from .clean import CleanCommand
from .config_cmd import ConfigCommand
from .dag import DagCommand
from .get import GetCommand
from .history import HistoryCommand
from .init import InitCommand
from .log import LogCommand
from .put import PutCommand
from .reproduce import ReproduceCommand
from .rm import RmCommand
from .run import RunCommand
from .show import ShowCommand
from .status import StatusCommand
from .sync import SyncCommand
from .verify import VerifyCommand

__all__ = [
    "AuthCommand",
    "BaseCommand",
    "BuildCommand",
    "CleanCommand",
    "ConfigCommand",
    "DagCommand",
    "GetCommand",
    "HistoryCommand",
    "InitCommand",
    "LogCommand",
    "PutCommand",
    "ReproduceCommand",
    "RmCommand",
    "RunCommand",
    "ShowCommand",
    "StatusCommand",
    "SyncCommand",
    "VerifyCommand",
]
