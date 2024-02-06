import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Directory and time
directoryfigure = '/Users/fridaperez/Developer/repos/Proposal/Proposal_Figures/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday
lastday = now.timetuple().tm_yday - 2

# Define the desired year range (2012 - 2023)
start_year = 2012
end_year = 2023

# Turn on to read in the data (slow!)
datareader = True
#plt.style.use('dark_background')

# Load csv
xpath = '/Users/fridaperez/Developer/repos/phase_project/SIE/S_seaice_extent_daily_v3.0.csv'
df = pd.read_csv(xpath)
print(df['Year'].unique())


# Filter the DataFrame to include only the desired year range
df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

# Create plot
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Avant Garde']})

# Set the background color to white
fig = plt.figure(figsize=(10, 6), facecolor='white')

plt.rc('savefig', facecolor='white')
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
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Calculate 5-day running mean for sea ice extent
df['5-day_mean'] = df['Extent'].rolling(window=5).mean()

# Calculate the month fractions based on 'year', 'month', and 'day'
df['month_fraction'] = df['Day'] / 31 + (df['Month'] - 1)

# Plot sea ice extent and the 5-day running mean
years = df['Year'].unique()
for year in years:
    data_year = df[df['Year'] == year]
    #plt.plot(data_year['month_fraction'], data_year['Extent'], label=str(year), alpha=0.4)  # Original data
    plt.plot(data_year['month_fraction'], data_year['5-day_mean'], label=str(year))# + ' (5-day mean)'))

# Set x-axis labels to months
plt.xticks(np.arange(0, 12, 1), months)

# Set x-axis and y-axis labels
plt.xlabel(r'\textbf{MONTH}')
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',fontsize=15)

# Move the legend outside of the graph to the right
plt.tight_layout()
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(directoryfigure + 'nsidc_sie_cpolar_w.png', dpi=500,  bbox_inches='tight')

