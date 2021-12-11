import typing

from .Command import Command
from .CheckCommand import CheckCommand
from .UnifyCommand import UnifyCommand
from .DedupCommand import DedupCommand
from .main import main

# List all commands that are available to use
commands: typing.List[typing.Type[Command]] = [CheckCommand, UnifyCommand, DedupCommand]

__all__ = ["main"] + [c.__name__ for c in commands]
