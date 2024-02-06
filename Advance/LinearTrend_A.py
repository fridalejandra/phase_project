import xarray as xr
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from xarrayutils.utils import linear_trend



def add_time_dim(xda):
    xda = xda.expand_dims(time = [datetime.now()])
    return xda

time_da = pd.date_range(start=pd.Timestamp(2013, 1, 1), periods=11, freq='A-FEB')

ds = xr.open_mfdataset('/Users/fridaperez/Developer/repos/phase_project/Advance/nan/nan_20*_A_5d_15p.nc', preprocess=add_time_dim, combine='nested',concat_dim='time')
ds = ds.assign_coords(time=time_da)
ds.load()
# create an array
BU_regressed = linear_trend(ds.__xarray_dataarray_variable__, 'time')
BU_regressed

BU_regressed.slope.plot(robust=True)
BU_regressed.p_value.plot(robust=True)

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import netCDF4 as nc

## Sans Serif ##
from matplotlib import rcParams
## Aesthetics
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
sns.set(color_codes=True)
plt.style.use('ggplot')
plt.style.use('dark_background')

# Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]
pval = BU_regressed.p_value
pval_95 = pval.where(pval<0.05)

# Create subplots only for the desired years
fig, ax =  plt.subplots(1,1,figsize=(16, 8))
#clev = np.linspace(-5,5,2)
#clev = np.linspace(-10,10,8)
clev = np.arange(-5, 6, 1)

# clev1 = np.linspace(0.5,0.6,0.8,0.9])


m = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
x_bu, y_bu = m(longitude, latitude)
m.drawcoastlines(color='k', linewidth=0.5)
parallels = np.arange(-80., 0., 20.)
m.fillcontinents(color='grey')
m.drawlsmask(land_color='black', ocean_color='k')


cs = m.contourf(x_bu, y_bu, BU_regressed.slope, cmap='coolwarm', levels=clev,alpha=0.8) #extend='both'
#ct = m.contour(x_bu, y_bu, pval_95, colors='none',hatches=['///'],levels=[0, 1])
ct = m.contourf(x_bu, y_bu, pval_95, colors='green', levels=[0, 0.05], hatches=['////'], extend='both')


# Add a common colorbar
#cax = fig.add_axes([0.06, 0.09, 0.7, 0.03])  # Adjust the position as needed
cbar = plt.colorbar(cs, orientation='horizontal',shrink=0.5) # extend='both'
cbar.set_label('DAY OF ADVANCE TREND',fontsize=14)
# cbar.tick_params(labelsize=14)
# Adjust layout and save the figure
plt.tight_layout()

#plt.title("Retreat (2012-2022)",fontsize=20)

#plt.show()

# Move the `plt.savefig()` function outside the loop
plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/A_Trend_13-23_black.png', bbox_inches="tight", dpi=500)
