"""
Reads in current year's regional Arctic sea ice extent from Sea Ice Index 3
(NSIDC)
Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/seaice_analysis/
Author    : Zachary M. Labe
Date      : 21 October 2017
"""
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Directory and time
directoryfigure = '/Users/fridaperez/Desktop/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday
doy = np.arange(0, 365, 1)
lastday = now.timetuple().tm_yday - 2
years = np.arange(2012, 2023 + 1, 1)
plt.style.use('dark_background')
# Turn on to read in the data (slow!)
datareader = True

# Load url
xpath = '/Users/fridaperez/Developer/repos/phase_project/SIE/S_Sea_Ice_Index_Regional_Daily_Data_G02135_v3.0.xlsx'

# Read files from NSIDC (not very efficient - lol)
# There are more regional seas that can easily be added!
if datareader:
    df_Bell_Amundsen = pd.read_excel(xpath, sheet_name='Bell-Amundsen-Extent-km^2', header=1, usecols=range(3, 43), engine='openpyxl')
    df_Indian = pd.read_excel(xpath, sheet_name='Indian-Extent-km^2', header=1, usecols=range(3, 43), engine='openpyxl')
    df_Pacific = pd.read_excel(xpath, sheet_name='Pacific-Extent-km^2', header=1, usecols=range(3, 43), engine='openpyxl')
    df_Ross = pd.read_excel(xpath, sheet_name='Ross-Extent-km^2', header=1, usecols=range(3, 43), engine='openpyxl')
    df_Weddell = pd.read_excel(xpath, sheet_name='Weddell-Extent-km^2', header=1, usecols=range(3, 43), engine='openpyxl')

    sie = [df_Bell_Amundsen, df_Indian, df_Pacific, df_Ross, df_Weddell]
    sie = np.asarray(sie) / 1e6

    print('\nCompleted: Read sea ice data!')

# Find statistics
yearsq = np.where((years >= 1979) & (years <= 2023))[0]
sieq = sie[:, :, yearsq]

mean = np.empty((sie.shape[0], sie.shape[1]))
std = np.empty((sie.shape[0], sie.shape[1]))
for i in range(sie.shape[0]):
    for j in range(sie.shape[1]):
        mean[i, j] = np.nanmean(sieq[i, j, :], axis=0)
        std[i, j] = np.nanstd(sieq[i, j, :], axis=0)

# +-2 standard deviation
maxe = mean + (2. * std)
mine = mean - (2. * std)

# Create plot
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Avant Garde']})

# Set the background color to white
fig = plt.figure(facecolor='black')

plt.rc('savefig', facecolor='black')
plt.rc('axes', edgecolor='darkgrey')

# Adjust axes in time series plots
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 2))
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

# Labels for months
xlabels = [r'Jan', r'Apr', r'Jul', r'Oct', r'Jan']
# Sea names
sienames = [r'\textbf{BELLINGSHAUSEN-AMUNDSEN}', r'\textbf{KING HAAKON}',
            r'\textbf{EAST ANTARCTICA}',
            r'\textbf{ROSS-AMUNDSEN}', r'\textbf{WEDDELL}']

# Loop through each regional sea
for i in range(sie.shape[0]):
    ax = plt.subplot(3, 2, i + 1)

    # if statement for adjusting plot axes between bottom and others
    if i >= 8:
        ax.tick_params('both', length=1, width=2, which='major')
        adjust_spines(ax, ['left', 'bottom'])
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.tick_params(color='darkgrey')
    else:
        ax.tick_params('both', length=1, width=2, which='major')
        adjust_spines(ax, ['left', 'bottom'])
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_linewidth(2)
        ax.tick_params(color='darkgrey')

    # PLOT
    plt.plot(sie[i, :, -1], color='aqua', zorder=2)
    ax.fill_between(doy, mine[i], maxe[i], facecolor='magenta', alpha=0.4)

    plt.yticks(np.arange(0, 8, 1), [str(x) for x in np.arange(0, 8, 1)], fontsize=6)

    plt.axvline(lastday, color='dimgrey', linestyle='--', linewidth=2, zorder=1)
    plt.scatter(lastday, sie[i, lastday, -1], color='aqua', s=15, zorder=3)

    plt.ylim([0, 8])

    # Set x-labels to xlabels (months)
    plt.xticks(np.arange(0, 361.5, 90.4), xlabels, fontsize=7)

    # Label each sea at the top center of the subplot
    plt.text(180, 7.5, sienames[i], color='white', fontsize=9, ha='center', va='center')

# Add text to plot
plt.text(-75, 20, r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
         fontsize=13, alpha=1, color='white', rotation=90)
plt.text(700, 3, r'$\bf{\pm}$2\ \textbf{std. dev.}', fontsize=17,
         color='magenta', alpha=0.7, ha='right')

# Adjust size of plot
fig.subplots_adjust(hspace=0.3)

# Save figure
plt.savefig(directoryfigure + 'nsidc_sie_regionals_1.png', dpi=300)

# Show the plot (optional)
plt.show()
