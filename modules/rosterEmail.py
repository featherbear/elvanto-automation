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
        print(Helpers.ParseServices(Helpers.ServicesOnDate(self.conn, Helpers.NextDate(Enums.Days.SUNDAY), ["volunteers"])))

        #self.conn._Post()
        smtpDetails = {
            "user": self.settings["email"]["username"],
            "password": self.settings["email"]["password"],
            "host": "smtp.gmail.com",
            "port": 465,
            "smtp_ssl": True,
        }



        """
        songs | only useful if songs are attached
        can extract songs from plans item
        """
        #
        # if services["status"] == "fail":
        #     raise Exception("Could not retrieve any details for the upcoming Sunday service")
        # services = services["services"]["service"]
        #
        # for service in services:
        #     print("ID", service["id"])
        #     print("Name", service["name"])
        #     print("Date", service["date"])
        #     print("Type", service["service_type"]["id"], service["service_type"]["name"])
        #     print("Location", service["location"]["id"], service["location"]["name"])
        #
        #     print("Songs", service["songs"])
        #
        #     roles = service["volunteers"]["plan"][0]["positions"]["position"]
        #     for role in roles:
        #         if role["volunteers"]:
        #             print(role["volunteers"]["volunteer"])
        #         """
        #         department_name
        #         sub_department_name
        #         position_name
        #         volunteers["volunteer"] {
        #           "person" | (firstname || preferred_name), lastname
        #           "status" | str
        #         }
        #         """
        #
        #     plan = service["plans"]["plan"][0]
        #     planItems = plan["items"]["item"]
        #     for item in planItems:
        #         """
        #         id
        #         heading
        #         duration
        #         title
        #         song
        #         description
        #         """
        #         # Item is a header if (item["heading"] == 1)
        #         pass

        import sys
        sys.exit()
        self.mail = yagmail.SMTP(**smtpDetails)
        # self.mail.send(to="",cc="",subject="",contents="")

        bo = "<b>"
        bc = "</b>"
        nl = "<br>"

        data = {} # TODO POPULATE

        body = ""
        body += "Morning Friends!" + nl + nl + "Below is the roster for this week's worship service. You should get an email later this week detailing the exact runsheet, if you have any further questions about what's happening, get in touch with this week's service leader, " + data.serviceLeader + "." + nl + nl
        body += bo + "Passage:" + bc + " " + data.sermonPassage + " - " + data.sermonPassageReader + nl + nl
        body += bo + "Speaker:" + bc + " " + data.speaker + nl + nl
        body += bo + "Service Leader:" + bc + " " + data.serviceLeader + nl + nl
        body += bo + "Pastoral Prayer:" + bc + " " + data.prayer + nl + nl
        body += bo + "Welcoming:" + bc + " " + data.welcoming + nl + nl
        body += bo + "Music:" + bc + " " + data.music + nl + nl
        body += bo + "Audio:" + bc + " " + data.sound + nl + nl
        body += bo + "Visual:" + bc + " " + data.visual + nl + nl
        body += bo + "Church Cleaning:" + bc + " " + data.cleaning + nl + nl
        body += "<b>NOTE</b>: If you are not able to serve this week please find a replacement for yourself, or get in touch directly with your team leader. Thanks!<br><br><b>Counters</b><br>-  Please give <b>metrics data sheet</b> and all completed <b>newcomer cards</b> (back of bulletin) to <b>" + metrics + "</b>.<br>- Please give offertory money for banking to <b>" + offertory + "</b><br><br><br><br><i><b>This is an automated email - if there are issues please get in touch with " + roster + ".</b></i>"
