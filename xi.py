#!/usr/local/bin/python3

#don't laugh.... I don't know python
import os
import sys
import subprocess

searchTerm = sys.argv[1]

process = subprocess.Popen(['grep -rin '+  searchTerm + " " + os.getcwd()], shell=True, stdout=subprocess.PIPE);

output = process.communicate()[0]

matches = [];

for line in output.decode("utf-8").split("\n"):
	if(line):
		matches.append(line)
option = 0

if output: 
	for line in matches:

		# Show each line, but chop off really long lines
		print(str(option) + " : " + (line[:100] + (line[100:] and "...")))
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
