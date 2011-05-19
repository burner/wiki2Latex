#!/usr/bin/python
import urllib.request, urllib.error
import re
import sys
import subprocess

wikibook = ["http://en.wikibooks.org/w/index.php?title=","&action=edit"]
wikipedia = ["http://en.wikipedia.org/w/index.php?title=","&action=edit"]
wikifile = "http://en.wikipedia.org/wiki/File:"

def download(url, page):
	save = []
	user_agent ="Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" 
	head={'User-Agent':user_agent,}
	
	r = urllib.request.Request(url[0] + page + url[1])
	r.add_header("User-Agent", user_agent)
	s = urllib.request.urlopen(r)

	good = False

	for line in s:
		jine = line.decode('utf-8')
		it = jine.find("name=\"wpTextbox1\">")
		if it != -1:
			save.append(jine[it+len("name=\"wpTextbox1\">"):])
			good = True
	
		it = jine.find("</textarea><div id=\"editpage-copywarn\">")
		if it != -1:
			save.append(jine[:it])
			good = False
	
		if good:
			save.append(jine)

	return save

def replaceHtml(line):
	while -1 != line.find(r"&lt;"):
		line = re.sub(r"&lt;", '<', line)
	while -1 != line.find(r"&gt;"):
		line = re.sub(r"&gt;", '>', line)
	while -1 != line.find(r"&amp;"):
		line = re.sub(r"&amp;", '&', line)
	while -1 != line.find(r"&quot;"):
		line = re.sub(r"&quot;", '&', line)
	while -1 != line.find(r"&nbsp;"):
		line = re.sub(r"&nbsp;", '&', line)
	return line

def makeName(name):
	ret = ""
	for x in name:
		if x != '/':
			ret += x
	return ret.lower()

def makeUnderScore(name):
	ret = ""
	for x in name:
		if x == ' ':
			ret += '_'
		else:
			ret += x
	return ret

def removeStickImage(line):
	#print(line)
	it = line.find(".png")
	if it == -1:
		it = line.find(".PNG")
	if it == -1:
		it = line.find(".jpg")
	if it == -1:
		it = line.find(".JPG")
	if it == -1:
		it = line.find(".svg")
	if it == -1:
		it = line.find(".SVG")
	if it == -1:
		return line

	return line[:it+4]

def getImagesFile(line):
	ret = []
	it = 0
	it = line[it:].find("[[File:")
	while it != -1:
		jt = line[it:].find("]]") + it
		s = makeUnderScore(line[it+len("[[File:"):jt])
		r = removeStickImage(s)
		ret.append(r)
		it = line[jt+len("]]"):].find("[[File:")

	return ret

def getImagesImage(line):
	ret = []
	it = 0
	it = line[it:].find("[[Image:")
	while it != -1:
		jt = line[it:].find("]]") + it
		s = makeUnderScore(line[it+len("[[Image:"):jt])
		r = removeStickImage(s)
		ret.append(r)
		it = line[jt+len("]]"):].find("[[Image:")

	return ret

def getImages(line):
	ret = []
	s = getImagesFile(line)
	r = getImagesImage(line)
	for i in s:
		ret.append(i)
	for i in r:
		ret.append(s)
	print("\n\n","images",ret,line.find("[[File:"),line.find("[[Image:"),"\n\n")
	return ret

def checkIfPureLink(line):
	it = line.find(":")
	if it != -1:
		return None
	else:
		jt = line.find("|")
		if jt == -1:
			return line
		else:
			return line[:jt]

def getLinks(line):
	ret = []
	it = 0
	it = line[it:].find("[[")
	while it != -1: 
		jt = line[it+len("[["):].find("]]") + it + len("[[")
		s = makeUnderScore(line[it+len("[["):jt])
		r = checkIfPureLink(s)
		if r is not None:
			ret.append(r)
		it = line[jt+len("]]"):].find("[[") 
		if it == -1:
			break
		it += jt + len("]]")

	return ret

def setVar():
	global childs
	global images
	global blacklist

def askUser(links, depth, childs, blacklist):
	for x in links:
		if blacklist.get(x) is not None:
			continue
		if childs.get(x) is not None:
			continue

		print("Follow not" ,x)
		i = sys.stdin.readline()
		if -1 != i.find("y") or -1 != i.find("yes"):
			childs[x] = depth
		else:
			blacklist[x] = "do not search again"
			continue

def downloadImages(images, url):
	print("download Images")
	for i in images:	
		user_agent ="Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" 
		head={'User-Agent':user_agent,}
		r = urllib.request.Request(url + i)
		print(url + i)
		r.add_header("User-Agent", user_agent)
		s = urllib.request.urlopen(r)
		for line in s:
			jine = line.decode('utf-8')
			it = jine.find("fullImageLink")
			if it == -1:
				continue
			jt = jine.find("href=\"", it)
			kt = jine.find("\">", jt)
			downloadurl = jine[jt+len("href=\""):kt]
			print(downloadurl)
			subprocess.Popen("wget "+downloadurl, shell=True)
			

if __name__ == "__main__":
	childs = {}
	blacklist = {}
	images = []

	#start = "Data_structure"
	start = "cathedral"
	depth = 0

	childs[start] = depth	
	
	while len(childs) > 0:
		name = childs.popitem()
		s = download(wikipedia, name[0])
		f = open(makeName(name[0]), "w")
		for i in s:
			f.write(replaceHtml(i))
			img = getImages(i)
			if img is not None:
				print("another found")
				images.extend(img)
			else:
				print("another empty")
			#print(i)
			if name[1] > 0:
				askUser(getLinks(i), name[1]-1, childs, blacklist)
				print("all childs",childs)
				print("all black",blacklist)

		#print(childs)
		f.close()

	print("images",images)
	downloadImages(images, wikifile)

