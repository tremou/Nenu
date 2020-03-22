#!/usr/bin/env python
import sys
import os
import numpy
import math
from casacore.tables import *
import argparse
import matplotlib.pyplot as plt
from astropy.coordinates import Angle
from astropy import units as u
from astropy.constants import c, R_earth
from astropy import constants as const
from astropy.time import Time
import seaborn as sns; sns.set()

parser = argparse.ArgumentParser(description='Quick plots of MSs', epilog="Output:plots", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("MS_file", help='input MeasurmentSet file')
parser.add_argument('-corr','--corr',dest='corr',help='Correlation index to plot. 0 or 1 or 2 or 3, default = 0 (0=XX, 1=XY, 2=YX, 3=YY)',default=0)
parser.add_argument('-ant','--ant',dest='ant',help='Plot only this antenna, or comma-separated list of antennas',default=[-1])

args = parser.parse_args()
parser.print_help()
corr = int(args.corr)
ant = args.ant


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__



def rad2deg(xx):
	# convert radians to degrees
	return 180.0*xx/numpy.pi


# Get the Measurement Set from the command line arguments
myms=args.MS_file.rstrip('/')
fldtab = table(myms+'/FIELD',ack=False)
# Get the NAME column
names = fldtab.getcol('NAME')
ids = fldtab.getcol('SOURCE_ID')
# Get the PHASE_DIR column
dirs = fldtab.getcol('PHASE_DIR')
fldtab.done()

obstab = table(myms+'/OBSERVATION',ack=False)
obsname = obstab.getcol('OBSERVER')
telname = obstab.getcol('TELESCOPE_NAME')
proj = obstab.getcol('PROJECT')
obstab.done()

spwtab = table(myms+'/SPECTRAL_WINDOW',ack=False)
nspw = len(spwtab)
spwfreqs = spwtab.getcol('REF_FREQUENCY')
chanwidth = spwtab.getcol('CHAN_WIDTH')[0][0]
nchans = spwtab.getcol('NUM_CHAN')
spwtab.done()

anttab = table(myms+'/ANTENNA',ack=False)
nant = len(anttab)
antpos = anttab.getcol('POSITION')
antnames = anttab.getcol('NAME')
anttab.done()

#The number of correlation polarization products. For example, for (RR) this value would be 1, for (RR, LL) it would be 2, and for (XX,YY,XY,YX) it would be 4, etc.
poltab = table(myms+'/POLARIZATION',ack=False)
num_corr = poltab.getcol('NUM_CORR')
poltab.done()

maintab = table(myms,ack=False)
usedants = numpy.unique(maintab.getcol('ANTENNA1'))
meanexp = round(numpy.mean(maintab.getcol('EXPOSURE')),2)
uvw = maintab.getcol('UVW')
u=uvw[:, 0]
v=uvw[:, 1]
uvdist = ((u**2.0)+(v**2.0))**0.5
uu=numpy.append(u, u*-1.0)
vv=numpy.append(v, v*-1.0)
data = maintab.getcol('DATA')
phase = numpy.angle(data[:,:,corr])#rads
amp = numpy.abs(data[:,:,corr])
real = numpy.real(data[:,:,corr])
imag = numpy.imag(data[:,:,corr])

times = maintab.getcol('TIME')
t0 = times[0]
t1 = times[-1]
length = round((t1 - t0),0)
mjd=t0/86400
t = Time(mjd, format='mjd')
st_time=t.iso
maintab.done()

if ant[0] != -1:
	ant = ant.split(',')
	for a in ant:
		if int(a) not in usedants:
			ant.remove(a)
			print ('Requested antenna ID '+str(a)+' not found')
	if len(ant) == 0:
		print ('No valid antennas have been requested')
		sys.exit(-1)
	else:
		ant = numpy.array(ant,dtype=int)
else:
	ant = usedants


print(plt.rcParams['agg.path.chunksize'])
plt.rcParams['agg.path.chunksize'] = 10000

#plt.rcParams['agg.path.chunksize'] = 10000000
#plt.ticklabel_format(useOffset=False, style='plain')
#plt.rcParams["figure.figsize"] = (15,10)
#plt.tick_params(axis ='both',which='both',direction = 'in',labelsize=25)
#plt.title(myms,fontsize = 10)
fig, axs = plt.subplots(2, 2, figsize=(15,9))
fig.suptitle(myms,fontsize = 10)
axs[0, 0].plot(uu, vv, ',', markersize =15)
#axs[0, 0].set_title('UV plot')
axs[0, 0].set(xlabel='U', ylabel='V')
axs[0, 1].plot(real, imag, ',', markersize =5, color='tab:orange')#, 'tab:orange')
axs[0, 1].ticklabel_format(useOffset=False, style='plain')
axs[0, 1].set(xlabel='Real', ylabel='Imaginary')
axs[0, 1].ticklabel_format(useOffset=False, style='plain')
axs[1, 0].plot(uvdist, amp, ',', markersize =3, color='tab:green')
axs[1, 0].set(xlabel='UV distance', ylabel='Amplitude')
axs[1, 0].ticklabel_format(useOffset=False, style='plain')
axs[1, 1].plot(times/86400, amp, ',', markersize =3, color='tab:red')
axs[1, 1].set(xlabel='Time (mjd)', ylabel='Amplitude')
axs[1, 1].ticklabel_format(useOffset=False, style='plain')
#axs[2, 0].plot(uvdist, phase, ',', markersize =3, color='tab:green')
#axs[2, 0].set(xlabel='UV distance', ylabel='Phase(rad)')
#axs[2, 0].ticklabel_format(useOffset=False, style='plain')
#axs[2, 1].plot(times/86400, phase, ',', markersize =3, color='tab:red')
#axs[2, 1].set(xlabel='Time (mjd)', ylabel='Phase(rad)')
#axs[2, 1].ticklabel_format(useOffset=False, style='plain')
#axs[1, 1].set_title('AmpvsTime')
#plt.plot(uu,vv, ',', markersize =15)
#plt.xlabel('U ', fontsize = 20)
#plt.ylabel('V ', fontsize = 20)
#plt.plot(real,imag, '.', markersize =5)
#plt.xlabel('real ', fontsize = 20)
#plt.ylabel('imag', fontsize = 20)
#plt.plot(times/86400,phase, ',', markersize =3)
#plt.xlabel('t ', fontsize = 20)
#plt.ylabel('amp', fontsize = 20)
fig.savefig(myms+'_plot.png',bbox_inches='tight')
plt.show()
