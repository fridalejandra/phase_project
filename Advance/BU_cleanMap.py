import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc

## Sans Serif ##
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']

#Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Volumes/WorkDrive/melt_dates/seaiceconc.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

# Data file paths
data_files = [
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y12_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y13_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y14_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y15_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y16_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y17_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y18_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y19_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y20_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y21_break5d_15.nc',
    '/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y21_break5d_15.nc',
]

# Open datasets and store DataArrays in a list
data_arrays = []
for file in data_files:
    ds = xr.open_dataset(file)
    data_arrays.append(ds['__xarray_dataarray_variable__'])

# Determine the number of subplots based on the number of data arrays available
# n_rows = len(data_arrays) // 6
# n_cols = min(len(data_arrays), 6)

# Create subplots for each year
fig, axes = plt.subplots(3, 4, figsize=(15, 9))

for i, ax in enumerate(axes.flatten()):
    if i >= len(data_arrays):  # In case there are fewer data arrays than subplots
        ax.axis('off')
        continue

    year = 2012 + i
    ax.set_title(str(year), fontsize=6)
    map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True, ax=ax)
    x, y = map(longitude, latitude)
    map.fillcontinents(color='grey')
    map.drawmapboundary(fill_color='grey')
    map.drawlsmask(land_color='white', ocean_color='white')
    map.drawcoastlines(color='white', linewidth=0.)
    # Draw parallels and Meridians
    map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k', fontsize=5)
    meridians = np.arange(0., 360., 30.)
    map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='white', fontsize=5, textcolor='white')
    cs = map.contourf(x, y, data_arrays[i][:], cmap='viridis')

    # # ADD Colorbar
    # cbar = map.colorbar(cs, location='right', drawedges=True, pad=0.20, ax=ax)
    # cbar.set_label('Dates since August')

# Move the `plt.savefig()` function outside the loop
plt.subplots_adjust(wspace=0.05, hspace=0.05, right=0.8)
plt.tight_layout()
plt.savefig('/Users/fridaperez/Desktop/years_white.png', bbox_inches="tight", dpi=300)
plt.show()
