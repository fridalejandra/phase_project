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

#### NC Files ####
ds = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y12_break5d_15.nc')
ds1 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y13_break5d_15.nc')
ds2 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y14_break5d_15.nc')
ds3 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y15_break5d_15.nc')
ds4 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y16_break5d_15.nc')
ds5 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y17_break5d_15.nc')
ds6 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y18_break5d_15.nc')
ds7 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y19_break5d_15.nc')
ds8 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y20_break5d_15.nc')
ds9 = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y21_break5d_15.nc')
###################################################################################################

ice12 = ds['__xarray_dataarray_variable__'][:]
ice13 = ds1['__xarray_dataarray_variable__'][:]
ice14 = ds2['__xarray_dataarray_variable__'][:]
ice15 = ds3['__xarray_dataarray_variable__'][:]
ice16 = ds4['__xarray_dataarray_variable__'][:]
ice17 = ds5['__xarray_dataarray_variable__'][:]
ice18 = ds6['__xarray_dataarray_variable__'][:]
ice19 = ds7['__xarray_dataarray_variable__'][:]
ice20 = ds8['__xarray_dataarray_variable__'][:]
ice21 = ds9['__xarray_dataarray_variable__'][:]

### YEAR PLOTS ####
plt.style.use('dark_background')
fig, axes = plt.subplots(3, 4)
for axis in axes:
    print(type(axis))
    axes=axes.flatten()
#########################2012#############################################
axes[0].set_title("2012",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True, ax=axes[0])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
clr1 = map.contourf(x, y, ice12[:], cmap='viridis')
##########################2013#########################
axes[1].set_title("2013",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[1])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice13[:], cmap='viridis')
##########################2014#########################
axes[2].set_title("2014",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[2])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice14[:], cmap='viridis')
##########################2015#########################
axes[3].set_title("2015",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[3])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice15[:], cmap='viridis')
##########################2016#########################
axes[4].set_title("2016",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[4])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice16[:], cmap='viridis')
##########################2017#########################
axes[5].set_title("2017",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[5])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice17[:], cmap='viridis')
##########################2018#########################
axes[6].set_title("2018",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[6])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice18[:], cmap='viridis')
##########################2019#########################
axes[7].set_title("2019",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[7])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice19[:], cmap='viridis')
##########################2020#########################
axes[8].set_title("2020",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[8])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice20[:], cmap='viridis')
##########################2021#########################
axes[9].set_title("2021",fontsize=6)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True,ax=axes[9])
x, y = map(longitude, latitude)
map.fillcontinents(color='dimgrey')
map.drawmapboundary(fill_color='white')
map.drawlsmask(land_color='white', ocean_color='k')
map.drawcoastlines(color='k', linewidth=0.)
# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
meridians = np.arange(0., 360., 30.)
map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')
map.contourf(x, y, ice21[:], cmap='viridis')

plt.subplots_adjust(wspace=0.05, hspace=0.05, right=0.8)
plt.tight_layout()
#fig.colorbar(clr1,label= 'DAYS SINCE AUGUST',orientation='horizontal')
plt.savefig('/Users/fridaperez/Desktop/years.png',bbox_inches="tight",dpi=300)  # write image to file
