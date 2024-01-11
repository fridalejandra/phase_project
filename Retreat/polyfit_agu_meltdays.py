import numpy as np
import xarray as xr
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
# Import the NetCDF file and extract necessary variables
data = xr.open_dataset('/Volumes/WorkDrive/melt_dates/SIC_07132012_02232023.nc')
def is_months(month):
    return (month >= 8) & (month <= 12)

data = data.sel(time=is_months(data['time.month']))

sic_xr = data.SI_12km_SH_ICECON_DAY_SpPolarGrid12km
latitude = data.GridLat_SpPolarGrid12km
longitude = data.GridLon_SpPolarGrid12km

sic_xr = sic_xr.where(sic_xr < 101, np.nan)

def continuous_meet(cond, window_size, dim):
    _found = cond.rolling(dim={'time': window_size},
                          center=True).sum(skipna=True).fillna(False).astype(np.float)

    melt_time = np.array(
        _found.rolling(dim={'time': window_size})
        .reduce(lambda a, axis: (a == window_size).any(axis=axis))
        .fillna(False)
        .astype(bool)
    )

    melt_time = melt_time.argmax(axis=0)

    # Initialize arrays to store trend and p-value
    trend = np.zeros_like(melt_time, dtype=float)
    p_value = np.zeros_like(melt_time, dtype=float)

    # Apply OLS regression for each grid cell
    for i in range(melt_time.shape[1]):
        y = melt_time[:, i]
        x = np.arange(len(y))
        x = sm.add_constant(x)
        model = sm.OLS(y, x)
        results = model.fit()
        trend[i] = results.params[1]
        p_value[i] = results.pvalues[1]

    return trend, p_value

# Apply the modified function
result_trend, result_p_value = continuous_meet(sic_xr > 15, window_size=5, dim='time')

# Plot the result as heatmaps using seaborn
fig, axes = plt.subplots(ncols=2, figsize=(12, 5))
sns.heatmap(result_trend.reshape(1, -1), annot=True, cmap='coolwarm', ax=axes[0])
axes[0].set_title('Melt Trend')

sns.heatmap(result_p_value.reshape(1, -1), annot=True, cmap='coolwarm', ax=axes[1])
axes[1].set_title('P-Value')
plt.savefig('/Users/fridaperez/Desktop/2.png')

plt.show()
# plt.savefig('/Users/fridaperez/Desktop/2.png')
# plt.savefig('/Users/fridaperez/Desktop/1.png')
