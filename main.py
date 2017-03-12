#!/usr/bin/python2.7
#-*- coding: utf-8 

from classes import API
from classes import IP
from console import Console
from update import Update
from utils import Utils
from botnet import Botnet
from random import randrange, uniform
from collections import Counter 
import time
import json


# Enter username and password
api = API("username","password")
# Enter Max Antivir to attack in normal mode
maxanti_normal = 3000

# Use booster
booster = True

# Finish all task by netcoins
Use_netcoins = True

# Enter Max Antivir to attack tournament
maxanti_tournament = 3200

# Enter Amount of Attacks normal
attacks_normal = 3

# Enter Amount of Attacks in tournament
attacks_tournament = 2

# define the initiale mode
mode = "Secure"

# change auto mode Potator for tournament
tournament_potator = True

# Enter Updates (inet, hdd, cpu, ram, fw, av, sdk, ipsp, spam, scan, adw)
updates = ["ipsp", "adw", "fw", "scan", "sdk", "av"]
#updates = ["fw"]
#updates = ["ipsp",  "sdk"]
#Do you want to attack during tournament [True, False]
joinTournament = True
#Time to wait between each cycle in seconds
wait = round(uniform(0,1), 2)
wait_load = round(uniform(1,3), 2)


c = Console(api)
u = Update(api)
b = Botnet(api)
updatecount = 0
attackneeded = False

while True:
	attackneeded = False

	if joinTournament:
		if c.getTournament():
			attackneeded = True
			if tournament_potator:
				mode = "Potator"
				print "** Force Mode to 'Potator' for Tournament **"
				stat = 1

	stat = "0"
	while "0" in stat:

		stat = u.startTask(updates[updatecount])
		if "0" in stat:
			print "updating " + updates[updatecount] + " level +1"
			#print "Started Update
			print "Waiting... in update"
			#u.useBooster()
			time.sleep(wait_load)
			updatecount += 1
			if updatecount == 14:
				while updatecount > 0:
					print(u.getTasks())
					#u.useBooster()

				if updatecount: 
					pass
					#u.finishAll()

			if updatecount >= len(updates):
				updatecount = 0

		elif "1" in stat:
			attackneeded = True

	if attackneeded == False and booster == True:
		try:
			usebooster = u.getTasks()
			json_data = json.loads(usebooster)
		except ValueError:
			print "Connexion Error try again..."
			pass
		except TypeError:
			print "Connexion Error try again..."
			pass
		try:
			while len(json_data["data"]) > 1:
				if int(json_data["boost"]) > 5:
					u.useBooster()
					print "Use the booster in rest " + str(int(json_data["boost"])-1)
					# UPDATE Value
				else:
					print "you are < 5 boost."
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
				print "I'm use netcoins for finish all task."
		except TypeError as e:
			print "Error connexion... " + e

	if b.attackable():
		print "Attacking with Botnet"
		attackbot = b.attackall()
		print attackbot

	if attackneeded:
		c.attack(attacks_tournament, maxanti_tournament, wait, mode, api)
		wait = round(uniform(0,1), 2)

	else:
		print "Waiting... in normal " + str(wait_load) + "s"
		attackneeded = True

		if attackneeded:
			c.attack(attacks_normal, maxanti_normal, wait_load, mode, api)
			attackneeded = False
		wait_load = round(uniform(1,3), 2)
