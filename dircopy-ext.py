# DIRCOPY-EXT: a simple backup script to copy files into folders based on their extensions

import os
from os.path import join

import shutil as sh

# get source (src) and destination (des) dir paths
src = 'C:\\dir'
des = 'C:\\dir2'

srcTree = os.walk(src)
	
for pth, drs, fls in srcTree:
	for fn in fls:
		ofn = join(pth, fn)
		desDir = os.path.splitext(fn)[1][1:].lower()
		if desDir == '':
			desDir = 'noExt'
		if not(os.path.exists(join(des,desDir))):
			os.mkdir(join(des,desDir))
		if os.path.exists(join(des,desDir,fn)):
			lext = len(desDir)
			if lext > 0:
				lext += 1
			cn = 1
			while os.path.exists(join(des,desDir,fn[:len(fn)-lext]+'-'+str(cn)+'.'+desDir)):
				cn += 1
			fn = fn[:len(fn)-lext]+'-'+str(cn)+'.'+desDir
		sh.copy2(ofn, join(des,desDir,fn))

print 'DONE'