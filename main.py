import sys
import time
from Logic import execute, redirect_output_handling
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


    if any(op in parts for op in [">","1>","2>", ">>", "1>>", "2>>"]):
        redirect_output_handling(parts)
        return

    cmd, *args = parts
    stdout, stderr = execute(cmd, args)

    if stdout:
        print(stdout, end="")
    if stderr:
        sys.stderr.write(stderr)





def main():
    try:
        while True:
            initialize_console()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nexiting")


if __name__ == "__main__":
    main()
