#Python
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time
import pyvisa
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
#Devices
try:
    from attocube import AMC 
    from snAPI.Main import * 
    from taiko_driver import TaikoLaser, PicoQuantException
except:
    print(f"Warning: AMC, SN and Laser could not be imported: {e}")
TAB20_COLORS = plt.colormaps['tab20'].colors

# Scale plots for 4K resolution
# mpl.rcParams['figure.dpi'] = 200        # Increase DPI
# mpl.rcParams['savefig.dpi'] = 300       # Higher quality saved images
# mpl.rcParams['figure.figsize'] = [10, 6]  # Default figure size in inches
# mpl.rcParams['font.size'] = 14           # Increase font size for readability
# 20-category tab20 color palette using updated Matplotlib API
def add_stop_button(fig, running_flag):
    """
    Adds a 'Stop' button to a matplotlib figure.
    Args:
        fig: The matplotlib figure to add the button to.
        running_flag (list): A list with one boolean element, e.g., [True].
                             The button click will set this element to False.
    Returns:
        The matplotlib Button widget instance.
    """
    # Define the callback function that the button will trigger
    def stop_loop(event):
        print("Stop button clicked. Halting loop.")
        running_flag[0] = False
    # Create an axes for the button [left, bottom, width, height]
    button_ax = fig.add_axes([0.8, 0.01, 0.1, 0.05])
    # Create the button and connect it to the callback
    stop_button = Button(button_ax, 'Stop')
    stop_button.on_clicked(stop_loop)
    # Return the button so it's not garbage-collected
    return stop_button
def start_laser(power=None, cw=True, softlock=False, engaged=False, close=False, read_power=False):
    """
    Controls and manages a Taiko laser connection.
    
    This function handles connection, parameter setting, and optional disconnection.

    Args:
        power (float, optional): Sets CW power as a percentage (0-100). 
                                 Example: 32.5 for 32.5%. Defaults to None.
        cw (bool, optional): Sets laser to Continuous Wave (CW) mode. Defaults to True.
        softlock (bool, optional): Enables the software lock. Defaults to False.
        engaged (bool, optional): If True, the connection remains open. Defaults to False.
        close (bool, optional): Sets power to 0 and softlocks the laser.
                                Defaults to False.
        read_power (bool, optional): Reads and prints the current CW power. Defaults to False.
    """
    laser = None
    try:
        laser = TaikoLaser()
        laser.open()
        print(f"Connected to: {laser.get_identity()}")

        if close:
            print("Closing laser: Setting power to 0 and softlocking...")
            laser.cw_power_permille = 0
            laser.softlock = True
            print("Laser is now softlocked (power at 0).")
            laser.close()
            return None

        if softlock:
            laser.softlock = True
            print(f"Softlock is now: {laser.softlock} (Laser ENABLED)")

        if power is not None:
            # Convert percentage (e.g., 32.5) to permille (e.g., 325)
            permille_power = int(power * 10)
            print(f"\nSetting CW power to {power}%...")
            laser.cw_power_permille = permille_power
            print(f"CW power is now: {laser.cw_power_permille} / 1000")

        if cw:
            laser.laser_mode = 'cw'

        if read_power:
            # Display current power as a percentage
            current_power_permille = laser.cw_power_permille
            current_power_percent = current_power_permille / 10
            print(f"Current CW power is: {current_power_percent:.1f}% ({current_power_permille} / 1000)")

    except Exception as e:
        print(f"An error occurred: {e}")
        if 'laser' in locals() and laser:
            laser.close()
        return None

    if engaged:
        print("Laser connection remains engaged.")
        return laser
    else:
        print("Laser connection closed.")
        if 'laser' in locals() and laser:
            laser.close()
        return None
def start_apds(detector_config=1, read_counts=False, graph_counts=False):
    """
    Initializes the MH150, and optionally reads or graphs count rates.

    Args:
        detector_config (int): Selects detector config 1 (Exciletas) or 2 (MPDs). Defaults to 2.
        read_counts (bool): If True, prints count rates once. Defaults to False.
        graph_counts (bool): If True, enters a blocking loop to plot live count rates.
                             This mode will automatically close the device upon exit.

    Returns:
        tuple: A tuple of (sn, d1, d2) if initialization is successful and graph_counts is False.
               Returns (None, None, None) on failure or after graph_counts is used.
    """
    # Define configuration paths
    config_path_1_det = r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\Exciletas_MH.ini'
    config_path_2_det = r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\MPDs_MH.ini'

    sn = None  # Initialize sn to None for robust error handling
    try:
        # --- Initialize snAPI Detector ---
        # REMOVED: sn.closeDevice() and sn.exitAPI() calls from the start.
        # This was the likely cause of your device becoming unresponsive.
        sn = snAPI()
        sn.getDevice("1043897") # Register the device by serial number.

        if not sn.initDevice():
            raise ConnectionError('MH150 device initialization failed.')

        if detector_config == 1:
            d1, d2 = 1, 2
            sn.loadIniConfig(config_path_1_det)
            print(f'Using Exciletas: {sn.deviceConfig["ID"]}')
        else:  # Default to config 2
            d1, d2 = 3, 4
            sn.loadIniConfig(config_path_2_det)
            print(f'Using MPDs: {sn.deviceConfig["ID"]}')

        # --- Read Counts Functionality ---
        if read_counts:
            print("Current count rates:", sn.getCountRates())

        # --- Graph Counts Functionality ---
        if graph_counts:
            print("Starting live count graph... Press Ctrl+C or use the 'Stop' button to exit.")
            fig = None # Initialize fig for the finally block
            try:
                start_time = time.time()
                times, counts1, counts2, totals = [], [], [], []
                running = [True] # Use a mutable list for the stop button flag

                plt.ion()
                fig, ax = plt.subplots()
                # stop_button = add_stop_button(fig=fig, running_flag=running) # Assuming this function exists
                
                ax.set_title('Live Detector Counts')
                ax.set_xlabel('Elapsed Time (s)'); ax.set_ylabel('Counts (cps)')
                line1, = ax.plot([], [], 'r.-', label=f'Channel {d1}')
                line2, = ax.plot([], [], 'b.-', label=f'Channel {d2}')
                line_total, = ax.plot([], [], 'g.-', label='Total')
                ax.legend(loc='upper left')
                plt.show(block=False)

                while running[0]:
                    cnt = sn.getCountRates()
                    c1, c2 = int(cnt[d1]), int(cnt[d2])
                    total = c1 + c2
                    
                    times.append(time.time() - start_time)
                    counts1.append(c1)
                    counts2.append(c2)
                    totals.append(total)

                    line1.set_data(times, counts1)
                    line2.set_data(times, counts2)
                    line_total.set_data(times, totals)
                    
                    ax.relim(); ax.autoscale_view()
                    fig.canvas.draw(); fig.canvas.flush_events()
                    plt.pause(0.1)

            except KeyboardInterrupt:
                print("\nGraphing stopped by user.")
            finally:
                # This block ensures cleanup happens for the graph_counts utility
                if fig and plt.fignum_exists(fig.number):
                    plt.ioff()
                    plt.close(fig)
                print("Closing device after graphing.")
                # Since this is a self-contained utility, we close the device it used.
                close_device_all(sn=sn)
                return None, None, None # The device is closed, so we return None

        # If not graphing, return the initialized device handles for external management
        return sn, d1, d2

    except Exception as e:
        print(f"An error occurred in start_apds: {e}")
        # Ensure cleanup happens on any initialization error
        if sn is not None:
             close_device_all(sn=sn)
        return None, None, None
