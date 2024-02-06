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
#plt.style.use('dark_background')
sns.set(color_codes=True)
plt.style.use('ggplot')
plt.style.use('dark_background')
# Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

# List of years (titles)
years = list(range(2013, 2024))  # Start from 2013 and include 2023

# Directory containing the .nc files
dir = '/Users/fridaperez/Developer/repos/phase_project/Advance/Mean_Files/Anom_Files/'

# Determine the number of rows and columns based on the number of years
num_years = len(years)
num_cols = 4  # Number of columns
num_rows = (num_years - 1) // num_cols + 1  # Calculate the number of rows

# Set up the figure and grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))
plt.subplots_adjust(wspace=0.08, hspace=0.24) #right=0.85

for i, year in enumerate(years):
    # Construct the full file path
    file_path = os.path.join(dir, f'anom_A_{year}.nc')

    if os.path.exists(file_path):
        data = nc.Dataset(file_path)
        ice = data['__xarray_dataarray_variable__'][:]
        row = i // num_cols
        col = i % num_cols
        ax = axes[row, col]

        map = Basemap(ax=ax, projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
        x, y = map(longitude, latitude)
        map.drawmapboundary(fill_color='grey')
        map.fillcontinents(color='grey')
        map.drawlsmask(land_color='white', ocean_color='k')
        map.drawcoastlines(color='white', linewidth=0.5)

        # Draw parallels and Meridians
        map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
        meridians = np.arange(0., 360., 30.)
        map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='white', fontsize=5, textcolor='white')

        ax.set_title(str(year), fontsize=20, y=1.06, color='white')

        # Plot using imshow and set contour levels
        im = map.imshow(ice, extent=[x.min(), x.max(), y.min(), y.max()], cmap='RdBu_r', vmin=-50, vmax=50)

# Remove the last subplot if num_years is less than num_rows * num_cols
if num_years < num_rows * num_cols:
    fig.delaxes(axes.flatten()[-1])

# Add a common colorbar
cax = fig.add_axes([0.15, 0.05, 0.7, 0.02])  # [left, bottom, width, height]
cbar = plt.colorbar(im, cax=cax, orientation='horizontal')
cbar.set_label('DAYS', color='white')
cbar.ax.tick_params(axis='x', colors='white')

plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/AnomYrs_A_black.png', bbox_inches="tight", dpi=500)  # write image to file