import sys
import shlex
import os
import subprocess

from typing import Optional

COMMANDS = ["cd", "pwd", "exit", "echo", "type"]
PATH = os.environ.get("PATH")

def locate_executable(file) -> Optional[str]:
    for dir in PATH.split(":"):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

def handle_exit(args):
    sys.exit(int(args[0]) if args else 0)

def handle_echo(args):
    print(" ".join(args))
        
def handle_type(args):
    if args[0] in builtins:
        print(f"{args[0]} is a shell builtin")
    elif path := locate_executable(args[0]):
        print(f"{args[0]} is {path}")
    else:
        print(f"{args[0]}: not found")
        
def handle_pwd(args):
    print(os.getcwd())
    
def handle_cd(args):
    if args:
        try:
            os.chdir(args[0] if args[0] != "~" else os.environ.get("HOME", ""))
        except FileNotFoundError:
            print(f"cd: {args[0]}: No such file or directory")
    
def find_file(file):
    dirs = PATH.split(":")
    for dir in dirs:
        path = f"{dir}/{file}"
        if os.path.isfile(path):
            return path
    return ""

def parse_input(input):
    return shlex.split(input)

builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "cd": handle_cd,
    "pwd": handle_pwd,
}

def main():
    while True:
        sys.stdout.write("$ ")
        
        sys.stdout.flush()
        
        # Wait for user input
        std_input = input()
        
        # parse input
        args = parse_input(std_input)
        command = args[0]
        
        if command in builtins:
            builtins[command](args[1:])
            continue
        elif path := locate_executable(command):
            subprocess.run([path, *args[1:]])
        else:
            print(f"{command}: command not found")
        
        sys.stdout.flush()

if __name__ == "__main__":
    main()
