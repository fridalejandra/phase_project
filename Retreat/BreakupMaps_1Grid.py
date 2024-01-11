import numpy as np
import csv
import glob
import matplotlib as mpl, matplotlib.pyplot as plt
import xarray as xr
import seaborn as sns
import netCDF4 as nc
import os
from matplotlib import ticker
from netCDF4 import Dataset
import calendar as cal
from matplotlib.colors import ListedColormap, BoundaryNorm
import cmocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from pylab import *
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

sns.set(color_codes=True)
plt.style.use('ggplot')

# Load the netCDF dataset
sicnc = nc.Dataset('/Volumes/WorkDrive/melt_dates/seaiceconc.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

# Specify the directory containing the netCDF files
dir = '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/'
Mytitle = list(map(str, list(range(2010, 2022))))

# Create a figure to hold all subplots
fig = plt.figure(figsize=(15, 10))

for i, title_name in zip(os.listdir(dir), Mytitle):
    if i.endswith('.nc'):
        data = nc.Dataset(os.path.join(dir, i))
        ice = data['__xarray_dataarray_variable__'][:]

        ax = fig.add_subplot(3, 4, i, projection=ccrs.Stereographic(central_longitude=180, central_latitude=-90))
        ax.set_extent([-180, 180, -90, -50], crs=ccrs.PlateCarree())

        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.LAND, facecolor='dimgrey')
        ax.add_feature(cfeature.OCEAN, facecolor='white')
        ax.gridlines(draw_labels=False, linewidth=0.4, color='k', alpha=0.5)

        lon_lat_labels = {
            (35, -58): 'KHVII',
            (140, -58): 'EA',
            (-135, -53): 'RAS',
            (-94, -52): 'ABS',
            (-46, -53): 'WS'
        }

        for (lon, lat), label in lon_lat_labels.items():
            ax.text(lon, lat, label, fontsize=6, fontweight='light', color='white', va='center', ha='center', transform=ccrs.PlateCarree())

        im = ax.contourf(longitude, latitude, ice, cmap='viridis', transform=ccrs.PlateCarree())
        cbar = plt.colorbar(im, ax=ax, drawedges=True, orientation='horizontal', pad=0.15)
        cbar.set_label('DAYS SINCE AUGUST')

        ax.text(0, 0, r'DATA:  AMSR-E/AMSR2 [Meier, W. N., T. Markus, and J. C. Comiso, 2018]', fontsize=5,
                rotation='horizontal', ha='left', color='darkgrey', transform=fig.transFigure)
        ax.text(0, -0.02, r'SOURCE: https://nsidc.org/data/au_si12/versions/1', fontsize=5, rotation='horizontal',
                ha='left', color='darkgrey', transform=fig.transFigure)
        ax.text(0.6, -0.02, r'GRAPHIC: Frida Perez (@fridalejandra)', fontsize=5, rotation='horizontal', ha='left',
                color='darkgrey', transform=fig.transFigure)
        ax.set_title(title_name, fontsize=25)

# Save the figure
plt.tight_layout()
figname = 'grid_of_maps.png'
mir = '/Users/fridaperez/Desktop/'
dest = os.path.join(mir, figname)
plt.savefig(dest, bbox_inches="tight", dpi=500)
plt.show()
