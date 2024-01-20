# Import packages
import numpy as np #deals with arrays
import matplotlib.pyplot as plt #plotting package
from pylab import *
import netCDF4
import pandas as pd
### Opening with xarray to do time selections
import xarray as xr #deals with multidimensional arrays
data = xr.open_dataset('/Users/fridaperez/Developer/repos/phase_project/SIC_07132012_01012024.nc') # opening sit for xarray
## Arange months up to Aug to December ##
def is_months(month):
    return (month >= 8) & (month <= 12)
data = data.sel(time=is_months(data['time.month']))

## Select SIC variable ##
sic_xr = data.SI_12km_SH_ICECON_DAY_SpPolarGrid12km
latitude = data.GridLat_SpPolarGrid12km
longitude = data.GridLon_SpPolarGrid12km

#sic_xr = sic_xr.where(sic_xr < 101,np.nan)
## Here we want all the values that are zero (open water) to be set to nan ##
sic_xr = sic_xr.where(sic_xr == 0, np.nan)

## Because the desired output is one slice/ image/grid for each year, I will process year by year
def continuous_meet(cond, window_size, dim):
    """
    Continuously meet a given condition along a dimension.
    """
    _found = cond.rolling(dim={'time': window_size},
                          center=True).sum(skipna=True).fillna(False).astype(np.float32)

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
            longitude=(["ygrid","xgrid"],data.GridLon_SpPolarGrid12km),
            latitude=(["ygrid","xgrid"],data.GridLat_SpPolarGrid12km),
            ),
            attrs=dict(
            description="Sea Ice Breakup",
            ),
        )
    filename = f"yr{file_yr}R_3d_15p.nc"
    temp_breakup.to_netcdf(f'/Users/fridaperez/Developer/repos/phase_project/Retreat/3d_comp/{filename}')

for year in list(range(2012,2024)):
    temp_da = sic_xr.sel(time=sic_xr.time.dt.year.isin([year]))
    breakup = continuous_meet(temp_da <= 15, window_size=3, dim='time')
    Data_Array(breakup,year)
    print('File created for:',year)





