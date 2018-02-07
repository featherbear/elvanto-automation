from modules.__stub__ import ModuleStub
from ElvantoAPIExtensions import Enums, Helpers
import yagmail

class Module(ModuleStub):
    __VERSION__ = "1.0"
    __NAME__ = "rosterEmail"

    settings = {
        "email": {
            "provider": "gmail",
            "username": "",
            "password": ""
        },
        "general": {
            "serviceName": ""
        },

        "responsibilities":
            {
                "adminEmail": "",
                "roster": "",
                "metrics": "",
                "offertory": "",
            }

    }
    def run(self):
        print(self.settings)
        print(self.conn.people)
        services = Helpers.ParseServices(Helpers.ServicesOnDate(self.conn, Helpers.NextDate(Enums.Days.SUNDAY), ["volunteers"]))
        service = next(filter(lambda _: _["name"] == self.settings["general"]["serviceName"], services))
        volunteerMap = {}
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
            _volunteerMapResolve[position] = map(lambda _: self.conn.findContact(id=_)[0], volunteerMap[position])

        _volunteerMapName = {}
        _volunteerMapNameJoin = {}
        for position in _volunteerMapResolve:
            nameArray = ["%s %s" % (volunteer["first_name"], volunteer["last_name"]) for volunteer in _volunteerMapResolve[position]]
            _volunteerMapName[position] = nameArray
            _volunteerMapNameJoin[position] = ", ".join(nameArray)

        _volunteerMapEmail = {}
        _volunteerMapEmailJoin = []
        for position in _volunteerMapResolve:
            emailArray = [volunteer["email"] for volunteer in _volunteerMapResolve[position]]
            _volunteerMapEmail[position] = emailArray
            _volunteerMapEmailJoin.extend(emailArray)
        _volunteerMapEmailJoin = ",".join(_volunteerMapEmailJoin)


        bo = "<b>"
        bc = "</b>"
        nl = "<br>"

        body = ""
        body += "Morning Friends!" + nl + nl + "Below is the roster for this week's worship service. You should get an email later this week detailing the exact runsheet, if you have any further questions about what's happening, get in touch with this week's service leader, " + _volunteerMapNameJoin["serviceLeader"] + "." + nl + nl
        # body += bo + "Passage:" + bc + " " + volunteerMap.sermonPassage + " - " + volunteerMap.sermonPassageReader + nl + nl
        body += bo + "Speaker:" + bc + " " + _volunteerMapNameJoin["speaker"] + nl + nl
        body += bo + "Service Leader:" + bc + " " + _volunteerMapNameJoin["serviceLeader"] + nl + nl
        # body += bo + "Pastoral Prayer:" + bc + " " + volunteerMap.prayer + nl + nl
        body += bo + "Welcoming:" + bc + " " + _volunteerMapNameJoin["welcoming"] + nl + nl
        body += bo + "Music:" + bc + " " + _volunteerMapNameJoin["music"] + nl + nl
        body += bo + "Audio:" + bc + " " + _volunteerMapNameJoin["audio"] + nl + nl
        body += bo + "Visual:" + bc + " " + _volunteerMapNameJoin["visual"] + nl + nl
        # body += bo + "Church Cleaning:" + bc + " " + data.cleaning + nl + nl
        body += "<b>NOTE</b>: If you are not able to serve this week please find a replacement for yourself, or get in touch directly with your team leader. Thanks!<br><br><b>Counters</b><br>-  Please give <b>metrics data sheet</b> and all completed <b>newcomer cards</b> (back of bulletin) to <b>" + self.settings["responsibilities"]["metrics"] + "</b>.<br>- Please give offertory money for banking to <b>" + self.settings["responsibilities"]["offertory"] + "</b><br><br><br><br><i><b>This is an automated email - if there are issues please get in touch with " + self.settings["responsibilities"]["roster"] + ".</b></i>"

        print(body)

        smtpDetails = {
            "user": self.settings["email"]["username"],
            "password": self.settings["email"]["password"],
            "host": "smtp.gmail.com",
            "port": 465,
            "smtp_ssl": True,
        }
        # self.mail = yagmail.SMTP(**smtpDetails)
        # self.mail.send(to=_volunteerMapEmailJoin, cc=self.settings["responsibilities"]["adminEmail"], subject='emailPrefix + "Worship Team " + data.dateDMMYYYY', contents=body)
