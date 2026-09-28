from pyHegel.commands import *

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# --- Placeholder for your existing function ---
# Remove this block if estimate_lifetime is already defined in your environment
def estimate_lifetime(time_bins_ns, hist_data):
    """
    Estimates the photoluminescence lifetime (tau) using a simple 
    monoexponential tail fit: y(t) = A * exp(-t / tau) + C
    """
    if len(hist_data) < 100 or np.max(hist_data) < 50:
        return 0.0
    
    i_peak = int(np.argmax(hist_data))
    y_peak = float(hist_data[i_peak])
    
    thr_start = 0.7 * y_peak
    post_peak_indices = np.arange(i_peak, len(hist_data))
    below_thresh_start = post_peak_indices[hist_data[post_peak_indices] <= thr_start]
    
    i0 = int(below_thresh_start[0]) if len(below_thresh_start) > 0 else i_peak + 1
    if i0 >= len(hist_data): return 0.0
    
    thr_end = 0.02 * y_peak
    below_thresh_end = post_peak_indices[hist_data[post_peak_indices] <= thr_end]
    i1 = int(below_thresh_end[0]) if len(below_thresh_end) > 0 else len(hist_data)
    
    if (i1 - i0) < 10:
        i1 = len(hist_data) - int(np.maximum(10, int(len(hist_data) * 0.15)))
    
    n_tail = int(np.maximum(10, int(len(hist_data) * 0.15)))
    C = float(np.maximum(0.0, float(np.median(hist_data[-n_tail:])))) 
    
    t_fit = time_bins_ns[i0:i1]
    y_fit = hist_data[i0:i1] - C
    
    valid_mask = y_fit > 0.5 
    if np.sum(valid_mask) < 10: return 0.0
    
    x = t_fit[valid_mask]
    x = x - x[0] 
    ln_y = np.log(y_fit[valid_mask])
    
    xbar, ybar = x.mean(), ln_y.mean()
    Sxx = np.sum((x - xbar)**2)
    Sxy = np.sum((x - xbar)*(ln_y - ybar))
    
    if Sxx == 0: return 0.0
    slope = Sxy / Sxx
    
    if slope >= 0: return 0.0 
    
    tau = -1.0 / slope
    return tau

# Setup your data directory and file extension here
data_dir = r"C:\Users\gauta\OneDrive - USherbrooke\Samples\ChBN12-LowTemp\Data complete\Data Sorted\Data-LTRT\E2\TRPL data"
file_pattern = os.path.join(data_dir, 'trpldata_*.txt') # <-- Adjust .txt to .dat if necessary

temperatures = []
lifetimes_ns = []

for filepath in glob.glob(file_pattern):
    filename = os.path.basename(filepath)
    
    # Split the filename by underscores
    # Example: trpldata_10.0MHz_300s_110_109_E1-OG-LTRT_2026_09_20_12_08_33
    # Index 0: trpldata
    # Index 1: 10.0MHz
    # Index 2: 300s
    # Index 3: 110 (Temperature!)
    try:
        parts = filename.split('_')
        temp = float(parts[3])
    except (IndexError, ValueError):
        print(f"Skipping {filename} - could not extract temperature.")
        continue
        
    try:
        # Read the file (v)
        v = readfile(filepath)
        time_bins = v[0]
        hist_data = v[1]
        
        # Estimate lifetime (returns picoseconds)
        lifetime_ps = estimate_lifetime(time_bins, hist_data)
        
        # Convert output to integer, then divide by 1000 to get nanoseconds
        lifetime_ns = int(lifetime_ps) / 1000.0
        
        temperatures.append(temp)
        lifetimes_ns.append(lifetime_ns)
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")

if not temperatures:
    print("No data was processed. Check your directory path and file extensions.")
else:
    # Sort data by temperature to ensure the plot lines up cleanly
    sorted_indices = np.argsort(temperatures)
    temperatures = np.array(temperatures)[sorted_indices]
    lifetimes_ns = np.array(lifetimes_ns)[sorted_indices]

    # --- Plotting ---
    plt.figure(figsize=(9, 6))

    # Plot each point individually so we can add it to the legend easily
    for t, tau in zip(temperatures, lifetimes_ns):
        plt.plot(t, tau, marker='o', markersize=8, linestyle='None', label=f"{t} K")

    # Add a dashed line connecting the points to show the trend
    plt.plot(temperatures, lifetimes_ns, linestyle='--', color='gray', alpha=0.5)

    plt.xlabel('Temperature (K)', fontsize=14)
    plt.ylabel('Lifetime (ns)', fontsize=14)
    plt.title('TRPL Lifetime vs. Temperature', fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Put the legend outside the plot area so it doesn't cover the data
    plt.legend(title="Temperatures", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()