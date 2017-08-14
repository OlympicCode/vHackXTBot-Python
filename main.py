#!/usr/bin/python2.7
# -*- coding: utf-8

from console import Console
from update import Update
from botnet import Botnet
import time
import json
import config
import ddos
from player import Player
import logging
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s [%(threadName)10s][%(module)10s][%(levelname)8s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


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
        self.c = Console(self.player)
        self.u = Update(self.player)
        self.b = Botnet(self.player)
        self.ddos = ddos.Ddos(self.player)
        self.init()

    def init(self):
        while True:
            # update the player

            time.sleep(self.wait_load)
            stat = "0"
            # prepare account
            self.get_max_update = int(self.u.infoUpdate("ram", "new")) - 1
            self.running_all = self.u.runningtasks()
            logger.info("you are running {}/{} tasks".format(self.running_all, self.get_max_update))

            if int(self.running_all) < int(self.get_max_update):
                while "0" in stat or "3" in stat:
                    if int(self.u.runningtasks()) < int(self.u.infoUpdate("ram", "new")) - 1:
                        try:
                            moneyforupdate = int(self.u.infoUpdate(self.updates[self.updatecount]))
                        except IndexError:
                            logger.info("reset")
                            self.updatecount = 0
                            moneyforupdate = int(self.u.infoUpdate(self.updates[self.updatecount]))
                            stat = "1"
                        mymoney = int(json.loads(self.c.myinfo())["money"])

                        if mymoney < moneyforupdate:
                            self.updatecount += 1

                            try:
                                logger.info("require {}$ for update {} your money {}$".format(moneyforupdate, self.updates[self.updatecount], mymoney))
                            except IndexError:
                                stat = "1"

                            totaltask = int(self.u.runningtasks()) + int(self.updatecount)
                            if int(totaltask) == int(self.get_max_update):
                                stat = "1"
                        else:
                            stat = self.u.startTask(self.updates[self.updatecount])
                            if "3" in stat or "0" in stat:
                                logger.info("updating {} level +1".format(self.updates[self.updatecount]))
                                # print "Started Update
                                logger.info("Waiting... in update")
                                # u.useBooster()
                                self.updatecount += 1
                                totaltask = int(self.u.runningtasks()) + int(self.updatecount)
                                if int(totaltask) == int(self.get_max_update):
                                    stat = "1"
                    else:
                        break

            # recheck running ask for boost and netcoins
            self.running_all = self.u.runningtasks()

            self.ddos.run_ddos()
            if self.BotNet_update:
                self.b.upgradebotnet()
            # attack botnet
            self.b.attack()
            if self.joinTournament and self.c.getTournament():
                self.mode = "Potator"
                logger.info("** Force Mode to 'Potator' for Tournament **")
            # task = self.u.doTasks(self.wait_load)
            if self.booster and self.running_all > 1:
                try:
                    usebooster = self.u.getTasks()
                    logger.info(usebooster)
                    # usebooster = None
                    json_data = json.loads(usebooster)
                    while len(json_data["data"]) > 1:
                        if int(json_data["boost"]) > 5:
                            self.u.useBooster()
                            logger.info("Using booster on rest {}".format(json_data["boost"] - 1))
                        # UPDATE Value
                        else:
                            logger.info("you have < 5 boost.")
                            break
                        # usebooster = self.u.getTasks()
                        usebooster = None
                        json_data = json.loads(usebooster)
                except Exception as e:
                    logger.error("Connection Error try again...{0}".format(e))
                    pass
            if self.Use_netcoins:
                time.sleep(2)
                if self.player.netcoins > 1 and self.running_all > 1:
                    self.u.finishAll()
                    self.player.refreshinfo()  # update player info
                    logger.info("I used Netcoins for finish all task.")
            # attack players
            self.c.attack(self)


if __name__ == "__main__":
    r = run()
