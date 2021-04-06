#!/usr/bin/env python
import sys
import os
import numpy
import math
from casacore.tables import *
from MSUtils.msutils import STOKES_TYPES
import argparse
import matplotlib.pyplot as plt
from astropy.coordinates import Angle
from astropy import units as u
from astropy.constants import c, R_earth
from astropy import constants as const
from astropy.time import Time

parser = argparse.ArgumentParser(description='Quick look at a Measurement Set, Plot of antenna positions, return the antenna positions in degrees (Lon, Lat)', epilog="Output:list info of MS and plot antenna positions, and return the antenna positions in degrees (Lon, Lat)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("MS_file", help='input MeasurmentSet file')

args = parser.parse_args()
parser.print_help()

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def gi(message):
        print ('\033[92m'+message+'\033[0m')


def ri(message):
        print ('\033[91m'+message+'\033[0m')


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

poltab = table(myms+'/POLARIZATION',ack=False)
num_corr = poltab.getcol('NUM_CORR')
corr_labels = [STOKES_TYPES[corr] for corr in poltab.getcol('CORR_TYPE', 0, 1).ravel()]
poltab.done()


maintab = table(myms,ack=False)
usedants = numpy.unique(maintab.getcol('ANTENNA1'))
meanexp = round(numpy.mean(maintab.getcol('EXPOSURE')),2)
times = maintab.getcol('TIME')
t0 = times[0]
t1 = times[-1]
length = round((t1 - t0),0)
mjd=t0/86400
t = Time(mjd, format='mjd')
st_time=t.iso
maintab.done()

# Loop over the number of rows
print ('')
gi('     '+myms)
print ('     Observer:                 '+   ''.join(obsname))
print ('     Telescope:                '+   ''.join(telname))
print ('     Project:                  '+   ''.join(proj))
print ('     Beginning of Observation: '+str(st_time)+' (ISO) -- '+str(mjd)+' (MJD) ')
print ('     Observation length:       '+str(length)+'s ('+str(round((length/3600.0),2))+' h)')
print ('     Mean integration time:    '+str(meanexp)+' s')
#print ('     Number of correlation     ')
#print ('     polarization products:    '+str(num_corr)+'')
print ('     Correlation products:    '+str(list(corr_labels)))

print ('')
#gi('     '+myms+'/FIELD')
gi('     ROW   ID    NAME          RA            DEC')
for i in range(0,len(names)):
        # MS uses SI units, so directions are in radians
        ra_rad = dirs[i][0][0]
        dec_rad = dirs[i][0][1]
        ra_deg = Angle(rad2deg(ra_rad), unit=u.deg)
        dec_deg = Angle(rad2deg(dec_rad), unit=u.deg)
        dec_dms=dec_deg.to_string(unit=u.degree, sep=('d', 'm', 's'))
        ra_hms=ra_deg.to_string(unit=u.hour)
        # Print out the
        print ('     %-6s%-6s%-14s%-14s%-14s' % (i,str(ids[i]),names[i],ra_hms,dec_dms))

print ('')
#gi('     '+myms+'/SPECTRAL_WINDOW')
gi('     ROW   CHANS         WIDTH[MHz]          REF_FREQ[MHz]')
for i in range(0,nspw):
	print ('     %-6s%-14s%-20s%-14s' % (i,str(nchans[i]),str(chanwidth/1e6),str(spwfreqs[i]/1e6)))
print ('')
#gi('     '+myms+'/ANTENNA')
gi('     ROW   NAME          POSITION ')
for i in range(0,nant):
	if i in usedants:
		print ('     %-6s%-14s%-14s' % (i,(antnames[i]),str(antpos[i])))
	else:
		ri('     %-6s%-14s%-14s' % (i,(antnames[i]),str(antpos[i])))
print ('')

#blockPrint()
plt.rcParams["figure.figsize"] = (12,8)
x = antpos[:,1]
y = antpos[:,0]
z = antpos[:,2]
R = 6378100 #earth-radius

print (' '*2, 'ANTENNA NAME' +' '*8+ 'LONG (DEG)' + ' '*10+ 'LAT (DEG)')

plt.plot(x, y, '1', markersize=25)
#ax = plt.axes(projection=ccrs.PlateCarree())
plt.ticklabel_format(useOffset=False, style='plain')
plt.xlabel('X (meters)', fontsize = 20)
plt.ylabel('Y (meters)', fontsize = 20)
plt.tick_params(axis ='both',which='both',direction = 'in',labelsize=16)
plt.title(myms,fontsize = 10)
for i, txt in enumerate(antnames):
        plt.annotate(txt, (x[i]+5, y[i]+5), ha='center', color='black', fontsize='8')
        lat = math.asin(z[i] / R)
        lon = math.atan2(x[i], y[i])
        lat_deg=180.0*lat/numpy.pi
        lon_deg=180.0*lon/numpy.pi
        #enablePrint()
        print ( ' '*5, antnames[i],  ' '*8,  lon_deg,     ' '*8,       lat_deg)
        #plt.plot(lon_deg, lat_deg, marker='1',markersize=25, transform=ccrs.Geodetic())


plt.show()
#plt.savefig(myms+'_plotant.png')
