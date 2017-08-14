#!/usr/bin/python2.7
# -*- coding: utf-8

from classes import Passwords
from utils import Utils
from ocr import OCR
from PIL import Image
import base64
import time
import json
import concurrent.futures
import random
import sys
import signal


class Console:
    def myinfo(self):
        ut = Utils()
        temp = ut.requestString("user::::pass::::gcm::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "eW7lxzLY9bE:APA91bEO2sZd6aibQerL3Uy-wSp3gM7zLs93Xwoj4zIhnyNO8FLyfcODkIRC1dc7kkDymiWxy_dTQ-bXxUUPIhN6jCUBVvGqoNXkeHhRvEtqAtFuYJbknovB_0gItoXiTev7Lc5LJgP2" + "::::" + "userHash_not_needed", "vh_update.php")
        return temp

    def requestPassword(self, ip):
        ut = Utils()
        arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_vulnScan.php")
        imgs = Passwords(arr)
        return imgs

    def enterPassword(self, passwd, target, uhash):
        passwd = passwd.split("p")
        ut = Utils()
        temp = ut.requestString("user::::pass::::port::::target::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(passwd[1].strip()) + "::::" + str(target) + "::::" + str(uhash), "vh_trTransfer.php")
        if temp == "10":
            return False
        else:
            return temp

    def scanUser(self):
        ut = Utils()
        arr = ut.requestArray("user::::pass::::", self.api.getUsername() + "::::" + self.api.getPassword() + "::::", "vh_scanHost.php")
        return arr

    def transferMoney(self, ip):
        ut = Utils()
        arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_trTransfer.php")
        return arr

    def clearLog(self, ip):
        ut = Utils()
        s = ut.requestString("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_clearAccessLogs.php")
        if s == "0":
            return True
        else:
            return False

    def uploadSpyware(self, ip):
        ut = Utils()
        s = ut.requestString("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_spywareUpload.php")
        if s == "0":
            return True
        else:
            return False

    def getTournament(self):
        ut = Utils()
        temp = ut.requestString("user::::pass::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "UserHash_not_needed", "vh_update.php")
        if "tournamentActive" in temp:
            if "2" not in temp.split('tournamentActive":"')[1].split('"')[0]:
                return True
            else:
                return False

    def get_main_color(self, file):
        img = Image.open(file)
        colors = img.getcolors(256)  # put a higher value if there are many colors in your image
        max_occurence, most_present = 0, 0
        try:
            for c in colors:
                if c[0] > max_occurence:
                    (max_occurence, most_present) = c
                    return max_occurence
        except TypeError:
            raise Exception("Too many colors in the image")

    def getIP(self, blank):
        ut = Utils()
        try:
            info = self.myinfo()
            info = json.loads(info)
            uhash = info['uhash']
            temp = ut.requestString("user::::pass::::uhash::::global", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + str(random.randint(0, 1)), "vh_getImg.php")
            jsons = json.loads(temp)
        except TypeError:
            return 0, 0
        for i in range(0, len(jsons["data"])):
            hostname = str(jsons["data"][i]["hostname"])

            # Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
            # bg = Image.new("RGB", image.size, (255,255,255))
            # bg.paste(image,image)

            imgdata = base64.b64decode(jsons["data"][i]['img'])
            filename = 'vhack.png'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            image = self.get_main_color(filename)
            # print image[0], image[1], image[2], image[3]
            if image < 13200:
                time.sleep(5)
                return 1, hostname
            else:
                temp = ut.requestString("user::::pass::::uhash::::hostname", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + hostname, "vh_scanHost.php")
                try:
                    jsons = json.loads(temp)
                    return 0, str(jsons['ipaddress'])
                except TypeError:
                    return 0, 0
                # print str(jsons['ipaddress'])

    def attackIP(self, ip, max, mode):
        ut = Utils()
        info = self.myinfo()
        info = json.loads(info)
        uhash = info['uhash']
        temp = ut.requestString("user::::pass::::uhash::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + uhash + "::::" + ip, "vh_loadRemoteData.php")

        jsons = json.loads(temp)

        o = OCR()
        imgs = o.getSolution(str(temp))
        if imgs is not None:
            try:
                # user = jsons['username']
                winchance = jsons['winchance']
            except TypeError:
                return False
            try:
                if "?" not in str(winchance):
                    fwlevel = jsons['fw']
                    avlevel = jsons['av']
                    # spamlevel = jsons['spam']
                    sdklevel = jsons['sdk']
                    # ipsplevel = jsons['sdk']
                    money = jsons['money']
                    saving = jsons['savings']
                    anonymous = jsons['anonymous']
                    username = jsons['username']
                    # winlo = jsons['winelo']
                    winchance = jsons['winchance']
                    # spywarelevel = jsons['spyware']
                else:
                    avlevel = "????"
                    winchance = 0
                    print "no scan username"
                    return False

            except TypeError:
                fwlevel = jsons['fw']
                avlevel = jsons['av']
                # spamlevel = jsons['spam']
                sdklevel = jsons['sdk']
                # ipsplevel = jsons['sdk']
                money = jsons['money']
                saving = jsons['savings']
                anonymous = jsons['anonymous']
                username = jsons['username']
                # winlo = jsons['winelo']
                winchance = jsons['winchance']
                # spywarelevel = jsons['spyware']

            if type(winchance) == "int":
                if "?" in winchance:
                    winchance = 0
                    print "no chance"
                    return False

            if mode == "Potator":
                if winchance > 49:
                    password = self.enterPassword(imgs, ip, uhash)
                    jsons = json.loads(password)
                    if password:
                        try:
                            if "?" not in str(money) and str(jsons['result']) == 0:
                                print("\n[TargetIP: {}]\n\nMade {:11,} and {:2d} Rep.\n Antivirus: {} Firewall: {} Sdk: {} TotalMoney: {:11,}\n YourWinChance: {} Anonymous: {} username: {} saving: {}".format(
                                      ip, jsons['amount'], jsons['eloch'], avlevel, fwlevel, sdklevel, money, winchance, anonymous, username, saving))
                                return True
                            else:
                                print("\n[TargetIP: {}]\n\nMade {:11,} and {:2d} Rep.\n Antivirus: {} Firewall: {} Sdk: {} TotalMoney: {:11,}\n YourWinChance: {} Anonymous: {} username: {} saving: {}".format(
                                      ip, jsons['amount'], jsons['eloch'], avlevel, fwlevel, sdklevel, money, winchance, anonymous, username, saving))
                                return True

                        except KeyError:
                            print "Bad attack"
                            return False

                        except ValueError as e:
                            print "Error: " + e
                            return True
                    else:
                        print "Password Wrong"
                        return False
                else:
                    print "winchance is poor: " + str(winchance)

            if "?" not in str(avlevel) and mode == "Secure":
                if int(avlevel) < max and int(winchance) > 75 and str(anonymous) == "YES":
                    password = self.enterPassword(imgs, ip, uhash)
                    jsons = json.loads(password)
                    if password:
                        try:
                            if "?" not in str(money) and str(jsons['result']) == 0:
                                print("\n[TargetIP: {}]\n\nMade {:11,} and {:2d} Rep.\n Antivirus: {} Firewall: {} Sdk: {} TotalMoney: {:11,}\n YourWinChance: {} Anonymous: {} username: {} saving: {}".format(
                                      ip, jsons['amount'], jsons['eloch'], avlevel, fwlevel, sdklevel, money, winchance, anonymous, username, saving))
                                return True
                            else:
                                print("\n[TargetIP: {}]\n\nMade {:11,} and {:2d} Rep.\n Antivirus: {} Firewall: {} Sdk: {} TotalMoney: {:11,}\n YourWinChance: {} Anonymous: {} username: {} saving: {}".format(
                                      ip, jsons['amount'], jsons['eloch'], avlevel, fwlevel, sdklevel, money, winchance, anonymous, username, saving))
                        except KeyError:
                            print "Bad attack"
                            return False
                    else:
                        print "Password Wrong"
                        return False
                else:
                    # print "\n"
                    if int(avlevel) > max:
                        print "Antivir to high " + str(avlevel)
                        # print "passed"
                        return False
                    if int(winchance) < 75:
                        print "winchance is poor: " + str(winchance)
                        # print "passed"
                        return False
                    if str(anonymous) == "NO":
                        print "No Anonymous needed"
                        # print "passed"
                        return False
            else:
                if len(avlevel) == 4:
                    print "Cant load User"
                    return False
                else:
                    print "Scan to low"
                    return False
        else:
            print "Password Error"
            return False

    def attackIP2(self, ip, max):
        # ut = Utils()
        o = OCR(False)
        imgs = self.requestPassword(ip)
        selection = o.getPassword(imgs)
        print selection

    def attack(self, amount, max, wait, mode, api):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(1, amount):
                FBI, ips = self.getIP(True)
                if FBI == 0:
                    executor.submit(self.attackIP, ips, max, mode)
                    print "Waiting..."
                    time.sleep(wait)
                else:
                    print "Warning FBI Blocking account on " + str(ips) + " I will not attack"

    def exit_gracefully(self, signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        signal.signal(signal.SIGINT, original_sigint)

        try:
            if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
                sys.exit(1)

        except KeyboardInterrupt:
            print("Ok ok, quitting")
            sys.exit(1)

        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def __init__(self, api):
        global original_sigint
        self.api = api
        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.exit_gracefully)
