from nenupy.skymodel import get_point_sources
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd

#vir_a = SkyCoord(187.70593075958, +12.39112329392, unit='deg')
#get_point_sources(freq=50, center=vir_a, radius=1*u.deg)


center = SkyCoord(187.70593075958, +12.39112329392, unit='deg)
#center = SkyCoord('-10h12m44s', '+17d27m25s', frame='icrs')
model=get_point_sources(freq=40, center=center, radius=0.5*u.deg)



df = pd.DataFrame(model)
df_tr = df.transpose()
df_tr.to_csv(r'model.csv', header=None, index=None, sep=' ', mode='a')


print (model)
