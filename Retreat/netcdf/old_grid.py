import numpy as np
import csv
import glob
import matplotlib
from matplotlib import pyplot as plt
import xarray as xr
import seaborn as sns
import netCDF4 as nc
import os
os.environ["PROJ_LIB"] = "/path/to/proj/data/files"
from matplotlib import ticker
from netCDF4 import Dataset
import calendar as cal
from matplotlib.colors import Normalize
import cmocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import re

from pylab import *
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

sns.set(color_codes=True)
plt.style.use('ggplot')

# Load the netCDF dataset
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

# Assuming you have 'ice' data loaded from the netCDF file
ice = sicnc.variables['SI_12km_SH_ICECON_DAY_SpPolarGrid12km'][:]
import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Specify the directory containing the netCDF files
dir = '/Users/fridaperez/Developer/repos/phase_project/Retreat/nan/'
data_files = [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith('.nc')]
#plt.style.use('dark_background')

# Create a figure to hold all subplots
fig, axes = plt.subplots(3, 4, figsize=(15, 9))

data_arrays = []
for file in data_files:
    ds = xr.open_dataset(file)
    data_arrays.append(ds['__xarray_dataarray_variable__'])
    print(data_arrays)

# Define a normalization for the colorbar
norm = Normalize(vmin=min([da.min() for da in data_arrays]), vmax=max([da.max() for da in data_arrays]))

for i, ax in enumerate(axes.flatten()):
    if i >= len(data_arrays):  # In case there are fewer data arrays than subplots
        ax.axis('off')
        continue

    year = 2012 + i
    ax.set_title(str(year), fontsize=20)

    map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True, ax=ax)
    x, y = map(longitude, latitude)

    map.fillcontinents(color='grey')
    map.drawmapboundary(fill_color='grey')
    map.drawlsmask(land_color='white', ocean_color='k')
    map.drawcoastlines(color='white', linewidth=0.)

    # Draw parallels and Meridians
    map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k', fontsize=5)
    meridians = np.arange(0., 360., 30.)
    map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='white', fontsize=5, textcolor='white')

    cs = map.contourf(x, y, data_arrays[i,:], cmap='viridis', norm=norm)

# ADD Colorbar outside the loop
#cbar_ax = fig.add_axes([0.96, 0.15, 0.02, 0.7])
cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.02])  # [left, bottom, width, height]
cbar = fig.colorbar(cs, cax=cbar_ax,orientation='horizontal')
cbar.set_label('DATES SINCE AUGUST')

# Manually adjust layout
plt.subplots_adjust(wspace=0.05, hspace=0.05, right=0.85)
plt.tight_layout()

# Move the `plt.savefig()` function outside the loop
plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/1Grid_BU_white.png', bbox_inches="tight", dpi=300)
plt.show()
