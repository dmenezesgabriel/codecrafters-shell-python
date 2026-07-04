"""
Terminology

REPL: Read-Eval-Print Loop

"""

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional, TypeAlias, get_args

CommandType: TypeAlias = Literal["exit", "echo", "type"]


class CommandNotFoundException(Exception): ...


@dataclass
class ParsedCommand:
    type: CommandType
    args: Optional[list[str]]


class Command(ABC):
    def __init__(self, args: list[str]):
        self.args = args

    @abstractmethod
    def execute(self) -> None: ...


class CommandLineParser:
    @staticmethod
    def parse_command_line(command_line: str) -> Command:
        tokens = command_line.split()

        return ParsedCommand(type=tokens[0], args=tokens[1:])


class ExitCommand(Command):
    def __init__(self, args) -> None:
        self.args = args

    def execute(self):
        exit()


class EchoCommand(Command):
    def __init__(self, args) -> None:
        self.args = args

    def execute(self):
        print(" ".join(self.args))


class TypeCommand(Command):
    def __init__(self, args) -> None:
        self.args = args

    def execute(self):
        if self.args[0] in set(get_args(CommandType)):
            print(f"{self.args[0]} is a shell builtin")
        else:
            raise CommandNotFoundException(f"{self.args[0]}: not found")


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
            print(str(error))


if __name__ == "__main__":
    main()
