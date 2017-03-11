#!/usr/bin/python2.7
#-*- coding: utf-8 

from classes import API
from classes import IP
from classes import Passwords
from utils import Utils
from ocr import OCR
import time
import json
import subprocess
from PIL import Image
import base64
import pytesseract
import cStringIO
import requests
import re
import concurrent.futures
from random import randint
import sys
import signal

original_sigint = None

class Console:
	def myinfo(self):
		ut = Utils()
		temp = ut.requestStringNoWait("user::::pass::::gcm::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "eW7lxzLY9bE:APA91bEO2sZd6aibQerL3Uy-wSp3gM7zLs93Xwoj4zIhnyNO8FLyfcODkIRC1dc7kkDymiWxy_dTQ-bXxUUPIhN6jCUBVvGqoNXkeHhRvEtqAtFuYJbknovB_0gItoXiTev7Lc5LJgP2" + "::::" + "userHash_not_needed", "vh_update.php")
		return temp

	def requestPassword(self,ip):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_vulnScan.php")
		imgs = Passwords(arr)
		return imgs

	def enterPassword(self, passwd, target, uhash):
		passwd = passwd.split("p")
		ut = Utils()
		temp = ut.requestStringNoWait("user::::pass::::port::::target::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(passwd[1].strip()) + "::::" +  str(target) + "::::" + str(uhash), "vh_trTransfer.php")
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
		s = ut.requestStringNoWait("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_spywareUpload.php")
		if s == "0":
			return True
		else:
			return False 

	def getTournament(self):
		ut = Utils()
		temp = ut.requestStringNoWait("user::::pass::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "UserHash_not_needed", "vh_update.php")
		if "tournamentActive" in temp:
			if not "2" in temp.split('tournamentActive":"')[1].split('"')[0]:
				return True
			else:
				return False
	
	def returncrawler(self, lineexec):
		print lineexec.result()

	def calc_img(self, ut, imgstring, uhash, hostname, max, mode):
		ut = Utils()
		pic = cStringIO.StringIO()
		image_string = cStringIO.StringIO(base64.b64decode(imgstring))
		image = Image.open(image_string)

		# Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
		#bg = Image.new("RGB", image.size, (255,255,255))
		#bg.paste(image,image)
		if "Hatched by the FBI" in pytesseract.image_to_string(image) or "Watched by the FBI" in pytesseract.image_to_string(image):
			return 1, hostname
		else:
			temp = ut.requestStringNoWait("user::::pass::::uhash::::hostname", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + str(hostname), "vh_scanHost.php")
			try:
				jsons = json.loads(temp)
				#print jsons
				if not ".vHack.cc" in str(jsons['ipaddress']) and int(jsons['vuln']) == 1:
					time.sleep(1)
					executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
					livexec = executor.submit(self.attackIP, jsons['ipaddress'], max, mode)
					return livexec.result(), jsons['ipaddress']

				#else:
				#	temp = ut.requestString("user::::pass::::uhash::::hostname", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + jsons['ipaddress'], "vh_scanHost.php")
				#	if not ".vHack.cc" in str(jsons['ipaddress']) and int(jsons['vuln']) == 1:
				#		time.sleep(1)
				#		self.attackIP(jsons['ipaddress'], max, mode)

			except TypeError:
				return 0, 0

	def getIP(self, blank, max, mode):
		ut = Utils()
		info = self.myinfo()
		try:
			info = json.loads(info)
			uhash = info['uhash']
		except TypeError:
			return False

		temp = ut.requestStringNoWait("user::::pass::::uhash::::by", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + str(randint(0,1)), "vh_getImg.php")
		jsons = json.loads(temp)
		list_image = []
		list_hostname = []

		for i in range(0, len(jsons["data"])):
			hostname = str(jsons["data"][i]["hostname"])
			imgstring = 'data: image/png;base64,'+jsons["data"][i]['img']
			imgstring = imgstring.split('base64,')[-1].strip()
			list_image.append(imgstring)
			list_hostname.append(hostname)
		
		white_list = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
			for i, image in enumerate(list_image):
				lineexec = executor.submit(self.calc_img, ut, image, uhash, list_hostname[i], max, mode)
				try:
					result, ip = lineexec.result()
				except:
					result = False
					pass
				if result == True:
					with open("database.txt", "a") as f:
						f.write(ip+"\n")
				time.sleep(1)



	def attackIP(self, ip, max, mode):
		ut = Utils()
		info = self.myinfo()
		info = json.loads(info)
		uhash = info['uhash']
		time.sleep(1)
		temp = ut.requestString("user::::pass::::uhash::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + ip, "vh_loadRemoteData.php")

		jsons = json.loads(temp)
		
		o = OCR() 
		imgs = o.getSolution(str(temp))
		if imgs != None:
			try:
				user = jsons['username']
				winchance = jsons['winchance']
			except TypeError:
				return False
			try:
				if winchance:
					fwlevel = jsons['fw']
					avlevel = jsons['av']
					spamlevel = jsons['spam']
					sdklevel = jsons['sdk']
					ipsplevel = jsons['sdk']
					money = jsons['money']
					saving = jsons['savings']
					anonymous = jsons['anonymous']
					username = jsons['username']
					winlo = jsons['winelo']
					winchance = jsons['winchance']
					spywarelevel = jsons['spyware']
				else:
					avlevel = "????"
					winchance = 0
					print "no scan username"
					return False

			except TypeError:
				fwlevel = jsons['fw']
				avlevel = jsons['av']
				spamlevel = jsons['spam']
				sdklevel = jsons['sdk']
				ipsplevel = jsons['sdk']
				money = jsons['money']
				saving = jsons['savings']
				anonymous = jsons['anonymous']
				username = jsons['username']
				winlo = jsons['winelo']
				winchance = jsons['winchance']
				spywarelevel = jsons['spyware']

			if type(winchance) == "str":
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
							if not "?" in str(money) and str(jsons['result']) == 0:
								print "\n[TargetIP: " + str(ip) +"]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: "+ str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
								return True
							else:
								print "\n[TargetIP: " + str(ip) + "]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: " + str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
								return True

						except KeyError:
							print "Bad attack"
							return False

						except ValueError as e:
							return True
					else:
						print "Password Wrong"
						return False
				else:
					print "winchance is poor: " + str(winchance)



			if not "?" in str(avlevel) and mode == "Secure":
				if int(avlevel) < max and int(winchance) > 75 and str(anonymous) == "YES":
					password = self.enterPassword(imgs, ip, uhash)
					jsons = json.loads(password)
					if password:
						try:
							if not "?" in str(money) and str(jsons['result']) == 0:
								print "\n[TargetIP: " + str(ip) +"]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: "+ str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
								return True
							else:
								print "\n[TargetIP: " + str(ip) + "]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: " + str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
						except KeyError:
							print "Bad attack"
							return False
					else:
						print "Password Wrong"
						return False
				else:
					#print "\n"
					if int(avlevel) > max:
						print "Antivir to high " + str(avlevel)
						#print "passed"
						return False
					if int(winchance) < 75:
						print "winchance is poor: " + str(winchance)
						#print "passed"
						return False
					if str(anonymous) == "NO":
						print "No Anonymous need"
						#print "passed"
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

	def attackIP2(self,ip,max):	
		ut = Utils()
		o = OCR(False)
		imgs = self.requestPassword(ip)
		selection = o.getPassword(imgs)
		print selection

	def attack(self, amount, max, wait, mode):
		for i in range(0, (amount*6)):
			data = self.getIP(True, max, mode)
			print "wait anti-blocking..."
			time.sleep(5)

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

	def __init__(self,api):
		global original_sigint
		self.api = api
		original_sigint = signal.getsignal(signal.SIGINT)
		signal.signal(signal.SIGINT, self.exit_gracefully)
