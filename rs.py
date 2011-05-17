#!/usr/bin/python
import sys
import re

ifile = ""
mainfile = ""

oneWordSubs = {"<br>":"\\\\"}

subs = { "part":["=","=","\\section{","}"]
,"section":["==","==","\\section{","}"]
,"subsection":["===","===","\\subsection{","}"]
,"subsubsection":["====","====","\\subsubsection{","}"]
,"paragraph":["=====","=====","\\paragraph{","}"]
,"boitalic":["\'\'\'\'\'","\'\'\'\'\'","\\texttt{\\textit{","}}"]
,"bold":["\'\'\'","\'\'\'","\\texttt{","}"]
,"ttverb":["<tt>\\verb","</tt>","\\texttt{\\verb","}"]
,"tt":["<tt>","</tt>","\\texttt{","}"]
,"source":["<source>","</source>","\\begin{lstlisting}","\\end{lstlistin}"]
,"math":["<math>","</math>","$","$"]
,"ref":["[[","]]","\\nameref{","}"]
,"code":["<code>","</code>","\\verb|","|"]
,"italic":["\'\'","\'\'","\\textit{","}"]}

buf = []
verbatim = []
math = []
source = []
curly = []
idx = 0

def printBuf():
	global buf
	print("buffer begin")
	for i in buf:
		sys.stdout.write(i)
	print("buffer end")

def readFile():
	global buf
	for line in ifile:
		buf.append(line)	

def beginList(state):
	if state == 1:
		return "\\begin{itemize}\n"
	elif state == 2:
		return "\\begin{enumerate}\n"
	elif state == 3:
		return "\\begin{description}\n"

def endList(state):
	if state == 1:
		return "\\end{itemize}\n"
	elif state == 2:
		return "\\end{enumerate}\n"
	elif state == 3:
		return "\\end{description}\n"

def lists():
	global buf
	global idx
	state = 0 # 1 itemize, 2 enumerate, 3 description
	count = 0
	line = buf[idx]
	if line[0] == '*':
		state = 1
	elif line[0] == '#':
		state = 2
	else:
		return
	buf.insert(idx, beginList(state))
	idx+=1

	while line[0] == '*' or line[0] == '#':
		if line[1] != ' ':
			buf[idx] = "\\item " + line[1:]
		else:
			buf[idx] = "\\item" + line[1:]
		idx+=1
		if idx < len(buf):
			line = buf[idx]
		else:
			break

	if idx < len(buf):
		buf.insert(idx, endList(state))
	else:
		buf.append(endList(state))

def description():
	global buf
	global idx
	line = buf[idx]
	if line[0] == ';':
		buf.insert(idx, beginList(3))
	else:
		return

	idx+=1
	while line[0] == ';':
		tmp = "\\item[" + line[1:]
		it = tmp.find(' ')	
		tmp = tmp[:it] + "] " + tmp[it:]
		buf[idx] = tmp

		idx+=1
		if idx < len(buf):
			line = buf[idx]
		else:
			break

	if idx < len(buf):
		buf.insert(idx, endList(3))
	else:
		buf.append(endList(3))
		

def subtitute(toSubB, toSubE, toSubWithB, toSubWithE):
	global buf
	global idx
	#print(44, line)
	retLine = ""
	lowIdx = 2
	line = ""
	count = 0
	print("curline",buf[idx])
	while lowIdx != -1 and idx < len(buf):
		count += 1
		line = buf[idx]
		if line[:8] == "argsNoSub":
			return
		lowIdx = line.find(toSubB)
		if lowIdx != -1:
			print("found low: ", lowIdx)
			highIdx = line.find(toSubE, lowIdx+len(toSubB))
			print("ret : ", retLine)
			while highIdx == -1:
				line += buf[idx+1]
				del buf[idx+1]
				buf[idx] = line
				highIdx = line.find(toSubE, lowIdx+len(toSubB))
			print("ret : ", retLine)

			print("found high: ", highIdx)

			if lowIdx != 0:
				print("retT : ", line[0:lowIdx-1] + toSubWithB)
				retLine = line[0:lowIdx-1] + toSubWithB
			else:
				retLine = toSubWithB
			print("ret : ", retLine)
			retLine += line[lowIdx+len(toSubB):highIdx].strip()
			print("ret : ", retLine)
			retLine += toSubWithE
			print("ret : ", retLine)
			retLine += line[highIdx+len(toSubE):len(line)]
			print("ret : ", retLine)
			buf[idx] = retLine
			print("buf : ", buf[idx])
		else:
			break
	print("done ",count)

