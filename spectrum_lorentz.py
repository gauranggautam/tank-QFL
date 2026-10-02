#%%
import os
import glob
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

from lmfit.models import LorentzianModel, ConstantModel

# ==========================================
# 1. Configuration, Loading & Cleaning
# ==========================================
data_dir = r"C:\Users\gauta\OneDrive - USherbrooke\Samples\ChBN12-LowTemp\Data complete\Data Sorted\Data-LTRT\E1-OG\Spectrum" 
bg_file_path = r"C:\Users\gauta\OneDrive - USherbrooke\Samples\ChBN12-LowTemp\Data complete\Data Sorted\Data-LTRT\spectrum_data_BG_150_147_E1-OG-LTRT_2026_09_21_03_23_51.txt"

# ZPL limits ONLY used for the mathematical fitting boundaries
zpl_min_wl = 434.0
zpl_max_wl = 438.0

file_pattern = os.path.join(data_dir, 'spectrum_data_*.txt')
bad_temperatures = [0] 
data_dict = {}
temp_regex = re.compile(r'spectrum_data_\d+_(\d+)_')

def safe_remove_cosmic_rays(wl, counts, protected_min=434.0, protected_max=438.0):
    filtered = medfilt(counts, kernel_size=5)
    diff = np.abs(counts - filtered)
    bg_mask = (wl < protected_min) | (wl > protected_max)
    std_diff = np.std(diff[bg_mask])
    
    spike_mask = (diff > 5 * std_diff) & bg_mask
    clean_counts = np.copy(counts)
    clean_counts[spike_mask] = filtered[spike_mask]
    return clean_counts

# Load Background Data
bg_counts = 0
if bg_file_path and os.path.exists(bg_file_path):
    bg_data = np.loadtxt(bg_file_path, comments='#')
    bg_counts = bg_data[:, 1]
    print(f"Loaded background from {os.path.basename(bg_file_path)}")
else:
    print("No background file found. Proceeding without background subtraction.")

# Load and filter measurement data
for filepath in glob.glob(file_pattern):
    match = temp_regex.search(os.path.basename(filepath))
    if match:
        temp = float(match.group(1))
        if temp not in bad_temperatures:
            if filepath == bg_file_path:
                continue
                
            data = np.loadtxt(filepath, comments='#')
            wl, raw_counts = data[:, 0], data[:, 1]
            
            raw_counts = raw_counts - bg_counts
            clean_counts = safe_remove_cosmic_rays(wl, raw_counts)
            data_dict[temp] = (wl, clean_counts)

temperatures = sorted(data_dict.keys())

# ==========================================
# 2. LMFit Model Setup & Tracking Lists
# ==========================================
model = LorentzianModel(prefix='p1_') + LorentzianModel(prefix='p2_') + ConstantModel(prefix='bg_')

fwhm_peak1_list = []
fwhm_peak2_list = []
center_peak1_list = [] # New list for Peak 1 position
center_peak2_list = [] # New list for Peak 2 position
fit_temperatures = []

# ==========================================
# 3. Plot 1: Deconvoluted Fits Grid
# ==========================================
cols = 6
rows = math.ceil(len(temperatures) / cols) if len(temperatures) > 0 else 1

# sharey=False allows each plot to scale automatically
fig, axes = plt.subplots(rows, cols, figsize=(20, 3 * rows), sharex=True, sharey=False)
if rows * cols == 1:
    axes = [axes] 
else:
    axes = axes.flatten()

