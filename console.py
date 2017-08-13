#!/usr/bin/python2.7
# -*- coding: utf-8

from classes import Passwords
from utils import Utils
import time
import json
from PIL import Image
import base64
import requests
import re
import concurrent.futures
import random
import sys
import signal
import io

original_sigint = None


class Console:
    ut = Utils()

    def __init__(self, player):
        global original_sigint
        self.username = player.username
        self.password = player.password
        self.uhash = player.uhash
        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def myinfo(self):
        temp = self.ut.requestString("user::::pass::::gcm::::uhash",
                                     self.username + "::::" + self.password + "::::" + "eW7lxzLY9bE:APA91bEO2sZd6aibQerL3Uy-wSp3gM7zLs93Xwoj4zIhnyNO8FLyfcODkIRC1dc7kkDymiWxy_dTQ-bXxUUPIhN6jCUBVvGqoNXkeHhRvEtqAtFuYJbknovB_0gItoXiTev7Lc5LJgP2" + "::::" + self.uhash,
                                     "vh_update.php")
        return temp

    def requestPassword(self, ip):
        arr = self.ut.requestArray("user::::pass::::target",
                                   self.username + "::::" + self.password + "::::" + ip,
                                   "vh_vulnScan.php")
        imgs = Passwords(arr)
        return imgs

    def enterPassword(self, target, passwd):
        passwd = passwd.split("p")
        temp = self.ut.requestString("user::::pass::::port::::target::::uhash",
                                     self.username + "::::" + self.password + "::::" + "0" + "::::" + str(target) + "::::" + self.uhash,
                                     "vh_trTransfer.php")  # passwd[1].strip()
        result = json.loads(temp)
        if str(result["result"]) == "0":
            return temp
        else:
            return False

    def check_Cluster(self, uhash):
        if self.uhash is None:
            temp = self.ut.requestString("user::::pass::::uhash",
                                         self.username + "::::" + self.password + "::::" + self.uhash,
                                         "vh_ClusterData.php")
        else:
            temp = self.ut.requestString("user::::pass::::uhash",
                                         self.username + "::::" + self.password + "::::" + self.uhash,
                                         "vh_ClusterData.php")
        return temp

    def scanUser(self):
        arr = self.ut.requestArray("user::::pass::::uhash",
                                   self.username + "::::" + self.password + "::::" + self.uhash, "vh_scanHost.php")
        return arr

    def GetTournamentPosition(self):
        temp = self.ut.requestString("user::::pass::::uhash",
                                     self.username + "::::" + self.password + "::::" + self.uhash,
                                     "vh_tournamentData.php")
        return temp

    def AttackCluster(self, tag):
        temp = self.ut.requestString("user::::pass::::uhash::::ctag",
                                     self.username + "::::" + self.password + "::::" + self.uhash + "::::" + str(
                                         tag), "vh_startDDoS.php")
        return temp

    def ScanCluster(self, tag):
        temp = self.ut.requestString("user::::pass::::uhash::::ctag",
                                     self.username + "::::" + self.password + "::::" + self.uhash + "::::" + str(
                                         tag), "vh_scanTag.php")
        return temp

    def transferMoney(self, ip):
        arr = self.ut.requestArray("user::::pass::::target",
                                   self.username + "::::" + self.password + "::::" + ip,
                                   "vh_trTransfer.php")
        return arr

    def clearLog(self, ip):
        s = self.ut.requestString("user::::pass::::target",
                                  self.username + "::::" + self.password + "::::" + ip,
                                  "vh_clearAccessLogs.php")
        if s == "0":
            return True
        else:
            return False

    def uploadSpyware(self, ip):
        s = self.ut.requestString("user::::pass::::target",
                                  self.username + "::::" + self.password + "::::" + ip,
                                  "vh_spywareUpload.php")
        if s == "0":
            return True
        else:
            return False

    def getTournament(self):
        temp = self.ut.requestString("user::::pass::::uhash",
                                     self.username + "::::" + self.password + "::::" + self.uhash,
                                     "vh_update.php")
        if "tournamentActive" in temp:
            if "2" not in temp.split('tournamentActive":"')[1].split('"')[0]:
                return True
            else:
                return False

    def returncrawler(fd, lineexec):
        fd.write('{0}\n'.format(lineexec.result()))
        fd.flush()

    def get_main_color(self, image_data):
        img = Image.open(io.BytesIO(image_data))
        colors = img.getcolors(256)  # put a higher value if there are many colors in your image
        max_occurence, most_present = 0, 0
        try:
            for c in colors:
                if c[0] > max_occurence:
                    (max_occurence, most_present) = c
                    return max_occurence
        except TypeError:
            raise Exception("Too many colors in the image")

    def calc_img(self, ut, imgstring, uhash, hostname, mode):
        # pic = cStringIO.StringIO()
        # image_string = cStringIO.StringIO(base64.b64decode(imgstring))
        # image = Image.open(image_string)

        # Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
        # bg = Image.new("RGB", image.size, (255,255,255))
        # bg.paste(image,image)

        imgdata = base64.b64decode(imgstring)
        image = self.get_main_color(imgdata)

        if image < 13200:
            print "Matched FBI"
            return 1, hostname

        else:
            # firewall = pytesseract.image_to_string(image).split(":")
            # print firewall[2].strip()
            try:
                # if int(firewall[2].strip()) < max:
                    try:
                        temp = self.ut.requestString("user::::pass::::uhash::::hostname",
                                                     self.username + "::::" + self.password + "::::" + self.uhash
                                                     + "::::" + str(hostname), "vh_scanHost.php")

                        jsons = json.loads(temp)
                        if ".vHack.cc" not in str(jsons['ipaddress']):
                            result = self.attackIP(jsons['ipaddress'], mode)
                            # remove spyware
                            """u = Update(self.username, self.password)
                            spyware = u.SpywareInfo()
                            if int(spyware[0].split(":")[-1]) > 0 and not int(spyware[0].split(":")[-1]) == 0:
                                u.removeSpyware()
                                print "I will remove " + str(spyware[0].split(":")[-1]) + " Spyware for your account."""

                            return result, jsons['ipaddress']

                        # else:
                        #     temp = self.ut.requestString("user::::pass::::uhash::::hostname", self.username + "::::" + self.password + "::::" + str(uhash) + "::::" + jsons['ipaddress'], "vh_scanHost.php")
                        #     if not ".vHack.cc" in str(jsons['ipaddress']) and int(jsons['vuln']) == 1:
                        #         time.sleep(1)
                        #         self.attackIP(jsons['ipaddress'], max, mode)

                    except TypeError as e:
                        print e
                        return 0, 0, "type error" + e
                # else:
                #    print "Firewall level is to High"
                #    return 0, 0

            except ValueError as e:
                print e
                return 0, 0, "value error"

    def getIP(self, blank, max, mode, active_protecte_cluster_ddos):
        stat_cluster = self.check_Cluster(self.uhash)
        stat_cluster = json.loads(stat_cluster)
        try:
            stat_cluter_blocked = stat_cluster['blocked']
        except:
            stat_cluter_blocked = ""

        if "Your Cluster is blocked" in stat_cluter_blocked and active_protecte_cluster_ddos:
            print "wait 2 minutes" + stat_cluter_blocked
            time.sleep(120)
        else:
            temp = self.ut.requestString("user::::pass::::uhash::::by",
                                         self.username + "::::" + self.password + "::::" + str(
                                             self.uhash) + "::::" + str(random.randint(0, 1)), "vh_getImg.php")
            jsons = json.loads(temp)
            list_image = []
            list_hostname = []

            for i in range(0, len(jsons["data"])):
                hostname = str(jsons["data"][i]["hostname"])
                imgstring = 'data: image/png;base64,' + jsons["data"][i]['img']
                imgstring = imgstring.split('base64,')[-1].strip()
                list_image.append(imgstring)
                list_hostname.append(hostname)

            print "Packing IP list " + str(len(list_image))
            # fd = open("database.txt", "a")

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                for i, image in enumerate(list_image):
                    wait_for = executor.submit(self.calc_img, self.ut, list_image[i], self.uhash, list_hostname[i], mode)
                    
                    try:
                        result, ip = wait_for.result()
                    
                    except TypeError:
                        result = False

                    except ValueError:
                        result = False

                    if result:
                        with open("database.text", "a") as f:
                            f.write(ip + "\n")

    def attackIP(self, ip, mode):
        temp = self.ut.requestString("user::::pass::::uhash::::target",
                                     self.username + "::::" + self.password + "::::" + self.uhash
                                     + "::::" + ip, "vh_loadRemoteData.php")
        jsons = json.loads(temp)

        # o = OCR()
        # imgs = o.getSolution(str(temp))
        imgs = True
        if imgs is not None:
            try:
                # user = jsons['username']
                winchance = jsons['winchance']
            except TypeError:
                print "error"
                return False

            try:
                if winchance:
                    fwlevel = jsons['fw']
                    avlevel = jsons['av']
                    # spamlevel = jsons['spam']
                    sdklevel = jsons['sdk']
                    ipsplevel = jsons['ipsp']
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
                ipsplevel = jsons['ipsp']
                money = jsons['money']
                saving = jsons['savings']
                anonymous = jsons['anonymous']
                username = jsons['username']
                # winlo = jsons['winelo']
                winchance = jsons['winchance']
                # spywarelevel = jsons['spyware']

            if type(winchance) == "str":
                if "?" in winchance:
                    winchance = 0
                    print "no chance"
                    return False

            if mode == "Potator":
                if winchance > 20:
                    password = self.enterPassword(ip, self.uhash)
                    jsons = json.loads(password)
                    if int(jsons["result"]) == 0:
                        try:
                            if "?" not in str(money) and str(jsons['result']) == 0:
                                print "\nYour Money: " + "{:11,}".format(
                                    int(jsons['newmoney'])) + "\n[TargetIP: " + str(
                                    ip) + "]\n\nMade " + "{:11,}".format(
                                    int(jsons['amount'])) + " and " + "{:2d}".format(
                                    int(jsons['eloch'])) + " Rep." + "\n Antivirus: " + str(
                                    avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(
                                    sdklevel) + " TotalMoney: " + "{:11,}".format(
                                    int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: " + str(
                                    anonymous) + " username: " + str(username) + " saving: " + str(saving) + "\n"
                                try:
                                    ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', username).group()
                                except AttributeError:
                                    pass
                                # print ip, type(ip), username, type(username)
                                s = requests.session()
                                if ip == username:
                                    print "send to database"
                                    s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&MONEY=" + str(money) + "&IPSP=" + str(ipsplevel) + "&FW=" + str(
                                        fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                                else:
                                    print "send to database"
                                    s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&USR=" + str(username) + "&MONEY=" + str(money) + "&IPSP=" + str(
                                        ipsplevel) + "&FW=" + str(fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                            else:
                                print "\nYour Money: " + "{:11,}".format(
                                    int(jsons['newmoney'])) + "\n[TargetIP: " + str(
                                    ip) + "]\n\nMade " + "{:11,}".format(
                                    int(jsons['amount'])) + " and " + "{:2d}".format(
                                    int(jsons['eloch'])) + " Rep." + "\n Antivirus: " + str(
                                    avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(
                                    sdklevel) + " TotalMoney: " + str(money) + "\n YourWinChance: " + str(
                                    winchance) + " Anonymous: " + str(anonymous) + " username: " + str(
                                    username) + " saving: " + str(saving) + "\n"
                                try:
                                    ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', username).group()
                                except AttributeError:
                                    pass
                                # print ip, type(ip), username, type(username)
                                s = requests.session()
                                if ip == username:
                                    print "send to database"
                                    s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&MONEY=" + str(money) + "&IPSP=" + str(ipsplevel) + "&FW=" + str(
                                        fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                                else:
                                    print "send to database"
                                    s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&USR=" + str(username) + "&MONEY=" + str(money) + "&IPSP=" + str(
                                        ipsplevel) + "&FW=" + str(fwlevel) + "&AV=" + str(avlevel))
                                    s.close()

                                return True

                        except KeyError:
                            print "Bad attack"
                            return False

                        except ValueError as e:
                            print "error: " + e
                            return True
                    else:
                        print "Password Wrong"
                        return False
                else:
                    print "winchance is poor: " + str(winchance)
                    return False

            if "?" not in str(avlevel) and "?" not in str(winchance) and mode == "Secure":
                if int(winchance) > 75 and str(anonymous) == "YES":
                    password = self.enterPassword(ip, self.uhash)
                    jsons = json.loads(password)
                    if int(jsons["result"]) == 0:
                        try:
                            if "?" not in str(money) and str(jsons['result']) == 0:
                                print "\nYour Money: " + "{:11,}".format(
                                    int(jsons['newmoney'])) + "\n[TargetIP: " + str(
                                    ip) + "]\n\nMade " + "{:11,}".format(
                                    int(jsons['amount'])) + " and " + "{:2d}".format(
                                    int(jsons['eloch'])) + " Rep." + "\n Antivirus: " + str(
                                    avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(
                                    sdklevel) + " TotalMoney: " + "{:11,}".format(
                                    int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: " + str(
                                    anonymous) + " username: " + str(username) + " saving: " + str(saving) + "\n"
                                try:
                                    ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', username).group()
                                except AttributeError:
                                    pass
                                # print ip, type(ip), username, type(username)
                                s = requests.session()
                                if ip == username:
                                    print "send to database"
                                    print s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&MONEY=" + str(money) + "&IPSP=" + str(ipsplevel) + "&FW=" + str(
                                        fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                                else:
                                    print "send to database"
                                    print s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&USR=" + str(username) + "&MONEY=" + str(money) + "&IPSP=" + str(
                                        ipsplevel) + "&FW=" + str(fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                                return True
                            else:
                                print "\nYour Money: " + "{:11,}".format(
                                    int(jsons['newmoney'])) + "\n[TargetIP: " + str(
                                    ip) + "]\n\nMade " + "{:11,}".format(
                                    int(jsons['amount'])) + " and " + "{:2d}".format(
                                    int(jsons['eloch'])) + " Rep." + "\n Antivirus: " + str(
                                    avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(
                                    sdklevel) + " TotalMoney: " + str(money) + "\n YourWinChance: " + str(
                                    winchance) + " Anonymous: " + str(anonymous) + " username: " + str(
                                    username) + " saving: " + str(saving) + "\n"
                                try:
                                    ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', username).group()
                                except AttributeError:
                                    pass
                                # print ip, type(ip), username, type(username)
                                s = requests.session()
                                if ip == username:
                                    print "send to database"
                                    s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&MONEY=" + str(money) + "&IPSP=" + str(ipsplevel) + "&FW=" + str(
                                        fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                                else:
                                    print "send to database"
                                    s.get("https://vhack.olympiccode.ga/database/submit.php?IP=" + str(
                                        ip) + "&USR=" + str(username) + "&MONEY=" + str(money) + "&IPSP=" + str(
                                        ipsplevel) + "&FW=" + str(fwlevel) + "&AV=" + str(avlevel))
                                    s.close()
                                return True

                        except KeyError:
                            print "Bad attack"
                            return False
                    else:
                        print "Password Incorrect"
                        return False
                else:
                    # print "\n"
                    if int(winchance) < 75:
                        print "winchance is poor: " + str(winchance)
                        # print "passed"
                        return False
                    if str(anonymous) == "NO":
                        print "Hack Anonymous is needed"
                        # print "passed"
                        return False
            else:
                if "?" in str(avlevel):
                    print "Cant load User"
                    return False
                else:
                    print "Scan to low ("+str(avlevel)+")"
                    return False
        else:
            print "Password Error"
            return False

    def attack(self, obj):
        for i in range(0, (obj.attacks_normal * random.randint(1, 2))):
            self.getIP(True, obj.maxanti_normal, obj.mode, obj.active_cluster_protection)
            print "wait anti-blocking..."

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
