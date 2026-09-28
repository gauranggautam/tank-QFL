#%%
import os
import glob
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

# --- Loading Logic ---
data_dir = r"C:\Users\gauta\OneDrive - USherbrooke\Samples\ChBN12-LowTemp\Data complete\Data Sorted\Data-E1-E10-5K\Spectrum-E1-E10"  
file_pattern = os.path.join(data_dir, 'spectrum_data_*.txt')
data_dict = {}

# Regex to capture anything between 'spectrum_data_' and '.txt'
label_regex = re.compile(r'spectrum_data_(.*?)\.txt')

for filepath in glob.glob(file_pattern):
    filename = os.path.basename(filepath)
    match = label_regex.search(filename)
    if match:
        label = match.group(1) 
        
        try:
            data = np.loadtxt(filepath, comments='#')
            if data.size > 0:
                data_dict[label] = (data[:, 0], data[:, 1])
        except Exception as e:
            print(f"Skipping {filename} due to read error: {e}")

# Helper for "natural sorting" (e.g., '2' comes before '10')
def natural_keys(text):
    return [float(c) if c.replace('.', '', 1).isdigit() else c.lower() for c in re.split(r'(\d+(?:\.\d+)?)', text)]

labels = sorted(data_dict.keys(), key=natural_keys)
n_files = len(labels)

if n_files == 0:
    print("No valid data files found.")
else:
    # --- Determine Grid Size (Strictly 2 Rows) ---
    rows = 2
    cols = max(1, math.ceil(n_files / rows))

    # Dynamically scale the figure size. 
    # Made slightly wider (5 inches per col) since x-axes are now independent and need space for labels.
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    
    # Flatten ensures we can loop through it as a 1D list, regardless of grid shape
    axes = np.atleast_1d(axes).flatten()

    def safe_remove_cosmic_rays(wl, counts):
        filtered = medfilt(counts, kernel_size=5)
        diff = np.abs(counts - filtered)
        bg_mask = (wl < 434.0) | (wl > 438.0)
        spike_mask = (diff > 5 * np.std(diff[bg_mask])) & bg_mask
        clean_counts = np.copy(counts)
        clean_counts[spike_mask] = filtered[spike_mask]
        return clean_counts

    for i, label in enumerate(labels):
        wl, counts = data_dict[label]
        clean_counts = safe_remove_cosmic_rays(wl, counts)
        
        ax = axes[i]
        ax.plot(wl, clean_counts, color='royalblue', lw=1.2)
        
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.5)

    # Turn off any empty subplots in the grid (e.g. if you have an odd number of files)
    for j in range(n_files, len(axes)):
        fig.delaxes(axes[j])

    fig.supxlabel('Wavelength (nm)', fontsize=14)
    fig.supylabel('Counts', fontsize=14)
    plt.tight_layout()
    plt.show()
# %%