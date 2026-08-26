#Python
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time
import pyvisa

#Devices
import AMC 
from snAPI.Main import * 
from taiko_driver import TaikoLaser, PicoQuantException


# Scale plots for 4K resolution
mpl.rcParams['figure.dpi'] = 200        # Increase DPI
mpl.rcParams['savefig.dpi'] = 300       # Higher quality saved images
mpl.rcParams['figure.figsize'] = [10, 6]  # Default figure size in inches
mpl.rcParams['font.size'] = 14           # Increase font size for readability


# 20-category tab20 color palette using updated Matplotlib API
TAB20_COLORS = plt.colormaps['tab20'].colors


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

def start_apds(detector_config=None, read_counts=False, graph_counts=False):
    """
    Initializes the APD detector, reads, or graphs count rates.
    
    Args:
        detector_config (int, optional): Selects detector config 1 or 2. 
                                         Defaults to None.
        read_counts (bool, optional): If True, prints count rates once. 
                                      Defaults to False.
        graph_counts (bool, optional): If True, plots count rates in a loop.
                                       Defaults to False.
    """
    
    # --- Init snAPI Detector ---
    # Define paths outside the function if they are constant
    # or pass them as arguments to make the function more reusable.
    config_path_1_det = r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\Exciletas_MH.ini'
    config_path_2_det = r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\MPDs_MH.ini'

    sn = snAPI(libType=LibType.MH)
    sn.closeDevice()
    
    if not sn.getDevice(0):
        raise ConnectionError('MH detector not found')
    
    sn.setLogLevel(LogLevel.Device, False)
    sn.setLogLevel(LogLevel.Api, False)
    sn.initDevice(MeasMode.T2)
    
    if detector_config == 1:
        d1, d2 = 1, 2
        sn.loadIniConfig(config_path_1_det)
    elif detector_config == 2: # Added explicit check for config 2
        d1, d2 = 3, 4
        sn.loadIniConfig(config_path_2_det)
    else:
        # Default behavior if no config is selected
        print("No detector configuration selected. Using defaults.")
        d1, d2 = 1, 2
        sn.loadIniConfig(config_path_1_det) # Default to config 1

    print(f"Using detector configuration {detector_config} (channels {d1}, {d2})")
    
    if read_counts: # Added colon
        print(sn.getCountRates())
    
    if graph_counts:
        start_time = time.time()
        print("To stop plotting press CTRL + C)")
        
        # Initialize a list to store data for plotting
        times = []
        counts1 = []
        counts2 = []
        totals = []
        
        try:
            plt.ion() # Turn on interactive plotting mode
            fig, ax = plt.subplots() # Create a figure and axes
            ax.set_title('Power dependence comparison') # Title should be outside the loop
            ax.set_xlabel('Elapsed Time (s)') # Changed label to reflect plotting time
            ax.set_ylabel('Counts (a.u.)')
            ax.set_xlim(0, None)
            ax.set_ylim(0, None)
            
            # Initialize plot lines
            line1, = ax.plot([], [], 'r-', label=f'Channel {d1}')
            line2, = ax.plot([], [], 'b-', label=f'Channel {d2}')
            line_total, = ax.plot([], [], 'g-', label='Total')
            ax.legend(loc='upper left')

            while True:
                # Get and process count data
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]
                
                elapsed_time = time.time() - start_time
                
                # Append data
                times.append(elapsed_time)
                counts1.append(cnt[d1])
                counts2.append(cnt[d2])
                totals.append(total)

                # Update plot data
                line1.set_data(times, counts1)
                line2.set_data(times, counts2)
                line_total.set_data(times, totals)

                # Adjust plot limits to auto-scale
                ax.relim()
                ax.autoscale_view(True,True,True)
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                
                plt.pause(0.1) # Pause to allow events to be processed

        except KeyboardInterrupt:
            print("Plotting stopped by user.")
        finally:
            plt.ioff() # Turn off interactive plotting
            plt.close(fig) # Close the figure
            
    return sn , d1, d2 # Return the sn object for further use outside the function  

