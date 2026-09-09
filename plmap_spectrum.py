import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from QFLv4 import *

def run_pl_spectrum_scan(camera, spectro, amc=None,
                         center_x=None, center_y=None, center_f=None,
                         x_size=5, y_size=5, step=0.1,
                         wl_min=None, wl_max=None,
                         vbg=None,
                         logz=False, exposure_s=0.2,
                         out_dir_base=r'D:\Data_Python_PL\PLmaps\Spectro',
                         show_plot=True,
                         waits=0):
    """
    Performs a 2D PL scan using a spectrograph and camera.
    Saves all spectrums at each pixel into a single structured text file.
    Plots the 2D map based on the sum of intensities within [wl_min, wl_max].
    """
    amc_local = False
    data_file_handle = None
    if camera is None: raise ConnectionError("No Camera")
    # setup exposure and single scan mode
    camera.conf(read_mode='full_vertical_binning',exposure_time=exposure_s,acq_mode="single_scan",acc_N=1)
    set(camera.cosmic_filter_en, False)
    try:
        # === Initialize Attocube (if not provided) ===
        if amc is None:
            # Assuming start_attocube() is defined elsewhere in your code
            amc = start_attocube() 
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        # === Setup Scan Area ===
        center_x = center_x if center_x is not None else amc.move.getPosition(0) / 1000
        center_y = center_y if center_y is not None else amc.move.getPosition(2) / 1000
        x_start, x_end = center_x - (x_size / 2), center_x + (x_size / 2)
        y_start, y_end = center_y - (y_size / 2), center_y + (y_size / 2)
        out_dir = output_dir_folder(base_dir=out_dir_base) # Assuming this def exists in your code

        if center_f is not None:
            print(f"Setting initial focus (Z-axis) to: {center_f} µm")
            amc.move.setControlTargetPosition(1, int(center_f * 1000))
            wait_until_stable(amc, axis=1) # Assuming wait_until_stable exists
        
        center_f = amc.move.getPosition(1) / 1000
        print(f"Initial pos (x,y,z) :  ({center_x:.2f}, {center_y:.2f}, {center_f:.2f}) µm")

        # === Get Wavelength Array and Setup Range Mask ===
        print("Taking initial dummy spectrum to calibrate wavelengths...")
        # Get one spectrum to read the exact wavelength bins
        set(camera.shutter, False)
        time.sleep(1)
        if vbg is not None:
            v_init = get(camera.readval, bkg_rem=vbg[1])
        else:
            v_init = get(camera.readval)
        
        wavelengths = v_init[0]
        
        # Determine wavelength mask for plotting sum
        if wl_min is None: wl_min = wavelengths[0]
        if wl_max is None: wl_max = wavelengths[-1]
        
        wl_mask = (wavelengths >= wl_min) & (wavelengths <= wl_max)
        print(f"Plotting sum of intensities between {wl_min:.1f} nm and {wl_max:.1f} nm.")

        # === Setup Plot and Data File ===
        x_pos, y_pos = np.arange(x_start, x_end + step, step), np.arange(y_start, y_end + step, step)
        Z = np.zeros((len(y_pos), len(x_pos)), dtype=float)
        extent = [x_start, x_end, y_start, y_end]

        plt.ion()
        fig, ax1 = plt.subplots()
        img1 = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
        cb_format = mticker.FuncFormatter(lambda x, _: f'{x/1000:.1f}k' if x >= 1000 else str(int(x)))
        cb1 = fig.colorbar(img1, ax=ax1, format=cb_format)
        ax1.set_xlabel('X (µm)'); ax1.set_ylabel('Y (µm)')
        ax1.set_title(f'PL map (Sum {wl_min:.1f}-{wl_max:.1f}nm)'); fig.tight_layout()

        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'plmap_spectro_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_spectro_data_{timestamp}.txt')

        print(f'Saving data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        
        # Write File Headers
        data_file_handle.write(f'# PL Spectro Mapping - {timestamp}\n')
        data_file_handle.write(f'# Center X: {center_x}, Y: {center_y}, F: {center_f}\n')
        data_file_handle.write(f'# Map Shape: {len(x_pos)} (X) by {len(y_pos)} (Y)\n')
        data_file_handle.write(f'# Integration range for Plot: {wl_min} to {wl_max} nm\n')
        
        # Create column headers: X, Y, then every wavelength
        wl_headers = "\t".join([f"{w:.2f}" for w in wavelengths])
        data_file_handle.write(f'X_act\tY_act\t{wl_headers}\n')

        # === Start Scan Loop ===
        max_int, best_x, best_y = -1, x_start, y_start
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()

        # Move to start position
        amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(y_start * 1000)); wait_until_stable(amc, axis=2)

        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)); wait_until_stable(amc, axis=2)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1] # Serpentine path

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, axis=0)

                x_act, y_act = amc.move.getPosition(0)/1000, amc.move.getPosition(2)/1000
                if waits > 0:
                    time.sleep(waits)
                
                # --- Read Spectrum ---
                if vbg is not None:
                    v = get(camera.readval, bkg_rem=vbg[1])
                else:
                    v = get(camera.readval)
                
                intensities = v[1]
                
                # Filter intensities by wavelength range and sum for the 2D plot
                filtered_sum = np.sum(intensities[wl_mask])
                
                Z[i, j] = np.log10(filtered_sum + 1) if logz else filtered_sum

                if filtered_sum > max_int:
                    max_int, best_x, best_y = filtered_sum, x_act, y_act

                # --- Write exact pixel data to file ---
                # X_act \t Y_act \t Int1 \t Int2 ...
                int_data_str = "\t".join([f"{count:.2f}" for count in intensities])
                data_file_handle.write(f'{x_act:.3f}\t{y_act:.3f}\t{int_data_str}\n')

                point_counter += 1
                elapsed = time.time() - start_time
                rem_time = (elapsed / point_counter) * (total_points - point_counter)
                mins, secs = divmod(int(rem_time), 60)
                print(f'Scan: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

                # Update plot
                img1.set_data(Z)
                img1.set_clim(vmin=Z.min(), vmax=Z.max())
                title = f'PL Spectrum Map ({"Log" if logz else "Linear"}) - Max Sum: {max_int:.0f} @({best_x:.2f},{best_y:.2f})'
                ax1.set_title(title)
                fig.canvas.draw(); fig.canvas.flush_events()

        print("\nScan complete.")
        plt.ioff()
        plt.savefig(plot_file); print(f"Plot saved to: {plot_file}")
        
        if show_plot: 
            plt.show()
        else: 
            plt.close(fig)

    except Exception as e:
        print(f"\nA critical error occurred during PL scan: {e}")
        return None, None, None
    except KeyboardInterrupt as k:
        print(f"\nKeyboard interrupt : {k}")
        print(f"Moving back to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(center_y * 1000)); wait_until_stable(amc, axis=2)
        return None, None, None    
    finally:
        # === Cleanup Resources ===
        print("\n--- Cleaning up PL scan resources ---")
        if data_file_handle:
            data_file_handle.close(); print("Data file closed.")
        if amc_local and amc: 
            close_device_all(amc=amc)