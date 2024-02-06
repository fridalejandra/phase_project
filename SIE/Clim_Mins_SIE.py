"""
Plots Antarctic  climatological minimum sea ice extent from January 2000-present
using NSCIDC metadata

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Frida A. Perez
Date      : 20 August 2017
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
plt.style.use('dark_background')

### Plot figure
matplotlib.rc('savefig', facecolor='black')
matplotlib.rc('axes', edgecolor='white')
matplotlib.rc('xtick', color='white')
matplotlib.rc('ytick', color='white')
matplotlib.rc('axes', labelcolor='white')
matplotlib.rc('axes', facecolor='black')
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

# Extract relevant data for January to April (1-120)
df_jan_apr = df[df['DOY'] <= 105]

# Extract relevant data
doy = df_jan_apr['DOY']
mean_1990s = df_jan_apr['Mean1990s']
mean_2000s = df_jan_apr['Mean2000s']
mean_2010s = df_jan_apr['Mean2010s']
values_2023 = df_jan_apr['2023']

# Find lowest values for each year
lowest_values = df_jan_apr.iloc[:, 5:].idxmin(axis=1)
lowest_values_values = df_jan_apr.min(axis=1)

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
min_indices = df[columns_to_plot].idxmin()

# Step 2: Create a scatter plot with these minimum values
plt.scatter(min_indices, df[columns_to_plot].min(),c=np.arange(len(columns_to_plot)), cmap='plasma_r',edgecolors='white')
custom_offset = 7
for i, col in enumerate(columns_to_plot):
    plt.annotate(col, (min_indices[col], df[col].min()), textcoords="offset points", xytext=(0, custom_offset), ha='center', fontsize=9, color='white')


# Add labels and title
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}', fontsize=15, color='white')#color='darkgrey')
# Define x labels explicitly
xlabels = ['Jan', 'Feb', 'Mar', 'Apr']

# Set x-axis tick positions and labels
plt.xticks(doy[::30], xlabels)

# Set x-axis limits
plt.xlim(1, 105)

# Set x-axis tick positions and labels
plt.xticks(doy[::30], xlabels, fontsize=10, color='white', fontname='Avant Garde')
# Set y-axis tick labels font properties
plt.yticks(fontsize=10, color='white', fontname='Avant Garde')


# Show plot
plt.legend(shadow=False, fontsize=7.5, loc='upper left',
               bbox_to_anchor=(0.787, 0.163), fancybox=True, ncol=1, frameon=False)
plt.savefig('/Users/fridaperez/Desktop/Proposal/Proposal_Figures/Clim_Mins_black.png',dpi=300)


