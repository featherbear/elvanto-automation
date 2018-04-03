from ElvantoAPIExtensions import Enums, Helpers
from modules.__stub__ import ModuleStub


class Module(ModuleStub):
    __VERSION__ = "1.0"
    __NAME__ = "elvantoToProPresenter_Kingsgrove"

    settings = {
        "general": {
            "api_key": "",
            "locationID": "",
            "folderName": ""
        },

    }

    def validate(self):
        # ensure that the API works
        pass

    def run(self):
        _serviceDate = Helpers.NextDate(Enums.Days.SUNDAY)
        import math
        weekNumber = math.ceil(_serviceDate.day / 7)
        try:
            services = self.conn.servicesOnDate(_serviceDate, locationID=self.settings["general"]["locationID"],
                                                fields=["plans"])

        except Exception as e:
            if e.__class__.__name__ == "ConnectionError":
                return False

        from propresenter import files as propresenter
        import os.path

        folderName = self.settings["general"]["folderName"]

        root = propresenter.playlist
        if folderName:
            if folderName not in root.children:
                root = root.add.folder(folderName)
            else:
                root = root.children[folderName]

        for service in services:
            if str(service) not in root.children:
                playlist = root.add.playlist(str(service))

                for item in service.plan:
                    type = item.__class__.__name__.lower()
                    if type == "header":
                        playlist.add.header(item.title)
                        if item.title == "Pre-service":

                            playlist.add.document(os.path.join(propresenter.documentPath, "Announcements" + ".pro6"))
                            # add countdown + auto cue

                        elif item.title == "Sermon":
                            playlist.add.document(os.path.join(propresenter.documentPath, "Sermon Passage Slide" + ".pro6"))
                    elif type == "song":
                        playlist.add.document(item.description if os.path.exists(item.description) else os.path.join(
                            propresenter.documentPath, item.title + ".pro6"))
                    else:
                        print(item.title)
                        if item.title == "Confession":
                            # weekNumber will only ever be 1, 2, 3, 4 or 5
                            print("Insert confession", weekNumber)
                            playlist.add.document(os.path.join(propresenter.documentPath, "Confession " + str(weekNumber) + ".pro6"))
                        # print("Skipping item with type:", type)
                # Add announcements roll
                playlist.add.document(os.path.join(propresenter.documentPath, "Announcements" + ".pro6"))
            else:
                print("Skipping", service,
                      "because it already exists in ProPresenter!\nTo create a new playlist for this service, please manually delete it in ProPresenter")
        propresenter.playlist.save()
