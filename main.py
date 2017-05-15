#!/usr/bin/python2.7
# -*- coding: utf-8

from classes import API
from classes import IP
from console import Console
from update import Update
from utils import Utils
from botnet import Botnet
from random import randrange, uniform
from collections import Counter
from bs4 import BeautifulSoup
import operator
import requests
import time
import json
import re
import warnings
import sqlite3
import os

# Enter username and password
api = API("username", "password")
# Enter Max Antivir to attack in normal mode
maxanti_normal = 500

# Active or not the protection for cluster
active_cluster_protection = True

# Use booster
booster = False

# Finish all task by netcoins
Use_netcoins = True

# Enter Max Antivir to attack tournament
maxanti_tournament = 500

# Enter Amount of Attacks normal
attacks_normal = 3

# Enter Amount of Attacks in tournament
attacks_tournament = 2

# define the initiale mode
mode = "Secure"

BotNet_update = False

ddos_cluster = False

# change auto mode Potator for tournament
tournament_potator = True

AttackTournamentDB = False
Max_point_tournament = 1300
# Enter Updates (inet, hdd, cpu, ram, fw, av, sdk, ipsp, spam, scan, adw)
updates = ["ipsp", "adw", "fw", "scan", "sdk", "av"]
# updates = ["fw"]
# updates = ["ipsp",  "sdk"]
# Do you want to attack during tournament [True, False]
joinTournament = False
# Time to wait between each cycle in seconds
wait = round(uniform(0, 1), 2)
wait_load = round(uniform(1, 3), 2)

c = Console(api)
u = Update(api)
b = Botnet(api)
updatecount = 0
attackneeded = False

"""	if int(json_data['data'][i]['bLVL']) < 100:
		for a in range(1, 100-int(json_data['data'][i]['bLVL'])):
			json_data = json.loads(u.botnetInfo())
			if int(json_data['data'][i]['bPRICE']) < int(money['money']):
				print "Update Botnet " + str(i) + " level : " + str(int(json_data['data'][a]['bLVL'])+1)
				u.upgradeBotnet(str(i))
			else:
				print "No money for update Botnet"
				break
	else:
		break"""