def removeVerbatim():
	global buf
	global verbatim
	global idx
	idx = 0
	vList = []
	while idx < len(buf):
		line = buf[idx]
		if line == "\\begin{verbatim}":
			vList.append(line)
			del buf[idx]
			line = buf[idx]
			while line != "\\end{verbatim}":
				vList.append(line)	
				del buf[idx]
				line = buf[idx]
			vList.append(line)	
			del buf[idx]
			buf.insert(idx, "argsNoSubVerbatim")
			verbatim.append(vList)
			vList = []
		else:
			idx+=1
	

def pre():
	global idx
	global buf
	'''
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line[1:].find('*')
		if it != -1:
			buf[idx] = line[:it] + "\n"
			buf.insert(idx+1, line[it:].strip()+ "\n")
		idx+=1

	print("pre 1")

	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line[1:].find('#')
		if it != -1:
			buf[idx] = line[:it] + "\n"
			buf.insert(idx+1, line[it:].strip()+ "\n")
		idx+=1

	print("pre 2")

	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line[1:].find(';')
		if it != -1:
			buf[idx] = line[:it] + "\n"
			buf.insert(idx+1, line[it:].strip()+ "\n")
		idx+=1

	print("pre 3")
	'''
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("<pre>")
		if it != -1:
			buf[idx] = line[:it] + "\n"
			buf.insert(idx+1, "\\begin{verbatim}")
			buf.insert(idx+2, line[it+6:].strip()+ "\n")
		idx+=1

	print("pre 4")

	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("</pre>")
		if it != -1:
			buf[idx] = line[:it] + "\n"
			buf.insert(idx+1, "\\end{verbatim}")
			buf.insert(idx+2, line[it+7:].strip()+ "\n")
		idx+=1

	print("pre done")

def sourceReplace():
	global idx
	global buf
	global source
	global math
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("<source")
		if it == -1:
			idx+=1
			continue
		jt = line.find("</source>")
		while jt == -1:
			tmp = buf[idx+1]
			line = line[:len(line)] + tmp
			buf[idx] = line
			del buf[idx+1]
			jt = line.find("</source>")
		source.append(line[it:jt+len("</source>")])
		if line[it:jt+len("</source>")] == None or len(line[it:jt+len("</source>")]) < 2:
			print(idx)
			done()
			
		buf[idx] = line[:it] + line[jt+len("</source>"):]
		buf.insert(idx, " argsNoSubSource ")

def LatexLatex():
	global idx
	global buf
	global verbatim
	global source
	global curly
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("{{")
		if it == -1:
			idx+=1
			continue
		jt = line.find("}}")
		while jt == -1:
			tmp = buf[idx+1]
			line = line[:len(line)-1] + tmp
			buf[idx] = line
			del buf[idx+1]
			jt = line.find("}}")
		print(line)
		curly.append(line[it:jt+2])
		buf[idx] = line[:it] + line[jt+2:]
		buf.insert(idx, " argsNoSubCurly ")
	


def tableChange():
	global idx
	global buf
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		if line[:2] == "{|":
			del buf[idx]
			buf.insert(idx, "\\begin{tabular}{ } \\hline\n")
			idx+=1
			line = buf[idx]
			last = False
			while line[:2] != "|}":
				print(line)
				if line[:2] == "|-":
					buf.insert(idx, "\\\\ \\hline\n")
					idx+=1
					last = False
				else:
					if last:	
						buf.insert(idx,"& " + line[1:])
					else:
						buf.insert(idx,line[1:])

					last = True
					idx+=1
				del buf[idx]
				line = buf[idx]

			del buf[idx]
			buf.insert(idx, "\\end{tabular}\n")

		idx+=1

def exampleChange():
	global idx
	global buf
	eList = []
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("{{LaTeX/Example")
		if it != -1:
			eList.append("\\begin{tabular}\n")
			eList.append("\\begin{verbatim}\n")
			del buf[idx]
			line = buf[idx]
			it = line.find("}}")
			while it == -1:
				if -1 == line.find("render") or -1 == line.find("math"):
					if -1 == line.find("render"):
						eList.append("\\end{verbatim}\n")
					if -1 == line.find("math"):
						eList.append("$\n")
				else:
					eList.append(line)

				del buf[idx]
				if idx >= len(buf):
					print(eList)
					done()
				line = buf[idx]

			eList = []
		else:
			idx+=1

