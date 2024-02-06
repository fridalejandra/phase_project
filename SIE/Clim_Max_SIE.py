"""
Plots Antarctic  climatological maximum sea ice extent from August 2000-present
using NSCIDC metadata

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Frida A. Perez
Date      : 25 January 2024
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import pandas as pd

## Data
# Load url
data = '/Users/fridaperez/Developer/repos/phase_project/SIE/Decade_Means.csv'
df = pd.read_csv(data)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#plt.style.use('dark_background')

### Plot figure
matplotlib.rc('savefig', facecolor='white')
matplotlib.rc('axes', edgecolor='black')
matplotlib.rc('xtick', color='black')
matplotlib.rc('ytick', color='black')
matplotlib.rc('axes', labelcolor='black')
matplotlib.rc('axes', facecolor='white')
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Avant Garde']})

### Adjust axes in time series plots
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])


# Create a day of year (doy) column
df['DOY'] = np.arange(1, len(df) + 1)

# Extract relevant data for August to November (213-304)
df_aug_nov = df[(df['DOY'] >= 213) & (df['DOY'] <= 304)]


# Extract relevant data
doy = df_aug_nov['DOY']
mean_1990s = df_aug_nov['Mean1990s']
mean_2000s = df_aug_nov['Mean2000s']
mean_2010s = df_aug_nov['Mean2010s']
values_2023 = df_aug_nov['2023']

# Find lowest values for each year
highest_values = df_aug_nov.iloc[:, 5:].idxmax(axis=1)
highest_values = df_aug_nov.max(axis=1)

# Plotting
plt.figure(figsize=(10, 6))

# Plot mean values for each decade
plt.plot(doy, mean_1990s,linewidth=3, linestyle='--',color='c', label='1990s Mean', alpha=0.8)
plt.plot(doy, mean_2000s,linewidth=3, linestyle='--',color='dodgerblue', label='2000s Mean', alpha=0.8)
plt.plot(doy, mean_2010s,linewidth=3, linestyle='--', color='darkmagenta', label='2010s Mean', alpha=0.8)

# Plot values for 2023
plt.plot(doy, values_2023, label='2023', color='r',linestyle='-',)

# Explicitly specify the columns you want to consider
columns_to_plot = ['2012', '2013', '2014', '2015',
                   '2016','2017','2018', '2019',
                   '2020', '2021','2022','2023']
# '2008', '2009','2010','2011',
#'2000', '2001', '2002', '2003','2004','2005','2006', '2007',
# Step 1: Find the indices of the minimum values for each specified column
max_indices = df[columns_to_plot].idxmax()

# Step 2: Create a scatter plot with these minimum values
plt.scatter(max_indices, df[columns_to_plot].max(),c=np.arange(len(columns_to_plot)), cmap='plasma_r',edgecolors='black')
custom_offset = 7
for i, col in enumerate(columns_to_plot):
    plt.annotate(col, (max_indices[col], df[col].max()), textcoords="offset points", xytext=(0, custom_offset), ha='center', fontsize=9, color='black')


# Add labels and title
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}', fontsize=15, color='black')#color='darkgrey')
# Define x labels explicitly
xlabels = ['Aug', 'Sep', 'Oct', 'Nov']

# Set x-axis tick positions and labels
plt.xticks(doy[::30], xlabels)

# Set x-axis limits
plt.xlim(213, 304)

# Set x-axis tick positions and labels
plt.xticks(doy[::30], xlabels, fontsize=10, color='black', fontname='Avant Garde')
# Set y-axis tick labels font properties
plt.yticks(fontsize=10, color='black', fontname='Avant Garde')


# Show plot
plt.legend(shadow=False, fontsize=7.5, loc='upper left',
               bbox_to_anchor=(0.787, 0.163), fancybox=True, ncol=1, frameon=False)
plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/Clim_Max_white.png',dpi=300)


