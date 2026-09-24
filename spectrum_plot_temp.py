#%%
data_dir = r"\\dphy-bob\Recherche\Salles Propres\GGautam\Samples\ChBN\ChBN12_LT\Data\Spectrum\data-nor" 
import os
import glob
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from scipy.optimize import curve_fit

# ==========================================
# 1. Configuration, Loading & Cleaning
# ==========================================
#data_dir = './' 
file_pattern = os.path.join(data_dir, 'spectrum_data_*.txt')

# Exclude files with focus drift or failed shutter
bad_temperatures = [0]

data_dict = {}
temp_regex = re.compile(r'spectrum_data_\d+_(\d+)_')

def safe_remove_cosmic_rays(wl, counts, protected_min=434.0, protected_max=438.0):
    """Applies median filter to remove cosmic rays, strictly ignoring the ZPL region."""
    filtered = medfilt(counts, kernel_size=5)
    diff = np.abs(counts - filtered)
    bg_mask = (wl < protected_min) | (wl > protected_max)
    std_diff = np.std(diff[bg_mask])
    
    spike_mask = (diff > 5 * std_diff) & bg_mask
    clean_counts = np.copy(counts)
    clean_counts[spike_mask] = filtered[spike_mask]
    return clean_counts

# Load and filter data
for filepath in glob.glob(file_pattern):
    match = temp_regex.search(os.path.basename(filepath))
    if match:
        temp = float(match.group(1))
        if temp not in bad_temperatures:
            data = np.loadtxt(filepath, comments='#')
            wl, raw_counts = data[:, 0], data[:, 1]
            clean_counts = safe_remove_cosmic_rays(wl, raw_counts)
            data_dict[temp] = (wl, clean_counts)

temperatures = sorted(data_dict.keys())

# ==========================================
# 2. Plot 1: 2D Heatmap (Contour)
# ==========================================
common_wl = data_dict[temperatures[0]][0]
intensity_matrix = np.array([data_dict[t][1] for t in temperatures])

plt.figure(figsize=(10, 6))
X, Y = np.meshgrid(common_wl, temperatures)
c = plt.pcolormesh(X, Y, intensity_matrix, shading='auto', cmap='inferno')
plt.colorbar(c, label='Raw Counts')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Temperature (K)')
plt.title('2D Heatmap of hBN Blue Emission')
plt.tight_layout()
plt.show()

# ==========================================
# 3. Plot 2: Raw Waterfall
# ==========================================
plt.figure(figsize=(10, 8))

# Calculate a dynamic offset based on the maximum raw intensity in all valid files
global_max_counts = np.max([np.max(counts) for _, counts in data_dict.items()])
offset_factor = global_max_counts * 0.15 

for i, t in enumerate(temperatures):
    wl, counts = data_dict[t]
    
    # Apply raw vertical offset
    offset_counts = counts + (i * offset_factor)
    
    plt.plot(wl, offset_counts, label=f'{t} K', lw=1.2)

plt.xlabel('Wavelength (nm)')
plt.ylabel('Raw Counts (Offset)')
plt.title('Waterfall Plot (Raw Data)')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small', ncol=1)
plt.tight_layout()
plt.show()

# ==========================================
# 4. Plot 3: ZPL Fitting & FWHM vs Temperature
# ==========================================
def lorentzian(x, amp, cen, wid, bg):
    return (amp * wid**2 / ((x - cen)**2 + wid**2)) + bg

fwhm_list = []
fit_temperatures = []

zpl_min_wl = 434.0
zpl_max_wl = 438.0

for t in temperatures:
    wl, counts = data_dict[t]
    
    # Isolate ZPL to avoid fitting the phonon sideband
    mask = (wl >= zpl_min_wl) & (wl <= zpl_max_wl)
    wl_fit = wl[mask]
    counts_fit = counts[mask]
    
    amp_guess = np.max(counts_fit) - np.min(counts_fit)
    cen_guess = wl_fit[np.argmax(counts_fit)]
    wid_guess = 0.5 
    bg_guess = np.min(counts_fit)
    
    p0 = [amp_guess, cen_guess, wid_guess, bg_guess]
    
    try:
        popt, _ = curve_fit(lorentzian, wl_fit, counts_fit, p0=p0, maxfev=2000)
        fwhm = 2 * abs(popt[2])
        fwhm_list.append(fwhm)
        fit_temperatures.append(t)
    except RuntimeError:
        print(f"Lorentzian fit failed for {t} K")

plt.figure(figsize=(8, 5))
plt.plot(fit_temperatures, fwhm_list, 'o-', color='darkred', markersize=6, linewidth=1.5)
plt.xlabel('Temperature (K)')
plt.ylabel('ZPL FWHM (nm)')
plt.title('Extracted ZPL Broadening')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# ==========================================
# 5. Plot 4: Grid / Collage (Quality Check)
# ==========================================
cols = 6
rows = math.ceil(len(temperatures) / cols)

fig, axes = plt.subplots(rows, cols, figsize=(20, 3 * rows), sharex=True, sharey=False)
axes = axes.flatten()

for i, t in enumerate(temperatures):
    wl, counts = data_dict[t]
    ax = axes[i]
    ax.plot(wl, counts, color='royalblue', lw=1.2)
    ax.legend([f'{t} K'], loc='upper right', handlelength=0)
    ax.grid(True, linestyle='--', alpha=0.5)

# Hide unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

fig.supxlabel('Wavelength (nm)', fontsize=14)
fig.supylabel('Raw Counts', fontsize=14)
plt.tight_layout()
plt.show()
# %%
