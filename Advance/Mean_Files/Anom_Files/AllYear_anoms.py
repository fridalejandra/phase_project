import numpy as np
import csv
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
import seaborn as sns
import netCDF4 as nc
from mpl_toolkits.basemap import Basemap
import os

# Sans Serif
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

# Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Volumes/WorkDrive/melt_dates/seaiceconc.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

# List of years (titles)
years = list(range(2012, 2023))  # Start from 2012 and include 2022

# Directory containing the .nc files
dir = '/Volumes/WorkDrive/freeze_dates/files/anoms/'

# Determine the number of rows and columns based on the number of years
num_years = len(years)
num_cols = 4  # Number of columns
num_rows = (num_years - 1) // num_cols + 1  # Calculate the number of rows

# Set up the figure and grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(16, 9))
plt.subplots_adjust(wspace=0.4, hspace=0.3)

for i, year in enumerate(years):
    # Construct the full file path
    file_path = os.path.join(dir, f'{year}anom.nc')

    if os.path.exists(file_path):
        data = nc.Dataset(file_path)
        ice = data['__xarray_dataarray_variable__'][:]
        row = i // num_cols
        col = i % num_cols
        ax = axes[row, col]

        map = Basemap(ax=ax, projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
        x, y = map(longitude, latitude)
        map.drawmapboundary(fill_color='white')
        map.fillcontinents(color='dimgrey')
        map.drawlsmask(land_color='white', ocean_color='k')
        map.drawcoastlines(color='k', linewidth=0.5)

        # Draw parallels and Meridians
        map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',
                          fontsize=5)
        meridians = np.arange(0., 360., 30.)
        map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=20, textcolor='white')

        ax.set_title(str(year), fontsize=20)

        # Plot using imshow and set contour levels
        li = map.imshow(ice, extent=[x.min(), x.max(), y.min(), y.max()], cmap='RdBu_r', vmin=-50, vmax=50) # im =

        # Add a common colorbar
        cax = fig.add_axes([0.15, 0.05, 0.7, 0.02])  # [left, bottom, width, height]
        cbar = plt.colorbar(li, cax=cax, orientation='horizontal')
        cbar.set_label('DAYS')
        plt.savefig('/Users/fridaperez/Desktop/Advance_anomsnew.png', dpi=300)  # write image to file