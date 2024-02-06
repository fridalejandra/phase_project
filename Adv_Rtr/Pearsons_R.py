import xarray as xr
import glob
import numpy as np
from scipy import stats
from datetime import datetime
import pandas as pd
import xskillscore as xs
import matplotlib.pyplot as plt

def add_time_dim(xda):
    xda = xda.expand_dims(time=[datetime.now()])
    return xda

time_A = pd.date_range(start=pd.Timestamp(2012, 1, 1), periods=12, freq='A-AUG')
time_R = pd.date_range(start=pd.Timestamp(2012, 1, 1), periods=12, freq='A-AUG')

print('time advance:', time_A)
print('time retreat:', time_R)

ds1 = xr.open_mfdataset('/Users/fridaperez/Developer/repos/phase_project/Retreat/nan/nan_20*_R_5d_15p.nc', preprocess=add_time_dim, combine='nested', concat_dim='time')
ds1 = ds1.assign_coords(time=time_R)
ds1.load()

ds2 = xr.open_mfdataset('/Users/fridaperez/Developer/repos/phase_project/Advance/nan/nan_20*_A_5d_15p.nc', preprocess=add_time_dim, combine='nested', concat_dim='time')
ds2 = ds2.assign_coords(time=time_A)
ds2.load()

# Check for NaN values and replace them with a fill value (e.g., 0)
ds1 = ds1.fillna(0)
ds2 = ds2.fillna(0)

# Data value extraction
var_R = ds1.__xarray_dataarray_variable__
var_A = ds2.__xarray_dataarray_variable__

# Calculate Pearson correlation coefficient with NaN handling
r = xs.pearson_r(var_A, var_R, dim='time', skipna=True)
print(r)

import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import netCDF4 as nc
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


# Create subplots only for the desired years
fig, ax = plt.subplots(1,1,figsize=(16, 8))

# Add labels and title
m = Basemap(projection='spstere', boundinglat=-50, lon_0=180, resolution='l', round=True)
x_bu, y_bu = m(longitude, latitude)
m.drawcoastlines(color='k', linewidth=0.5)
parallels = np.arange(-80., 0., 20.)
m.fillcontinents(color='grey')
m.drawlsmask(land_color='black', ocean_color='k')


cs = m.contourf(x_bu, y_bu, r, cmap='PRGn',alpha=0.8) #extend='both'

# Add a common colorbar
cbar = plt.colorbar(cs, orientation='horizontal',shrink=0.5) # extend='both'
cbar.set_label('CORRELATION COEFFICIENTS',fontsize=14)
# Adjust layout and save the figure
plt.tight_layout()
#plt.show()

# Move the `plt.savefig()` function outside the loop
plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/Pearsons_R_black.png', bbox_inches="tight", dpi=500)


