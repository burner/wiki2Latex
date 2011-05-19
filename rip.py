#!/usr/bin/python
import urllib.request, urllib.error
import re

wikibook = ["http://en.wikibooks.org/w/index.php?title=","&action=edit"]
wikipedia = ["http://en.wikipedia.org/w/index.php?title=","&action=edit"]

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
		it = line.find(".jpg")
	if it == -1:
		it = line.find(".svg")
	if it == -1:
		return line

	return line[:it+4]

def getImages(line):
	ret = []
	it = 0
	it = line[it:].find("[[Image:")
	while it != -1:
		#print(line)
		jt = line[it:].find("]]") + it
		print(line[it+len("[[Image:"):jt])
		s = makeUnderScore(line[it+len("[[Image:"):jt])
		r = removeStickImage(s)
		print(s)
		print(r)
		print(len(line), it, jt)
		ret.append(r)
		it = line[jt+len("]]"):].find("[[Image:")

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
		print(it,jt,line[it+len("[["):jt])
		#print(line)
		s = makeUnderScore(line[it+len("[["):jt])
		r = checkIfPureLink(s)
		if r is not None:
			print(s, r)
			ret.append(r)
		it = line[jt+len("]]"):].find("[[") 
		if it == -1:
			break
		it += jt + len("]]")

	return ret


if __name__ == "__main__":
	#name = "LaTeX/Tables"
	name = "Data_structure"
	s = download(wikipedia, name)

	images = []
	links = []
	
	f = open(makeName(name), "w")
	cnt = 0
	for i in s:
		f.write(replaceHtml(i))
		#for j in getImages(i):
		#	images.append(j)
		for j in getLinks(i):
			links.append(j)
		cnt+=1

	f.close()

	#print(images)
	print(links)
