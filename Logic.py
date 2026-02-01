import os

def handle_executables(cmd: str, args: list[str]) -> bool:
    pid = os.fork()
    if pid == 0:
        try:
             os.execvp(cmd, [cmd, *args])
        except FileNotFoundError:
            print(f"{cmd}: command not found")
            os._exit(127)
        except PermissionError:
            print(f"{cmd}: permission denied")
            os._exit(126)
        except Exception:
            print(f"{cmd}: execution failed unknown error")
            os._exit(1)
    else:
        os.waitpid(pid,0)
        return True


def check_path(cmd):
    os_paths = get_path(cmd)
    for path in os_paths:
        full_path = os.path.join(path, cmd)
        if os.path.isfile(full_path):
            if os.access(full_path, os.X_OK):
                return True, full_path
    return False, None


def get_path(args) -> list:
    return os.environ['PATH'].split(os.pathsep)

