import numpy as np
import csv
import glob
import matplotlib as mpl, matplotlib.pyplot as plt
plt.style.use('dark_background')

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
import numpy as np
import datetime
import calendar as cal
from matplotlib.colors import ListedColormap, BoundaryNorm
import cmocean

## Sans Serif ##
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

# Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from mpl_toolkits.basemap import Basemap
import os

# Set the directory containing the NetCDF files
dir = '/Users/fridaperez/Developer/repos/phase_project/Retreat/nan/'

# Loop through each year from 2012 to 2023
for year in range(2012, 2024):
    # Create the filename for the corresponding year
    filename = f'nan_{year}_R_5d_15p.nc'

    # Load the NetCDF file
    data = nc.Dataset(os.path.join(dir, filename))
    ice = data['__xarray_dataarray_variable__'][:]

    # Create a figure and map
    fig, ax = plt.subplots(figsize=(6, 8))
    map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
    x, y = map(longitude, latitude)

    # Plot the map and add labels, title, etc.
    map.drawmapboundary(fill_color='white')
    map.fillcontinents(color='dimgrey')
    map.drawlsmask(land_color='white', ocean_color='k')
    map.drawcoastlines(color='k', linewidth=0.5)

    # Draw parallels and Meridians
    map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',
                      fontsize=5)
    meridians = np.arange(0., 360., 30.)
    map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='k', fontsize=5, textcolor='white')

    # Plot the sea ice data
    map.contourf(x, y, ice[:], cmap='viridis')

    # Create an axes for the colorbar to the right of the main plot
    cax = fig.add_axes([0.93, 0.15, 0.02, 0.7])  # Adjust position and size as needed
    cbar = plt.colorbar(drawedges=True, orientation='vertical', cax=cax)
    cbar.ax.set_aspect(15)  # Adjust the value as needed to make the colorbar smaller
    cbar.set_label('DAYS SINCE AUGUST', color='white')
    # Set color of colorbar ticks
    cbar.ax.yaxis.set_tick_params(color='white')
    for ticklabel in cbar.ax.get_yticklabels():
        ticklabel.set_color('white')

    # Add the year as the title
    plt.title(str(year), loc='left', fontsize=25, pad=20, color='white')

    # Save the figure
    figname = f'fig_{year}_R.png'
    mir = '/Users/fridaperez/Desktop/'  # Adjust the save directory as needed
    dest = os.path.join(mir, figname)
    plt.savefig(dest, bbox_inches="tight", dpi=500)  # Adjust dpi as needed

    # Close the figure to release memory
    plt.close()

    print('Done for year:', year)
