"""
Terminology

REPL: Read-Eval-sys.stdout.write Loop

"""

import os
import shlex
import subprocess
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


class ExecutableFinder:
    @staticmethod
    def find(command_name: str) -> str | None:
        paths = os.getenv("PATH").split(os.pathsep)
        for directory in paths:
            candidate = os.path.join(directory, command_name)

            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
        return None


class ExitCommand(Command):
    def execute(self) -> None:
        exit()


class EchoCommand(Command):
    def execute(self) -> None:
        sys.stdout.write(f"{' '.join(self.args)}\n")


class TypeCommand(Command):
    def execute(self) -> None:
        command_name = self.args[0]
        if CommandRegistry.is_builtin(command_name):
            sys.stdout.write(f"{command_name} is a shell builtin\n")
            return None

        executable = ExecutableFinder.find(command_name)
        if executable:
            sys.stdout.write(f"{command_name} is {executable}\n")
            return

        raise CommandNotFoundException(f"{command_name}: not found")


class ExternalCommand(Command):
    def __init__(self, executable: str, args: list[str]):
        super().__init__(args)
        self.executable = executable

    def execute(self):
        subprocess.run([self.executable, *self.args])


class CommandRegistry:
    COMMANDS: dict[CommandType, type[Command]] = {
        "exit": ExitCommand,
        "echo": EchoCommand,
        "type": TypeCommand,
    }

    @classmethod
    def create_command(cls, parsed_command: ParsedCommand) -> Command:
        if CommandRegistry.is_builtin(parsed_command.type):
            command_cls = cls.COMMANDS.get(parsed_command.type)
            return command_cls(parsed_command.args)
        executable = ExecutableFinder.find(parsed_command.type)
        if executable is not None:
            return ExternalCommand(executable=executable, args=parsed_command.args)
        if command_cls is None:
            raise CommandNotFoundException(f"{parsed_command.type}: not found")

    @classmethod
    def is_builtin(command_name: str) -> bool:
        return command_name in set(get_args(CommandType))


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
