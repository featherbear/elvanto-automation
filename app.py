import time

from ElvantoAPIExtensions import ElvantoAPI
import schedule


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
        _config.set("config", "api_key", "")
        with open(_configFilePath, "w") as _configFile:
            _config.write(_configFile)
        print("Created '%s'. Please enter in your API key to continue. Exiting" % _configFilePath)
        sys.exit()
    elif not os.path.isfile(_configFilePath):
        raise Exception(_configFilePath + " is not a file! Aborting")
    _config.read(_configFilePath)
    api_key = _config.get("config", "api_key")


import modules

ModuleException = modules.__stub__.ModuleStub.ModuleException
modules = modules.modules
def strIsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    print("""= SWEC Elvanto Automation =\n""")
    print("Connecting to Elvanto")
    api = ElvantoAPI.Connection(APIKey = settings.api_key)

    print("Fetching contacts...")
    import requests.exceptions

    try:
        api.getPeople()
    except requests.exceptions.ConnectionError:
        print("  Could not connect to Elvanto to fetch contact details!\n")

    # Create module objects
    try:
        for module in modules:
            print("Loading module `%s` (v%s)" % (module, modules[module]['version']))
            modules[module]["instance"] = modules[module]['class'](api)
    except ModuleException as e:
        print(e)

    print()

    weekdays = (
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
    )

    # Schedule the modules
    for module in modules:
        if "instance" in modules[module]:
            result = False
            print("Scheduling module `%s`" % module)
            __day = modules[module]["instance"].__executeDay__
            __time = modules[module]["instance"].__executeTime__
            if __time:
                timeH, timeM = __time.split(":")
                assert 0 <= int(timeH) <= 23 and 0 <= int(timeM) <= 59
            runner = modules[module]["instance"].run
            if __day is None:
                if __time is None:
                    print(" Running `%s` as it is a once-only module" % module)
                    if runner() == False:
                        print(" Module did not finish because of an error!")
                    continue
                else:
                    schedule.every().day.at(__time).do(runner)
                    result = True
            else:
                if __time is None:
                    schedule.every().day.do(runner)
                    result = True
                else:
                    sch = schedule.every()
                    if strIsInt(__day) and 0 <= int(__day) <= 6:
                        __day = weekdays[int(__day)]
                    sch.start_day = __day
                    sch.unit = "weeks"
                    sch.at(__time).do(runner)
                    result = True
            print("  Schedule %s" % "success" if result else "failed")

    while True:
        schedule.run_pending()
        time.sleep(1)
        # __executeTime__ = "tuesday"
        # __executeDay__ = "14:50"
        #

    # # Start the modules
    # for module in modules:
    #     if "instance" in modules[module]:
    #         print("Starting module `%s`" % module)
    #         if modules[module]["instance"].run() == False:
    #             print("  Module did not start because of an error!")
