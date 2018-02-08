from modules.__stub__ import ModuleStub
from ElvantoAPIExtensions import Enums, Helpers
import yagmail
import os

class Module(ModuleStub):
    __VERSION__ = "1.1"
    __NAME__ = "rosterEmail"

    settings = {
        "email": {
            "provider": "gmail",
            "username": "",
            "password": "",
            "ssl": ""
        },
        "general": {
            "serviceName": "",
            "template": ""
        },

        "responsibilities":
            {
                "adminEmail": "",
                "roster": "",
                "metrics": "",
                "offertory": "",
            }

    }
    def validate(self):
        _templateFile = os.path.join("files", self.__NAME__, self.settings["general"]["template"])
        if os.path.isdir(_templateFile) or not os.path.exists(_templateFile):
            raise self.ModuleException("Invalid template file path")
        self._templateFile = _templateFile

    def run(self):
        _serviceDate = Helpers.NextDate(Enums.Days.SUNDAY)
        services = Helpers.ParseServices(Helpers.ServicesOnDate(self.conn, _serviceDate, ["volunteers"]))
        service = next(filter(lambda _: _["name"] == self.settings["general"]["serviceName"], services))
        volunteerMap = {
            "serviceLeader": "",
            "speaker": "",
            "bibleReader": "",
            "visual": "",
            "audio": "",
            "welcoming": "",
            "music": "",

            "prayer": "",
            "cleaning": "",
        }

        for position in service["volunteers"]:

            if position["position_name"] == "Service leader": volunteerMap["serviceLeader"] = position["volunteers"].keys()
            elif position["position_name"] == "Speaker": volunteerMap["speaker"] = position["volunteers"].keys()
            elif position["position_name"] == "Bible reader": volunteerMap["bibleReader"] = position["volunteers"].keys()
            elif position["position_name"] == "ProPresenter": volunteerMap["visual"] = position["volunteers"].keys()
            elif position["position_name"] == "Sound Desk": volunteerMap["audio"] = position["volunteers"].keys()
            elif position["position_name"] == "Welcomers": volunteerMap["welcoming"] = position["volunteers"].keys()
            elif position["position_name"] == "Worship Leader": volunteerMap["music"] = position["volunteers"].keys()

        _volunteerMapResolve = {}
        for position in volunteerMap:
            _volunteerMapResolve[position] = list(map(lambda _: self.conn.findContact(id=_)[0], volunteerMap[position]))

        _volunteerMapName = {}
        _volunteerMapEmail = {}

        _volunteerMapNameJoin = {}
        _volunteerMapEmailJoin = []
        for position in _volunteerMapResolve:
            nameArray = ["%s %s" % (volunteer["first_name"], volunteer["last_name"]) for volunteer in _volunteerMapResolve[position]]
            _volunteerMapName[position] = nameArray
            _volunteerMapNameJoin[position] = ", ".join(nameArray)

            emailArray = [volunteer["email"] for volunteer in _volunteerMapResolve[position]]
            _volunteerMapEmail[position] = emailArray
            _volunteerMapEmailJoin.extend(emailArray)

        replacements = {
            "serviceLeader": _volunteerMapNameJoin["serviceLeader"],
            "speaker": _volunteerMapNameJoin["speaker"],
            "prayer": _volunteerMapNameJoin["prayer"],

            "bibleReader": _volunteerMapNameJoin["bibleReader"],
            "welcoming": _volunteerMapNameJoin["welcoming"],

            "music": _volunteerMapNameJoin["music"],
            "audio": _volunteerMapNameJoin["audio"],
            "visual": _volunteerMapNameJoin["visual"],

            "cleaning": _volunteerMapNameJoin["cleaning"],

            "Dmmyyyy": _serviceDate.strftime("%A, %#d %B %Y"),

            "metrics": self.settings["responsibilities"]["metrics"],
            "offertory": self.settings["responsibilities"]["offertory"],
            "roster": self.settings["responsibilities"]["roster"]
        }

        with open(self._templateFile, "r") as template:
            body = template.read()
        for key in replacements:
            body = body.replace("{" + key + "}",replacements[key])

        customSMTPServer = False if self.settings["email"]["provider"].lower() == "gmail" else self.settings["email"]["provider"].split(":")[-2:] + [465] # Add default SSL port if the user does not add
        smtpDetails = {
            "user": self.settings["email"]["username"],
            "password": self.settings["email"]["password"],
            "host": customSMTPServer[0] if customSMTPServer else "smtp.gmail.com",
            "port": int(customSMTPServer[1]) if customSMTPServer else 465,
            "smtp_ssl": (self.settings["email"]["ssl"].lower() == "true") if customSMTPServer else True,
        }

        self.mail = yagmail.SMTP(**smtpDetails)
        self.mail.send(to=_volunteerMapEmailJoin, cc=self.settings["responsibilities"]["adminEmail"], subject=self.settings["general"]["serviceName"] + " Worship Team | " + _serviceDate.strftime("%D"), contents=[yagmail.raw(body)])
