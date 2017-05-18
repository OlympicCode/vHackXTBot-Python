#!/usr/bin/python2.7
# -*- coding: utf-8

from console import Console
from update import Update
from botnet import Botnet
from random import randrange, uniform
import operator
import time
import json
import re
import sqlite3
import os
import config


class run:

    def __init__(self):
        """
        PUll all variables from config.py file.
        """
        self.username = config.user
        self.password = config.password
        self.ddos_cluster = config.ddos_cluster
        self.database = config.database
        self.Max_point_tournament = config.Max_point_tournament
        self.BotNet_update = config.BotNet_update
        self.joinTournament = config.joinTournament
        self.tournament_potator = config.tournament_potator
        self.updates = config.updates
        self.updatecount = config.updatecount
        self.booster = config.booster
        self.Use_netcoins = config.Use_netcoins
        self.attacks_normal = config.attacks_normal
        self.maxanti_normal = config.maxanti_normal
        self.active_cluster_protection = self.active_cluster_protection
        self.init()

        self.c = Console(self.username, self.password)
        self.u = Update(self.username, self.password)
        self.b = Botnet(self.username, self.password)

    def init(self):
        while True:
            if self.ddos_cluster:
                checkcluster = json.loads(self.c.check_Cluster())
                TournamentPosition = json.loads(self.c.GetTournamentPosition())
                try:
                    # determine and attack cluster tournament
                    db = sqlite3.connect(self.database)
                    cursor = db.cursor()

                    try:
                        cursor.execute("""CREATE TABLE Cluster (ID TEXT, cluster_name TEXT, cluster_point TEXT) """)
                    except sqlite3.OperationalError:
                        pass

                    tournament_left = re.findall('\d+', TournamentPosition["tleft"])
                    print "Tournament star finish in " + str(TournamentPosition["tleft"])
                    try:
                        tournament_hour = tournament_left[0]
                        tournament_minute = tournament_left[1]
                    except IndexError:
                        tournament_hour = 0
                        try:
                            tournament_minute = tournament_left[0]
                        except IndexError:
                            tournament_minute = 0

                    if int(tournament_hour) == 0 and int(tournament_minute) < 60:

                        cluster_name = {}
                        for row in cursor.execute(
                                "SELECT * FROM (SELECT cluster_point, cluster_name FROM Cluster ORDER BY cluster_point ASC)"):
                            cluster_name[row[0]] = row[1]

                        newA = sorted(cluster_name.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(cluster_name)]

                        for i in range(0, len(newA)):
                            Cluster_name = newA[i][1]
                            Cluster_point = newA[i][0]

                            checkcluster = json.loads(self.c.check_Cluster())
                            if "DDoS not ready" in checkcluster["ddosready"]:
                                print checkcluster["ddosready"]
                                break
                            else:
                                try:
                                    scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                                except UnicodeEncodeError:
                                    scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))

                                if scan_cluster["result"] == "0":
                                    scan_cluster["ddoschance"] = scan_cluster["ddoschance"].split("%")
                                    ddoschance = re.findall('\d+', scan_cluster["ddoschance"][0])
                                    if int(ddoschance[0]) > 50:
                                        print "attack " + Cluster_name + "(" + str(Cluster_point) + ")" + " Your chance is " + \
                                              scan_cluster["ddoschance"][0] + "%"
                                        result = json.loads(self.c.AttackCluster(Cluster_name))
                                        os.remove(self.database)
                                        if result['result'] == 6:
                                            pass
                                        else:
                                            break
                    else:
                        # Analyse Cluster in tournament
                        db = sqlite3.connect(self.database)
                        cursor = db.cursor()

                        try:
                            cursor.execute("""CREATE TABLE Cluster (ID TEXT, cluster_name TEXT, cluster_point TEXT) """)
                        except sqlite3.OperationalError:
                            pass

                        count = 0
                        data = []
                        point = {}
                        nb = len(TournamentPosition['data'])
                        for i in range(1, nb):
                            getCluster = TournamentPosition['data'][i]['user'].split("|")
                            data.append(getCluster[0])
                            point[getCluster[0].strip()] = point.get(getCluster[0].strip(), 0) + i

                        data2 = {}
                        for i in data:
                            data2[str(i.encode("utf-8")).strip()] = int(data.count(i))
                        newA = sorted(data2.iteritems(), key=operator.itemgetter(1), reverse=True)[0:nb]

                        print "best list for tournament :"
                        final_data = {}
                        for i in range(0, len(newA)):
                            Cluster_name = newA[i][0]
                            Cluster_pepole = newA[i][1]
                            print " cluster : " + Cluster_name.decode("utf-8") + " | people on cluster : " + str(
                                Cluster_pepole) + " | Points in clusters = " + str(
                                point[Cluster_name.decode("utf-8")] / Cluster_pepole)
                            final_data[Cluster_name.decode("utf-8")] = int(point[Cluster_name.decode("utf-8")] * Cluster_pepole)

                        newA = sorted(final_data.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(newA)]
                        for i in range(0, len(newA)):
                            Cluster_name = newA[i][0]
                            Cluster_point = newA[i][1]
                            if Cluster_point < self.Max_point_tournament:
                                # try:
                                #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                                # except UnicodeEncodeError:
                                #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))

                                count = count + 1
                                print "if attack " + Cluster_name + "(" + str(Cluster_point) + ")"
                                Cluster = [(0, Cluster_name, str(Cluster_point))]
                                cursor.executemany("INSERT INTO Cluster VALUES (?,?,?)", Cluster)
                                self.b.commit()
                        else:
                            count = 0
                            for i in range(0, len(newA)):
                                Cluster_name = newA[i][0]
                                Cluster_point = newA[i][1]
                                if Cluster_point < self.Max_point_tournament and count < 5:
                                    # try:
                                    #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                                    # except UnicodeEncodeError:
                                    #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))

                                    count = count + 1
                                    print "if attack " + Cluster_name + "(" + str(Cluster_point) + ")"
                                    Cluster = [(0, Cluster_name, str(Cluster_point))]
                                    cursor.executemany("INSERT INTO Cluster VALUES (?,?,?)", Cluster)
                                    self.b.commit()
                            time.sleep(5)


                except KeyError:
                    # attack cluster for not in tournament
                    tournament_next = re.findall('\d+', TournamentPosition['nexttournament'])
                    try:
                        tournament_hour = tournament_next[0]
                        tournament_minute = tournament_next[1]
                    except IndexError:
                        tournament_hour = 0
                        try:
                            tournament_minute = tournament_next[0]
                        except:
                            tournament_minute = 0

                    if int(tournament_hour) > 4:
                        data = []
                        point = {}
                        nb = len(TournamentPosition['data'])
                        for i in range(1, nb):
                            getCluster = TournamentPosition['data'][i]['user'].split("|")
                            data.append(getCluster[0])
                            point[getCluster[0].strip()] = point.get(getCluster[0].strip(), 0) + i

                        data2 = {}
                        for i in data:
                            data2[str(i.encode("utf-8")).strip()] = int(data.count(i))
                        newA = sorted(data2.iteritems(), key=operator.itemgetter(1), reverse=True)[0:nb]

                        print "best list for tournament :"
                        final_data = {}
                        for i in range(0, len(newA)):
                            Cluster_name = newA[i][0]
                            Cluster_pepole = newA[i][1]
                            # print " cluster : "+ Cluster_name.decode("utf-8") + " people on cluster : " + str(Cluster_pepole)  + " Points in clusters = " + str(point[Cluster_name.decode("utf-8")]/Cluster_pepole)
                            final_data[Cluster_name.decode("utf-8")] = int(point[Cluster_name.decode("utf-8")] * Cluster_pepole)

                        newA = sorted(final_data.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(newA)]
                        for i in range(0, len(newA)):
                            Cluster_name = newA[i][0]
                            Cluster_point = newA[i][1]
                            if Cluster_point < self.Max_point_tournament:
                                checkcluster = json.loads(self.c.check_Cluster())
                                test = "no"
                                if "DDoS not ready" in checkcluster["ddosready"] and test == "no":
                                    print checkcluster["ddosready"]
                                    break
                                else:
                                    try:
                                        scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                                    except UnicodeEncodeError:
                                        scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))
                                    if scan_cluster["result"] == "0":
                                        scan_cluster["ddoschance"] = scan_cluster["ddoschance"].split("%")
                                        ddoschance = re.findall('\d+', scan_cluster["ddoschance"][0])
                                        if int(ddoschance[0]) > 50:
                                            print "attack " + Cluster_name + "(" + str(
                                                Cluster_point) + ")" + " Your chance is " + scan_cluster["ddoschance"][0] + "%"
                                            result = json.loads(self.c.AttackCluster(Cluster_name))
                                            if result['result'] == 6:
                                                pass
                                            else:
                                                break
                                        else:
                                            print "no attack possible to " + Cluster_name + " (" + str(
                                                Cluster_point) + ")" + " Your chance is " + scan_cluster["ddoschance"][0] + "%"
                    else:
                        print "next tournament in " + TournamentPosition['nexttournament']

            global change
            change = False
            if self.BotNet_update:
                money = json.loads(self.c.myinfo())
                json_data = json.loads(self.u.botnetInfo())
                print "analysing configuration... botnet"
                for i in range(0, int(json_data['count'])):
                    moneycheck = True
                    ireal = i + 1
                    # json_data = json.loads(self.u.botnetInfo())
                    # money = json.loads(self.c.myinfo())
                    if json_data['data'][i]['bLVL'] == 100:
                        break
                    elif change == True:
                        json_data = json.loads(self.u.botnetInfo())
                        money = json.loads(self.c.myinfo())
                    while int(json_data['data'][i]['bLVL']) is not 100 and moneycheck == True:
                        if int(json_data['data'][i]['bPRICE']) < int(money['money']):
                            print "Updating Botnet " + str(ireal) + " level : " + str(int(json_data['data'][i]['bLVL']) + 1)
                            self.u.upgradeBotnet(str(ireal))
                            json_data = json.loads(self.u.botnetInfo())
                            money = json.loads(self.c.myinfo())
                            change = True
                        else:
                            print "No money to update Botnet #" + str(ireal)
                            moneycheck = False
                            change = False
                            break

            attackneeded = False
            Tournament = False
            if self.joinTournament == True:
                if self.c.getTournament():
                    Tournament = True
                    attackneeded = True
                    if self.tournament_potator:
                        mode = "Potator"
                        print "** Force Mode to 'Potator' for Tournament **"
                        stat = 1

            stat = "0"
            while "0" in stat and attackneeded == False:

                stat = self.u.startTask(self.updates[self.updatecount])
                if "0" in stat:
                    print "updating " + self.updates[self.updatecount] + " level +1"
                    # print "Started Update
                    print "Waiting... in update"
                    # self.u.useBooster()
                    time.sleep(wait_load)
                    self.updatecount += 1
                    if self.updatecount == 14:
                        while self.updatecount > 0:
                            print(self.u.getTasks())
                        # self.u.useBooster()

                        if self.updatecount:
                            pass
                        # self.u.finishAll()

                    if self.updatecount >= len(self.updates):
                        self.updatecount = 0

                elif "1" in stat:
                    attackneeded = True

            if attackneeded == False and self.booster == True:
                try:
                    usebooster = self.u.getTasks()
                    json_data = json.loads(usebooster)
                except ValueError:
                    print "Connection Error try again..."
                    pass
                except TypeError:
                    print "Connection Error try again..."
                    pass
                try:
                    while len(json_data["data"]) > 1:
                        if int(json_data["boost"]) > 5:
                            self.u.useBooster()
                            print "Using booster on rest " + str(int(json_data["boost"]) - 1)
                        # UPDATE Value
                        else:
                            print "you have < 5 boost."
                            break
                        usebooster = self.u.getTasks()
                        json_data = json.loads(usebooster)
                except KeyError:
                    pass
                except TypeError:
                    pass

            if attackneeded == False and self.Use_netcoins == True:
                myinfo = self.c.myinfo()
                time.sleep(2)
                json_data = json.loads(myinfo)
                try:
                    if json_data['netcoins'] > 1:
                        self.u.finishAll()
                        print "I used Netcoins for finish all task."
                except TypeError as e:
                    i = 0
                    while i <= 10:
                        print "Blocked, trying again. Delaying {0} seconds".format(i)
                        time.sleep(i)
                        i += 1
                    else:
                        exit(0)

            if self.b.attackable():
                print "Attacking with Botnet"
                attackbot = self.b.attackall()
                print attackbot
                attackneeded = True
                print "Waiting... in normal " + str(wait_load) + "s"
            attackneeded = True

            if attackneeded and Tournament == False:
                self.c.attack(self.attacks_normal, self.maxanti_normal, wait_load, mode, self.active_cluster_protection)
                attackneeded = False
                wait_load = round(uniform(0, 1), 2)

r = run()
