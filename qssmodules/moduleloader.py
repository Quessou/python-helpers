import importlib

def try_load(module_name):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError : # TODO: specialize for potential other exceptions that can be encountered here ?
        print(f'Module {module_name} not found')
        return False
    return True


pip_module_present = True
pip_module_present = try_load('pip_api')

if pip_module_present: # Here the assumption is made that modules have the same name when you install them than when you import them. Is that assumption wonky ?
    def try_install(module_name):
        # We may want to consider what is said here : https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
        print(f'trying installing {module_name}')
else:
    print("Please install pip_api module with following command line :\n\tpip install pip-api")
    sys.exit()
