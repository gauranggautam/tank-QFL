#%%
import os
import glob
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

# --- Loading Logic ---
data_dir = r"\\dphy-bob\Recherche\Salles Propres\GGautam\Samples\ChBN\ChBN12_LT\Data\Spectrum\data"  
file_pattern = os.path.join(data_dir, 'spectrum_data_*.txt')
data_dict = {}
temp_regex = re.compile(r'spectrum_data_\d+_(\d+)_')

for filepath in glob.glob(file_pattern):
    match = temp_regex.search(os.path.basename(filepath))
    if match:
        data = np.loadtxt(filepath, comments='#')
        data_dict[float(match.group(1))] = (data[:, 0], data[:, 1])

temperatures = sorted(data_dict.keys())
n_files = len(temperatures)

# --- Determine Grid Size (e.g., 5x6) ---
cols = 6
rows = math.ceil(n_files / cols)

fig, axes = plt.subplots(rows, cols, figsize=(20, 3 * rows), sharex=True)
# Flatten axes for easy iteration, even if it's a 2D array
axes = axes.flatten()

# Reusing the safe cleaning function from above
def safe_remove_cosmic_rays(wl, counts):
    filtered = medfilt(counts, kernel_size=5)
    diff = np.abs(counts - filtered)
    bg_mask = (wl < 434.0) | (wl > 438.0)
    spike_mask = (diff > 5 * np.std(diff[bg_mask])) & bg_mask
    clean_counts = np.copy(counts)
    clean_counts[spike_mask] = filtered[spike_mask]
    return clean_counts

for i, t in enumerate(temperatures):
    wl, counts = data_dict[t]
    clean_counts = safe_remove_cosmic_rays(wl, counts)
    
    ax = axes[i]
    ax.plot(wl, clean_counts, color='royalblue', lw=1.2)
    
    # Put the temperature as a legend inside each subplot
    ax.legend([f'{t} K'], loc='upper right', handlelength=0)
    ax.grid(True, linestyle='--', alpha=0.5)

# Turn off any unused subplots (if n_files isn't a perfect multiple of cols)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

fig.supxlabel('Wavelength (nm)', fontsize=14)
fig.supylabel('Counts', fontsize=14)
plt.tight_layout()
plt.show()
# %%
