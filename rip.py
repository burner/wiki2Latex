#!/usr/bin/python
import urllib.request, urllib.error
import re
import sys
import subprocess
import os

wikibook = ["http://en.wikibooks.org/w/index.php?title=","&action=edit"]
wikipedia = ["http://en.wikipedia.org/w/index.php?title=","&action=edit"]
wikifile = "http://en.wikipedia.org/wiki/File:"

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def download(url, page):
	save = []
	user_agent ="Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" 
	head={'User-Agent':user_agent,}

	if not is_ascii(page):
		return
	
	r = urllib.request.Request(url[0] + page + url[1])
	print(url[0] +page+url[1])
	r.add_header("User-Agent", user_agent)
	s = urllib.request.urlopen(r)

	good = False

	for line in s:
		jine = line.decode('utf-8')
		it = jine.find("name=\"wpTextbox1\"")
		if it != -1:
			save.append(jine[it+len("name=\"wpTextbox1\""):])
			good = True
	
		it = jine.find("</textarea>")
		if it != -1:
			save.append(jine[:it])
			good = False
	
		if good:
			save.append(jine)

	print("len save", len(save))
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
	cnt = 0
	while it != -1 and cnt < 5:
		jt = line[it:].find("]]",it)
		print(it,jt,line)
		s = makeUnderScore(line[it+len("[[File:"):jt])
		r = removeStickImage(s)
		if r not in ret:
			ret.append(r)
		it = line[jt+len("]]"):].find("[[File:")
		cnt+=1

	return ret

def getImagesImage(line):
	ret = []
	it = 0
	it = line[it:].find("[[Image:")
	cnt = 0
	while it != -1 and cnt < 5:
		jt = line[it:].find("]]") + it
		s = makeUnderScore(line[it+len("[[Image:"):jt])
		r = removeStickImage(s)
		if r not in ret:
			ret.append(r)
		it = line[jt+len("]]"):].find("[[Image:")
		cnt+=1

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

def askUser(links, depth, childs, blacklist,cur):
	for x in links:
		if blacklist.get(x) is not None:
			continue
		if childs.get(x) is not None:
			continue

		#print("Follow not" ,x)
		#i = sys.stdin.readline()
		#if -1 != i.find("y") or -1 != i.find("yes"):
		childs[x] = depth
		#else:
		#	blacklist[x] = "do not search again"
		#	continue

def downloadImages(images, url):
	print("download Images")
	for i in images:	
		if not isinstance(i, str):
			continue
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
	start = "Mathematics"
	depth = 1

	childs[start] = depth	
	os.mkdir(start)
	os.chdir(start)
	
	while len(childs) > 0:
		name = childs.popitem()
		blacklist[name] = 0
		print("ripping",name[0])
		s = download(wikipedia, name[0])
		f = open(makeName(name[0]) + ".w", "w")
		if s is None:
			continue
		for i in s:
			rp = replaceHtml(i)
			f.write(rp)
			img = getImages(rp)
			if img is not None:
				images.extend(img)
			#print(i)
			if name[1] > 0:
				askUser(getLinks(rp), name[1]-1, childs, blacklist, name[0])

		print("childs ", len(childs), "blacklist ", len(blacklist))


		#print(childs)
		f.close()

	print("images",len(images),images)
	downloadImages(images, wikifile)
