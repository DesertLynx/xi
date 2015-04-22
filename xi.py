#!/usr/local/bin/python3

#don't laugh.... I don't know python
import os
import re
import sys
import subprocess

# a list of folders not to search
folderBlacklist = [
		'node_modules',
		'.git'
		]

if len(sys.argv) < 2:
	print("Usage: xi <searchterm> [path]")
	exit(1)

# Grab options out of the args list
method = "grep" if('--grep' in sys.argv) else "fgrep"
debug = True if ('--debug' in sys.argv) else False

args = list(filter(lambda x: not re.match('^--', x), sys.argv))

#process standard positional args
if len(args) >= 3: 
	path = args[2] 
else: 
	path = os.getcwd()

searchTerm = sys.argv[1]
excludeFolders = "".join([str(' --exclude-dir ' + x) for x in folderBlacklist])

searchConstruct =  method + ' -rin "'+  searchTerm + '" ' + path + ' ' + excludeFolders + ' --binary-files=without-match --no-messages' 

if(debug):
	print('Searchmethod: ' + searchConstruct)

process = subprocess.Popen([searchConstruct], shell=True, stdout=subprocess.PIPE);
output = process.communicate()[0]

matches = [];

def getTerminalWidth():
	process = subprocess.Popen(['tput', 'cols'], stdout=subprocess.PIPE);
	return int(re.sub('[^0-9]*', '', str(process.communicate()[0])))

truncationWidth = getTerminalWidth() - 20

for line in output.decode("utf-8").split("\n"):
	if(line):
		matches.append(line)
option = 0

if output: 
	for line in matches:

		#trim unnecessarily long paths
		line = line.replace(os.getcwd(), '.')

		#display matches with prettiness 
		if method == 'fgrep':
			line = re.sub(searchTerm, '\033[94m' + searchTerm + '\033[0m', line)

		# newlines in the middle of results are annoying
		line = re.sub("\n", "", line);
		line = re.sub("\r", "", line);

		# Show each line, but chop off really long lines
		print(str(option) + " : " + (line[:truncationWidth] + (line[truncationWidth- 20:] and "...")))
		option = option + 1

	selection = int(input())

	if matches[selection]:

		file = matches[selection].split(":")[0];
		lineNumber = matches[selection].split(":")[1];

		os.system('vi ' + file + ' +' + lineNumber);

	else: 
		exit(1)
else:
	print('nothing found')

