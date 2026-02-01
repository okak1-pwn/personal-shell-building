import sys
import os
from Register import register, SYS_COMMANDS
from Logic import check_path

@register(name="echo",kind="builtin",arg=True)
def echo(args) -> None:
    print(*args)

@register(name="exit",kind="builtin",arg=True)
def cmd_exit(args) -> None:
    sys.exit(0)

@register(name="type", kind="builtin",arg=True)
def func_type(args) -> None:

    if not args:
        print(f"type: needs a argument")
        return

    cmd = args[0]

    if cmd in SYS_COMMANDS:
        info = SYS_COMMANDS[cmd]
        print(f"{cmd} is a shell {info['kind']}")
        return

    real, path = check_path(cmd)

    if real:
        print(f"{args[0]} is {path}")
        return

    print(f"{args[0]}: not found")

@register(name="pwd",kind="builtin",arg=False)
def pwd() -> None:
    print(os.getcwd())

@register(name="cd",kind="builtin",arg=True)
def cd(args: list) -> None:
    if len(args) > 1:
        print("cd: too many arguments")
        return

    directory = args[0] if args else "~"
    expanded_path = os.path.expanduser(directory)

    '''if not os.path.isdir(expanded_path):
        print(f"cd: not a directory: {args[0]}")
        return'''

    try:
        os.chdir(expanded_path)
    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {args[0]} not a directory")
    except PermissionError:
        print(f"cd: {args[0]} permission denied")