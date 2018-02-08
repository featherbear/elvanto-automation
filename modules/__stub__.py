from ElvantoAPIExtensions import ElvantoAPI

class ModuleStub():
    class ModuleException(Exception):
        pass

    __VERSION__ = ""
    __NAME__ = ""

    settings = {
    }
    def __init__(self, connectionObj: ElvantoAPI.Connection):
        import configparser
        import os
        _configFilePath = os.path.join("settings", self.__NAME__ + ".ini")
        _config = configparser.ConfigParser()
        _config.optionxform = str
        if not os.path.exists(_configFilePath):
            for section in self.settings:
                _config.add_section(section)
                for key in self.settings[section]:
                    _config.set(section, key, self.settings[section][key])
            with open(_configFilePath, "w") as _configFile:
                _config.write(_configFile)
            raise self.ModuleException("Created '%s'. Please enter in your API key to continue. Exiting" % _configFilePath)
        elif not os.path.isfile(_configFilePath):
            raise self.ModuleException(_configFilePath + " is not a file! Aborting")
        _config.read(_configFilePath)

        for section in self.settings:
            for key in self.settings[section]:
                val = _config.get(section, key, fallback = None)
                self.settings[section][key] = val

        self.validate()
        self.conn = connectionObj

    def validate(self):
        # stub
        return
        raise self.ModuleException("Error")


    def run(self):
        pass
