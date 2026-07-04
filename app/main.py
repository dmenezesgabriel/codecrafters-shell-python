"""
Terminology

REPL: Read-Eval-sys.stdout.write Loop

"""

import os
import shlex
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional, TypeAlias, get_args

CommandType: TypeAlias = Literal["exit", "echo", "type"]


class CommandNotFoundException(Exception): ...


@dataclass
class ParsedCommand:
    type: Optional[CommandType]
    args: Optional[list[str]]


class Command(ABC):
    def __init__(self, args: list[str]):
        self.args = args

    @abstractmethod
    def execute(self) -> None: ...


class CommandLineParser:
    @staticmethod
    def parse_command_line(command_line: str) -> Command:
        tokens = shlex.split(command_line)

        if not tokens:
            return ParsedCommand(type=None, args=[])

        return ParsedCommand(type=tokens[0], args=tokens[1:])


class ExitCommand(Command):
    def execute(self) -> None:
        exit()


class EchoCommand(Command):
    def execute(self) -> None:
        sys.stdout.write(f"{' '.join(self.args)}\n")


class TypeCommand(Command):
    def execute(self) -> None:
        command_name = self.args[0]
        if command_name in set(get_args(CommandType)):
            sys.stdout.write(f"{command_name} is a shell builtin\n")
            return None

        paths = os.getenv("PATH").split(os.pathsep)
        for directory in paths:
            candidate = os.path.join(directory, command_name)

            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                sys.stdout.write(f"{command_name} is {candidate}\n")
                return None

        raise CommandNotFoundException(f"{command_name}: not found")


class CommandRegistry:
    COMMANDS: dict[CommandType, type[Command]] = {
        "exit": ExitCommand,
        "echo": EchoCommand,
        "type": TypeCommand,
    }

    @classmethod
    def create_command(cls, parsed_command: ParsedCommand) -> Command:
        command_cls = cls.COMMANDS.get(parsed_command.type)
        if command_cls is None:
            raise CommandNotFoundException(f"{parsed_command.type}: not found")
        return command_cls(parsed_command.args)


def main():
    while True:
        sys.stdout.write("$ ")

        command_line = input("")

        parsed_command = CommandLineParser.parse_command_line(command_line=command_line)

        try:
            command = CommandRegistry.create_command(parsed_command=parsed_command)
            command.execute()
        except CommandNotFoundException as error:
            sys.stdout.write(str(error) + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\nGood Bye!\n")
