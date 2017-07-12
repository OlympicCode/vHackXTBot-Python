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
from player import Player

class run:

    def __init__(self):
        """
        Pull all variables from config.py file.
        """
        self.player = Player()
        self.database = config.database
        self.Max_point_tournament = config.Max_point_tournament
        self.BotNet_update = config.BotNet_update
        self.joinTournament = config.joinTournament
        self.tournament_potator = config.tournament_potator
        self.booster = config.booster
        self.Use_netcoins = config.Use_netcoins
        self.attacks_normal = config.attacks_normal
        self.updates = config.updates
        self.updatecount = config.updatecount
        self.maxanti_normal = config.maxanti_normal
        self.active_cluster_protection = config.active_cluster_protection
        self.mode = config.mode
        self.stat = "0"
        self.wait_load = config.wait_load
        self.c = Console(self.player.username, self.player.password)
        self.u = Update(self.player.username, self.player.password)
        self.b = Botnet(self.player)
        self.ddos = ddos.Ddos()
        self.init()

    def init(self):

        self.get_max_update = int(self.u.infoUpdate("ram", "new"))
        while True:

            stat = "0"
            # prepare account 
            self.running_all = self.u.runningtasks()
            print("your are running " + str(self.running_all) + "/" + str(self.get_max_update) + " tasks")

            if int(self.running_all) < int(self.get_max_update):
                while "0" in stat or "3" in stat:

                    try:
                        moneyforupdate = int(self.u.infoUpdate(self.updates[self.updatecount]))
                    except IndexError:
                        self.updatecount = 0
                        moneyforupdate = int(self.u.infoUpdate(self.updates[self.updatecount]))
                        
                    mymoney = int(self.player.getmoney())
                    if mymoney < moneyforupdate:
                        self.updatecount += 1
                        time.sleep(self.wait_load)
                        print "require " + str(moneyforupdate) + "$ for update " + self.updates[self.updatecount] + " your money " + str(mymoney) + "$"
                        totaltask = int(self.running_all)+int(self.updatecount)
                        print(totaltask)
                        if int(totaltask) == int(self.get_max_update):
                            stat = "1"
                    else:
                        stat = self.u.startTask(self.updates[self.updatecount])
                        if "3" in stat:
                            print "updating " + self.updates[self.updatecount] + " level +1"
                            #print "Started Update
                            print "Waiting... in update"
                            #u.useBooster()
                            time.sleep(self.wait_load)
                            self.updatecount += 1
                            totaltask = int(self.running_all)+int(self.updatecount)
                            if int(totaltask) == int(self.get_max_update):
                                stat = "1"

            # recheck running ask for boost and netcoins
            self.running_all = self.u.runningtasks()

            self.ddos.run_ddos()
            if self.BotNet_update:
                self.b.upgradebotnet()
            # attack botnet
            self.b.attack()
            if self.joinTournament and self.c.getTournament():
                self.mode = "Potator"
                print "** Force Mode to 'Potator' for Tournament **"
            # task = self.u.doTasks(self.wait_load)
            if self.booster and self.running_all > 1:
                try:
                    # usebooster = self.u.getTasks()
                    usebooster = None
                    json_data = json.loads(usebooster)
                    while len(json_data["data"]) > 1:
                        if int(json_data["boost"]) > 5:
                            self.u.useBooster()
                            print "Using booster on rest " + str(int(json_data["boost"]) - 1)
                        # UPDATE Value
                        else:
                            print "you have < 5 boost."
                            break
                        # usebooster = self.u.getTasks()
                        usebooster = None
                        json_data = json.loads(usebooster)
                except Exception as e:
                    print "Connection Error try again...{0}".format(e)
                    pass
            if self.Use_netcoins:
                time.sleep(2)
                if self.player.netcoins > 1 and self.running_all > 1:
                    self.u.finishAll()
                    self.player.refreshinfo()  # update player info
                    print "I used Netcoins for finish all task."
            # attack players
            self.c.attack(self)

r = run()
