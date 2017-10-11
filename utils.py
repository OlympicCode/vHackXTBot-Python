#!/usr/bin/python2.7
# -*- coding: utf-8

import base64
import hashlib
import time
import urllib2
import config
import ssl
import logging
import json
logger = logging.getLogger(__name__)

USER_AGENT = ['Dalvik/2.1.0 (Linux; U; Android 5.0.1; GT-I9508V Build/LRX22C)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.1; MX4 Build/LRX22C)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D5322 Build/19.3.A.0.472)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D816w Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC D816v Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC E9pw Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC M8t Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC One M8s Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; LG-F320L Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Letv X500 Build/DBXCNOP5500912251S)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Nexus 5 Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; SM-N9005 Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0; ASUS_Z00ADB Build/LRX21V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0; Nexus 5 Build/LPX13D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1 Build/LYZ28N)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; 2014811 MIUI/6.1.26)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; D5833 Build/23.4.A.1.232)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; GT-I9152 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; LG-D802 Build/LMY48W)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2 Build/LMY48B)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2SC Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 3 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Mi-4c MIUI/6.1.14)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; NX403A Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONE A2001 Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; R7Plusm Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Redmi Note 2 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-J3109 Build/LMY47X)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N9200 Build/LMY47X)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Sparkle V Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Xperia Z2 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; titan Build/LMY48W)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC M9w Build/LMY47O)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC One M9 Build/LMY47O)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; LG-H818 Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; MX5 Build/LMY47I)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1060 Build/LPA23.12-39.7)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1085 Build/LPE23.32-53)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m1 note Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 note Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; 2014813 Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; A0001 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ASUS_Z00A Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 4LTE Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Mi-4c Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 LTE Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 4 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Sensation Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Z1 Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2 Build/MRA58K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2A Build/MRA58K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; Moto G 2014 Build/MDB08M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; XT1097 Build/MPE24.49-18)']


class Utils:
    def __init__(self):
        self.secret = "aeffI"
        self.url = "https://api.vhack.cc/v/13/"
        self.username = config.user
        self.password = config.password
        self.user_agent = ""

    def generateUA(self, identifier):
        pick = int(self.md5hash(identifier), 16)
        user_agents = tuple(USER_AGENT)
        return user_agents[pick % len(user_agents)]

    def getTime(self):
        return int(round(time.time()))

    def md5hash(self, txt):
        m = hashlib.md5()
        m.update(txt)
        return m.hexdigest()

    def generateUser(self, bArr):
        return base64.b64encode(bArr).replace("=", "")

    def generateURL(self, username, password, uhash, php, **kwargs):
        if not kwargs:
            jsonString = {"": ""}
        else:
            jsonString = kwargs
        currentTimeMillis = str(self.getTime())
        jsonString.update({'time': currentTimeMillis, 'uhash': uhash, 'user': username, 'pass': password})
        jsonString = json.dumps(jsonString, separators=(',', ':'))
        a = self.generateUser(jsonString)
        a2 = self.md5hash(str(len(jsonString)) + self.md5hash(currentTimeMillis))
        str5 = username + self.md5hash(self.md5hash(password))
        str6 = self.md5hash(currentTimeMillis + jsonString)
        a3 = self.md5hash(self.secret + self.md5hash(self.md5hash(self.generateUser(a2))))
        str9 = self.md5hash(a3 + self.generateUser(str5))
        str7 = self.generateUser(str6)
        str8 = self.md5hash(self.md5hash(a3 + self.md5hash(self.md5hash(str9) + str7) + str9 + self.md5hash(str7)))
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

    def requestString(self, username, password, uhash, php, **kwargs):
        logger.debug("Request: {}".format(php))
        self.user_agent = self.generateUA(username + password)
        time.sleep(1)
        t = None
        i = 0
        while t is None:
            if i > 10:
                exit(0)
            try:
                req = urllib2.Request(self.generateURL(username, password, uhash, php, **kwargs))
                req.add_header('User-agent', self.user_agent)
                r = urllib2.urlopen(req, context=ssl._create_unverified_context(), timeout=15)
                t = r.read()
                logger.debug("Response:\n{}\n".format(t))
                if t == "5":
                    logger.info("Check your Internet.")
                elif t == "8":
                    logger.info("User/Password wrong!")
                elif t == "10":
                    logger.info("API is updated.")
                elif t == "15":
                    logger.info("You are Banned sorry :(")
                elif t == "99":
                    logger.info("Server is down for Maintenance, please be patient.")
                return t
            except urllib2.URLError as e:
                logger.error('Error: {}'.format(e))
                logger.info('Timeout while requesting "{}"'.format(php))
                time.sleep(1 + i)
            except Exception as e:
                logger.error('Error: {}'.format(e))
                logger.info("Blocked, trying again. Delaying {0} seconds".format(i))
                time.sleep(1 + i)
            i += 1

    def requestStringNoWait(self, username, password, uhash, php, **kwargs):
        self.user_agent = self.generateUA(username + password)
        for i1 in range(0, 10):
            try:
                req = urllib2.Request(self.generateURL(username, password, uhash, php, **kwargs))
                req.add_header('User-agent', self.user_agent)
                r = urllib2.urlopen(req, context=ssl._create_unverified_context(), timeout=15)
                t = r.read()
                # print i1
                return t
            except Exception as e:
                logger.error('Error: {}'.format(e))
                time.sleep(1)
        return "null"

    def printit(self, txt):
        logger.info(txt)

    def requestArray(self, username, password, uhash, php, **kwargs):
        temp = self.requestString(username, password, uhash, php, **kwargs)
        if temp != "null":
            return self.parse(temp)
        else:
            return []
