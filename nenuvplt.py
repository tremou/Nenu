#!/usr/bin/env python
import matplotlib
import daskms as xms
import dask.array as da
from daskms import xds_from_table, xds_to_table
from daskms import xds_from_ms
import datashader as ds
import dask.dataframe as dd
import dask
import sys
import numpy
import matplotlib.pyplot as plt
import os
import math
import argparse
from astropy.time import Time
from bokeh.plotting import figure, output_file, show
import seaborn as sns; sns.set()
import xarray as xr
import pandas as pd

parser = argparse.ArgumentParser(description='Plot of UV coverage', epilog="Output:UV coverage plot (meters)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("MS_file", help='input MeasurmentSet file')

args = parser.parse_args()
parser.print_help()

myms=args.MS_file.rstrip('/')

datasets = xds_from_ms(myms)
# Create short names mapped to the full table path
table_name = {short: "::".join((myms, full)) for short, full in
[('antenna', "ANTENNA"),
('ddid', "DATA_DESCRIPTION"),
('spw', "SPECTRAL_WINDOW"),
('pol', "POLARIZATION"),
('field', "FIELD")]}

# Get datasets for DATA_DESCRIPTION, SPECTRAL_WINDOW  POLARIZATION and FIELD, partitioned by row
ddid_ds = list(xds_from_table(table_name['ddid'], group_cols="__row__"))
spwds = list(xds_from_table(table_name['spw'], group_cols="__row__"))
pds = list(xds_from_table(table_name['pol'], group_cols="__row__"))
field_ds = list(xds_from_table(table_name['field'], group_cols="__row__"))
ant_ds = list(xds_from_table(table_name['antenna'], group_cols="__row__"))

# Look up the Spectral Window and Polarization datasets, given the Data Descriptor ID
for ms_ds in datasets:
    field = field_ds[ms_ds.attrs['FIELD_ID']]
    ddid = ddid_ds[ms_ds.attrs['DATA_DESC_ID']]
    spw = spwds[ddid.SPECTRAL_WINDOW_ID.values[0]]
    pol = pds[ddid.POLARIZATION_ID.values[0]]

#pol_table = '::'.join((myms, 'POLARIZATION'))
#for p in xds_from_table(pol_table):
        #corr=p.CORR_PRODUCT.data.squeeze().compute()


#corr[0] = XX
#corr[1] = XY
#corr[2] = YX
#corr[3] = XX

c = 299792458.0 #(m/s)
spw_table = '::'.join((myms, 'SPECTRAL_WINDOW'))


for a in xds_from_table(spw_table):
        chan=a.CHAN_FREQ.data.squeeze(0).compute()

wavel=c/chan
#msdata = xms.xds_from_ms(myms, columns=['TIME', 'FLAG', 'FIELD_ID', 'UVW', 'CORRECTED_DATA', 'DATA'])
for i in datasets:
        mjd=i.TIME.values/86400
        t = Time(mjd, format='mjd')
        st_time = t.iso
        v = i.UVW.values[:,1]
        u = i.UVW.values[:,0]
        phase = numpy.angle(i.DATA.values[:,0])#rads
        amp = numpy.abs(i.DATA.values[:,0])
        real = numpy.real(i.DATA.values[:,0])
        imag = numpy.imag(i.DATA.values[:,0])
        #corr=p.POLARIZATION.CORR_PRODUCT.data.
        #print (st_time)


#UV distance
uvdist = ((u**2.0)+(v**2.0))**0.5

#convert the xarray into panda dataframe to prepare it for plotting ... 
#frame=i.to_dataframe()
#u and v in wavelengths:
#for z in u:
        #uwav=z/wavel*len(u)

#for x in v:
        #vwav=x/wavel*len(v)

#conjugate points for uvplot
uu=numpy.append(u, u*-1.0)
vv=numpy.append(v, v*-1.0)

#ax = sns.scatterplot(x=real, y=imag)

#output_file("uv.html")
#p = figure(plot_width=1200, plot_height=800)
#p = figure(output_backend="canvas")

#p = Plot(output_backend="webgl")
#p.scatter(u, v, alpha=0.1)
#p.dash(u, v, size=5, color="blue", alpha=0.5)


matplotlib.rcParams['agg.path.chunksize'] = 100000
plt.ticklabel_format(useOffset=False, style='plain')
plt.rcParams["figure.figsize"] = (12,8)
plt.tick_params(axis ='both',which='both',direction = 'in',labelsize=25)
plt.title(myms,fontsize = 10)
plt.plot(uu,vv, ',', markersize =15)
#plt.xlabel('X (meters)', fontsize = 20)
#plt.ylabel('Y (meters)', fontsize = 20)
plt.show()
