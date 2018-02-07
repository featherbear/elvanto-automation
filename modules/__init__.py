modules = {}
def __init__():
    import importlib
    import pkgutil

    for _, fp, _ in pkgutil.walk_packages(path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + '.'):
        try:
            pyfile = fp[len(__name__) + 1:]
            if pyfile == "__stub__": continue
            module = importlib.import_module(fp)
            module = module.Module
            moduleName = module.__NAME__
            modules[moduleName] = {
                "version": module.__VERSION__,
                "class": module
            }
        except Exception as e:
            print("Error importing " + pyfile + " - " + str(e))
    return modules
__init__()
