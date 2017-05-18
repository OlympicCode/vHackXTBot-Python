#!/usr/bin/python2.7
# -*- coding: utf-8

from console import Console
from update import Update
from botnet import Botnet
from random import randrange, uniform
import time
import json
import config
import ddos


class run:

    def __init__(self):
        """
        Pull all variables from config.py file.
        """
        self.username = config.user
        self.password = config.password
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
        self.active_cluster_protection = config.active_cluster_protection
        self.mode = config.mode
        self.wait_load = config.wait_load
        self.c = Console(self.username, self.password)
        self.u = Update(self.username, self.password)
        self.b = Botnet(self.username, self.password)
        self.ddos = ddos.Ddos()

        self.init()

    def init(self):
        while True:
            self.ddos.run_ddos()
            if self.BotNet_update:
                self.b.update()
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
                    time.sleep(self.wait_load)
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

            if not attackneeded and self.booster:
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
            # attack botnet
            self.b.attack()
            attackneeded = True

            if attackneeded and Tournament is False:
                self.c.attack(self.attacks_normal, self.maxanti_normal, self.wait_load, self.mode, self.active_cluster_protection)
                attackneeded = False
                wait_load = round(uniform(0, 1), 2)

r = run()