def detector_switch(moveto = 'camera',ESP_address="GPIB1::7::INSTR",showcmd=True):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    
    if moveto == 'apd':
        try:
            if showcmd:
                print("Detection axis moving to 0mm for APDs")
            esp.write("3PA0")
            time.sleep(5)
            pos_now = esp.query("3TP?")
            if showcmd:
                print("Detection axis moving to 0mm for APDs")
            print("Detection axis Position:", pos_now.strip(), "mm")
        except: return None
    if moveto == 'spectro':
        try:
            print("Detection axis moving to -49mm for Spectrometer")
            esp.write("3PA-49")
            time.sleep(5)
            pos_now = esp.query("3TP?")
            print("Detection axis Position:", pos_now.strip(), "mm")
        except: return None
    if moveto == 'camera':
        try:
            print("Detection axis moving to 47.5mm for Camera")
            esp.write("3PA47.5")
            time.sleep(5)
            pos_now = esp.query("3TP?")
            print("Detection axis Position:", pos_now.strip(), "mm")
        except: return None
    return esp
def filter_switch(moveto = 'no',ESP_address="GPIB1::7::INSTR",showcmd=True):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    
    if moveto == 'no':
        try:
            if showcmd:
                print("Filter axis moving to -24mm for No Filter")
            esp.write("2PA-24")
            time.sleep(5)
            pos_now = esp.query("2TP?")
            if showcmd:
                print("Filter axis Position:", pos_now.strip(), "mm")
        except: return None
    if moveto == 'n405':
        try:
            print("Filter axis moving to 0mm for Notch 405nm")
            esp.write("2PA0")
            time.sleep(5)
            pos_now = esp.query("2TP?")
            print("Filter axis Position:", pos_now.strip(), "mm")
        except: return None
    if moveto == 'n533':
        try:
            print("Filter axis moving to 25mm for Notch 533nm")
            esp.write("2PA25")
            time.sleep(5)
            pos_now = esp.query("2TP?")
            print("Filter axis Position:", pos_now.strip(), "mm")
        except: return None
    return esp
def start_attocube(amc_address='amc100num-a01-0248.local'):
    """
    Initializes and connects to an AMC positioner.
    Args:
        amc_address (str): The network address of the AMC controller.
    Returns:
        AMC.Device or None: The connected AMC device object on success, 
                            otherwise returns None on failure.
    """
    amc = None
    try:
        # --- AMC Positioner Init ---
        #print(f"Attempting to connect to AMC controller at {amc_address}...")
        amc = AMC.Device(amc_address)
        amc.connect()
        
        # Configure axes for control and movement
        for axis in [0, 1, 2]:
            amc.control.setControlOutput(axis, True)
            amc.control.setControlMove(axis, True)
            
        print(f"Using AMC : {amc_address}")
        # Return the connected device object so it can be used later
        return amc
    

    except Exception as e:
        print(f"ERROR: Failed to connect or initialize AMC controller: {e}")
        # Clean up by closing the connection if an error occurs
        if amc:
            amc.close()
        return None
