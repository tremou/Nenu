#!/usr/bin/python
#evangelia.tremou@obspm.fr

#It plots the altitude and the sepration distance between A-team sources and the phase center of the observations (pointing). 
#Edit the config.toml to set the desired pointing, time of the desired observing run and the telescope location if used other than nenuFAR. 
#The script is similar to https://github.com/lofar-astron/LOFAR-Contributions/blob/master/Maintained/plot_Ateam_elevation.py which is reading the above information from an MS file. 
#The difference is that the current script could be used before the observations in order to avoid certain proximity of an A-team source. This can help avoiding the heavy computing demixing-process (https://support.astron.nl/LOFARImagingCookbook/tutorial.html#flagging-and-demixing) 

import matplotlib.pyplot as plt
import numpy
from matplotlib import dates
import datetime
import astropy.units as u
import matplotlib
from astropy.time import Time
import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
import seaborn as sns; sns.set()
import toml
from matplotlib import rc
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
#matplotlib.rcParams['savefig.dpi'] = 350
matplotlib.rcParams['figure.figsize'] = (13, 8)
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.sans-serif'] = ['Verdana']

#import the config file (config.toml), edit it accordingly (pointing, time and telescope location)
config = toml.load('config.toml')

#parsing the telescope location
nenulocation=EarthLocation(lat=config.get('TELESCOPE').get('latitude'), lon=config.get('TELESCOPE').get('longtitude'), height=config.get('TELESCOPE').get('elevation'))

#parsing the observation time
start_time = Time(config.get('TIME').get('start_time'), scale='utc', location=nenulocation)
end_time = Time(config.get('TIME').get('end_time'), scale='utc', location=nenulocation)
delta_t = end_time - start_time
observe_time = Time(start_time + delta_t*np.linspace(0, 1, 75), format='isot', scale='utc')
#LST=observe_time.sidereal_time('mean')

#parsing the coordinates of A-team sources and target
myobs=SkyCoord(config.get('POINTING').get('RA'), config.get('POINTING').get('DEC'), frame=config.get('POINTING').get('frame'))
CasA=SkyCoord(config.get('CasA').get('RA'), config.get('CasA').get('DEC'), frame=config.get('CasA').get('frame'))
CygA=SkyCoord(config.get('CygA').get('RA'), config.get('CygA').get('DEC'), frame=config.get('CygA').get('frame'))
TauA=SkyCoord(config.get('TauA').get('RA'), config.get('TauA').get('DEC'), frame=config.get('TauA').get('frame'))
HerA=SkyCoord(config.get('HerA').get('RA'), config.get('HerA').get('DEC'), frame=config.get('HerA').get('frame'))
VirA=SkyCoord(config.get('VirA').get('RA'), config.get('VirA').get('DEC'), frame=config.get('VirA').get('frame'))
HydraA=SkyCoord(config.get('HydraA').get('RA'), config.get('HydraA').get('DEC'), frame=config.get('HydraA').get('frame'))

#convert the coordinates into AltAz format so the y-axis (Altitude of the sources) can be plotted
myobsaltaz = myobs.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# myobsaz=np.array(myobsaltaz.az)
#myobsalt=np.array(myobsaltaz.alt)
casaltaz = CasA.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# casaz=np.array(casaltaz.az)
#casalt=np.array(casaltaz.alt)
cygaltaz = CygA.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# cygaz=np.array(cygaltaz.az)
#cygalt=np.array(cygaltaz.alt)
taualtaz = TauA.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# tauaz=np.array(taualtaz.az)
#taualt=np.array(taualtaz.alt)
heraltaz = HerA.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# heraz=np.array(heraltaz.az)
#heralt=np.array(heraltaz.alt)
viraltaz = VirA.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# viraz=np.array(viraltaz.az)
#viralt=np.array(viraltaz.alt)
ydraltaz = HydraA.transform_to(AltAz(obstime=observe_time,location=nenulocation))
# ydraz=np.array(ydraltaz.az)
#ydralt=np.array(ydraltaz.alt)

#calculate the angular separation between the A-team sources and the telescope pointing (target)
angdist_cas=myobs.separation(CasA)
angdist_cyg=myobs.separation(CygA)
angdist_tau=myobs.separation(TauA)
angdist_her=myobs.separation(HerA)
angdist_vir=myobs.separation(VirA)
angdist_ydr=myobs.separation(HydraA)
angdist_point=myobs.separation(myobs)

#plot the source altitude (yaxis) in degrees as a function of the observation time in MJD format (x-axis) and label the angular seperation in the Figure legend
fig, ax = plt.subplots()
ax.plot(observe_time.mjd,myobsaltaz.alt, label='Pointing - '+ str((angdist_point.to_string(unit=u.deg, decimal=True))+ ' deg'))
ax.plot(observe_time.mjd,casaltaz.alt, label='Cas A - '+ str((angdist_cas.to_string(unit=u.deg, decimal=True))+ ' deg'))
ax.plot(observe_time.mjd,cygaltaz.alt, label='Cyg A - '+ str((angdist_cyg.to_string(unit=u.deg, decimal=True))+ ' deg'))
ax.plot(observe_time.mjd,taualtaz.alt, label='Tau A - '+ str((angdist_tau.to_string(unit=u.deg, decimal=True))+ ' deg'))
ax.plot(observe_time.mjd,heraltaz.alt, label='Her A - '+ str((angdist_her.to_string(unit=u.deg, decimal=True))+ ' deg'))
ax.plot(observe_time.mjd,viraltaz.alt, label='Vir A - '+ str((angdist_vir.to_string(unit=u.deg, decimal=True))+ ' deg'))
ax.plot(observe_time.mjd,ydraltaz.alt, label='Hydra A - '+ str((angdist_ydr.to_string(unit=u.deg, decimal=True))+ ' deg'))

#plot customizing
ax.ticklabel_format(useOffset=False, style='plain')
plt.title('Angular separation between phase center ('+myobs.to_string('hmsdms')+') and A-team sources', fontsize=18)
plt.xlabel('Date (MJD)',fontsize=22)
plt.ylabel('Altitude (deg)', fontsize=22)
plt.tick_params('both', length=9, width=1, which='major')
plt.tick_params('both', length=5, width=1, which='minor')
plt.tick_params(axis='both', which='both',direction='in',right=True,top=True, left=True, bottom=True, labelsize=14)
plt.legend(shadow=True)
plt.show()
