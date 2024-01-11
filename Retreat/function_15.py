# Import packages
import numpy as np #deals with arrays
import matplotlib.pyplot as plt #plotting package
from pylab import *
import netCDF4
import pandas as pd
### Opening with xarray to do time selections
import xarray as xr #deals with multidimensional arrays
data = xr.open_dataset('/Volumes/WorkDrive/melt_dates/SIC_07132012_02232023.nc') # opening sit for xarray
## Arange months up to Aug to December ##
def is_months(month):
    return (month >= 8) & (month <= 12)
data = data.sel(time=is_months(data['time.month']))

## Select SIC variable ##
sic_xr = data.SI_12km_SH_ICECON_DAY_SpPolarGrid12km
latitude = data.GridLat_SpPolarGrid12km
longitude = data.GridLon_SpPolarGrid12km

## Here we want all the values that are over 100 (missing or land mask) to be set to nan ##
#sic_xr = sic_xr.where(sic_xr < 101,np.nan)
## Here we want all the values that are zero (open water) to be set to nan ##
#sic_xr = sic_xr.where(~np.isnan(sic_xr) & (sic_xr == 0), np.nan)
sic_xr = sic_xr.where(sic_xr == 0, 999)


# Because the desired output is one slice/ image/grid for each year, I will process year by year
def continuous_meet(cond, window_size, dim):
    """
    Continuously meet a given condition along a dimension.
    """
    _found = cond.rolling(dim={'time': window_size},
                          center=True).sum(skipna=True).fillna(False).astype(np.float)

    detected = np.array(
        _found.rolling(dim={'time': window_size})
        .reduce(lambda a, axis: (a == window_size).any(axis=axis))
        .fillna(False)
        .astype(bool)
    )

    indices = (detected * np.arange(detected.shape[0]).reshape(detected.shape[0], 1, 1))
    indices[indices == 0] = detected.shape[0]
    output = indices.argmin(axis=0)

    return xr.DataArray(output)

def Data_Array(breakup,year):
    file_yr = str(year)[-2:]
    temp_breakup = xr.DataArray(breakup)
    temp_breakup = xr.DataArray(
        data=temp_breakup,
        dims=["ygrid","xgrid"],
        coords=dict(
            longitude=(["ygrid","xgrid"],longitude),
            latitude=(["ygrid","xgrid"],latitude),
            ),
            attrs=dict(
            description="Sea Ice Breakup",
            ),
        )
    filename = f"y{file_yr}_break5d_15.nc"
    temp_breakup.to_netcdf(f'/Volumes/WorkDrive/melt_dates/files/5d_15p_dec_nc/netcdf/{filename}')

for year in list(range(2012,2023)):
    temp_da = sic_xr.sel(time=sic_xr.time.dt.year.isin([year]))
    breakup = continuous_meet(temp_da <= 15, window_size=5, dim='time')
    Data_Array(breakup,year)
    print('File created for:',year)