def close_device_all(sn=None, amc=None,showcmd=True):
    try:
        if amc:
            amc.close()
            if showcmd:
                print("AMC closed.")
        if sn:
            sn.closeDevice(allDevices=True)
            sn.exitAPI()
            if showcmd:
                print("MH150 closed.")
    except:
        print("Nothing to close.")
        return None
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
def run_focus_sweep(fbase=None, fstep=0.1, fsize=30, movetobest=True, showplt=True, engaged=False, sn=None, d1=None, d2=None, amc=None):
    """
    Performs a Z-axis sweep to find the optimal focus.

    Args:
        ... (your args) ...
        engaged (bool): If True, signals that devices are managed externally and MUST NOT be closed.
        sn, d1, d2, amc: Externally managed device handles.

    Returns:
        float: The best focus position found (in µm). Returns the initial focus on error.
    """
    amc_local = False
    sn_local = False
    fnow = fbase # Keep track of initial focus for error case

    try:
        # --- Device Initialization ---
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        # Corrected the logical condition here
        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds()
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

        if engaged:
            amc_local = sn_local = False

        # --- Sweep Logic ---
        if fbase is None:
            fnow = amc.move.getPosition(1) / 1000
        else:
            fnow = fbase
            
        fstart, fend = fnow - (fsize / 2), fnow + (fsize / 2)
        frange = np.arange(fstart, fend + fstep, fstep)
        focus, totals, ch1s, ch2s = [], [], [], []
        maxc, bestf = -1, fnow

        plt.ion()
        fig, ax = plt.subplots()
        line_ch1, = ax.plot([], [], 'r.-', label='Ch1 Counts')
        line_ch2, = ax.plot([], [], 'g.-', label='Ch2 Counts')
        line_total, = ax.plot([], [], 'b.-', label='Total Counts')
        ax.legend(loc='upper left')
        ax.set_xlabel('Focus (µm)'); ax.set_ylabel('Counts (cps)')
        ax.set_xlim(fstart, fend)

        print("Starting focus sweep...")
        for f in frange:
            amc.move.setControlTargetPosition(1, int(f * 1000))
            wait_until_stable(amc, 1)

            cnt = sn.getCountRates()
            ch1, ch2 = cnt[d1], cnt[d2]
            total = ch1 + ch2
            focus.append(f)
            ch1s.append(ch1)
            ch2s.append(ch2)
            totals.append(total)

            if total > maxc:
                bestf, maxc = f, total
            line_ch1.set_data(focus, ch1s)
            line_ch2.set_data(focus, ch2s)
            line_total.set_data(focus, totals)
            ax.set_title(f'Focus Sweep | Best F: {bestf:.2f} µm')
            ax.relim()
            ax.autoscale_view(True, True, True)
            fig.canvas.draw(); fig.canvas.flush_events()

        print(f"\nFocus sweep complete. Best focus at: {bestf:.2f} µm")
        if movetobest:
            amc.move.setControlTargetPosition(1, int(bestf * 1000))
            wait_until_stable(amc, 1)
            print(f"Moved to best focus: {bestf:.2f} µm")

        plt.ioff()
        if showplt: plt.show()
        else: plt.close(fig)

        return bestf

    except Exception as e:
        print(f"An error occurred during focus sweep: {e}")
        return fnow # Return original focus on error

    finally:
        # --- Cleanup ---
        # Close devices only if they were opened locally within this function.
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)
def run_pl_scan(center_x=0, center_y=0, center_f=None,
                focus_sweep=False, f_size=50,
                x_size=5, y_size=5, step=1,
                detector_config=2,
                logz=False,
                out_dir_base='C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/PLmaps',
                show_plot=True,
                amc=None, sn=None, d1=None, d2=None):
    """
    Performs a 2D photoluminescence scan. Manages its own device lifecycle
    if handles are not provided, making it suitable for single calls or loops.
    """
    amc_local = False
    sn_local = False
    data_file_handle = None

    try:
        # === Initialize Devices (if not provided) ===
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

        # === Setup Scan Area, Output, and Focus ===
        x_start, x_end = center_x - (x_size / 2), center_x + (x_size / 2)
        y_start, y_end = center_y - (y_size / 2), center_y + (y_size / 2)
        out_dir = output_dir_folder(base_dir=out_dir_base)

        if center_f is not None:
            print(f"Setting initial focus (Z-axis) to: {center_f} µm")
            amc.move.setControlTargetPosition(1, int(center_f * 1000))
            wait_until_stable(amc, axis=1)

        fnow = center_f if center_f is not None else amc.move.getPosition(1) / 1000
        
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(center_y * 1000)); wait_until_stable(amc, axis=2)
        
        if focus_sweep:
            print(f"Running focus sweep around: {fnow:.2f} µm")
            # Pass existing handles and set 'engaged=True' to prevent closing.
            amc
            best_f = run_focus_sweep(fbase=fnow, sn=sn, amc=amc, d1=d1, d2=d2,
                                     movetobest=True, showplt=False, fsize=f_size, engaged=True)
            fnow = best_f
            time.sleep(5)
        center_f = fnow # Final focus position
        print(f"Initial pos (x,y,z) :  ({center_x:.2f}, {center_y:.2f}, {center_f:.2f}) µm")
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
        ax1.set_title('PL map'); fig.tight_layout()

        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'plmap_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')

        print(f'Saving data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# PL Mapping - {timestamp}\n# Center X: {center_x}, Y: {center_y}, F: {center_f}\n')
        data_file_handle.write(f'# readback numpy shape for line part: {len(x_pos)}, {len(y_pos)} \n')
        data_file_handle.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')

        # === Start Scan Loop ===
        max_int, best_x, best_y = -1, x_start, y_start
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()

        amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(y_start * 1000)); wait_until_stable(amc, axis=2)

        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)); wait_until_stable(amc, axis=2)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1] # Serpentine path

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, axis=0)

                x_act, y_act = amc.move.getPosition(0)/1000, amc.move.getPosition(2)/1000
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]

                Z[i, j] = np.log10(total + 1) if logz else total

                # Always compare raw counts to find the true maximum
                if total > max_int:
                    max_int, best_x, best_y = total, x_act, y_act

                data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

                point_counter += 1
                elapsed = time.time() - start_time
                rem_time = (elapsed / point_counter) * (total_points - point_counter)
                mins, secs = divmod(int(rem_time), 60)
                print(f'Scan: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

                # Update plot
                img1.set_data(Z)
                img1.set_clim(vmin=Z.min(), vmax=Z.max())
                title = f'PL Map ({"Log" if logz else "Linear"})–Max: {max_int:.0f} @({best_x:.2f},{best_y:.2f})'
                ax1.set_title(title)
                fig.canvas.draw(); fig.canvas.flush_events()

        print("\nScan complete.")
        plt.ioff()
        plt.savefig(plot_file); print(f"Plot saved to: {plot_file}")
        if show_plot: plt.show()
        else: plt.close(fig)

    except Exception as e:
        print(f"\nA critical error occurred during PL scan: {e}")
        return None, None, None, None, None

    finally:
        # === Cleanup Resources ===
        print("\n--- Cleaning up PL scan resources ---")
        if data_file_handle:
            data_file_handle.close(); print("Data file closed.")

        # Close devices ONLY if they were opened by this function call.
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)

    return best_x, best_y, center_f, Z, extent
