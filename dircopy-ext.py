# DIRCOPY-EXT: a simple backup script to copy files into folders based on their extensions

import os
from os.path import join

import shutil as sh

import sys

def nextAvailName(dir, fn):
	ext = os.path.splitext(fn)[1][1:].lower()
	lenExt = len(ext)
	if lenExt > 0:
		lenExt += 1
		dot = '.'
	else:
		dot = ''
	cn = 1
	while os.path.exists(join(dir,fn[:len(fn)-lenExt]+'-'+str(cn)+dot+ext)):
		cn += 1
	return fn[:len(fn)-lenExt]+'-'+str(cn)+dot+ext

print
print 'DIRCOPY-EXT: The easy way to backup and arrange your files by filetype.'
print

# get source (src) and destination (des) dir paths
src = ''
while not(os.path.exists(src)):
	src = raw_input('Source directory (copy from): ')
	if not(os.path.exists(src)):
		print src+' does not exist.'
des = raw_input('Target directory (copy to): ')

if not(os.path.exists(des)):
	print
	print des+' does not exist.'
	response = raw_input('Do you want to create it? (y/N) ')
	if response.lower() == 'y':
		try:
			os.mkdir(des)
		except:
			print
			print 'Directory creation failed!', sys.exc_info()[1]
			print
			sys.exit()
	else:
		sys.exit()
else:
	if src == des:
		print
		print 'Error: Cannot copy source to itself!'
		print
		sys.exit()
	print
	print des+' already exits.'
	response = raw_input('Are you sure you want to write to it? (y/N) ')
	if response.lower() != 'y':
		sys.exit()

srcTree = os.walk(src)

logFn = 'log.html'
if os.path.exists(join(des,logFn)):
	logFn = nextAvailName(des, logFn)
log = open(join(des,logFn),'w')
logEntry = '<html>\n<head><title>Log for backup of '+src+'</title>\n</head>\n<body>\n<table>\n'
log.write(logEntry)
logEntry = '<th>File</th><th>Source</th>'
log.write(logEntry)

for pth, drs, fls in srcTree:
	for fn in fls:
		ofn = join(pth, fn)
		desDir = os.path.splitext(fn)[1][1:].lower()
		if desDir == '':
			desDir = 'noExt'
		if not(os.path.exists(join(des,desDir))):
			os.mkdir(join(des,desDir))
		if os.path.exists(join(des,desDir,fn)):
			fn = nextAvailName(join(des,desDir),fn)
#			lext = len(desDir)
#			if lext > 0:
#				lext += 1
#			cn = 1
#			while os.path.exists(join(des,desDir,fn[:len(fn)-lext]+'-'+str(cn)+'.'+desDir)):
#				cn += 1
#			fn = fn[:len(fn)-lext]+'-'+str(cn)+'.'+desDir
		logEntry = '<tr><td><a href="'+join(des,desDir,fn)+'">'+fn+'</a></td><td>'+ofn+'</td></tr>\n'
		log.write(logEntry)
		sh.copy2(ofn, join(des,desDir,fn))
		print '.',

logEntry = '</table>\n</body>\n</html>'
log.write(logEntry)
log.close()
print
print 'DONE.'
print 'Log file: '+join(des,logFn)
print