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

#available_steps=[preflag=1, aoflag=2, gaincal=3, applycal=4, wsclean=5]
steps= [1,2,3,4,5]

if 1 in steps:
	for myms in mslist:
		syscall= 'NDPPP '
		syscall+= 'msin='+myms+' '
		syscall+= 'msin.datacolumn=DATA '
		syscall+= 'msout=. '
		syscall+= 'steps=[preflagger] '
		syscall+= 'preflagger.corrtype=auto ' 
		print syscall
		os.system(syscall)

if 2 in steps:
	for myms in mslist:
		syscall= 'aoflagger '+myms+' '
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
		
if 5 in steps: 
	if 5 in steps: 
	imgname = 'sub_img_'+mslist[0]+'_data'
	syscall = 'wsclean '
	syscall+= '-size 1024 1024 '
	syscall+= '-scale 5arcmin '
	#syscall+= '-intervals-out 3 '
	syscall+= '-niter 9000 '
	syscall+= '-gain 0.1 '
	syscall+= '-mgain 0.85 '
	syscall+= '-weight briggs -0.3 '
	#syscall+= '-minuv-l 50 '
	syscall+= '-datacolumn DATA '
	syscall+= '-local-rms '
	syscall+= '-auto-threshold 0.3 '
	syscall+= '-auto-mask 8.0 '
	syscall+= '-name '+imgname+' '
	#syscall+= '-channelsout 5 '
	#syscall+= '-fit-spectral-pol 3 '
	#syscall+= '-joinchannels '
	syscall+= '-mem 90 '
	syscall+= '*.MS_CAL'
	print syscall 
	os.system(syscall)
