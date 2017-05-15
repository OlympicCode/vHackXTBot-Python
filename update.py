from classes import API
from utils import Utils


class Update:
    def getTasks(self):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed",
                                "vh_tasks.php")
        return temp

    def SpywareInfo(self):
        ut = Utils()
        arr = ut.requestArray("user::::pass::::uhash:::::",
                              self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "UserHash_not_needed" + ":::::",
                              "vh_spywareInfo.php")
        return arr

    def removeSpyware(self):
        ut = Utils()
        arr = ut.requestArray("user::::pass::::uhash:::::",
                              self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "UserHash_not_needed" + ":::::",
                              "vh_removeSpyware.php")
        return arr

    def getTaskAmount(self):
        ut = Utils()
        temp = self.getTasks()
        return len(temp.split("taskid")) - 1

    def getTaskIDs(self):
        temp = self.getTasks()
        tasks = temp.split('"taskid":"')[1:]
        n = []
        for i1 in tasks:
            n.append(i1.split('"')[0])
        return n

    def startTask(self, type):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash::::utype",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed" + "::::" + type,
                                "vh_addUpdate.php")
        if "result" in temp:
            return temp.split('result":"')[1].split('"')[0]
        return "2"

    def botnetInfo(self):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed",
                                "vh_botnetInfo.php")
        return temp

    def upgradeBotnet(self, ID):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash::::bID",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed" + "::::" + ID,
                                "vh_upgradeBotnet.php")
        return temp

    def finishTask(self, taskID):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash::::taskid",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed" + "::::" + taskID,
                                "vh_finishTask.php")
        if "4" in temp:
            return True
        else:
            return False

    def finishAll(self):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed",
                                "vh_finishAll.php")
        if "0" in temp:
            return True
        else:
            return False

    def useBooster(self):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash::::boost",
                                self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "userHash_not_needed" + "::::" + "1",
                                "vh_tasks.php")
        return temp

    def __init__(self, api):
        self.api = api
