from mailmerge import MailMerge
import re
import os.path
from ElvantoAPIExtensions import Enums, Helpers
from modules.__stub__ import ModuleStub


class Module(ModuleStub):
    __VERSION__ = "1.0"
    __NAME__ = "bulletinGenerator_Kingsgrove"

    settings = {
        "general": {
            "template": "",
            "serviceName": "",

            "pastorName": "",
            "pastorTelephone": "",
            "pastorEmail": "",
        },
    }

    def validate(self):
        self._baseFolder = os.path.join("files", self.__NAME__)
        _templateFile = os.path.join(self._baseFolder, self.settings["general"]["template"])
        if not os.path.isfile(_templateFile):
            raise self.ModuleException("Invalid template file path")
        self._templateFile = _templateFile

    def run(self):
        _serviceDate = Helpers.NextDate(Enums.Days.SUNDAY)
        import math
        weekNumber = int(math.ceil(_serviceDate.day / 7))

        try:
            thisWeekServices = Helpers.ServicesOnDate(self.conn, _serviceDate, ["volunteers", "plans"])
            thisWeekService = next(
                filter(lambda _: _.name == self.settings["general"]["serviceName"], thisWeekServices))

        except Exception as e:
            if e.__class__.__name__ == "ConnectionError":
                print("Couldn't connect to Elvanto API")
                return False
            if type(e) == StopIteration:
                print("Couldn't find an upcoming service called \"%s\"" % self.settings["general"]["serviceName"])
                return False
            print("An error occured:", e)

        def getWeeklyConfession(week: int):
            assert 1 <= week <= 5
            confessionOne = """
        Almighty and most merciful Father,
        You have loved us with an everlasting love,
        But we have gone our own way
        And have rejected you in thought, word, and deed.
        We are sorry for our sins
        And turn away from them
        For the sake of your Son who died for us,
        Forgive us, cleanse us and change us.
        By your Holy Spirit, enable us to live for you,
        And to please you more and more;
        Through Jesus Christ our Lord.
        Amen.
        """
            confessionTwo = """
        Most merciful God,
        we humbly admit that we need your help.
        We confess that we have wandered from your way:
        We have done wrong, and we have failed to do what is right.
        You alone can save us.
        Have mercy on us:
        Wipe out our sins and teach us to forgive others.
        Bring forth in us the fruit of the Spirit
        That we may live as disciples of Christ.
        This we ask in the name of Jesus our Saviour.
        Amen.
        """
            confessionThree = """
        Heavenly Father,
        We praise you for adopting us as your children
        And making us heirs of eternal life.
        In your mercy you have washed us from our sins
        And made us clean in your sight.
        Yet we still fail to love you as we should and serve you as we ought.
        Forgive us our sins and renew us by your grace,
        That we may continue to grow as members of Christ,
        In whom alone is our salvation.
        Amen.
        """
            confessionFour = """
        Merciful God, our maker and our judge, we have sinned against you in thought, word, and deed:
        we have not loved you with our whole heart, we have not loved our neighbours as ourselves:
        we repent, and are sorry for all our sins.
        Father, forgive us.
        Strengthen us to love and obey you in newness of life;
        through Jesus Christ our Lord.
        Amen
        """
            confessionFive = """
        Lord God,
        we have sinned against you;
        we have done evil in your sight.
        We are sorry and repent.
        Have mercy on us according to your love.
        Wash away our wrongdoing and cleanse us from our sin.
        Renew a right spirit within us
        and restore us to the joy of your salvation,
        through Jesus Christ our Lord. Amen. 
        """
            return [None, confessionOne, confessionTwo, confessionThree, confessionFour, confessionFive][
                week].strip()

        stringify = lambda volunteerArray: ", ".join(map(repr, volunteerArray))

        replacements = {
            "prettyDate": _serviceDate.strftime("%A, %#d %B %Y"),
            "branch": self.settings["general"]["serviceName"],
            "weeklyConfession": getWeeklyConfession(weekNumber),

            "pastorName": self.settings["general"]["pastorName"],
            "pastorTelephone": self.settings["general"]["pastorTelephone"],
            "pastorEmail": self.settings["general"]["pastorEmail"],

            "scripturePassage": None,
            "sermonPassage": None,
            "speaker": None,
        }

        scripturePassageItem = next(filter(lambda _: _.title == "Bible Reading", thisWeekService.plan))
        replacements["scripturePassage"] = re.sub('<.*?>', "", scripturePassageItem.description).strip()

        sermonPassageItem = next(filter(lambda _: _.title == "Bible Reading (Sermon)", thisWeekService.plan))
        replacements["sermonPassage"] = re.sub('<.*?>', "", sermonPassageItem.description).strip()

        replacements["speaker"] = stringify(thisWeekService.volunteers.byPositionName("Speaker"))

        with MailMerge(self._templateFile) as document:
            document.merge(**replacements)
            filePath = os.path.join(self._baseFolder, "SWEC %s - Bulletin %s.docx"
                                    % (self.settings["general"]["serviceName"], _serviceDate.strftime("%#d %B %Y")))
            document.write(filePath)
