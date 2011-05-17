#!/usr/bin/python

import urllib.request, urllib.error

user_agent ="Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" 
head={'User-Agent':user_agent,}
page = "LaTeX/Tables"
url = "http://en.wikibooks.org/w/index.php?title=" + page + "&action=edit"
print(url)

r = urllib.request.Request(url)
r.add_header("User-Agent", user_agent)
s = urllib.request.urlopen(r)

for i in s:
	print(i)
