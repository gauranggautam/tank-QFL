import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Configuration
# =============================================================================
data_dir = r"C:\Users\gauta\OneDrive - USherbrooke\Samples\ChBN12-LowTemp\Data complete\Polarization\2026_09_18_02_38_05_20_20_E2-LTRT"  # <-- Update this to your folder path
target_temp = "20"  # Updated to match the "20" in your new filename example

# Regex Breakdown:
# spectrum_data_(\d+)  -> Captures the very first number (Temperature)
# .*?_deg_             -> Skips all intervening text (like 'E2-LTRT') until it finds '_deg_'
# (\d+)(?:_(\d+))?     -> Captures the integer angle, and optionally the decimal angle after the underscore
file_regex = re.compile(r'spectrum_data_(\d+)_.*?_deg_(\d+)(?:_(\d+))?')

angles_deg = []
intensities = []

# =============================================================================
# Data Extraction
# =============================================================================
file_pattern = os.path.join(data_dir, 'spectrum_data_*')

for filepath in glob.glob(file_pattern):
    filename = os.path.basename(filepath)
    match = file_regex.search(filename)
    
    if match:
        file_temp = match.group(1)
        
        # Combine the integer and decimal parts of the degree (e.g., "10" and "0" -> 10.0)
        angle_int = match.group(2)
        angle_dec = match.group(3) if match.group(3) else "0"
        angle = float(f"{angle_int}.{angle_dec}")
        
        if file_temp == target_temp:
            try:
                # Load data (assuming space/tab delimited, col 0: wl, col 1: intensity)
                data = np.loadtxt(filepath, comments='#', unpack=True)
                wl = data[0]
                counts = data[1]
                
                # Mask wavelengths strictly between 430nm and 450nm
                mask = (wl >= 430.0) & (wl <= 450.0)
                integrated_intensity = np.sum(counts[mask])
                
                angles_deg.append(angle)
                intensities.append(integrated_intensity)
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")

if not intensities:
    print(f"No valid data found for temperature {target_temp}K. Check your directory and filenames.")
else:
    # =============================================================================
    # Processing & Sorting
    # =============================================================================
    angles_deg = np.array(angles_deg)
    intensities = np.array(intensities)
    
    # Normalize intensities to a maximum of 1
    intensities = intensities / np.max(intensities)
    
    # Sort by angle to draw the line correctly from left to right
    sort_indices = np.argsort(angles_deg)
    angles_deg = angles_deg[sort_indices]
    intensities = intensities[sort_indices]

    # =============================================================================
    # Linear Plotting
    # =============================================================================
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(angles_deg, intensities, marker='o', color='royalblue', 
            linewidth=2, markersize=8, label=f'{target_temp} K')
    
    ax.set_title(f'Normalized Intensity vs. Polarizer Angle ({target_temp} K)\nIntegration window: 430-450 nm', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Polarizer Angle (Degrees)', fontsize=12)
    ax.set_ylabel('Normalized Intensity', fontsize=12)
    
    ax.set_ylim(max(0, np.min(intensities) - 0.1), 1.1)
    
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()