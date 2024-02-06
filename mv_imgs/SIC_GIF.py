import xarray as xr
import os, glob
import imageio
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import *
from matplotlib import rcParams
import cmocean

## Aesthetics
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
sns.set(color_codes=True)
plt.style.use('ggplot')
plt.style.use('dark_background')

# Open the netCDF file
dir = "/Users/fridaperez/Developer/repos/phase_project/mv_imgs/"
sic_data = xr.open_dataset("/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc")
sic = sic_data.SI_12km_SH_ICECON_DAY_SpPolarGrid12km[:]
lat = sic_data.GridLat_SpPolarGrid12km.data[:]
lon = sic_data.GridLon_SpPolarGrid12km.data[:]

date_list = pd.date_range(start="2012-07-13", end="2013-07-13", freq='D')
# Define the `days` list for a one-year dataset (2016 is a leap year)
days = list(range(0, 366))  # Adjust the range based on your dataset's actual length

for i, day in enumerate(days):
    plt.figure(figsize=(8, 6))
    map = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
    x, y = map(lon, lat)
    map.drawmapboundary(fill_color='grey')
    map.fillcontinents(color='grey')
    map.drawlsmask(land_color='white', ocean_color='k')
    map.drawcoastlines(color='white', linewidth=0.)

    # Draw parallels and Meridians
    map.drawparallels(np.arange(-80., 0., 20.), labels=[False, False, False, False], linewidth=0.4, color='k',fontsize=5)
    meridians = np.arange(0., 360., 30.)
    map.drawmeridians(meridians, labels=[1, 1, 1, 1], linewidth=0.4, color='white', fontsize=5, textcolor='white')

    # Format date as a string
    formatted_date = date_list[day].strftime('%Y-%m-%d')

    plt.title(formatted_date, fontsize=35, y=1.03)

    cs = map.contourf(x, y, sic[day], cmap=cmocean.cm.ice, levels=[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

    plt.colorbar()
    plt.tight_layout()
    plt.savefig(dir + 'sic16_days_' + formatted_date + '.png')

# Sort the image files by filename
variable_cb_images = sorted(glob.glob(dir + 'sic16_days_*'))

var = [imageio.imread(file) for file in variable_cb_images]
imageio.mimsave(dir + '/movie_variable_cb.gif', var, fps=10)