while True:
    if ddos_cluster:
        checkcluster = json.loads(c.check_Cluster())
        TournamentPosition = json.loads(c.GetTournamentPosition())
        try:
            # determine and attack cluster tournament
            db = sqlite3.connect("database.db")
            cursor = db.cursor()

            try:
                cursor.execute("""CREATE TABLE Cluster (ID TEXT, cluster_name TEXT, cluster_point TEXT) """)
            except sqlite3.OperationalError:
                pass

            tournament_left = re.findall('\d+', TournamentPosition["tleft"])
            print "Tournament star finish in " + str(TournamentPosition["tleft"])
            try:
                tournament_heure = tournament_left[0]
                tournament_minute = tournament_left[1]
            except IndexError:
                tournament_heure = 0
                try:
                    tournament_minute = tournament_left[0]
                except IndexError:
                    tournament_minute = 0

            if int(tournament_heure) == 0 and int(tournament_minute) < 60:

                cluster_name = {}
                for row in cursor.execute(
                        "SELECT * FROM (SELECT cluster_point, cluster_name FROM Cluster ORDER BY cluster_point ASC)"):
                    cluster_name[row[0]] = row[1]

                newA = sorted(cluster_name.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(cluster_name)]

                for i in range(0, len(newA)):
                    Cluster_name = newA[i][1]
                    Cluster_point = newA[i][0]

                    checkcluster = json.loads(c.check_Cluster())
                    if "DDoS not ready" in checkcluster["ddosready"]:
                        print checkcluster["ddosready"]
                        break
                    else:
                        try:
                            scan_cluster = json.loads(c.ScanCluster(Cluster_name.decode("utf-8")))
                        except UnicodeEncodeError:
                            scan_cluster = json.loads(c.ScanCluster(Cluster_name.encode("utf-8")))

                        if scan_cluster["result"] == "0":
                            scan_cluster["ddoschance"] = scan_cluster["ddoschance"].split("%")
                            ddoschance = re.findall('\d+', scan_cluster["ddoschance"][0])
                            if int(ddoschance[0]) > 50:
                                print "attack " + Cluster_name + "(" + str(Cluster_point) + ")" + " Your chance is " + \
                                      scan_cluster["ddoschance"][0] + "%"
                                result = json.loads(c.AttackCluster(Cluster_name))
                                os.remove("database.db")
                                if result['result'] == 6:
                                    pass
                                else:
                                    break
            else:
                # Analyse Cluster in tournament
                db = sqlite3.connect("database.db")
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
                    if Cluster_point < Max_point_tournament:
                        # try:
                        #	scan_cluster = json.loads(c.ScanCluster(Cluster_name.decode("utf-8")))
                        # except UnicodeEncodeError:
                        #	scan_cluster = json.loads(c.ScanCluster(Cluster_name.encode("utf-8")))

                        count = count + 1
                        print "if attack " + Cluster_name + "(" + str(Cluster_point) + ")"
                        Cluster = [(0, Cluster_name, str(Cluster_point))]
                        cursor.executemany("INSERT INTO Cluster VALUES (?,?,?)", Cluster)
                        db.commit()
                else:
                    count = 0
                    for i in range(0, len(newA)):
                        Cluster_name = newA[i][0]
                        Cluster_point = newA[i][1]
                        if Cluster_point < Max_point_tournament and count < 5:
                            # try:
                            #	scan_cluster = json.loads(c.ScanCluster(Cluster_name.decode("utf-8")))
                            # except UnicodeEncodeError:
                            #	scan_cluster = json.loads(c.ScanCluster(Cluster_name.encode("utf-8")))

                            count = count + 1
                            print "if attack " + Cluster_name + "(" + str(Cluster_point) + ")"
                            Cluster = [(0, Cluster_name, str(Cluster_point))]
                            cursor.executemany("INSERT INTO Cluster VALUES (?,?,?)", Cluster)
                            db.commit()
                    time.sleep(5)


        except KeyError:
            # attack cluster for not in tournament
            tournament_next = re.findall('\d+', TournamentPosition['nexttournament'])
            try:
                tournament_heure = tournament_next[0]
                tournament_minute = tournament_next[1]
            except IndexError:
                tournament_heure = 0
                try:
                    tournament_minute = tournament_next[0]
                except:
                    tournament_minute = 0

            if int(tournament_heure) > 4:
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
                    if Cluster_point < Max_point_tournament:
                        checkcluster = json.loads(c.check_Cluster())
                        test = "no"
                        if "DDoS not ready" in checkcluster["ddosready"] and test == "no":
                            print checkcluster["ddosready"]
                            break
                        else:
                            try:
                                scan_cluster = json.loads(c.ScanCluster(Cluster_name.decode("utf-8")))
                            except UnicodeEncodeError:
                                scan_cluster = json.loads(c.ScanCluster(Cluster_name.encode("utf-8")))
                            if scan_cluster["result"] == "0":
                                scan_cluster["ddoschance"] = scan_cluster["ddoschance"].split("%")
                                ddoschance = re.findall('\d+', scan_cluster["ddoschance"][0])
                                if int(ddoschance[0]) > 50:
                                    print "attack " + Cluster_name + "(" + str(
                                        Cluster_point) + ")" + " Your chance is " + scan_cluster["ddoschance"][0] + "%"
                                    result = json.loads(c.AttackCluster(Cluster_name))
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
    if BotNet_update:
        money = json.loads(c.myinfo())
        json_data = json.loads(u.botnetInfo())
        print "analysing configuration... botnet"
        for i in range(0, int(json_data['count'])):
            moneycheck = True
            ireal = i + 1
            # json_data = json.loads(u.botnetInfo())
            # money = json.loads(c.myinfo())
            if json_data['data'][i]['bLVL'] == 100:
                break
            elif change == True:
                json_data = json.loads(u.botnetInfo())
                money = json.loads(c.myinfo())
            while int(json_data['data'][i]['bLVL']) is not 100 and moneycheck == True:
                if int(json_data['data'][i]['bPRICE']) < int(money['money']):
                    print "Updating Botnet " + str(ireal) + " level : " + str(int(json_data['data'][i]['bLVL']) + 1)
                    u.upgradeBotnet(str(ireal))
                    json_data = json.loads(u.botnetInfo())
                    money = json.loads(c.myinfo())
                    change = True
                else:
                    print "No money to update Botnet #" + str(ireal)
                    moneycheck = False
                    change = False
                    break

    attackneeded = False
    Tournament = False
    if joinTournament == True:
        if c.getTournament():
            Tournament = True
            attackneeded = True
            if tournament_potator:
                mode = "Potator"
                print "** Force Mode to 'Potator' for Tournament **"
                stat = 1

    stat = "0"
    while "0" in stat and attackneeded == False:

        stat = u.startTask(updates[updatecount])
        if "0" in stat:
            print "updating " + updates[updatecount] + " level +1"
            # print "Started Update
            print "Waiting... in update"
            # u.useBooster()
            time.sleep(wait_load)
            updatecount += 1
            if updatecount == 14:
                while updatecount > 0:
                    print(u.getTasks())
                # u.useBooster()

                if updatecount:
                    pass
                # u.finishAll()

            if updatecount >= len(updates):
                updatecount = 0

        elif "1" in stat:
            attackneeded = True

    if attackneeded == False and booster == True:
        try:
            usebooster = u.getTasks()
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
                    u.useBooster()
                    print "Using booster on rest " + str(int(json_data["boost"]) - 1)
                # UPDATE Value
                else:
                    print "you have < 5 boost."
                    break
                usebooster = u.getTasks()
                json_data = json.loads(usebooster)
        except KeyError:
            pass
        except TypeError:
            pass

    if attackneeded == False and Use_netcoins == True:
        myinfo = c.myinfo()
        time.sleep(2)
        json_data = json.loads(myinfo)
        try:
            if json_data['netcoins'] > 1:
                u.finishAll()
                print "I used Netcoins for finish all task."
        except TypeError as e:
            print "Error with connection... " + str(e)

    if b.attackable():
        print "Attacking with Botnet"
        attackbot = b.attackall()
        print attackbot

        attackneeded = True
        print "Waiting... in normal " + str(wait_load) + "s"
    attackneeded = True

    if attackneeded and Tournament == False:
        c.attack(attacks_normal, maxanti_normal, wait_load, mode, api, active_cluster_protection)
        attackneeded = False
        wait_load = round(uniform(0, 1), 2)
