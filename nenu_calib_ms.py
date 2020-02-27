#!/usr/bin/env python
import os
import glob
import numpy

mslist = glob.glob('*.MS')

#make sure you have the sourcedb model in the same folder and change
#NDPPP ndppp-gaincal.parset ===> you need to run makesourcedb command using a text skymodel
#to generate a sourcedb table  (folder "sky") to be used as a skymodel by NDPPP,
#gaincal will create a folder "instrument" which  contains calibration solution that can be visualized with parmdbplot.py
#eg: makesourcedb in=your_skymodel_path/CasApoint.skymodel out=testmodelvi
#your out name should be edited accordingly below in the gaical task.

#available_steps=[preflag=1, aoflag=2, gaincal=3, applycal=4]
steps= [1,2,3,4]

if 1 in steps:
	for myms in mslist:
		syscall= 'NDPPP '
		syscall+= 'msin='+myms+' '
		syscall+= 'msin.datacolumn=DATA '
		syscall+= 'msout=. '
		syscall+= 'steps=[preflagger] '
		syscall+= 'preflagger.corrtype=auto ' # nothing or cross or auto
		print syscall
		os.system(syscall)

if 2 in steps:
	for myms in mslist:
		syscall= 'aoflagger '+myms+' '
		#syscall+= 'msin='+myms+' '
		print syscall
		os.system(syscall)

if 3 in steps:
	for myms in mslist:
		syscall= 'NDPPP '
		syscall+= 'msin='+myms+' '
		syscall+= 'msout='+myms+' '
		syscall+= 'steps=[gaincal] '
		syscall+= 'gaincal.sourcedb=testmodelvi '
		syscall+= 'gaincal.parmdb='+myms+'/instrument '
		syscall+= 'gaincal.caltype=fulljones '
		syscall+= 'gaincal.solint=10 '
		syscall+= 'gaincal.nchan=0 '
		print syscall
		os.system(syscall)

if 4 in steps:
	for myms in mslist:
		syscall= 'NDPPP '
		syscall+= 'msin='+myms+' '
		syscall+= 'msout='+myms+'_CAL '
		syscall+= 'msin.datacolumn=DATA '
		syscall+= 'steps=[applycal] '
		syscall+= 'applycal.parmdb='+myms+'/instrument '
		print syscall
		os.system(syscall)
