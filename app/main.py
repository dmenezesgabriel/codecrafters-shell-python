import sys


def main():
    while True:
        sys.stdout.write("$ ")
        prompt = input("")
        prompt_slices = str(prompt).split(" ")
        command = prompt_slices[0]
        args = prompt_slices[1:]

        if command == "exit":
            break
        if command == "echo":
            print(" ".join(args) + "\n")
        else:
            print(f"{command}: not found")


if __name__ == "__main__":
    main()