def subSingleBackslash():
	global idx
	global buf
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		new = re.sub(r"[^>]\\([^\s\",]+)", "\\\\verb|\\\\\g<1>|", line)
		while line != new:
			new = re.sub(r"[^>]\\([^\s\",]+)", "\\\\verb|\\\\\g<1>|", line)
			line = new
			print(line)

		buf[idx] = line

		idx+=1

def sub(sub):
	global idx
	idx = 0
	while idx < len(buf):
		subtitute(sub[0], sub[1], sub[2], sub[3])
		idx+=1
	print("sub ", idx)

def subList():
	global idx
	idx = 0
	while idx < len(buf):
		lists()	
		idx+=1

	idx = 0
	while idx < len(buf):
		description()	
		idx+=1

def done():
	ifile.close()
	ofile.close()
	sys.exit()

def writeOut():
	global verbatim
	global math
	global source
	global idx
	global buf
	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("argsNoSubCurly")
		while it != -1:
			line = line[:it] + getNextCurly() + line[it+len("argsNoSubCurly")]
			it = line.find("argsNoSubCurly")

		buf[idx] = line
		idx+=1

	idx = 0
	while idx < len(buf):
		line = buf[idx]
		it = line.find("argsNoSubSource")
		while it != -1:
			if line[:it] == None:
				print(line)
				done()
			line = line[:it] + getNextSource() + line[it+len("argsNoSubSource"):]
			it = line.find("argsNoSubSource")

		buf[idx] = line
		idx+=1

	for line in buf:
		if line == "argsNoSubVerbatim":
			tmp = verbatim[0]
			del verbatim[0]
			for j in tmp:
				ofile.write(j)
			continue		

		ofile.write(line)

def getNextSource():
	global source
	tmp = source[0]
	del source[0]
	print(tmp)
	ret = "\\begin{lstlisting}\n"
	it = tmp.find(">")
	ret += tmp[it+1:len(tmp)-len("</source>")] + "\n"
	ret += "\\end{lstlisting}\n"
	print(ret)
	return ret

def getNextCurly():
	global curly
	tmp = curly[0]
	del curly[0]
	return processCurly(tmp)

def processCurly(cur):
	if cur[:len("{{LaTeX/LaTeX|code=")] == "{{LaTeX/LaTeX|code=":
		return "\\verb|"+cur[len("{{LaTeX/LaTeX|code="):len(cur)-2]+"|"
	if cur[:len("{{LaTeX/Usage|code=")] == "{{LaTeX/Usage|code=":
		return "\\verb|"+cur[len("{{LaTeX/Usage|code="):len(cur)-2]+"|"
	if cur[:len("{{LaTeX/Environment|")] == "{{LaTeX/Environment|":
		return "\\verb|"+cur[len("{{LaTeX/Environment|"):len(cur)-2]+"|"
	if cur[:len("{{LaTeX/Parameter|")] == "{{LaTeX/Parameter":
		return "\\texttt{"+cur[len("{{LaTeX/Parameter"):len(cur)-2]+"}"
	if cur[:len("{{LaTeX/Package|")] == "{{LaTeX/Package|":
		return "\\textit{"+cur[len("{{LaTeX/Package|"):len(cur)-2]+"}"
	if cur[:len("{{LaTeX/Example|code=\\[")] == "{{LaTeX/Example|code=\\[":
		retLine = "\\begin{tabular}{c} \\begin{verbatim}"
		it = cur.find("|render=")
		retLine += cur[len("{{LaTeX/Example|code=\\["):it-2] + "\\end{verbatim}"
		retLine += "\\\\ \\hline\n"
		retLine += "$ " + cur[it+len("|render=<math>"):len(cur)-len("</math>")-2] + " $ \\end{tabular}"
		return retLine
		
	else:
		return cur

def main():
	global ifile
	global ofile
	if(len(sys.argv) == 2):
		ifile = open(sys.argv[1] + ".w", "r")
		ofile = open(sys.argv[1] + ".tex", "w")

	readFile()
	print("after read file")

	LatexLatex()
	print("after latex latex")
	pre()
	#exampleChange()
	removeVerbatim()
	sourceReplace()
	subSingleBackslash()
	tableChange()
	sub(subs["paragraph"])
	sub(subs["subsubsection"])
	sub(subs["subsection"])
	sub(subs["section"])
	sub(subs["part"])
	sub(subs["boitalic"])
	#sub(subs["bold"])
	sub(subs["italic"])
	sub(subs["ttverb"])
	sub(subs["tt"])
	sub(subs["ref"])
	sub(subs["code"])
	#subList()
	print(buf)

	writeOut()

	print("\n\n\n")
	for x in curly:
		print(processCurly(x))


if __name__ == "__main__":
	main()
