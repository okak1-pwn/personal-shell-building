import sys
import os
from pathlib import Path
from Register import register, SYS_COMMANDS
from Logic import check_path

@register(name="echo",kind="builtin",arg=True)
def echo(args) -> str:
    return ' '.join(args)+"\n"


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
def pwd() -> str:
    return str(Path.cwd())+"\n"



@register(name="cd",kind="builtin",arg=True)
def cd(args: list[str]) -> str:
    if len(args) > 1:
        return "cd: too many arguments\n"


    directory = args[0] if args else "~"
    expanded_path = Path(directory).expanduser().resolve()


    try:
        os.chdir(expanded_path)
    except FileNotFoundError:
        return f"cd: {args[0]}: No such file or directory\n"
    except NotADirectoryError:
        return f"cd: {args[0]} not a directory\n"
    except PermissionError:
        return f"cd: {args[0]} permission denied\n"

    return ""
