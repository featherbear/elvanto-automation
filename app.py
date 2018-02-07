from ElvantoAPIExtensions import ElvantoAPI

class settings:
    import configparser
    import os
    import sys

    _configFilePath = os.path.join("settings", "app.ini")
    _config = configparser.ConfigParser()
    _config.optionxform = str
    if not os.path.exists(_configFilePath):
        os.makedirs(os.path.dirname(_configFilePath), exist_ok = True)
        _config.add_section("config")
        _config.set("config","api_key", "")
        with open(_configFilePath, "w") as _configFile:
            _config.write(_configFile)
        print("Created '%s'. Please enter in your API key to continue. Exiting" % _configFilePath)
        sys.exit()
    elif not os.path.isfile(_configFilePath):
        raise Exception(_configFilePath + " is not a file! Aborting")
    _config.read(_configFilePath)
    api_key = _config.get("config","api_key")

api = ElvantoAPI.Connection(APIKey = settings.api_key)
print("Fetching contacts")
api.getPeople()

import datetime
date_today = datetime.date.today()
date_service = date_today + datetime.timedelta((6 - date_today.weekday()) % 7)

import modules
ModuleException = modules.__stub__.ModuleException
modules = modules.modules

try:
    for module in modules:
        print("Starting module `%s` (v%s)" % (module, modules[module]['version']))
        modules[module]["instance"] = modules[module]['class'](api)
except ModuleException as e:
    print(e)

for module in modules:
    if "instance" in modules[module]:
        instance = modules[module]["instance"]
        print(instance.run())
