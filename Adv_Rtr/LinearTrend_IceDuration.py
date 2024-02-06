import os
import xarray as xr
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from xarrayutils.utils import linear_trend
import netCDF4 as nc

# Define the years you want to process
years = range(2013, 2024)  # Adjust the range as needed

# Define the directory where the files are located
dir_A = '/Users/fridaperez/Developer/repos/phase_project/Advance/nan'  # Modify the directory path
dir_R = '/Users/fridaperez/Developer/repos/phase_project/Retreat/nan'  # Modify the directory path

ice_season_durations = []  # Initialize a list to store ice season duration for each year

for year in years:
    # Construct the full file paths for advance and retreat files
    advance_file_path = os.path.join(dir_A, f'nan_{year}_A_5d_15p.nc')
    retreat_file_path = os.path.join(dir_R, f'nan_{year}_R_5d_15p.nc')

    # Check if the advance and retreat files exist for the current year
    if os.path.exists(advance_file_path) and os.path.exists(retreat_file_path):
        # Read data from the advance file
        advance_data = nc.Dataset(advance_file_path)
        advance_ice = advance_data['__xarray_dataarray_variable__'][:]  # Replace '__xarray_dataarray_variable__' with the actual variable name

        # Read data from the retreat file
        retreat_data = nc.Dataset(retreat_file_path)
        retreat_ice = retreat_data['__xarray_dataarray_variable__'][:]  # Replace '__xarray_dataarray_variable__' with the actual variable name

        # Convert NumPy masked arrays to xarray DataArray
        advance_ice = xr.DataArray(advance_ice)
        retreat_ice = xr.DataArray(retreat_ice)

        # Calculate ice season duration for the current year
        ice_season_duration = retreat_ice - advance_ice

        # Append the ice season duration for the current year to the list
        ice_season_durations.append(ice_season_duration)

        # Close the netCDF files
        advance_data.close()
        retreat_data.close()
    else:
        print(f"Files for year {year} not found.")

# Concatenate ice season durations along a new dimension
ice_season_duration_combined = xr.concat(ice_season_durations, dim='year')
print(ice_season_duration_combined)

# # Calculate the linear trend for the combined ice season duration
# create an array
dur_regressed = linear_trend(ice_season_duration_combined, 'year')

dur_regressed.slope.plot(robust=True)
dur_regressed.p_value.plot(robust=True)

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
pval = dur_regressed.p_value
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


cs = m.contourf(x_bu, y_bu, dur_regressed.slope, cmap='coolwarm', levels=clev,alpha=0.8) #extend='both'
#ct = m.contour(x_bu, y_bu, pval_95, colors='none',hatches=['///'],levels=[0, 1])
ct = m.contourf(x_bu, y_bu, pval_95, colors='green', levels=[0, 0.05], hatches=['////'], extend='both')


# Add a common colorbar
#cax = fig.add_axes([0.06, 0.09, 0.7, 0.03])  # Adjust the position as needed
cbar = plt.colorbar(cs, orientation='horizontal',shrink=0.5) # extend='both'
cbar.set_label('ICE SEASON DURATION TREND',fontsize=14)
# cbar.tick_params(labelsize=14)
# Adjust layout and save the figure
plt.tight_layout()

#plt.title("Retreat (2012-2022)",fontsize=20)

#plt.show()

# Move the `plt.savefig()` function outside the loop
plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/Duration_Trend_13-23_black.png', bbox_inches="tight", dpi=500)

