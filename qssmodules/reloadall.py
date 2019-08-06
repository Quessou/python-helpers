import types
from imp import reload

def print_status(module):
    print(f'reloading {module.__name__}')

def try_reload(module):
    try:
        reload(module)
    except Exception as e:
        print(f'FAILED {e.__repr__()} : {module}')

def transitive_reload(module, visited):
    if not module in visited:
        print_status(module)
        try_reload(module)
        visited[module] = True
        for attrobj in module.__dict__.values():
            if type(attrobj) == types.ModuleType:
                transitive_reload(attrobj, visited)

def reload_all(*args):
    visited = {}
    for arg in args:
        if type(arg) == types.ModuleType:
            transitive_reload(arg, visited)

if __name__ == '__main__':
    def tester(reloader, modname):
        import importlib, sys
        if len(sys.argv) > 1: 
            modname = sys.argv[1]
        module = importlib.import_module(modname)
        reloader(module)

    tester(reload_all, 'reloadall')