def detector_switch(moveto = 'camera',ESP_address="GPIB1::7::INSTR"):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    
    if moveto == 'apd':
        try:
            print("Detection axis moving to 0mm for APDs")
            esp.write("3PA0")
            time.sleep(5)
            pos_now = esp.query("3TP?")
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
def filter_switch(moveto = 'no',ESP_address="GPIB1::7::INSTR"):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    
    if moveto == 'no':
        try:
            print("Filter axis moving to -24mm for No Filter")
            esp.write("2PA-24")
            time.sleep(5)
            pos_now = esp.query("2TP?")
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
        print(f"Attempting to connect to AMC controller at {amc_address}...")
        amc = AMC.Device(amc_address)
        amc.connect()
        
        # Configure axes for control and movement
        for axis in [0, 1, 2]:
            amc.control.setControlOutput(axis, True)
            amc.control.setControlMove(axis, True)
            
        print(f"Successfully connected to AMC controller at {amc_address}")
        
        # Return the connected device object so it can be used later
        return amc

    except Exception as e:
        print(f"ERROR: Failed to connect or initialize AMC controller: {e}")
        # Clean up by closing the connection if an error occurs
        if amc:
            amc.close()
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

def focus_sweep(fbase=None, fstep=0.1, fsize=50):
    amc, sn = None, None # Initialize for the finally block
    try:
        amc = start_attocube()
        sn, d1, d2 = start_apds()

        # Determine starting focus
        if fbase is not None:
            fnow = fbase
        else:
            fnow = amc.move.getPosition(1) / 1000

        # Define the range from low to high
        fstart = fnow - (fsize/2)
        fend = fnow + (fsize/2)
        frange = np.arange(fstart, fend + fstep, fstep)

        # Initialize data lists
        focus, counts1, counts2, totals = [], [], [], []
        maxc, bestf = 0, fnow

        # Setup interactive plot
        plt.ion()
        fig, ax = plt.subplots()
        ax.set_title('Focus Sweep')
        ax.set_xlabel('Focus (µm)')
        ax.set_ylabel('Counts (cps)')
        line1, = ax.plot([], [], 'r.-', label=f'Channel {d1}')
        line2, = ax.plot([], [], 'b.-', label=f'Channel {d2}')
        line_total, = ax.plot([], [], 'g.-', label='Total')
        ax.legend(loc='upper left')
        # Removed stray 'best_f' line

        for f in frange:
            amc.move.setControlTargetPosition(1, int(f * 1000))
            wait_until_stable(amc, 1)
            
            cnt = sn.getCountRates()
            total = cnt[d1] + cnt[d2]

            focus.append(f)
            counts1.append(cnt[d1])
            counts2.append(cnt[d2])
            totals.append(total)

            if total > maxc:
                bestf, maxc = f, total

            # Update plot data
            line1.set_data(focus, counts1)
            line2.set_data(focus, counts2)
            line_total.set_data(focus, totals)

            # Update title with best focus found so far
            ax.set_title(f'Focus Sweep | Best F: {bestf:.2f} µm')

            # Auto-scale plot axes
            ax.relim()
            ax.autoscale_view(True, True, True)
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.01)

        print(f"\nScan complete. Best focus found at: {bestf:.2f} µm")
        plt.ioff()
        plt.show()
        return bestf

    finally:
        print("\n--- Cleaning up resources ---")
        if amc:
            amc.close()
            print("Attocube controller closed.")
        if sn:
            sn.closeDevice()
            print("Detector device closed.")
    

