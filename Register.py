SYS_COMMANDS = {}

def register(name: str, kind: str, arg: bool):
    def wrapper(func):
        SYS_COMMANDS[name] = {
            "func":func,
            "kind": kind,
            "args": arg
        }
        return func
    return wrapper