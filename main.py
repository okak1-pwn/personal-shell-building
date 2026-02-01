import sys
import time
from Logic import handle_executables
from Commands import *
import shlex #Built to manage ' ' " " and \ for shell syntax

def initialize_console() -> None:
    sys.stdout.write("$ ")
    sys.stdout.flush()
    command = sys.stdin.readline().strip()
    check_command(command)

def check_command(command: str) -> None:
    parts = shlex.split(command)

    if not parts:
        return
    cmd, *args = parts

    if cmd in SYS_COMMANDS:
        func = SYS_COMMANDS[cmd]["func"]
        if SYS_COMMANDS[cmd]["args"]:
            func(args)
        else:
            func()
        return

    if handle_executables(cmd, args):
        return





def main():
    try:
        while True:
            initialize_console()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("exiting")


if __name__ == "__main__":
    main()
