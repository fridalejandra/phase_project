import numpy as np
import csv
import glob
import matplotlib as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import xarray as xr
import seaborn as sns
import netCDF4 as nc
import os
os.environ["PROJ_LIB"] = "/path/to/proj/data/files"

from matplotlib import ticker
from netCDF4 import Dataset
import calendar as cal
from matplotlib.colors import ListedColormap, BoundaryNorm
import cmocean
import cartopy
from pylab import *
from matplotlib import rcParams
## Aesthetics
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
sns.set(color_codes=True)
plt.style.use('ggplot')
#plt.style.use('dark_background')

## Load the netCDF dataset
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

# Determine the number of rows and columns based on the number of years
years = list(range(2012, 2024))  # Start from 2012 and include 2023
num_years = len(years)
num_cols = 4  # Number of columns
num_rows = (num_years - 1) // num_cols + 1  # Calculate the number of rows

# Specify the directory containing the netCDF files
dir = '/Users/fridaperez/Developer/repos/phase_project/Retreat/nan/'

# Set up the figure and grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))
plt.subplots_adjust(wspace=0.05, hspace=0.05) #,right=0.85)

for i, year in enumerate(years):
    # Construct the full file path
    file_path = os.path.join(dir, f'nan_{year}_R_5d_15p.nc')

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
        map.drawcoastlines(color='white', linewidth=0.)

        # Draw parallels and Meridians
        map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
        meridians = np.arange(0., 360., 30.)
        map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='white', fontsize=5, textcolor='white')

        ax.set_title(str(year), fontsize=20,y=1.1)

        # Plot using imshow and set contour levels
        cs = map.contourf(x,y,ice,cmap='viridis')

        # Add a common colorbar
        #cax = fig.add_axes([0.15, -0.09, 0.7, 0.02])  # [left, bottom, width, height]
        cbar = plt.colorbar(cs)
        cbar.set_ticks([0, 25,45,65,85,105,125,145,165 ])

        cbar.set_label('DAYS SINCE AUGUST')

        # ## Citations
        # ax.text(0.14, 0.1, r'DATA:  AMSR-E/AMSR2 [Meier, W. N., T. Markus, and J. C. Comiso, 2018]', fontsize=5,
        #         rotation='horizontal', ha='left', color='darkgrey', transform=fig.transFigure)
        # ax.text(0.14,0.17, r'SOURCE: https://nsidc.org/data/au_si12/versions/1', fontsize=5, rotation='horizontal',
        #         ha='left', color='darkgrey', transform=fig.transFigure)
        # ax.text(0.14, 0.16, r'GRAPHIC: Frida Perez (@fridalejandra)', fontsize=5, rotation='horizontal', ha='left',
        #         color='darkgrey', transform=fig.transFigure)
# Save the figure
plt.tight_layout()
figname = 'grid_of_maps_R_white.png'
mir = '/Users/fridaperez/Desktop/Proposal/Proposal_Figures/'
dest = os.path.join(mir, figname)
plt.savefig(dest, dpi=500) #bbox_inches="tight"
#plt.show()