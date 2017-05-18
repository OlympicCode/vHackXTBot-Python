#!/usr/bin/python2.7
# -*- coding: utf-8

class Passwords:
    def getImage1(self):
        return self.img1

    def __init__(self, arr):
        if len(arr) == 5:
            self.img1 = arr[0].split(":")[1]
        else:
            self.img1 = "null"


class IP:
    def getIP(self):
        return self.ip

    def getFirewallLevel(self):
        return self.firewallLevel

    def getAttacked(self):
        return self.attacked

    def __init__(self, arr):
        if len(arr) == 3:
            self.ip = arr[0].split(":")[1]
            self.firewallLevel = int(arr[1].split(":")[1])
            self.attacked = int(arr[2].split(":")[1])
        else:
            self.ip = ""
            self.firewallLevel = 0
            self.attacked = 0
