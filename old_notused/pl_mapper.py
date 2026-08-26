import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time
import os
import AMC  # Assuming AMC is a custom library for the AMC100 controller
from snAPI.Main import * # Assuming snAPI is a custom library for the detector


def output_dir_folder(base_dir=r'./PlotBasic/Output/'):
    """
    Creates a subdirectory named with the current date (YYYY_MM_DD)
    inside a given base directory.
    Args:
        base_dir (str): The path to the parent directory.
    Returns:
        str: The full path to the daily output directory.
    """
    # Get the current date as a string, e.g., '2025_09_25'
    datestamp = time.strftime('%Y_%m_%d')
    # Create the full path for the new daily directory
    output_dir_base = os.path.join(base_dir, datestamp)
    # Create the directory; exist_ok=True prevents errors if it already exists
    os.makedirs(output_dir_base, exist_ok=True)
    # Return the path to the directory
    return output_dir_base

def run_pl_scan(
    center_x=0,
    center_y=0,
    center_f=0,
    x_size=5,
    y_size=5,
    step=1,
    detector_config=2,
    amc_address='amc100num-a01-0248.local',
    config_path_1_det=r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\Exciletas_MH.ini',
    config_path_2_det=r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\MPDs_MH.ini',
    out_dir_base='./PlotBasic/Output/PLmaps',
    show_plot=True,
):
    """
    Performs an automated and optimized photoluminescence (PL) map scan.

    This function defines a scan area by its center point, size, and a
    Z-axis focus value, making it ideal for automated routines.
    The outer loop scans Y, and the inner "fast" loop scans X.
    """
    
    
    # === Calculate Scan Boundaries from Center and Size ===
    x_start = center_x - x_size / 2
    x_end = center_x + x_size / 2
    y_start = center_y - y_size / 2
    y_end = center_y + y_size / 2
    
    out_dir = output_dir_folder(base_dir=r'./PlotBasic/Output/')
    
    os.makedirs(out_dir, exist_ok=True)

    # === Helper Function ===
    def wait_until_stable(amc_dev, axis):
        """Waits for the specified AMC axis to become stable."""
        timeout = 10
        start = time.time()
        while True:
            if amc_dev.status.getStatusMoving(axis) == 0 and \
               amc_dev.status.getStatusTargetRange(axis):
                break
            amc_dev.control.setControlOutput(axis, True)
            amc_dev.control.setControlMove(axis, True)
            if time.time() - start > timeout:
                print(f"Timeout waiting for stage axis {axis}")
                break
            time.sleep(0.01)

    # === Initialize Devices & Resources ===
    sn = None
    amc = None
    data_file_handle = None
    try:        
        # --- Init snAPI Detector ---
        sn = snAPI(libType=LibType.MH)
        sn.closeDevice()
        if not sn.getDevice(0):
            raise ConnectionError('MH detector not found')
        sn.setLogLevel(LogLevel.Device, False); sn.setLogLevel(LogLevel.Api, False)
        sn.initDevice(MeasMode.T2)

        # --- Detector Configuration ---
        if detector_config == 1:
            d1, d2 = 1, 2
            sn.loadIniConfig(config_path_1_det)
        else:
            d1, d2 = 3, 4
            sn.loadIniConfig(config_path_2_det)
        print(f"Using detector configuration {detector_config} (channels {d1}, {d2})")

        # --- AMC Positioner Init ---
        amc = AMC.Device(amc_address)
        amc.connect()
        for axis in [0, 1, 2]:
            amc.control.setControlOutput(axis, True); amc.control.setControlMove(axis, True)
        print(f"Connected to AMC controller at {amc_address}")

        # --- Set Focus (Z-axis, axis 1) ---
        print(f"Setting focus (Z-axis) to: {center_f} µm")
        amc.move.setControlTargetPosition(1, int(center_f * 1000))
        wait_until_stable(amc, axis=1)
        print("Focus set.")

        # === Grid and Plot Setup ===
        x_pos = np.arange(x_start, x_end + step, step)
        y_pos = np.arange(y_start, y_end + step, step)
        Z = np.zeros((len(y_pos), len(x_pos)), dtype=float)
        Zlog = np.zeros_like(Z)
        extent = [x_start, x_end, y_start, y_end]

        plt.ion()
        #fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
        fig, ax1 = plt.subplots()
        img1 = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
        #img2 = ax2.imshow(Zlog, cmap='plasma', origin='lower', extent=extent, aspect='auto')
        cb1 = fig.colorbar(img1, ax=ax1, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))
        #cb2 = fig.colorbar(img2, ax=ax2, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))

        # Apply settings directly to the single axes object 'ax1'
        ax1.set_xlabel('X (µm)'); ax1.set_ylabel('Y (µm)')
        ax1.set_xlim(x_start, x_end); ax1.set_ylim(y_start, y_end)
        ax1.invert_xaxis(); ax1.invert_yaxis()
        
        ax1.set_title('PL map - Raw counts'); #ax2.set_title('PL map - Log counts')
        fig.tight_layout()

        # === Output File Setup (Open once) ===
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    #       out_dir = os.path.join(output_dir_base, timestamp)
        plot_file = os.path.join(out_dir, f'plmap_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')
        print(f'Saving data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# PL Mapping - {timestamp}\n')
        data_file_handle.write(f'# Center X: {center_x}, Center Y: {center_y}, Center F: {center_f}\n')
        data_file_handle.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')

        # === Scan Loop (Outer loop: Y, Inner loop: X) ===
        max_int, best_x, best_y = 0, x_start, y_start
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()

        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)) # Move Y position (slow axis)
            wait_until_stable(amc, axis=2)
            # Apply snake scan to the X-axis (fast axis)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1]
            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                try:
                    amc.move.setControlTargetPosition(0, int(x * 1000)) # Move X position
                    wait_until_stable(amc, axis=0)
                    x_act = amc.move.getPosition(0) / 1000
                    y_act = amc.move.getPosition(2) / 1000
                    
                    # Get the counts from the measurement that just finished
                    cnt = sn.getCountRates()
                    total = cnt[d1] + cnt[d2]
                    
                    # i = y-index (row), j = x-index (column)
                    Z[i, j] = total
                    Zlog[i, j] = np.log10(total + 1)

                    if total > max_int:
                        max_int, best_x, best_y = total, x_act, y_act
                    
                    data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

                    point_counter += 1
                    elapsed = time.time() - start_time
                    avg_time = elapsed / point_counter if point_counter > 0 else 0
                    rem = avg_time * (total_points - point_counter)
                    mins, secs = divmod(int(rem), 60)
                    print(f'Scan progress: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

                    # === Plot Update (after each point) ===
                    global_max = np.amax(Z) if point_counter > 0 else 1
                    global_log_max = np.amax(Zlog) if point_counter > 0 else 1
                    
                    img1.set_data(Z); 
                    #img2.set_data(Zlog)
                    img1.set_clim(vmin=0, vmax=global_max)
                    #img2.set_clim(vmin=0, vmax=global_log_max)
                    ax1.set_title(f'PL Map (Linear) – Max: {max_int:.0f} @ ({best_x:.2f}, {best_y:.2f})')
                    
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                except Exception as e:
                    print(f'\nError at ({x:.2f}, {y:.2f}): {e}')

        # === Finish Scan ===
        print("\nScan complete.")
        plt.ioff()
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")
        if show_plot:
            plt.show()

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    finally:
        # === Cleanup Resources ===
        if data_file_handle:
            data_file_handle.close()
            print("Data file closed.")
        if sn:
            sn.closeDevice(0)
            print("Detector device closed.")
        if amc:
            for axis in [0, 1, 2]:
                amc.control.setControlOutput(axis, True); amc.control.setControlMove(axis, True)
            amc.close()
if __name__ == '__main__':
    # === Configuration ===
    # Define the scan using a center point, scan size, and focus position.
    run_pl_scan(
        center_x=65,
        center_y=-370,
        center_f=-9.8,      # Focus position for the Z-axis in µm
        x_size=60,         # Total width of the scan area in µm
        y_size=60,         # Total height of the scan area in µm
        step=5,
        detector_config=2,
        amc_address='amc100num-a01-0248.local'
    )

