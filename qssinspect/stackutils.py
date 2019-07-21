import inspect

def fnname() -> str:
    stack = inspect.stack()
    if len(stack) < 2:
        return
    return stack[1][3]
