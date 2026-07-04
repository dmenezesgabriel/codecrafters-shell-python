"""
Terminology

REPL: Read-Eval-Print Loop

"""

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional, TypeAlias, get_args

CommandType: TypeAlias = Literal["exit", "echo", "type"]


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


COMMANDS: dict[CommandType, type[Command]] = {
    "exit": ExitCommand,
    "echo": EchoCommand,
    "type": TypeCommand,
}


def command_factory(parsed_command: ParsedCommand) -> Command:
    cls = COMMANDS.get(parsed_command.type)
    if cls is None:
        raise ValueError(f"{parsed_command.type}: not found")
    return cls(parsed_command.args)


def main():
    while True:
        sys.stdout.write("$ ")

        command_line = input("")

        parsed_command = CommandLineParser.parse_command_line(command_line=command_line)

        try:
            command = command_factory(parsed_command=parsed_command)
        except Exception as error:
            print(str(error))

        command.execute()


if __name__ == "__main__":
    main()
