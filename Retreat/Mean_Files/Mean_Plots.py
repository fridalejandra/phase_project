import numpy as np #deals with arrays
import matplotlib.pyplot as plt #plotting package
import xarray as xr #deals with multidimensional arrays
import seaborn as sns; sns.set(color_codes=True) # plotting aes
plt.style.use('ggplot')
import netCDF4 as nc  #deals with nc files
from mpl_toolkits.basemap import Basemap # plots maps

data = xr.open_dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/12-23_meanbreakup.nc')
#/Volumes/WorkDrive/melt_dates/mean/data_mean_np.nc        1
#/Volumes/WorkDrive/melt_dates/mean/data_mean_np_nan.nc    2
#/Volumes/WorkDrive/melt_dates/mean/data_mean_timmean.nc   3
#/Volumes/WorkDrive/melt_dates/mean/data_mean_xr.nc        4
#/Volumes/WorkDrive/melt_dates/mean/data_mean_xr_nan.nc    5

mean = data.__xarray_dataarray_variable__
print(mean)

#### FOR PLOTTING PURPOSES ONLY #####

#Here we use the netcdf package to assing all variables
sicnc = nc.Dataset('/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/nan/nan_y2012_break5d_15.nc')
print(sicnc)
latitude = sicnc.variables['latitude'][:]
longitude = sicnc.variables['longitude'][:]

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors

fig = plt.figure(figsize=(10,8))
#plt.style.use('dark_background')

 # Plotting
fig = plt.figure()
ax = fig.add_subplot(111)
map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
x, y = map(longitude, latitude)
map.drawmapboundary(fill_color='white')
map.fillcontinents(color='dimgrey')
map.drawlsmask(land_color='white',ocean_color='k')
map.drawcoastlines(color='k',linewidth=0.5)

# Draw parallels and Meridians
map.drawparallels(np.arange(-80., 0., 20.),labels=[False,False,False,False],linewidth=0.4,color='k',fontsize=5)
meridians = np.arange(-180., 180., 30.)
map.drawmeridians(meridians,labels=[True,True,False,False], linewidth=0.4,color='k',fontsize=5, textcolor='white')
map.contourf(x,y,mean,40,cmap='viridis')
cbar = plt.colorbar(drawedges=True, orientation='horizontal', pad = 0.15)
cbar.set_label('DAYS SINCE JULY')
plt.savefig('/Users/fridaperez/Desktop/Retreat_mean12-22.png', dpi=500)