def run_focus_plane_model(cal_distance=500, amc=None, sn=None, d1=None, d2=None, engaged=False):
    """
    Calibrates the sample's focus plane by measuring the optimal focus at three
    distinct points and solving for the plane equation z = ax + by + c.

    Args:
        cal_distance (float): The distance (µm) for the calibration triangle sides.
        amc (AMC.Device, optional): Existing AMC controller object. If None, one will be created.
        sn (snAPI, optional): Existing detector object. If None, one will be created.
        d1, d2 (int, optional): Detector channel numbers.
        engaged (bool): If True, leaves devices open on exit. Defaults to False.

    Returns:
        tuple (a, b, c) or None: The coefficients of the plane equation on success, else None.
    """
    try:
        # --- Initialize Devices if not provided ---
        if amc is None:
            amc = start_attocube()
        if sn is None:
            sn, d1, d2 = start_apds(detector_config=2)

        x_axis, y_axis = 0, 2
        print("\n--- Starting Focus Plane Calibration ---")

        # --- Define the three calibration points ---
        x_start = amc.move.getPosition(x_axis) / 1000
        y_start = amc.move.getPosition(y_axis) / 1000
        
        points_xy = [
            (x_start, y_start),
            (x_start + cal_distance, y_start),
            (x_start, y_start + cal_distance)
        ]
        points_3d = []

        # --- Find the optimal Z focus at each point ---
        for i, (x, y) in enumerate(points_xy):
            print(f"\nCalibrating Point {i+1}/3 at (X={x:.2f}, Y={y:.2f})...")
            amc.move.setControlTargetPosition(x_axis, int(x * 1000))
            amc.move.setControlTargetPosition(y_axis, int(y * 1000))
            wait_until_stable(amc, x_axis)
            wait_until_stable(amc, y_axis)

            # Run a focus sweep, keeping devices engaged
            best_z = run_focus_sweep(amc=amc, sn=sn, d1=d1, d2=d2, 
                                     fsize=50, fstep=0.1, movetobest=True, 
                                     showplt=False, engaged=True)
            points_3d.append((x, y, best_z))
            print(f"-> Best focus Z found at: {best_z:.2f} µm")

        # --- Solve for the plane equation z = ax + by + c ---
        print("\n--- Measured Calibration Points (X, Y, Z) ---")
        for p in points_3d:
            print(f"  ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})")

        M = np.array([[p[0], p[1], 1] for p in points_3d])
        z_vector = np.array([p[2] for p in points_3d])
        
        try:
            coeffs = np.linalg.solve(M, z_vector)
            a, b, c = coeffs
            print("\n--- Plane Equation Solved ---")
            print(f"Equation: z = {a:.6f}*x + {b:.6f}*y + {c:.2f}")
            return a, b, c
        except np.linalg.LinAlgError:
            print("ERROR: Could not solve for the plane. Points may be collinear.")
            return None

    except Exception as e:
        print(f"An error occurred during focus plane calibration: {e}")
        return None
    finally:
        if not engaged:
            print("\n--- Closing devices from plane calibration ---")
            close_device_all(sn=sn, amc=amc)            
