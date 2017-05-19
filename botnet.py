#!/usr/bin/python2.7
# -*- coding: utf-8

from utils import Utils
import json
from console import Console
from update import Update


class Botnet:
    ut = Utils()

    def __init__(self, u, p):
        self.username = u
        self.password = p
        self.c = Console(self.username, self.password)
        self.u = Update(self.username, self.password)
        self.change = True
        self.moneycheck = True

    def getInfo(self):
        temp = self.ut.requestString("user::::pass::::uhash",
                                     self.username + "::::" + self.password + "::::" + "userHash_not_needed",
                                     "vh_botnetInfo.php")
        arr = temp.split('","canAtt')
        l = []
        for i1 in arr[1:]:
            l.append(i1.split(':')[1].split('"')[1])
        return l

    def attackable(self):
        t = self.getInfo()
        attack = False
        for i1 in t:
            if "1" in i1:
                attack = True
        return attack

    def attack(self):
        if self.attackable():
            print "Attacking with Botnet"
            attackbot = self.attackall()
            print attackbot

    def attackall(self):
        temp = self.ut.requestString("user::::pass::::uhash::::cID",
                                     self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "1",
                                     "vh_attackCompany.php")
        temp = self.ut.requestString("user::::pass::::uhash::::cID",
                                     self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "2",
                                     "vh_attackCompany2.php")
        temp = self.ut.requestString("user::::pass::::uhash::::cID",
                                     self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "3",
                                     "vh_attackCompany3.php")
        temp = self.ut.requestString("user::::pass::::uhash::::cID",
                                     self.username + "::::" + self.password + "::::" + "userHash_not_needed" + "::::" + "4",
                                     "vh_attackCompany4.php")
        return temp

    def update(self):
        money = json.loads(self.c.myinfo())
        json_data = json.loads(self.u.botnetInfo())
        print "analysing configuration... botnet"
        for i in range(0, int(json_data['count'])):
            moneycheck = True
            ireal = i + 1
            if json_data['data'][i]['bLVL'] == 100:
                break
            elif self.change:
                json_data = json.loads(self.u.botnetInfo())
                money = json.loads(self.c.myinfo())
            while int(json_data['data'][i]['bLVL']) is not 100 and moneycheck == True:
                if int(json_data['data'][i]['bPRICE']) < int(money['money']):
                    print "Updating Botnet " + str(ireal) + " level : " + str(int(json_data['data'][i]['bLVL']) + 1)
                    self.u.upgradeBotnet(str(ireal))
                    json_data = json.loads(self.u.botnetInfo())
                    money = json.loads(self.c.myinfo())
                    self.change = True
                else:
                    print "No money to update Botnet #" + str(ireal)
                    self.moneycheck = False
                    self.change = False
                    break