def run_pl_scan(center_x=0,center_y=0,center_f=None,x_size=5,y_size=5,step=1,detector_config=2,out_dir_base='./PlotBasic/Output/PLmaps',show_plot=True):
    """
    Performs an automated and optimized photoluminescence (PL) map scan.

    Args:
        center_x (float): Center position of the scan on the X-axis (µm).
        center_y (float): Center position of the scan on the Y-axis (µm).
        center_f (float, optional): Focus position for the Z-axis (µm). If None, focus is not set.
        x_size (float): Total width of the scan area (µm).
        y_size (float): Total height of the scan area (µm).
        step (float): Distance between scan points (µm).
        detector_config (int): Detector configuration (1 or 2).
        out_dir_base (str): Base directory to save the daily output folder.
        show_plot (bool): If True, displays the plot after the scan is complete.
    """
    # === Calculate Scan Boundaries from Center and Size ===
    x_start = center_x - x_size / 2
    x_end = center_x + x_size / 2
    y_start = center_y - y_size / 2
    y_end = center_y + y_size / 2

    # === Setup Output Directory ===
    out_dir = output_dir_folder(base_dir=out_dir_base)

    # === Initialize Resources to None for Robust Cleanup ===
    sn, amc, data_file_handle = None, None, None
    try:
        # === Initialize Devices & Resources ===
        # CORRECTED: Capture the returned device objects and channel numbers
        sn, d1, d2 = start_apds(detector_config=detector_config)
        amc = start_attocube()

        # --- Set Focus (Z-axis, axis 1) if provided ---
        if center_f is not None:
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
        fig, ax1 = plt.subplots()
        img1 = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
        cb1 = fig.colorbar(img1, ax=ax1, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))
        ax1.set_xlabel('X (µm)'); ax1.set_ylabel('Y (µm)')
        ax1.set_xlim(x_start, x_end); ax1.set_ylim(y_start, y_end)
        ax1.invert_xaxis(); ax1.invert_yaxis()
        ax1.set_title('PL map - Raw counts')
        fig.tight_layout()

        # === Output File Setup (Open once) ===
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'plmap_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')
        
        print(f'Saving data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# PL Mapping - {timestamp}\n')
        data_file_handle.write(f'# Center X: {center_x}, Center Y: {center_y}, Center F: {center_f}\n')
        # CORRECTED: Syntax for the f-string
        data_file_handle.write(f'# Numpy Shape (X, Y): {x_pos.shape[0]}, {y_pos.shape[0]}\n')
        data_file_handle.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')

        # === Scan Loop (Outer loop: Y, Inner loop: X) ===
        max_int, best_x, best_y = 0, x_start, y_start
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()

        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)) # Move Y
            wait_until_stable(amc, axis=2)
            
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1]
            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                try:
                    amc.move.setControlTargetPosition(0, int(x * 1000)) # Move X
                    wait_until_stable(amc, axis=0)
                    
                    x_act = amc.move.getPosition(0) / 1000
                    y_act = amc.move.getPosition(2) / 1000
                    
                    cnt = sn.getCountRates()
                    total = cnt[d1] + cnt[d2]
                    
                    Z[i, j] = total
                    Zlog[i, j] = np.log10(total + 1)

                    if total > max_int:
                        max_int, best_x, best_y = total, x_act, y_act
                    
                    data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

                    point_counter += 1
                    elapsed = time.time() - start_time
                    avg_time = elapsed / point_counter
                    rem = avg_time * (total_points - point_counter)
                    mins, secs = divmod(int(rem), 60)
                    print(f'Scan progress: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

                    # === Plot Update ===
                    global_max = np.amax(Z)
                    img1.set_data(Z)
                    img1.set_clim(vmin=0, vmax=global_max)
                    ax1.set_title(f'PL Map (Linear) – Max: {max_int:.0f} @ ({best_x:.2f}, {best_y:.2f})')
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                except Exception as e:
                    print(f'\nError at point ({x:.2f}, {y:.2f}): {e}')

        # === Finish Scan ===
        print("\nScan complete.                                 ")
        plt.ioff()
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")
        if show_plot:
            plt.show()

    except Exception as e:
        print(f"\nA critical error occurred: {e}")
    
    finally:
        # === Cleanup Resources ===
        print("\n--- Cleaning up resources ---")
        if data_file_handle:
            data_file_handle.close()
            print("Data file closed.")
        if sn:
            sn.closeDevice()
            print("Detector device closed.")
        if amc:
            amc.close()
            print("AMC controller closed.")

# --------------------------------------------------------------------------
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

# --------------------------------------------------------------------------
def plot_plmap(input, mode='custom', flog=False, xi=0, yi=2, zi=6, id='Plot',invxy=False):
    """
    Plots a PL map (2D spatial scan) from the input data.

    Parameters:
    - input: Path to the data file.
    - mode: Predefined mode for selecting x, y, z indices ('apd', 'spec', 'specw').
    - flog: If True, applies log10 scaling to Z axis.
    - xi, yi, zi: Custom indices if mode is 'custom'.
    - id: Identifier to label the plot.
    - invxy=True to invert xy on pl map
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')
    fig, ax = plt.subplots()

    x_index, y_index, z_index = {
        'apd': (0, 2, 6),
        'spec': (0, 2, 5),
        'specw': (0, 2, 8)
    }.get(mode, (xi, yi, zi))
    
    Z = np.log10(v[z_index]) if flog else v[z_index]
    plmap = ax.pcolor(v[x_index], v[y_index], Z, cmap='plasma')
    cbar = fig.colorbar(plmap, ax=ax)
    cbar.set_label('Log10 Counts' if flog else 'Counts')
    if invxy:
        ax.invert_xaxis()
        ax.invert_yaxis()
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    ax.set_title(f'{id}_{os.path.basename(input)}')

# --------------------------------------------------------------------------
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

# --------------------------------------------------------------------------
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

def plot_parameters(xi,yi, xr,yr): #xi adn yi center; xr and yr total x-yrange 
    xs=xi-xr/2
    print(f'xstart= {xs}')
    xe=xi+xr/2
    print(f'xend= {xe}')
    ys=yi-yr/2
    print(f'ystart= {ys}')
    ye=yi+yr/2
    print(f'yend= {ye}')
