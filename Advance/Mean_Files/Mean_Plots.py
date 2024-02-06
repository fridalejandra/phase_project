import numpy as np #deals with arrays
import matplotlib.pyplot as plt #plotting package
import xarray as xr #deals with multidimensional arrays
import seaborn as sns; sns.set(color_codes=True) # plotting aes
import netCDF4 as nc  #deals with nc files
from mpl_toolkits.basemap import Basemap # plots maps

# Sans Serif
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
plt.style.use('dark_background')
sns.set(color_codes=True)
plt.style.use('ggplot')
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors

## Load in data
data = xr.open_dataset('/Users/fridaperez/Developer/repos/phase_project/Advance/Mean_Files/2013_23_mean_xr_5d.nc')
mean = data.__xarray_dataarray_variable__
print(mean)

#### FOR PLOTTING PURPOSES ONLY #####

# Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]


fig = plt.figure(figsize=(10,8))
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
x, y = map(longitude, latitude)
map.drawmapboundary(fill_color='grey')
map.fillcontinents(color='grey')
map.drawlsmask(land_color='grey',ocean_color='k')
map.drawcoastlines(color='grey',linewidth=0.5)

# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.),labels=[False,False,False,False],linewidth=0.4,color='k',fontsize=5)
meridians = np.arange(-180., 180., 30.)
map.drawmeridians(meridians,labels=[True,True,False,False], linewidth=0.4,color='white',fontsize=8, textcolor='white')
map.contourf(x,y,mean,cmap='viridis')
cbar = plt.colorbar(drawedges=True, orientation='horizontal', pad = 0.15)
cbar.set_label('DAYS SINCE FEBRUARY',color='white')
cbar.ax.tick_params(axis='x', colors='white')

plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/Advance_mean12-22_black.png', dpi=500)