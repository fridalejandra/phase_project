import numpy as np
import csv
import glob
import matplotlib as mpl, matplotlib.pyplot as plt
print(mpl.__version__)
import xarray as xr
import seaborn as sns;
sns.set(color_codes=True)
plt.style.use('ggplot')
import netCDF4 as nc
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors

from pylab import *
import os
from matplotlib import ticker
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np
import datetime
import calendar as cal
from matplotlib.colors import ListedColormap, BoundaryNorm
import cmocean


## Sans Serif ##
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

plt.style.use('ggplot')
plt.style.use('dark_background')

#Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]


map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
#plt.show()
plt.savefig('/Users/fridaperez/Desktop/Basemap_Ant_dark.png',dpi=500)  # write image to file