for i, t in enumerate(temperatures):
    wl, counts = data_dict[t]
    
    # Isolate ZPL strictly for fitting mathematically
    mask = (wl >= zpl_min_wl) & (wl <= zpl_max_wl)
    wl_fit = wl[mask]
    counts_fit = counts[mask]
    
    bg_guess = np.min(counts_fit)
    max_counts = np.max(counts_fit)
    main_cen = wl_fit[np.argmax(counts_fit)]
    
    # --- Set Initial Guesses and Bounds for LMFit ---
    params = model.make_params()
    params['p1_center'].set(value=main_cen, min=zpl_min_wl, max=zpl_max_wl)
    params['p1_amplitude'].set(value=max_counts - bg_guess, min=0)
    params['p1_sigma'].set(value=0.2, min=0.01, max=2.0)
    
    params['p2_center'].set(value=main_cen + 0.5, min=zpl_min_wl, max=zpl_max_wl)
    params['p2_amplitude'].set(value=(max_counts - bg_guess) * 0.3, min=0)
    params['p2_sigma'].set(value=0.5, min=0.01, max=2.0)
    
    params['bg_c'].set(value=bg_guess, min=0)
    
    ax = axes[i]
    ax.plot(wl, counts, 'o', color='black', markersize=3, alpha=0.5, label='Raw Data')
    
    try:
        result = model.fit(counts_fit, params, x=wl_fit)
        full_eval = result.eval(x=wl)
        comps = result.eval_components(x=wl)
        
        c1 = result.params['p1_center'].value
        c2 = result.params['p2_center'].value
        
        # Enforce Ordering: Peak 1 is always the left-most peak
        if c1 > c2:
            fwhm1 = result.params['p2_fwhm'].value
            fwhm2 = result.params['p1_fwhm'].value
            cen1 = c2
            cen2 = c1
            peak1_curve = comps['p2_']
            peak2_curve = comps['p1_']
        else:
            fwhm1 = result.params['p1_fwhm'].value
            fwhm2 = result.params['p2_fwhm'].value
            cen1 = c1
            cen2 = c2
            peak1_curve = comps['p1_']
            peak2_curve = comps['p2_']
            
        bg_curve = comps['bg_']
        
        fwhm_peak1_list.append(fwhm1)
        fwhm_peak2_list.append(fwhm2)
        center_peak1_list.append(cen1)
        center_peak2_list.append(cen2)
        fit_temperatures.append(t)
        
        # Plot deconvoluted fits across the full range
        ax.plot(wl, full_eval, color='darkred', lw=1.5, label='Total Fit')
        ax.fill_between(wl, bg_curve, peak1_curve + bg_curve, color='royalblue', alpha=0.4, label='Peak 1')
        ax.fill_between(wl, bg_curve, peak2_curve + bg_curve, color='forestgreen', alpha=0.4, label='Peak 2')
        
    except Exception as e:
        print(f"LMFit failed for {t} K: {e}")
        
    ax.set_title(f"{t} K")
    ax.grid(True, linestyle='--', alpha=0.5)

# Clean up empty subplots
for j in range(len(temperatures), len(axes)):
    fig.delaxes(axes[j])
    
if len(temperatures) > 0:
    axes[0].legend(fontsize='small', loc='upper right')

fig.supxlabel('Wavelength (nm)', fontsize=14)
fig.supylabel('Counts (Background Subtracted)', fontsize=14)
plt.tight_layout()
plt.show()

# ==========================================
# 4. Plot 2: Dual FWHM vs Temperature
# ==========================================
if len(fit_temperatures) > 0:
    plt.figure(figsize=(9, 6))
    
    plt.plot(fit_temperatures, fwhm_peak1_list, 'o-', color='royalblue', 
             markersize=7, linewidth=2, label='Peak 1 (Main)')
    plt.plot(fit_temperatures, fwhm_peak2_list, 's-', color='forestgreen', 
             markersize=7, linewidth=2, label='Peak 2 (Shoulder)')

    plt.xlabel('Temperature (K)', fontsize=12)
    plt.ylabel('ZPL FWHM (nm)', fontsize=12)
    plt.title('Extracted ZPL Broadening (LMFit)', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# ==========================================
# 5. Plot 3: Center Position vs Temperature
# ==========================================
if len(fit_temperatures) > 0:
    plt.figure(figsize=(9, 6))
    
    plt.plot(fit_temperatures, center_peak1_list, 'o-', color='royalblue', 
             markersize=7, linewidth=2, label='Peak 1 Position')
    plt.plot(fit_temperatures, center_peak2_list, 's-', color='forestgreen', 
             markersize=7, linewidth=2, label='Peak 2 Position')

    plt.xlabel('Temperature (K)', fontsize=12)
    plt.ylabel('Peak Center Wavelength (nm)', fontsize=12)
    plt.title('ZPL Center Shift vs Temperature', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
# %%