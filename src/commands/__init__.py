import typing

from .Command import Command
from .Command import registered_commands

# List all commands that are available to use
from src.commands.check.CheckCommand import CheckCommand
from src.commands.unify.UnifyCommand import UnifyCommand
from src.commands.dedup.DedupCommand import DedupCommand

commands: typing.List[typing.Type[Command]] = [CheckCommand, UnifyCommand, DedupCommand]

__all__ = [Command, registered_commands] + commands
