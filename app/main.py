import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input("")
        print(f"{command}: not found")


if __name__ == "__main__":
    main()
