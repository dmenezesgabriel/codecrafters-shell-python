import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input("")

        if command == "exit":
            break
        if command.startswith("echo"):
            print(command[5:])
        if command.startswith("type"):
            if command[5:] in ["exit", "echo", "type"]:
                print(f"{command[5:]} is a shell builtin")
        else:
            print(f"{command}: not found")


if __name__ == "__main__":
    main()
