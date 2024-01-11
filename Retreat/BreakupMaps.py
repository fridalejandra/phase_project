### MAKE SURE THE SCRIPT IS IN THE FOLDER WHERE THE FILES ARE ####
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

#Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Volumes/WorkDrive/melt_dates/seaiceconc.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

## LOOPY
# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))
dir = '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/'

count = 0
#plt.style.use('dark_background')
Mytitle = list(map(str,list(range(2010,2022))))
print(Mytitle)

files = []
for i,title_name in zip(os.listdir(dir),Mytitle):
    if i.endswith('.nc'):
        files.append(open(i))
        data = nc.Dataset(i)
        ice = data['__xarray_dataarray_variable__'][:]

        fig = plt.subplots(figsize=(5, 10))

        ax = fig.add_subplot(111)
        map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
        x, y = map(longitude, latitude)
        map.drawmapboundary(fill_color='white')
        map.fillcontinents(color='dimgrey')
        map.drawlsmask(land_color='white', ocean_color='k')
        map.drawcoastlines(color='k', linewidth=0.5)

        # Draw parallels and Meridians
        map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',
                          fontsize=5)
        meridians = np.arange(0., 360., 30.)
        map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')

        # REGIONS##
        # KING HAKON VII
        lon_I = 35
        lat_I = -58
        x_I, y_I = map(lon_I, lat_I)
        plt.text(x_I, y_I, 'KHVII', fontsize=6, fontweight='light', color='white', verticalalignment='center')

        # EAST ANTARCTICA
        lon_P = 140
        lat_P = -58
        x_P, y_P = map(lon_P, lat_P)
        plt.text(x_P, y_P, 'EA', fontsize=6, fontweight='light', color='white', verticalalignment='center')
        # ROSS AMUNDSEN SEA
        lon_R = -135
        lat_R = -53
        x_R, y_R = map(lon_R, lat_R)
        plt.text(x_R, y_R, 'RAS', fontsize=6, fontweight='light', color='white', verticalalignment='center')
        # Amundsen-Bellingshausen
        lon_A = -94
        lat_A = -52
        x_A, y_A = map(lon_A, lat_A)
        plt.text(x_A, y_A, 'ABS', fontsize=6, fontweight='light', color='white', verticalalignment='center')
        # Weddell Sea
        lon_W = -46
        lat_W = -53
        x_W, y_W = map(lon_W, lat_W)
        plt.text(x_W, y_W, 'WS', fontsize=6, fontweight='light', color='white', verticalalignment='center')

        map.contourf(x, y, ice[:], cmap='viridis')
        plt.subplots_adjust(wspace=.50, hspace=0.05, right=0.8)
        cbar = plt.colorbar(drawedges=True, orientation='horizontal', pad=0.15)
        cbar.set_label('DAYS SINCE AUGUST')
        plt.text(0, 0, r'DATA:  AMSR-E/AMSR2 [Meier, W. N., T. Markus, and J. C. Comiso, 2018]', fontsize=5,
             rotation='horizontal', ha='left', color='darkgrey', transform=plt.gcf().transFigure)
        plt.text(0, -.02, r'SOURCE: https://nsidc.org/data/au_si12/versions/1', fontsize=5, rotation='horizontal',
             ha='left', color='darkgrey', transform=plt.gcf().transFigure)
        plt.text(.6, -.02, r'GRAPHIC: Frida Perez (@fridalejandra)', fontsize=5, rotation='horizontal', ha='left',
             color='darkgrey', transform=plt.gcf().transFigure)
        #plt.text(.01, 0.85, '2012', fontsize=30, rotation='horizontal', ha='left', color='white', transform=plt.gcf().transFigure)

        plt.title(title_name, loc='left', fontsize=25)
        figname = 'fig_{}.png'.format(i)
        mir = '/Users/fridaperez/Desktop/'
        dest = os.path.join(mir, figname)
        plt.savefig(dest,bbox_inches="tight",dpi=500)  # write image to file
        plt.tight_layout()
        print('Done.')


