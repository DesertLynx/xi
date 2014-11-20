#!/usr/local/bin/python3

#don't laugh.... I don't know python
import os
import re
import sys
import subprocess

if len(sys.argv) < 1:
	print("Usage: xi <searchterm> [path]")

if len(sys.argv) >= 3: 
    path = sys.argv[2] 
else: 
    path = os.getcwd()

searchTerm = sys.argv[1]
process = subprocess.Popen(['grep -rin '+  searchTerm + " " + path], shell=True, stdout=subprocess.PIPE);
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

        #display matches with prettiness 
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

