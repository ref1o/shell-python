import sys
import shlex
import os
import subprocess

COMMANDS = ["cd", "pwd", "exit", "echo", "type"]
PATH = os.environ.get("PATH")

def handle_exit(args):
    if len(args) > 2:
        print("invalid arguments")
    elif len(args) == 1:
        sys.exit(0)
    else:
        try:
            sys.exit(int(args[1]))
        except ValueError:
            print("invalid exit code")

def handle_echo(args):
    if len(args) == 1:
        print()
    else:
        print(" ".join(args[1:]))
        
def handle_type(args):
    cmd = args[1]
    dirs = PATH.split(":")
    print_string = f"{cmd}: not found"
    
    for dir in dirs:
        path = f"{dir}/{cmd}"
        if os.path.isfile(path):
            print_string = f"{cmd} is {path}"
            
    if cmd in COMMANDS:
        print_string = f"{cmd} is a shell builtin"
    print(print_string)
    
def find_file(file):
    dirs = PATH.split(":")
    for dir in dirs:
        path = f"{dir}/{file}"
        if os.path.isfile(path):
            return path
    return ""

def parse_input(input):
    return shlex.split(input)

def main():
    while True:
        sys.stdout.write("$ ")
        
        sys.stdout.flush()
        
        # Wait for user input
        std_input = input()
        
        # parse input
        args = parse_input(std_input)
        command = args[0]
        path = find_file(command)
        
        if len(args) == 0:
            continue
        
        if command == "exit":
            handle_exit(args)
            
        elif command == "echo":
            handle_echo(args)
            
        elif command == "type":
            handle_type(args)
            
        elif path != "":
            result = subprocess.run(args, capture_output=True, text=True)
            print(result.stdout, end="")
            
        elif command not in COMMANDS:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
