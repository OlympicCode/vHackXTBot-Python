import config
from utils import Utils
import json
import logging
import sys


class Player:
    ut = Utils()

    def __init__(self):
        self.username = config.user
        self.password = config.password
        self.money = 0
        self.ip = ''
        self.score = ''
        self.netcoins = ''
        self.boosters = ''
        self.rank = ''
        self.uhash = ''
        self.localspyware = ''
        self.remotespyware = ''
        self.email = 0
        self.savedIPs = []
        self.anon_attack = config.anon
        self._init()  # 10 secs

    def __repr__(self):
        return "Money: {0}, Score: {1}".format(self.money, self.score)

    def getplayerinfo(self):
        pass

    def setmoney(self, amount):
        """
        Change class money value, pass in neg or postive values
        :param amount:
        :return:
        """
        self.money = amount

    def getmoney(self):
        return self.money

    def removespy(self):
        response = self.ut.requestArray(self.username, self.password, self.uhash, "vh_removeSpyware.php")
        return response

    def _init(self):
        """
        {"id":"924198","money":"14501972","ip":"83.58.131.20",
        "inet":"10","hdd":"10","cpu":"10","ram":"14","fw":"256","av":"410","sdk":"580","ipsp":"50","spam":"71","scan":"436","adw":"76",
        "actadw":"","netcoins":"5550","energy":"212286963","score":"10015",
        "urmail":"1","active":"1","elo":"2880","clusterID":null,"position":null,"syslog":null,
        "lastcmsg":"0","rank":32022,"event":"3","bonus":"0","mystery":"0","vipleft":"OFF",
        "hash":"91ec5ed746dfedc0a750d896a4e615c4",
        "uhash":"9832f717079f8664109ac9854846e753282c72cdf42fe33fb33c734923e1931c","use":"0",
        "tournamentActive":"2","boost":"294","actspyware":"0","tos":"1","unreadmsg":"0"}
        :return:
        """
        data = self.ut.requestString(self.username, self.password, self.uhash, "vh_update.php")
        if len(data) == 1:
            logging.warn('Username and password entered in config.py?')
            sys.exit()
        try:
            j = json.loads(data)
            self.setmoney(j['money'])
            self.ip = j['ip']
            self.score = j['score']
            self.netcoins = j['netcoins']
            self.localspyware = j['actspyware']
            self.rank = j['rank']
            self.boosters = j['boost']
            self.remotespyware = j['actadw']
            self.email = int(j['urmail'])
            self.uhash = str(j['uhash'])
        except:
            exit()

    def get_uhash(self):
        return self.uhash

    def refreshinfo(self):
        """
        Refresh player info. Useful after a dev attack to pick up new email etc.
        :return:
        """
        self._init()

    def readmail(self):
        """
        Read any new emails. Print to console.
        :return: None
        """
        if self.email:
            pass
