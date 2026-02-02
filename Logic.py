import os
import subprocess
from pathlib import Path
from Register import SYS_COMMANDS


def execute(cmd: str, args: list[str]) -> tuple[str,str]:
    if cmd in SYS_COMMANDS:
        entry = SYS_COMMANDS[cmd]
        func = entry["func"]

        res = func(args) if entry["args"] else func()
        return res or "", ""

    try:
        result = subprocess.run([cmd, *args], capture_output=True, text=True)
        return result.stdout, result.stderr
    except FileNotFoundError:
        return "", f"{cmd}: command not found\n"


def redirect_output_handling(parts: list[str]) -> None:
    operations = {"output_write":{">","1>"},
                  "output_append":{">","1>>"},
                  "error_write":{"2>"},
                  "error_append":{"2>>"}}

    #Combines all the values in operations to a new set
    all_ops = set().union(*operations.values())

    #Enumerates input to find the first iteration of operations and otherwise gives the length
    first_idx = next((i for i, p in enumerate(parts) if p in all_ops), len(parts))

    # Gets the command and arguments then follows the format: operator -> filename -> operator -> ...
    cmd = parts[0]
    command_args = parts[1:first_idx]
    redirections = parts[first_idx:]

    if len(redirections) % 2 != 0:
        print(f"syntax error: expected filename after '{redirections[-1]}")
        return

    stdout, stderr = execute(cmd, command_args)

    last_stdout_file = None
    last_stderr_file = None

    for i in range(0, len(redirections), 2):
        op = redirections[i]
        filename = redirections[i + 1]


        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        if op in operations["output_write"]:
            last_stdout_file = (filename,"w")

            with open(filename, "w"): pass

        elif op in operations["output_append"]:
            last_stdout_file = (filename,"a")

            with open(filename, "a"): pass

        elif op in operations["error_write"]:
            last_stderr_file = (filename,"w")

            with open(filename, "w"): pass

        elif op in operations["error_append"]:
            last_stderr_file = (filename,"a")

            with open(filename, "a"): pass


    if last_stdout_file:
        file_name, mode = last_stdout_file

        with open(file_name, mode) as f:
            f.write(stdout)

    elif stdout:
        print(stdout, end="")

    if last_stderr_file:
        fn, mode = last_stderr_file

        with open(fn, mode) as f:
            f.write(stderr)

    elif stderr:
        print(stderr, end="")





def check_path(cmd:str):
    paths = get_path()

    for path in paths:
        full_path = path / cmd

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return True, full_path

    return False, None


def get_path() -> list[Path]:
    return [Path(p) for p in os.environ["PATH"].split(os.pathsep)]
