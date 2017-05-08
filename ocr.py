from PIL import Image
from io import BytesIO
import base64
import sys
import difflib

class OCR:
	def analyze(self, im):
		#im = Image.open(name)
		pix = im.load()

		l = []
		for i1 in range(0,im.size[0]):
			count = 0
			for i2 in range (0, im.size[1]):
				if pix[i1,i2] != 0:
					count += 1
			l.append(count)
		return l

	def splitnumbers(self, l):
		nrs = []
		i1 = 0
		while i1 < len(l):
			if l[i1] > 3:
				temp = []
				add = 0
				for i2 in range(0,9):
					if not l[i1+i2] < 4:
						temp.append(l[i1+i2])
					else:
						add = i2
						break
				if add == 0:
					add = 8
				i1 += add
				nrs.append(temp)
			i1 += 1
		return nrs

	def readit(self, l):
		nrs = []
		for i1 in l:
			ratio = 0.0
			current = 0
			for i2 in range(0,len(self.nrlist)):
				sm = difflib.SequenceMatcher(None,i1,self.nrlist[i2])
				trat = sm.ratio()
				if trat > ratio:
					ratio = trat
					current = i2
			nrs.append(current)
		return nrs
				
	def rightSolution(self, nr, possies):
		current = 0
		ratio = 0.0
		for i1 in range(0,len(possies)):
			temp = []
			for i2 in possies[i1]:
				temp.append(int(i2))
			sm = difflib.SequenceMatcher(None,nr,temp)
			trat = sm.ratio()
			if trat > ratio:
				ratio = trat
				current = i1
		return "p" + str(current + 1)

	def base64toImage(self, string):
		im = Image.open(BytesIO(base64.b64decode(string)))
		return im			

	def getSolution(self, response):
		try:
			string = response.split(',')[0].split('{"img":"')[1].split('"')[0]
		except IndexError:
			return False
		possies = []
		for i1 in range(1,7):
			possies.append(response.split(',')[i1].split(':')[1])
		im = self.base64toImage(string)
		l = self.analyze(im)
		l = self.splitnumbers(l)
		l = self.readit(l)
		s = self.rightSolution(l, possies)
		return s

	def __init__(self):
		self.nrlist = [[13,14,15,8,6,7,15,15,12],[4,4,15,15,15],[9,12,13,11,14,14,13,9],[7,9,9,10,10,15,15,14],[5,8,8,11,10,12,15,15],[12,12,11,9,9,13,13,12],[13,15,10,9,9,12,14,11],[4,11,13,15,9,6,4],[14,15,12,9,10,15,15,14],[10,13,14,10,11,15,15,14]]