def run_pl_scan_focusplanemodel(center_x=0, center_y=0, x_size=5, y_size=5, step=1,
                                detector_config=2, logz=False,
                                out_dir_base='C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/PLmaps_autofocus',
                                show_plot=True, cal_distance=500,
                                plane_coeffs=None,
                                amc=None, sn=None, d1=None, d2=None):
    """
    Performs a PL map scan with dynamic focus correction based on a 3-point plane model.

    If `plane_coeffs` are provided, it uses them directly. Otherwise, it runs a new
    calibration routine automatically before starting the scan. It can operate with
    pre-initialized device objects or handle initialization and cleanup internally.

    Args:
        center_x, center_y (float): Center position of the scan (µm).
        x_size, y_size (float): Total dimensions of the scan area (µm).
        step (float): Distance between scan points (µm).
        detector_config (int): Detector configuration (1 or 2).
        logz (bool): If True, plots and saves the Z-axis data on a log10 scale.
        out_dir_base (str): Base directory to save the output.
        show_plot (bool): If True, displays the plot after the scan is complete.
        cal_distance (float): Distance for the focus plane calibration triangle (µm).
        plane_coeffs (tuple, optional): Pre-calculated plane coefficients (a, b, c).
                                         If None, a new calibration is performed.
        amc (AMC.Device, optional): An existing, engaged AMC controller object.
        sn (snAPI, optional): An existing, engaged detector object.
        d1, d2 (int, optional): Detector channel numbers for the existing sn object.
    """
    try:
        # --- Initialize Devices if not provided ---
        if amc is None:
            amc = start_attocube()
        if sn is None:
            sn, d1, d2 = start_apds()
        if not sn or not amc:
            raise ConnectionError("Failed to start one or more devices.")

        # --- Calibrate Focus Plane if needed ---
        if plane_coeffs is None:
            print("No plane coefficients provided, running new calibration...")
            amc.move.setControlTargetPosition(0, int(center_x * 1000))
            amc.move.setControlTargetPosition(2, int(center_y * 1000))
            wait_until_stable(amc, 0)
            wait_until_stable(amc, 2)
            
            plane_coeffs = run_focus_plane_model(cal_distance=cal_distance, amc=amc, sn=sn, d1=d1, d2=d2, engaged=True)
            if plane_coeffs is None:
                raise RuntimeError("Focus plane calibration failed. Aborting scan.")
        else:
            print("Using provided plane coefficients.")

        a, b, c = plane_coeffs
        
        # --- Grid and Plot Setup ---
        x_start, x_end = center_x - (x_size / 2), center_x + (x_size / 2)
        y_start, y_end = center_y - (y_size / 2), center_y + (y_size / 2)
        out_dir = output_dir_folder(base_dir=out_dir_base)

        x_pos = np.arange(x_start, x_end + step, step)
        y_pos = np.arange(y_start, y_end + step, step)
        Z = np.zeros((len(y_pos), len(x_pos)))
        extent = [x_start, x_end, y_start, y_end]

        plt.ion()
        fig, ax1 = plt.subplots()
        img1 = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
        cb1 = fig.colorbar(img1, ax=ax1, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))
        ax1.set_xlabel('X (µm)'); ax1.set_ylabel('Y (µm)')
        ax1.set_xlim(x_start, x_end); ax1.set_ylim(y_start, y_end)
        ax1.invert_xaxis(); ax1.invert_yaxis()

        # --- Output File Setup ---
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'plmap_af_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_af_data_{timestamp}.txt')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# Auto-Focus PL Mapping - {timestamp}\n')
        data_file_handle.write(f'# Center: ({center_x}, {center_y}), Size: ({x_size}, {y_size}), Step: {step}\n')
        data_file_handle.write(f'# Plane Equation: z = {a:.6f}*x + {b:.6f}*y + {c:.2f}\n')
        data_file_handle.write('# x_req\ty_req\tz_calc\tx_act\ty_act\tz_act\tcount1\tcount2\ttotal\n')
        
        # --- Scan Loop with Dynamic Focus ---
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()
        max_int, best_x, best_y = 0, x_start, y_start

        for i, y in enumerate(y_pos):
            # Serpentine scan path for efficiency
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1]
            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                
                # *** DYNAMIC FOCUS CALCULATION AND MOVE ***
                target_z = a * x + b * y + c
                amc.move.setControlTargetPosition(0, int(x * 1000))
                amc.move.setControlTargetPosition(2, int(y * 1000))
                amc.move.setControlTargetPosition(1, int(target_z * 1000))
                wait_until_stable(amc, 0)
                wait_until_stable(amc, 2)
                wait_until_stable(amc, 1)

                # --- Data Acquisition ---
                x_act = amc.move.getPosition(0) / 1000
                y_act = amc.move.getPosition(2) / 1000
                z_act = amc.move.getPosition(1) / 1000
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]
                total_val = np.log10(total + 1) if logz else total
                Z[i, j] = total_val

                if total_val > max_int:
                    max_int, best_x, best_y = total_val, x_act, y_act
                
                data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{target_z:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{z_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

                # --- Progress Update and Live Plotting ---
                point_counter += 1
                elapsed = time.time() - start_time
                rem = (elapsed / point_counter) * (total_points - point_counter)
                mins, secs = divmod(int(rem), 60)
                print(f'Scan: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

                img1.set_data(Z)
                img1.set_clim(vmin=Z.min(), vmax=Z.max())
                ax1.set_title(f'Auto-Focus PL Map – Max: {max_int:.0f} @ ({best_x:.2f}, {best_y:.2f})')
                fig.canvas.draw()
                fig.canvas.flush_events()

        print("\nScan complete.                                       ")
        plt.ioff()
        plt.savefig(plot_file)
        if show_plot: plt.show()

    except Exception as e:
        print(f"\nA critical error occurred: {e}")
    finally:
        print("\n--- Cleaning up resources ---")
        if data_file_handle: data_file_handle.close(); print("Data file closed.")
        close_device_all(sn=sn,amc=amc)
def multi_run_plscan():
    # === DEFINE YOUR SCAN JOBS HERE ===
    scan_jobs = [
        {
            'center_x': 65, 'center_y': -370, 'center_f': -9.8,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake K10'
        },
        {
            'center_x': 1120, 'center_y': -285, 'center_f': -17,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake K13'
        },
    ]
    print(f"Starting batch of {len(scan_jobs)} PL scans...")

    for i, params in enumerate(scan_jobs):
        print(f"\n--- Running Scan Job {i+1}/{len(scan_jobs)} ({params.get('comment', 'No comment')}) ---")
        print(f"Parameters: {params}")
        
        try:
            # This will cause the plot to appear and pause the script.
            run_pl_scan(
                center_x=params['center_x'],
                center_y=params['center_y'],
                center_f=params['center_f'],
                x_size=params['x_size'],
                y_size=params['y_size'],
                step=params['step'],
                detector_config=2,
                show_plot=False,
                focus_sweep=True
                
            )
        except Exception as e:
            print(f"!!! An error occurred during scan job {i+1}: {e} !!!")
            print("Continuing with the next job.")

    print("\nAll scan jobs are complete.")
def run_pl_position_optimizer(scan_size=2, scan_step=0.1, movetoxy=True, run_focus_sweep=False,show_plot=True,
                              sn=None, d1=None, d2=None, amc=None):
    """
    Runs a small PL scan to find the brightest spot. Can be used as a standalone
    tool (showing a plot) or as a data provider for other functions.
    
    Returns:
        tuple: Best X, Y, F coordinates, and the map data (Z_map, extent).
    """
    sn_local = False
    amc_local = False
    
    # Initialize local variables to ensure they exist for the return statement
    bx, by, bf = None, None, None
    Z_map, extent = None, None

    try:
        # --- Robust Device Initialization ---
        if sn is None:
            sn, d1, d2 = start_apds(detector_config=2)
            if sn is None: raise ConnectionError("Optimizer failed to start APDs.")
            sn_local = True
            
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Optimizer failed to start Attocube.")
            amc_local = True

        print("Starting position optimization scan...")
        x_now = amc.move.getPosition(0) / 1000
        y_now = amc.move.getPosition(2) / 1000
        f_now = amc.move.getPosition(1) / 1000
        
        # We now pass the show_plot flag and capture the map data in the return.
        bx, by, bf, Z_map, extent = run_pl_scan(
            center_x=x_now, center_y=y_now, center_f=f_now,
            x_size=scan_size, y_size=scan_size, step=scan_step,
            focus_sweep=run_focus_sweep,
            show_plot=show_plot, # <-- Pass the flag here
            sn=sn, d1=d1, d2=d2, amc=amc
        )
        print(f"Optimization scan complete. Best position found: ({bx:.2f}, {by:.2f})")

        # --- Move to Best Position ---
        if movetoxy:
            print(f"Moving to best X-Y position...")
            amc.move.setControlTargetPosition(0, int(bx * 1000))
            wait_until_stable(amc, 0)
            amc.move.setControlTargetPosition(2, int(by * 1000))
            wait_until_stable(amc, 2)
            print("Move complete.")
            
    finally:
        # --- Cleanup Locally Opened Devices ---
        # The 'engaged' logic is handled by only closing if opened locally.
        if sn_local: 
            close_device_all(sn=sn)
            print("Locally started detector closed.")
        if amc_local: 
            close_device_all(amc=amc)
            print("Locally started positioner closed.")
            
    # --- UPDATED return statement ---
    return bx, by, bf, Z_map, extent
def _set_tab20_cycle(ax):
    """
    Sets the color cycle of the given axes to the tab20 color palette.
    Ensures this is done only once per axes object.
    """
    if not hasattr(ax, '_color_cycle_set'):
        ax.set_prop_cycle(color=TAB20_COLORS)
        ax._color_cycle_set = True
def plot_spectrum(input, compare=False, fig=11, id='Plot'):
    """
    Plots the photoluminescence (PL) spectrum from the input file.

    Parameters:
    - input: Path to the data file.
    - compare: Whether to overlay on an existing plot (True) or create a new one.
    - fig: Figure number to use if comparing multiple plots.
    - id: Identifier to label the plot.
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')

    if compare:
        plt.figure(fig)
        ax = plt.gca()
    else:
        _, ax = plt.subplots()

    _set_tab20_cycle(ax)

    ax.plot(v[1], v[2], label=f'{id}_{os.path.basename(input)}')
    ax.set_xlim(np.min(v[1]), np.max(v[1]))
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Counts (Arb.)')
    ax.grid(True)

    ax.set_title('PL Spectrum compare' if compare else os.path.basename(input))
    ax.legend(loc='upper right')
def plot_plmap(fpath, mode='custom', flog=False, xi=0, yi=1, zi=2, 
               id='Plot', invxy=False, force1d=False, encoding='latin1'):
    """
    Plots a photoluminescence (PL) map from a text data file.

    This compact version automatically detects a shape hint in the file header
    (e.g., '#readback numpy shape for line part: Y, X') to use a fast
    numpy.reshape. If the hint is missing or reshape fails, it falls back
    to a robust manual gridding method.
    """
    fast_shape = None
    try:
        with open(fpath, 'r', encoding=encoding) as f:
            for line in f:
                if match := re.search(r'# readback numpy shape for line part:\s*(\d+),\s*(\d+)', line):
                    fast_shape = (int(match.group(1)), int(match.group(2)))
                    print(f"Found numpy readback in file, using...") if force1d is not True else print(f"Found numpy readback in file but force 1D is true...")
                    break
    except Exception:
        pass

    try:
        cols = np.loadtxt(fpath, unpack=True, encoding=encoding)
        idx_map = {'apd': (0, 2, 6), 'spec': (0, 2, 5), 'specw': (0, 2, 8), 'vscode': (0, 1, 6)}
        xi, yi, zi = idx_map.get(mode, (xi, yi, zi))
        x, y, z = cols[xi], cols[yi], cols[zi]
    except Exception as e:
        print(f"Failed to load or parse data: {e}")
        return

    if flog:
        z = np.log10(z, where=(z > 0), out=np.full_like(z, np.nan))
    
    use_fast_path = fast_shape is not None and force1d is not True 
    
    if use_fast_path:
        try:
            Z = z.reshape(fast_shape)
            extent = [x.min(), x.max(), y.min(), y.max()]
        except ValueError:
            use_fast_path = False
    
    if not use_fast_path:
        def make_grid(gx, gy, gz):
            x_u, y_u = np.unique(gx), np.unique(gy)
            X, Y = np.meshgrid(x_u, y_u)
            Z_grid = np.full_like(X, np.nan)
            Z_grid[np.searchsorted(y_u, gy), np.searchsorted(x_u, gx)] = gz
            return X, Y, Z_grid
        Xg, Yg, Z = make_grid(x, y, z)
        extent = [Xg.min(), Xg.max(), Yg.min(), Yg.max()]

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
    
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Log10 Counts' if flog else 'Counts')
    
    if invxy:
        ax.invert_xaxis()
        ax.invert_yaxis()

    ax.set_xlabel(f'X (um)')
    ax.set_ylabel(f'Y (um)')
    ax.set_title(f'{id}: {os.path.basename(fpath)}')
    #plt.tight_layout()
    plt.show()
def plot_plmap_3d(input_path, res=50,mode='custom', flog=False, xi=0, yi=2, zi=6, id='Plot',invxy=False):
    """
    Plots a 3D contour map from the input data.

    Parameters:
    - input_path: Path to the data file.
    - mode: Predefined mode for selecting x, y, z indices ('apd', 'spec', 'specw', 'vscode').
    - flog: If True, applies log10 scaling to Z axis.
    - xi, yi, zi: Custom indices if mode is 'custom'.
    - id: Identifier to label the plot.
    - invxy: If True, inverts the xy axes.
    """
    def make_grid(x, y, z):
        x_unique = np.unique(x)
        y_unique = np.unique(y)
        X, Y = np.meshgrid(x_unique, y_unique)
        Z = np.full(X.shape, np.nan) # Use nan for missing points
        
        # A more efficient way to fill the grid
        y_map = {val: i for i, val in enumerate(y_unique)}
        x_map = {val: i for i, val in enumerate(x_unique)}
        
        for i in range(len(x)):
            try:
                Z[y_map[y[i]], x_map[x[i]]] = z[i]
            except KeyError:
                continue
        return X, Y, Z

    v = readfile(input_path, encoding='latin1', multi_sweep='force')
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    x_index, y_index, z_index = {
        'apd': (0, 2, 6),
        'spec': (0, 2, 5),
        'specw': (0, 2, 8),
        'vscode': (0, 1, 6) 
    }.get(mode, (xi, yi, zi))

    x_data = v[x_index]
    y_data = v[y_index]
    z_data = v[z_index]

    if flog:
        # Apply log scaling before gridding
        z_data = np.log10(z_data, where=z_data > 0, out=np.full_like(z_data, np.nan))
    
    # The data is now always gridded, regardless of the 'mode'
    
    if x_data.ndim == 1:
        # Data is 1D, so it needs to be gridded.
        print("Detected 1D data. Applying make_grid...")
        if flog:
            z_data = np.log10(z_data, where=z_data > 0, out=np.full_like(z_data, np.nan))
        X, Y, Z = make_grid(x_data, y_data, z_data)
        
    elif x_data.ndim == 2:
        # Data is already 2D, so we can use it directly.
        print("Detected 2D gridded data. Using directly...")
        X, Y, Z = x_data, y_data, z_data
        if flog:
            Z = np.log10(Z, where=Z > 0, out=np.full_like(Z, np.nan))
            
    else:
        raise ValueError(f"Unsupported data dimension: {x_data.ndim}. Data must be 1D or 2D.")
    
    contour_plot = ax.contour3D(X, Y, Z, res, cmap='plasma')
    
    cbar = fig.colorbar(contour_plot, shrink=0.6, aspect=10, pad=0.1)
    cbar.set_label('Log10 Counts' if flog else 'Counts')
    
    if invxy:
        ax.invert_xaxis()
        ax.invert_yaxis()
        
    ax.set_title(f'{id}_{os.path.basename(input_path)}')
    ax.set_xlabel(f'X (column {x_index})')
    ax.set_ylabel(f'Y (column {y_index})')
    ax.set_zlabel(f'Z (column {z_index})')
    
    plt.show()
def plot_powerd(input, compare=False, fig=66, mode='custom', xi=2, yi=5, id='Plot'):
    """
    Plots power dependence of PL intensity from the input file.

    Parameters:
    - input: Path to the data file.
    - compare: Whether to overlay with previous plot.
    - fig: Figure number to use if comparing.
    - mode: Predefined index set ('apd', 'spec', 'specw').
    - xi, yi: Custom indices for x and y if mode is 'custom'.
    - id: Identifier to label the plot.
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')

    x_index, y_index = {
        'apd': (2, 5),
        'spec': (2, 6),
        'specw': (5, 7)
    }.get(mode, (xi, yi))

    x = v[x_index] * 1000  # Convert power to mW
    y = v[y_index] - np.min(v[y_index])

    if compare:
        plt.figure(fig)
        ax = plt.gca()
    else:
        _, ax = plt.subplots()

    _set_tab20_cycle(ax)

    ax.plot(x, y, label=f'{id}_{os.path.basename(input)}')
    ax.set_title('Power dependence comparison' if compare else f'Power dependence for {os.path.basename(input)}')
    ax.set_xlabel('Power (mW)')
    ax.set_ylabel('Counts (a.u.)')
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)
    ax.legend(loc='upper left')
def plot_polarization(input, polar=True, mode='custom', flog=False, xi=0, yi=1):
    """
    Plots polarization dependence (as polar or Cartesian plot) of PL intensity.

    Parameters:
    - input: Path to the data file.
    - polar: Whether to plot in polar coordinates (True) or Cartesian (False).
    - mode: Predefined mode for indices ('apd', 'spec', 'specw').
    - flog: If True, applies log10 scaling to intensity values.
    - xi, yi: Custom indices for angle and intensity if mode is 'custom'.
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')

    x_index, y_index = {
        'apd': (0, 4),
        'spec': (0, 5),
        'specw': (0, 6)
    }.get(mode, (xi, yi))

    x = v[x_index]
    y = v[y_index] - np.min(v[y_index])

    if polar:
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
    else:
        fig, ax = plt.subplots()
        x = np.radians(x)

    _set_tab20_cycle(ax)

    if polar:
        ax.scatter(x, y, label=os.path.basename(input), linewidth=0.5)
    else:
        ax.plot(x, y, label=os.path.basename(input))
        ax.set_xlabel('Theta (deg)')
        ax.set_ylabel('Counts (Arb.)')

    ax.set_title('Polarization dependence')
    ax.legend(loc='lower left' if polar else 'best')
    ax.grid(True)
def plot_parameters(xi,yi, xr,yr):
    xs=xi-xr/2
    print(f'xstart= {xs}')
    xe=xi+xr/2
    print(f'xend= {xe}')
    ys=yi-yr/2
    print(f'ystart= {ys}')
    ye=yi+yr/2
    print(f'yend= {ye}')
def run_g2(measure_time_s=600, bin_ps=100, window_ps=100000,detector_config=2,optimize_position=False,save_data=True,output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output',sn=None, d1 = None, d2 = None, amc=None):
    """
    Performs a g2 measurement with optional pre-optimization and a high-performance live plot.

    If optimize_position is True, it displays a 2x2 grid plot.
    If optimize_position is False, it displays a standard 1x2 side-by-side plot.
    
    The measurement loop is controlled by the hardware's status (isFinished), and the
    stop button gracefully ends the measurement by calling stopMeasure().
    """
    sn_local = amc_local = False
    main_fig = None
    a, b = detector_config

    try:
        # === 1. Device Initialization ===
        if sn or d1 or d2 is None:
            print("Initializing APDs...")
            sn, d1, d2 = start_apds()
            sn_local = True
        
        if optimize_position:
            if amc is None:
                print("Initializing Attocube stage controller...")
                amc = start_attocube()
                amc_local = True
            if not amc: raise ConnectionError("Attocube device is required for optimization.")
        
        plt.ion()

        # === 2. Plot Layout Setup ===
        if optimize_position:
            print("Optimizer enabled. Creating 2x2 grid plot layout.")
            main_fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)
            ax_map = axes[0, 0]
            ax_focus = axes[1, 0]
            ax_g2 = axes[0, 1]
            ax_trace = axes[1, 1]
        else:
            print("Standard mode. Creating 1x2 side-by-side plot layout.")
            main_fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
            ax_g2, ax_trace = axes
        
        # === 3. Stop Button Setup ===
        def stop_callback(event):
            print("Stop button pressed. Sending stop command to hardware...")
            sn.correlation.stopMeasure()
        
        stop_ax = main_fig.add_axes([0.9, 0.01, 0.08, 0.04])
        stop_button = Button(stop_ax, 'Stop', hovercolor='0.975')
        stop_button.on_clicked(stop_callback)

        # === 4. Run Optimizer (if enabled) ===
        if optimize_position:
            print("\n--- Running Position and Focus Optimizer ---")
            bx, by, best_f, Z_map, extent = run_pl_position_optimizer(
                scan_size=1, scan_step=0.2, movetoxy=True, run_focus_sweep=True,
                show_plot=False, sn=sn, d1=a, d2=b, amc=amc
            )
            
            ax_map.imshow(Z_map, extent=extent, origin='lower', cmap='plasma', aspect='auto')
            ax_map.set_title(f'Position Scan | Best: ({bx:.2f}, {by:.2f})')
            ax_map.set_xlabel('X (µm)'); ax_map.set_ylabel('Y (µm)')

            focus_positions, focus_counts = focus_data
            ax_focus.plot(focus_positions, focus_counts, 'g.-')
            ax_focus.set_title(f'Focus Sweep | Best: {best_f:.2f} µm')
            ax_focus.set_xlabel('Focus Z (µm)'); ax_focus.set_ylabel('Counts (cps)')
            main_fig.canvas.draw()

        # === 5. Main g(2) Measurement ===
        dt_now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        if save_data:
            os.makedirs(output_dir, exist_ok=True)
            ptu_filename = os.path.join(output_dir, f'g2data_{measure_time_s}s_{dt_now}.ptu')
            details_filename = os.path.join(output_dir, f"g2details_{measure_time_s}s_{dt_now}.txt")
            sn.setPTUFilePath(ptu_filename)
            print(f'\nSaving PTU data to: {os.path.basename(ptu_filename)}')

        sn.correlation.setG2Parameters(a, b, window_ps, bin_ps)
        sn.correlation.measure(int(measure_time_s * 1000), savePTU=save_data)
        start_time = time.time()
        print(f'Starting main g(2) measurement for {measure_time_s} s...')

        # --- Blitting Plot Setup ---
        ax_g2.set_xlabel('Time Delay (ns)'); ax_g2.set_ylabel('g?²?(t)'); ax_g2.grid(True, ls=':')
        line_g2, = ax_g2.plot([], [], 'k-', lw=1.0, animated=True)
        ax_g2.set_ylim(0, 2.5)
        
        ax_trace.set_xlabel('Elapsed Time (s)'); ax_trace.set_ylabel('Count Rate (cps)'); ax_trace.grid(True, ls=':')
        line_ch1, = ax_trace.plot([], [], 'b.--', lw=1, marker='o', ms=4, label=f"Ch {a}", animated=True)
        line_ch2, = ax_trace.plot([], [], 'r.--', lw=1, marker='s', ms=4, label=f"Ch {b}", animated=True)
        ax_trace.legend(loc='upper right')
        
        main_fig.canvas.draw()
        bg_g2 = main_fig.canvas.copy_from_bbox(ax_g2.bbox)
        bg_trace = main_fig.canvas.copy_from_bbox(ax_trace.bbox)

        final_g2, final_lagtimes = None, None

        with open(details_filename, 'w') as f:
            f.write(f"# Measurement Details started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            times, counts1, counts2 = [], [], []

            while not sn.correlation.isFinished():
                g2, lagtimes = sn.correlation.getG2Data()
                if g2 is None or len(g2) < 1:
                    plt.pause(0.1); continue
                
                final_g2, final_lagtimes = g2, lagtimes
                lagtimes_ns = np.array(lagtimes) / 1000.0
                g2_zero = np.min(g2)
                counts = sn.getCountRates()
                
                elapsed_t = time.time() - start_time
                times.append(elapsed_t); counts1.append(counts[a]); counts2.append(counts[b])
                
                percent_done = (elapsed_t * 100) / measure_time_s
                ax_g2.set_title(f'g?²?(t) | g²(0) = {g2_zero:.3f}')
                ax_trace.set_title(f'Time Trace | {percent_done:.1f}% Done ({elapsed_t:.0f}s / {measure_time_s}s)')
                
                line_g2.set_data(lagtimes_ns, g2)
                line_ch1.set_data(times, counts1)
                line_ch2.set_data(times, counts2)

                main_fig.canvas.restore_region(bg_g2); main_fig.canvas.restore_region(bg_trace)
                ax_trace.relim(); ax_trace.autoscale_view()
                ax_g2.draw_artist(line_g2); ax_trace.draw_artist(line_ch1); ax_trace.draw_artist(line_ch2)
                main_fig.canvas.blit(ax_g2.bbox); main_fig.canvas.blit(ax_trace.bbox)
                main_fig.canvas.flush_events()
                plt.pause(0.5)

            if final_g2 is not None:
                f.write("\n# Final g2 data (Time_ps, Norm_Counts)\n")
                final_data_to_save = np.column_stack((final_lagtimes, final_g2))
                np.savetxt(f, final_data_to_save)

        print("Measurement loop ended.")
        if save_data:
            fig_path = os.path.join(output_dir, f'g2plot_{measure_time_s}s_{dt_now}.png')
            main_fig.savefig(fig_path, dpi=150)
            print(f"Final plot saved to: {os.path.basename(fig_path)}")
        
        plt.ioff(); plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # === 6. Final Cleanup ===
        if sn_local and sn:
            print("Closing APD connection.")
            sn.closeDevice(allDevices=True)
        if amc_local and amc:
            print("Closing Attocube connection.")
            amc.close()
        print("Script finished.")