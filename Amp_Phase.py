import numpy as np
import matplotlib.pyplot as plt## Sans Serif ##
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
plt.style.use('ggplot')
plt.style.use('dark_background')

# Define the frequency, amplitude, and phase of the sine waves
frequency = 1.0  # Frequency in Hz
amplitude = 2.0
phase1 = np.pi / 4  # Phase in radians for the first wave
phase2 = np.pi / 8  # Phase in radians for the second wave

# Create time values for one period of the sine wave
t = np.linspace(0, 1, 1000)  # 1000 points for one period

# Generate the two sine waves with different phases
sine_wave1 = amplitude * np.sin(2 * np.pi * frequency * t + phase1)
sine_wave2 = amplitude * np.sin(2 * np.pi * frequency * (t - 0.2) + phase2)  # Shifted to the left

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the sine waves with solid lines
ax.plot(t, sine_wave1)
ax.plot(t - 0.4, sine_wave2, linestyle='--')

# # Add horizontal dashed line for phase
# ax.hlines(phase1, 0, 1, linestyle='--', colors='r', label='Phase 1')
# ax.hlines(phase2, -0.2, 0.8, linestyle='--', colors='g', label='Phase 2')  # Adjust the x-axis range

# Remove x and y axis labels
ax.set_xticks([])
ax.set_yticks([])

# # Set the title
# ax.set_title('Two Sine Waves with Different Phases and Shifts')
#
# # Add a legend
# ax.legend(loc='upper right')

# Display the plot
plt.show()
