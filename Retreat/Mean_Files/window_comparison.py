import numpy as np #deals with arrays
import matplotlib.pyplot as plt #plotting package
import xarray as xr #deals with multidimensional arrays
import seaborn as sns; sns.set(color_codes=True) # plotting aes
plt.style.use('ggplot')
import netCDF4 as nc  #deals with nc files
from mpl_toolkits.basemap import Basemap # plots maps

data3 = xr.open_dataset('/Users/fridaperez/Developer/repos/phase_project/Retreat/Mean_Files/2012_23_mean_xr_15p.nc')
data5 = xr.open_dataset('/Users/fridaperez/Developer/repos/phase_project/Retreat/Mean_Files/2012_23_mean_xr_3d.nc')
data7 = xr.open_dataset('/Users/fridaperez/Developer/repos/phase_project/Retreat/Mean_Files/2012_23_mean_xr_7d.nc')

mean3 = data3.__xarray_dataarray_variable__
mean5 = data5.__xarray_dataarray_variable__
mean7 = data7.__xarray_dataarray_variable__
print(mean5)
#
#Here we use the netcdf package to assing all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import seaborn as sns
import netCDF4 as nc
from mpl_toolkits.basemap import Basemap
import seaborn as sns


# Set plotting style
sns.set(color_codes=True)
plt.style.use('ggplot')

plt.style.use('dark_background')
# Plotting
fig, axes = plt.subplots(1, 3, figsize=(15, 9), sharex=True, sharey=True)
cmap = 'viridis'

def plot_map(ax, mean_data):
    map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True, ax=ax)
    x, y = map(longitude, latitude)
    map.drawmapboundary(fill_color='white')
    map.fillcontinents(color='dimgrey')
    map.drawlsmask(land_color='white', ocean_color='k')
    map.drawcoastlines(color='k', linewidth=0.5)
    map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k', fontsize=5)
    meridians = np.arange(-180., 180., 30.)
    map.drawmeridians(meridians, labels=[True, True, False, False], linewidth=0.4, color='k', fontsize=5, textcolor='white')
    cs = map.contourf(x, y, mean_data, cmap=cmap)
    return cs

cs1 = plot_map(axes[0], mean3)
#axes[0].set_title('15%',fontsize=20)

cs2 = plot_map(axes[1], mean5)
#axes[1].set_title('30%',fontsize=20)

cs3 = plot_map(axes[2], mean7)
#axes[2].set_title('40%',fontsize=20)

# # cbar = plt.colorbar(cs1, ax=axes, drawedges=True, orientation='horizontal', pad=0.15)
# # cbar.set_label('DAYS SINCE AUGUST')

plt.savefig('/Users/fridaperez/Desktop/windowcomp_dark.png', dpi=300)
plt.show()
