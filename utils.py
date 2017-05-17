#!/usr/bin/python2.7
# -*- coding: utf-8

import base64
import commands
import hashlib
import sys
import time
import urllib2
from classes import Passwords
import random


class Utils:
    def getTime(self):
        return int(round(time.time()))

    def md5hash(self, txt):
        m = hashlib.md5()
        m.update(txt)
        return m.hexdigest()

    def generateUser(self, bArr):
        return base64.b64encode(bArr).replace("=", "")

    def generateURL(self, format, data, php):
        split = format.split("::::")
        split2 = data.split("::::")
        currentTimeMillis = str(self.getTime())
        jsonString = "{"
        for i1 in range(0, len(split)):
            jsonString += "\"" + split[i1] + "\":"
            jsonString += "\"" + split2[i1] + "\","
        jsonString += "\"time\":\"" + currentTimeMillis + "\"}"
        a = self.generateUser(jsonString)
        a2 = self.md5hash(str(len(jsonString)) + self.md5hash(currentTimeMillis))
        str5 = split2[0] + self.md5hash(self.md5hash(split2[1]))
        str6 = self.md5hash(currentTimeMillis + jsonString)
        a3 = self.md5hash(self.secret + self.md5hash(self.md5hash(self.generateUser(a2))))
        str9 = self.generateUser(str5)
        str7 = self.generateUser(str6)
        str8 = self.md5hash(self.md5hash(a3 + self.md5hash(self.md5hash(str9) + str7)))
        return self.url + php + "?user=" + a + "&pass=" + str8

    def parse(self, string):
        return string[1:-1].replace("\"", "").split(",")

    def parseMulti(self, string):
        temp = string
        temp = temp.replace("[", "").replace("]", "")
        temp = temp[len(temp.split(":")[0]) + 1:-1]

        arr = temp.split("},{")
        n = []
        for i1 in arr:
            temp = i1
            if not temp.startswith("{"):
                temp = "{" + temp
            if not temp.endswith("}"):
                temp += "}"
            n.append(self.parse(temp))
        return n


    def requestString(self, format, data, php):
        time.sleep(random.randint(1, 2))
        t = None
        i = 1
        while t == None:
            i += 1
            try:
                r = urllib2.urlopen(self.generateURL(format, data, php))
                t = r.read()
                return t
            except Exception as err:
                print "Blocked, trying again. Delaying {0} seconds".format(i)
                time.sleep(1+i)
                
    
    def requestStringNoWait(self, format, data, php):
        for i1 in range(0, 10):
            try:
                r = urllib2.urlopen(self.generateURL(format, data, php))
                t = r.read()
                # print i1
                return t
            except Exception as err:
                time.sleep(1)
        return "null"

    def printit(self, txt):
        print txt

    def requestArray(self, format, data, php):
        temp = self.requestString(format, data, php)
        if temp != "null":
            return self.parse(temp)
        else:
            return []

    def __init__(self):
        self.secret = "aeffI"
        self.url = "https://api.vhack.cc/v/7/"
