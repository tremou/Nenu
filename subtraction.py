#!/usr/bin/env python

import os
import glob
import numpy

mslist = glob.glob('*.ms')


#available_steps=[source subtraction]
steps= [source_sub]

if source_sub in steps: 
	for myms in mslist:
		syscall= 'NDPPP ' 
		syscall+= 'msin='+myms+' '
		syscall+= 'msin.datacolumn=CORRECTED_DATA '
		syscall+= 'msout='+myms+'_sub ' 
		syscall+= 'steps=[subtractcasA, applycal] '
		syscall+= 'subtractcasA.type=predict '
 		syscall+= 'subtractcasA.operation=subtract '
		syscall+= 'subtractcasA.sourcedb=/data/etremou/nenufar/skymodel/CasApoint.sourcedb '
		syscall+= 'subtractcasA.sources=[CasAPoint] '
		syscall+= 'subtractcasA.applycal.parmdb='+myms+'/instrument '
		syscall+= 'applycal.parmdb='+myms+'/instrument '
		print (syscall) 
		os.system(syscall)

