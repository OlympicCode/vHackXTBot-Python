#!/usr/bin/python2.7
# -*- coding: utf-8

from utils import Utils


class Botnet:
    ut = Utils()

    def __init__(self, u, p):
        self.username = u
        self.password = p

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

