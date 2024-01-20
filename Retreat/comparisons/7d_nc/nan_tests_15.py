#### Python File must be in folder with .nc files ####
import numpy as np
import csv
import glob
import matplotlib as plt
import matplotlib.pyplot as plt
# %matplotlib inline
import xarray as xr
import seaborn as sns;
import netCDF4 as nc
from pylab import *
import os
from netCDF4 import Dataset
import numpy as np


#Here we use the netcdf package to assign all variables
sicnc = nc.Dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc')
latitude = sicnc.variables['GridLat_SpPolarGrid12km'][:]
longitude = sicnc.variables['GridLon_SpPolarGrid12km'][:]

## Automate this for all the files ##

dir = '/Users/fridaperez/Developer/repos/phase_project/Retreat//comparisons/7d_nc/'
count = 0
files = []
for i in os.listdir(dir):
    if i.endswith('.nc'):
        files.append(open(i))
        data = xr.open_dataarray(i)
        ice = data.values

        ice = ice.astype(np.float32)
        ## now that our data is a numpy array, we can convert the zeros and two's into NaNs for a cleaner plot ##
        BU_nan = ice.copy()
        BU_nan[BU_nan == 0.0] = np.nan
       # BU_nan[BU_nan == 1.0] = np.nan
        # BU_nan[BU_nan == 2.0] = np.nan
        # BU_nan[BU_nan == 3.0] = np.nan
        #BU_nan[BU_nan == 4.0] = np.nan
        BU_nan[BU_nan == 6.0] = np.nan


        breakup = xr.DataArray(BU_nan)
        breakup = xr.DataArray(
            data=breakup,
            dims=["ygrid","xgrid"],
            coords=dict(
                longitude=(["ygrid","xgrid"],longitude),
                latitude=(["ygrid","xgrid"],latitude),
                ),
                attrs=dict(
                description="Sea Ice Breakup",
                ),
        )

        figname = 'nan_{}'.format(i)
        mir = '/Users/fridaperez/Developer/repos/phase_project/Retreat/comparisons/7d_nan/'
        dest = os.path.join(mir, figname)
        breakup.to_netcdf(dest)  # write image to fill
        print('Done.')
