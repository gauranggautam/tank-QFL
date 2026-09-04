# %%
from pyHegel import start_pyHegel
start_pyHegel()

import os, re, time, traceback, builtins
from datetime import datetime
from io import StringIO
# Third-party
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
import pyvisa

TAB20_COLORS = plt.colormaps['tab20'].colors
# Hardware-Specific Imports
uhd_plots = False
#from andor import *
try: from attocube import AMC
except ImportError as e: print(e)

try: from snAPI.Main import *
except ImportError as e: print(e)

#try: from taiko_driver import TaikoLaser, PicoQuantException
#except ImportError as e: print(e)

try: import nidaqmx; from nidaqmx.constants import Edge
except ImportError as e: print(e)

try: import labview_buttons_v2 as lv
except ImportError as e: print(e)

try: from pylablib.devices import Thorlabs
except ImportError as e: print(e)

try: from montana import cryocore
except ImportError as e: print(e)


import os, re, time, traceback, builtins
from datetime import datetime
from io import StringIO

# Third-party
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
import pyvisa

TAB20_COLORS = plt.colormaps['tab20'].colors
# Hardware-Specific Imports
uhd_plots = False

try: from attocube import AMC
except ImportError as e: print(e)

try: from snAPI.Main import *
except ImportError as e: print(e)

#try: from taiko_driver import TaikoLaser, PicoQuantException
#except ImportError as e: print(e)

try: import nidaqmx; from nidaqmx.constants import Edge
except ImportError as e: print(e)

try: import labview_buttons_v2 as lv
except ImportError as e: print(e)


# LabView control imports
#         "btn0",  # scroll
#         "btn1",   #scollup
#         "btn2",   #apdswitch
#         "btn3",   #filterwheel
#         "btn4",   #FW450to420
#         "btn5",   #Detector
#         "btn6",   #D:APDtoSpectro
#         "btn7",   #AcquireAndor(set_settings)
#         "btn8",   #D:SpectrotoAPD
#         "btn9",   #FW420to450
    #     "btn10",  

# LabView controls
def acq_andor(): #Working
    lv.focus_maximiser()
    lv.click_scroll(name="btn1", times=50, delay=0.01)
    lv.click_scroll(name="btn0", times=38, delay=0.01)
    lv.click_button(name="btn2", move_duration=0.1) #apds off
    time.sleep(0.1)
    lv.click_button(name="btn3", move_duration=0.1) #FW
    time.sleep(0.1)
    lv.click_button(name="btn4", move_duration=0.1) #FW450t0420
    time.sleep(0.1)
    #lv.click_button(name="btn5", move_duration=0.1) #DetectorSwitch
    #time.sleep(0.1)
    #lv.click_button(name="btn6", move_duration=0.1) #D toSpectro
    #time.sleep(8)
    detector_switch(moveto="spectro")
    lv.click_button(name="btn7", move_duration=0.1) #Andoracq
    #return lv
def revert_from_andor(): #Workring
    detector_switch(moveto="apd")
    lv.focus_maximiser()
    #lv.click_button(name="btn5", move_duration=0.1) #DetectorSwitch
    #time.sleep(0.1)
    #lv.click_button(name="btn8", move_duration=0.1) #D toAPDs
    #time.sleep(8)
    lv.click_button(name="btn3", move_duration=0.1) #FW
    time.sleep(0.1)
    lv.click_button(name="btn9", move_duration=0.1) #FW420t0450
    time.sleep(0.1)
    lv.click_button(name="btn2", move_duration=0.1)#apds back-on
    #return lv
# Plotting scale for 4K displays
def set_4k():
    # Scale plots for 4K resolution
    mpl.rcParams['figure.dpi'] = 200      # Increase DPI
    mpl.rcParams['savefig.dpi'] = 300     # Higher quality saved images
    mpl.rcParams['figure.figsize'] = [10, 6] # Default figure size in inches
    mpl.rcParams['font.size'] = 14        # Increase font size for readability
    mpl.rcParams['lines.linewidth'] = 2   # Thicker lines   
    mpl.rcParams['lines.markersize'] = 6  # Larger markers
    mpl.rcParams['axes.titlesize'] = 16   # Larger title font size
    mpl.rcParams['axes.labelsize'] = 14   # Larger axis label font size
    mpl.rcParams['xtick.labelsize'] = 12  # Larger x-tick label size
    mpl.rcParams['ytick.labelsize'] = 12  # Larger y-tick label size
    mpl.rcParams['legend.fontsize'] = 12  # Larger legend font size
    uhd_plots = True
    # 20-category tab20 color palette using updated Matplotlib API
def set_size_poster(size=45):
        sz=size
        sz_small = sz - 10
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = sz_small
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['axes.labelweight'] = 'bold'
        plt.rcParams['axes.titlesize'] = sz
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['axes.labelsize'] = sz_small
        plt.rcParams['legend.fontsize'] = sz_small-10
        plt.rcParams['xtick.labelsize'] = sz_small
        plt.rcParams['ytick.labelsize'] = sz_small
        poster = True   
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
# Hardware control functions
# Laser
def set_laser(power=None, cw=True, softlock=False, engaged=False, close=False, read_power=False):
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
        laser = instruments.picoQuant.PicoQuant_Taiko_PDL_M1()
        #print(f"Connected to: {laser.get_identity()}")

        if close:
            print("Closing laser: Setting power to 0 and softlocking...")
            set(laser.cw_power_permille, 0)
            set(laser.softlock_en, True)
            print("Laser is now softlocked (power at 0).")
            unload(laser)
            return None

        
        set(laser.softlock_en, softlock)
        print(f"Softlock is now: {get(laser.softlock_en)} (Laser ENABLED)")

        if power is not None:
            # Convert percentage (e.g., 32.5) to permille (e.g., 325)
            permille_power = int(power * 10)
            print(f"\nSetting CW power to {power}%...")
            set(laser.cw_power_permille, permille_power)
            print(f"CW power is now: {get(laser.cw_power_permille)} / 1000")
            set(laser.softlock_en, False)

        if cw:
            set(laser.laser_mode, "cw")

        if read_power:
            # Display current power as a percentage
            current_power_permille = get(laser.cw_power_permille)
            current_power_percent = current_power_permille / 10
            print(f"Current CW power is: {current_power_percent:.1f}% ({current_power_permille} / 1000)")

    except Exception as e:
        print(f"An error occurred: {e}")
        if 'laser' in locals() and laser:
            laser.close()
            unload(laser)
        return None

    if engaged:
        print("Laser connection remains engaged.")
        return laser
    else:
        print("Laser connection closed.")
        if 'laser' in locals() and laser:
            laser.close()
            unload(laser)
        return None
def start_apds(detector_config=2, read_counts=False, graph_counts=False):
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
        sn = snAPI()
        #sn.closeDevice(allDevices=True)
        #sn = snAPI()
        #sn.exitAPI()
        #sn = snAPI()
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
                #line_total, = ax.plot([], [], 'g.-', label='Total')
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
                    #line_total.set_data(times, totals)
                    
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

def start_daq(device='Dev1',ch1='PFI8', ch2='PFI9',read_counts=False, graph_counts=False, bin=0.1):
    PFI_CH1 = f"/{device}/{ch1}"
    PFI_CH2 = f"/{device}/{ch2}"
    # Channel 2: ctr1 on PFI9
    daq=nidaqmx
    t_ch1=daq.Task()
    #t_ch1.channels.ci_count_edges_count_reset_reset_cnt()
    t_ch1.ci_channels.add_ci_count_edges_chan(
        counter=f"{device}/ctr0",
        edge=Edge.RISING,
        initial_count=0
    )
    t_ch1.ci_channels.all.ci_count_edges_term = PFI_CH1
    
    # Channel 2: ctr1 on PFI9
    t_ch2=daq.Task()
    t_ch2.ci_channels.add_ci_count_edges_chan(
        counter=f"{device}/ctr1",
        edge=Edge.RISING,
        initial_count=0
    )
    t_ch2.ci_channels.all.ci_count_edges_term = PFI_CH2
    print(f'Using MPD with DAQ')
    return daq, t_ch1, t_ch2 
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
def amc_disable():
    amc= start_attocube()
    for axis in [0, 1, 2]:
        #amc.control.setControlOutput(axis, False)
        amc.control.setControlMove(axis, False)
        print(f"Disabled: Axis {axis}")
    amc.close()
def close_device_all(sn=None, amc=None,showcmd=True, daq=None, t_ch1=None, t_ch2=None, spectro=None, camera=None):
    try:
        if amc:
            amc.close()
            if showcmd:
                print("AMC closed.")
        if sn:
            sn.closeDevice(allDevices=True)
            sn.exitAPI()
            time.sleep(3)
            if showcmd:
                print("MH150 closed.")
        if daq:
            if t_ch1:
                t_ch1.stop()
            if t_ch2:
                t_ch2.stop()
            if showcmd:
                print("DAQ closed.") 
        if camera is not None:
            unload(camera)
        if spectro is not None:
            unload(spectro)
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
def amc_move(amc=None, axis=None, d=None):
    if amc is None:
        amc = start_attocube()
    amc.move.setControlTargetPosition(axis, int(d * 1000));wait_until_stable(amc, axis)
def amc_movexyz(x,y,f,amc=None):
    if amc is None:
        amc = start_attocube()
    amc.move.setControlTargetPosition(0, int(x * 1000));wait_until_stable(amc, 0)
    amc.move.setControlTargetPosition(1, int(f * 1000));wait_until_stable(amc, 1)
    amc.move.setControlTargetPosition(2, int(y * 1000));wait_until_stable(amc, 2)      
def output_dir_folder(base_dir=r'D:\Data_Python_PL'):
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
def run_focus_sweep(fbase=None, fstep=0.1, fsize=30, movetobest=True, showplt=True, engaged=False, sn=None, d1=None, d2=None, amc=None, detector_config=2):
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
            sn, d1, d2 = start_apds(detector_config=detector_config)
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
    except KeyboardInterrupt as k:
        print(f"Keyboard interrupt : {k}")
        print(f"Keyboard interrupt : Moving to initial position ---")
        amc.move.setControlTargetPosition(1, int(fnow * 1000)); wait_until_stable(amc, axis=0)
        return fnow
    finally:
        # --- Cleanup ---
        # Close devices only if they were opened locally within this function.
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)
def run_pl_scan(center_x=None, center_y=None, center_f=None,
                focus_sweep=False, f_size=50,
                x_size=5, y_size=5, step=0.1,
                detector_config=2,
                logz=False,
                out_dir_base=r'D:\Data_Python_PL\PLmaps',
                show_plot=True,
                waits=0,
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
        
        center_x = center_x if center_x is not None else amc.move.getPosition(0) / 1000
        center_y = center_y if center_y is not None else amc.move.getPosition(2) / 1000
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
                time.sleep(waits)
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]

                Z[i, j] = np.log10(total + 1) if logz else total

                # Always compare raw counts to find the true maximum
                if total > max_int:
                    max_int, best_x, best_y = total, x_act, y_act
                #if total>2000000:
                #    print(f"Total counts exceded set limit(1M) : {total}")
                #    print(f"Moving to scan start location")
                #    amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
                #    amc.move.setControlTargetPosition(2, int(y_start * 1000)); wait_until_stable(amc, axis=2)
                #    raise Exception(f"Max counts reached {total}: Reduce power")

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
        return None, None, None
    except KeyboardInterrupt as k:
        print(f"Keyboard interrupt : {k}")
        print(f"Keyboard interrupt : Moving to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(center_y * 1000)); wait_until_stable(amc, axis=2)
        return None, None, None    
    finally:
        # === Cleanup Resources ===
        print("\n--- Cleaning up PL scan resources ---")
        if data_file_handle:
            data_file_handle.close(); print("Data file closed.")
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)

    return best_x, best_y, center_f
def run_edge_sweep(center_x=None, center_f=None, f_size=5,
                x_size=5, step=1,
                detector_config=2,
                logz=False,
                out_dir_base=r'D:\Data_Python_PL\PLmaps',
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

        xnow = center_x if center_x is not None else amc.move.getPosition(0) / 1000
        center_x = xnow
        fnow = center_f if center_f is not None else amc.move.getPosition(1) / 1000
        center_f = fnow # Final focus 

        # === Setup Scan Area, Output, and Focus ===
        x_start, x_end = center_x - (x_size / 2), center_x + (x_size / 2)
        f_start, f_end = center_f - (f_size / 2), center_f + (f_size / 2)
        out_dir = output_dir_folder(base_dir=out_dir_base)


        
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(center_f * 1000)); wait_until_stable(amc, axis=1)
        
        
        print(f"Initial pos (x,f) :  ({center_x:.2f}, {center_f:.2f}) µm")
        # === Setup Plot and Data File ===
        x_pos, f_pos = np.arange(x_start, x_end + step, step), np.arange(f_start, f_end + step, step)
        Z = np.zeros((len(f_pos), len(x_pos)), dtype=float)
        extent = [x_start, x_end, f_start, f_end]

        plt.ion()
        fig, ax1 = plt.subplots()
        img1 = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
        cb_format = mticker.FuncFormatter(lambda x, _: f'{x/1000:.1f}k' if x >= 1000 else str(int(x)))
        cb1 = fig.colorbar(img1, ax=ax1, format=cb_format)
        ax1.set_xlabel('X (µm)'); ax1.set_ylabel('F (µm)')
        ax1.set_title('PL Focus-Edge sweep'); fig.tight_layout()

        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'plmap_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')

        print(f'Saving data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# PL Mapping - {timestamp}\n# Center X: {center_x}, F: {center_f}\n')
        data_file_handle.write(f'# readback numpy shape for line part: {len(x_pos)}, {len(f_pos)} \n')
        data_file_handle.write('# x_req\tf_req\tx_act\tf_act\tcount1\tcount2\ttotal\n')

        # === Start Scan Loop ===
        max_int, best_x, best_y = -1, x_start, f_start
        total_points = len(x_pos) * len(f_pos)
        point_counter = 0
        start_time = time.time()

        amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(f_start * 1000)); wait_until_stable(amc, axis=1)

        for i, y in enumerate(f_pos):
            amc.move.setControlTargetPosition(1, int(y * 1000)); wait_until_stable(amc, axis=1)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1] # Serpentine path

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, axis=0)

                x_act, f_act = amc.move.getPosition(0)/1000, amc.move.getPosition(1)/1000
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]

                Z[i, j] = np.log10(total + 1) if logz else total

                # Always compare raw counts to find the true maximum
                if total > max_int:
                    max_int, best_x, best_y = total, x_act, f_act
                if total>2000000:
                    print(f"Total counts exceded set limit(1M) : {total}")
                    print(f"Moving to scan start location")
                    amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
                    amc.move.setControlTargetPosition(1, int(f_start * 1000)); wait_until_stable(amc, axis=1)
                    raise Exception(f"Max counts reached {total}: Reduce power")

                data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{f_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

                point_counter += 1
                elapsed = time.time() - start_time
                rem_time = (elapsed / point_counter) * (total_points - point_counter)
                mins, secs = divmod(int(rem_time), 60)
                print(f'Scan: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

                # Update plot
                img1.set_data(Z)
                img1.set_clim(vmin=Z.min(), vmax=Z.max())
                title = f'PL Focus-Edge sweep ({"Log" if logz else "Linear"})–Max: {max_int:.0f} @({best_x:.2f},{best_y:.2f})'
                ax1.set_title(title)
                fig.canvas.draw(); fig.canvas.flush_events()

        print("\nScan complete.")
        plt.ioff()
        plt.savefig(plot_file); print(f"Plot saved to: {plot_file}")
        if show_plot: plt.show()
        else: plt.close(fig)

    except Exception as e:
        print(f"\nA critical error occurred during PL scan: {e}")
        return None, None, None
    except KeyboardInterrupt as k:
        print(f"Keyboard interrupt : {k}")
        print(f"Keyboard interrupt : Moving to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(center_f * 1000)); wait_until_stable(amc, axis=1)
        return None, None, None    
    finally:
        # === Cleanup Resources ===
        print(f"Finished : Moving to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(center_f * 1000)); wait_until_stable(amc, axis=1)
        print("\n--- Cleaning up PL scan resources ---")
        if data_file_handle:
            data_file_handle.close(); print("Data file closed.")
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)

    return best_x, best_y, center_f
def run_pl_scan_daq(center_x=0, center_y=0, center_f=None,
                focus_sweep=False, f_size=50,
                x_size=5, y_size=5, step=1,t_acq=0.1,
                logz=False,
                out_dir_base=r'D:\Data_Python_PL\PLmaps',
                show_plot=True,
                amc=None, daq=None, ch1=None, ch2=None):
    """
    Performs a 2D photoluminescence scan. using daq
    """
    amc_local = False
    daq_local = False
    data_file_handle = None

    try:
        # === Initialize Devices (if not provided) ===
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if daq is None or ch1 is None or ch2 is None:
            daq, ch1, ch2 = start_daq()
            if daq is None: raise ConnectionError("Failed to start DAQ-APDs.")
            daq_local = True

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
        
        #if focus_sweep:
        #    print(f"Running focus sweep around: {fnow:.2f} µm")
        #    # Pass existing handles and set 'engaged=True' to prevent closing.
        #    amc
        #    best_f = run_focus_sweep(fbase=fnow, sn=sn, amc=amc, d1=d1, d2=d2,
        #                             movetobest=True, showplt=False, fsize=f_size, engaged=True)
        #    fnow = best_f
        #    time.sleep(5)
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
        ch1.start()
        ch2.start()

        # Initial readings
        pr1 = ch1.read()
        pr2 = ch2.read()
        

        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)); wait_until_stable(amc, axis=2)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1] # Serpentine path

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, axis=0)

                x_act, y_act = amc.move.getPosition(0)/1000, amc.move.getPosition(2)/1000
                pr1,pr2=ch1.read(),ch2.read()
                time.sleep(t_acq)
                cnt1,cnt2 = ch1.read(),ch2.read()
                cnt1_n = cnt1-pr1
                cnt2_n = cnt2-pr2
                total = cnt1_n + cnt2_n

                Z[i, j] = np.log10(total + 1) if logz else total

                # Always compare raw counts to find the true maximum
                if total > max_int:
                    max_int, best_x, best_y = total, x_act, y_act

                data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt1_n}\t{cnt2_n}\t{total}\n')

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
        if daq_local and daq: close_device_all(daq=daq, t_ch1=ch1, t_ch2=ch2)
        if amc_local and amc: close_device_all(amc=amc)

    return best_x, best_y, center_f
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
                              sn=None, d1=None, d2=None, amc=None, detector_config=2):
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
            sn, d1, d2 = start_apds(detector_config=detector_config)
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
        bx, by, bf = run_pl_scan(
            center_x=x_now, center_y=y_now, center_f=f_now,
            x_size=scan_size, y_size=scan_size, step=scan_step,
            focus_sweep=run_focus_sweep,
            show_plot=show_plot,
            sn=sn, d1=d1, d2=d2, amc=amc
        )
        print(f"Optimization scan complete. Best position found: ({int(bx):.2f}, {int(by):.2f}")

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
        if amc_local: 
            close_device_all(amc=amc)
            
    # --- UPDATED return statement ---
    return bx, by, bf
def run_g2(measure_time_s=600, bin_ps=100, window_ps=100000, detector_config=2, inp_hyst = 0, optimize_position=False, save_data=True, output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/acquired', sn=None, d1=None, d2=None, amc=None):
    """
    Performs a g2 measurement using the specified parameters.
    Args:
        measure_time_s (int): Total measurement time in seconds. (600s = 10min as default)
        bin_ps (int): Time bin size in picoseconds.
        window_ps (int): Correlation window size in picoseconds.
        detector_config (int): Detector configuration (1 or 2).
        inp_hyst (int): Input hysteresis setting for the detector.
        optimize_position (bool): If True, runs a position optimizer before measurement.
        save_data (bool): If True, saves the measurement data to a file.
        output_dir (str): Directory to save output files.
        sn (snAPI, optional): An existing, engaged detector object.
        d1, d2 (int, optional): Detector channel numbers for the existing sn object.
        amc (AMC.Device, optional): An existing, engaged AMC controller object.
    The output data file is formatted with tab separators.
    """
    sn_local = amc_local = False
    main_fig = None

    try:
        # === 1. Device Initialization ===
        if sn is None or d1 is None or d2 is None:
            print("Initializing APDs...")
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True
        a, b = d1, d2

        # === 2. Run Optimizer (if enabled) ===
        if optimize_position:
            if amc is None:
                print("Initializing Attocube stage controller...")
                amc = start_attocube()
                if amc is None: raise ConnectionError("Failed to start Attocube.")
                amc_local = True
            
            print("\n--- Running Position and Focus Optimizer ---")
            run_pl_position_optimizer(
                scan_size=1, scan_step=0.2, movetoxy=True, run_focus_sweep=True,
                show_plot=True, sn=sn, d1=a, d2=b, amc=amc
            )
            print("--- Optimization Finished ---")
        #sn.device.setInputHysteresis(inp_hyst)
        # === 3. Plotting and File Setup ===
        plt.ion()
        main_fig, (ax_g2, ax_trace) = plt.subplots(1, 2, figsize=(12, 5.5))
        main_fig.suptitle("g\u00b2(\u03c4) Measurement", fontsize=16)

        stop_button_ax = main_fig.add_axes([0.9, 0.01, 0.08, 0.04])
        stop_button = Button(stop_button_ax, 'Stop', hovercolor='0.975')
        stop_button.on_clicked(lambda event: (print("Stop command sent."), sn.correlation.stopMeasure()))

        dt_now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        details_filename = "g2_details_temp.txt" # Default filename
        if save_data:
            os.makedirs(output_dir, exist_ok=True)
            ptu_filename = os.path.join(output_dir, f'g2data_{measure_time_s}s_{dt_now}.ptu')
            details_filename = os.path.join(output_dir, f"g2details_{measure_time_s}s_{dt_now}.txt")
            sn.setPTUFilePath(ptu_filename)
            print(f'\nSaving PTU data to: {os.path.basename(ptu_filename)}')

        # === 4. Start Measurement ===
        sn.correlation.setG2Parameters(a, b, window_ps, bin_ps)
        sn.correlation.measure(int(measure_time_s * 1000), savePTU=save_data)
        start_time = time.time()
        start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Starting g(2) measurement for {measure_time_s} s...')

        # --- High-Performance Blitting Plot Setup ---
        ax_g2.set_xlabel('Time Delay (ns)'); ax_g2.set_ylabel('$g^{(2)}(\\tau)$'); 
        #ax_g2.grid(True, linestyle=':')
        line_g2, = ax_g2.plot([], [], lw=0.5, animated=True)
        ax_g2.set_ylim(0, 2.5)
        
        ax_trace.set_xlabel('Elapsed Time (s)'); ax_trace.set_ylabel('Count Rate (cps)'); 
        #ax_trace.grid(True, linestyle=':')
        line_ch1, = ax_trace.plot([], [], 'r-', lw=0.5, label=f"Ch {a}", animated=True)
        line_ch2, = ax_trace.plot([], [], 'g-', lw=0.5, label=f"Ch {b}", animated=True)
        ax_trace.legend(loc='upper right')
        
        main_fig.tight_layout(rect=[0, 0.05, 0.9, 0.95])
        main_fig.canvas.draw()
        bg_g2 = main_fig.canvas.copy_from_bbox(ax_g2.bbox)
        bg_trace = main_fig.canvas.copy_from_bbox(ax_trace.bbox)
        
        times, counts1, counts2 = [], [], []
        final_g2, final_lagtimes = None, None

        with open(details_filename, 'w') as f:
            f.write(f"# Measurement Details started at {start_timestamp}\n")
            f.write(f"# Ch1={a}\tCh2={b}\tWindow={window_ps}ps\tBin={bin_ps}ps\tTime={measure_time_s}s\n\n")
            f.write(f"# Elapsed Time (s)\tChannel 1 (cps)\tChannel 2 (cps)\tg2(0)\n")

            # === 5. Measurement & Fast Plotting Loop ===
            while not sn.correlation.isFinished():
                g2, lagtimes = sn.correlation.getG2Data()
                counts = sn.getCountRates()
                
                if g2 is None or len(g2) < 1:
                    plt.pause(0.1); continue
                
                if not hasattr(counts, '__len__') or len(counts) <= a or len(counts) <= b:
                    print(f"Warning: Invalid count data: {counts}. Skipping point.")
                    plt.pause(0.1); continue

                final_g2, final_lagtimes = g2, lagtimes
                elapsed_t = time.time() - start_time
                g2_zero = np.min(g2)
                
                times.append(elapsed_t); counts1.append(counts[a]); counts2.append(counts[b])
                
                f.write(f"{elapsed_t:.2f}\t{counts[a]}\t{counts[b]}\t{g2_zero:.4f}\n")
                if len(times) % 10 == 0: f.flush()

                raw_percent = (elapsed_t * 100) / measure_time_s
                percent_done = raw_percent if raw_percent < 100.0 else 100.0
                
                ax_g2.set_title(f'$g^{{(2)}}(0)$ = {g2_zero:.3f}')
                ax_trace.set_title(f'Time Trace | {percent_done:.1f}% Done')
                
                line_g2.set_data(np.array(lagtimes) / 1000.0, g2)
                line_ch1.set_data(times, counts1)
                line_ch2.set_data(times, counts2)
            
                main_fig.canvas.restore_region(bg_g2)
                main_fig.canvas.restore_region(bg_trace)
                
                g2_max = np.max(g2)
                if g2_max > 1.5:
                    ax_g2.set_ylim(0, g2_max * 1.1)  # Rescale with 10% padding
                else:
                    ax_g2.set_ylim(0, 1.5) 
                
                #ax_trace.relim(); ax_trace.autoscale_view()
                
                ax_g2.relim(); ax_g2.autoscale_view(scalex=True, scaley=False)
                ax_trace.relim(); ax_trace.autoscale_view()
                
                ax_g2.draw_artist(line_g2)
                ax_trace.draw_artist(line_ch1)
                ax_trace.draw_artist(line_ch2)

                main_fig.canvas.blit(ax_g2.bbox)
                main_fig.canvas.blit(ax_trace.bbox)
                main_fig.canvas.flush_events()
                
                plt.pause(0.01)

            print("Measurement loop ended.")

            # ? FIX LOCATION: This entire block is now correctly placed inside the 'with'
            # statement, ensuring the file 'f' is still open when this code runs.
            if save_data and final_g2 is not None:
                f.write("\n\n# Final g2 data (Time_ps\tNorm_Counts)\n")
                np.savetxt(f, np.column_stack((final_lagtimes, final_g2)), delimiter='\t')
                
                fig_path = os.path.join(output_dir, f'g2plot_{measure_time_s}s_{dt_now}.png')
                # Redraw figure once without animation for a clean save
                line_g2.set_animated(False); line_ch1.set_animated(False); line_ch2.set_animated(False)
                main_fig.canvas.draw()
                main_fig.savefig(fig_path, dpi=150)
                print(f"Final plot saved to: {os.path.basename(fig_path)}")
        
        # This part of the code now runs after the 'with' block has successfully closed the file.
        plt.ioff()
        print("Script finished. The plot window is now static. Close it to exit.")
        ax_trace.set_title(f'Time Trace | Measurement Complete')
        plt.show()

    except Exception as e:
        print(f"An error occurred in run_g2: {e}")
        traceback.print_exc()
    finally:
        # === 7. Final Cleanup ===
        if sn_local and sn:
            close_device_all(sn=sn)
            print("MH150 closed")
        if amc_local and amc:
            close_device_all(amc=amc)
            print("AMC closed")
def run_g2_from_file(input_file, detector_config=2, output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/fildevice', save_data=True, bin=100, window=100000):
    """
    Processes a .ptu file to generate, plot, and save a g2 correlation curve and its data.
    Args:
        input_file (str): Path to the .ptu file.
        detector_config (int): Detector configuration (1 for Exciletas or 2 for MPDs).
        output_dir (str): Directory to save output files. (Default : r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/acquired')
        save_data (bool): If True, saves the plot and data to files.
        bin (int): Time bin size in picoseconds
    """
    sn = snAPI()
    try:
        if detector_config==1:
            a,b = 1,2
        else:
            a, b = 3, 4
        # Process the single file
        sn.getFileDevice(input_file)
        print(f"Data from {os.path.basename(input_file)} loaded successfully")
        sn.correlation.setG2Parameters(a, b, window, bin)
        sn.correlation.measure(waitFinished=True)

        # Plotting
        fig, ax = plt.subplots()
        g2, lagtimes = sn.correlation.getG2Data()

        ax.plot(lagtimes, g2, label=f'{os.path.basename(input_file)}', linewidth=0.5)
        ax.set_xlabel('Delay (s)')
        ax.set_ylabel('g(2)')
        ax.set_title(f'g(2) Correlation (Bin = {bin} ps & Window = {window} ps)')
        ax.legend(loc='upper right')
        #ax.grid(True)

        # Save the plot and data if save_data is True
        if save_data:
            base_name = os.path.basename(input_file).replace('.ptu', '')
            dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # --- Save Plot ---
            plot_filename = f'g2_filedevice_plot_{base_name}_{dt_now}.png'
            plot_path = os.path.join(output_dir, plot_filename)
            try:
                fig.savefig(plot_path, dpi=150)
                print(f"Plot saved as {plot_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")

            # --- Save Data ---
            data_filename = f'g2_filedevice_data_{base_name}_{dt_now}.txt'
            data_path = os.path.join(output_dir, data_filename)
            try:
                # Stack lagtimes and g2 as two columns
                data_to_save = np.column_stack((lagtimes, g2))
                # Save to a tab-delimited text file with a header
                np.savetxt(data_path, data_to_save, delimiter='\t', header='Lag Time (ps)\tg2(tau)', comments='# ')
                print(f"Data saved as {data_path}")
            except Exception as e:
                print(f"Error saving data: {e}")

        plt.show()

    finally:
        # === Final Cleanup ===
        if sn:
            close_device_all(sn=sn)
def getposall():
    amc = start_attocube()
    print(f"x = {amc.move.getPosition(0) / 1000}")
    print(f"y = {amc.move.getPosition(2) / 1000}")
    print(f"f = {amc.move.getPosition(1) / 1000}")  
    close_device_all(amc=amc)
def wobble(size=2, speed=1, fbase=None):
    amc = start_attocube()
    # === CONFIG ===
    wobble_speed = speed
    wobble_size = size          # ± range from current focus
    # === AMC Init ===
    if fbase is not None:
        f_now=fbase
    else:
        f_now = amc.move.getPosition(1) / 1000
    print(f"wobble around = {f_now}")
    wobble_range= np.arange(f_now-wobble_size,f_now+wobble_size,wobble_speed)
    rev_wobble_range= np.arange(f_now+wobble_size,f_now-wobble_size,-wobble_speed)

    try:
        while True:
            for f in wobble_range:
                amc.move.setControlTargetPosition(1, int(f * 1000))
                wait_until_stable(amc_dev=amc, axis=1)
            for f in rev_wobble_range:
                amc.move.setControlTargetPosition(1, int(f * 1000))
                wait_until_stable(amc_dev=amc, axis=1)
    except KeyboardInterrupt:
        amc.move.setControlTargetPosition(1, int(f_now * 1000))
        close_device_all(amc=amc)
def gohome(amc=None):
    if amc is None:
        amc = start_attocube()
    for ax in [0,1,2]:
        amc_move(amc=amc,axis=ax,d=0)
    getposall()
def start_spectro(spectro_set_cw=484, shutter_init=True,waitfortemp=True,showrange=True):
    
    spectro = instruments.andor_kymera()
    set(spectro.wavelength_nm, spectro_set_cw)
    camera = instruments.andor_iDus(spectro_instr=spectro,cooler_temp=-80,shutter_init=shutter_init)
    camera.conf(read_mode='full_vertical_binning',exposure_time=5,acq_mode="accumulate", acc_N=2)
    set(camera.cosmic_filter_en, True)
    vbg=None
    if waitfortemp:
        camera.wait_for_cooler_stable(-80)
    minw = int(get(spectro.sensor_wavelengths_nm)[0])
    maxw = int(get(spectro.sensor_wavelengths_nm)[-1])
    if showrange:
        print(f"Current wavelength range : {minw}nm to {maxw}nm")
    return spectro, camera, minw, maxw
        
def close_spectro(spectro=None,camera=None):
    if camera is not None:
        unload(camera)
    if spectro is not None:
        unload(spectro)

def take_spectrum_bg(camera=None):
    set(camera.shutter, False)
    time.sleep(1)
    vbg = get(camera.readval)
    set(camera.shutter, True)
    return vbg

def take_spectrum(bg=True, vbg=None,
                  read_mode='full_vertical_binning',
                  exposure_time=5,
                  acq_mode="accumulate",
                  acc_N=2,
                  data_only=False,
                  show_plot=True,
                  camera=None,spectro=None):
    if camera is None:
        spectro, camera, minw, maxw = start_spectro()
    camera.conf(read_mode=read_mode,exposure_time=exposure_time,acq_mode=acq_mode, acc_N=acc_N)
    if bg:
        if vbg is None:
            set(camera.shutter, False)
            time.sleep(1)
            vbg = get(camera.readval)
            set(camera.shutter, True)
            time.sleep(1)
        v = get(camera.readval, bkg_rem=vbg[1])
    else:
        v = get(camera.readval)
    #plot
    if show_plot:
        _, ax = plt.subplots()
        ax.plot(v[0], v[1]) #label=f'{}')
        ax.set_xlim(np.min(v[0]), np.max(v[0]))
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Counts (Arb.)')
        ax.grid(True)
        ax.set_title('PL Spectrum')
        plt.show()
    if data_only:
        return v[1]
    else:
        return v
# === Plotting Utilities ===

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
def plot_plmap(fpath, mode='vscode', flog=False, xi=0, yi=1, zi=2, 
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
def plot_plmap_poster(
    fpath,
    mode="apd",
    flog=False,
    id="PL map",
    invxy=False,
    force1d=False,
    encoding="latin1",
    figsize=(9, 7),
    poster=True,
    nticks=5, size=45
):
    """
    Poster-ready PL map plotter with centered origin, bold fonts,
    fewer tick labels, and APD/SPEC/custom modes.
    """

    # -------- Poster Font Preset --------
    if poster:
        sz=size
        sz_small = sz - 10
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = sz_small
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['axes.labelweight'] = 'bold'
        plt.rcParams['axes.titlesize'] = sz
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['axes.labelsize'] = sz_small
        plt.rcParams['legend.fontsize'] = sz_small-10
        plt.rcParams['xtick.labelsize'] = sz_small
        plt.rcParams['ytick.labelsize'] = sz_small

    # -------- Fast reshape hint --------
    fast_shape = None
    try:
        with open(fpath, "r", encoding=encoding) as f:
            for line in f:
                m = re.search(r"#\s*readback numpy shape for line part:\s*(\d+),\s*(\d+)", line)
                if m:
                    fast_shape = (int(m.group(1)), int(m.group(2)))
                    break
    except:
        pass

    # -------- Load Data --------
    cols = np.loadtxt(fpath, unpack=True, encoding=encoding)

    idx_map = {
        "apd": (0, 2, 6),
        "spec": (0, 2, 5),
        "custom": (0, 1, 2)
    }
    xi, yi, zi = idx_map.get(mode, (0, 2, 6))
    x, y, z = cols[xi], cols[yi], cols[zi]

    if flog:
        z = np.log10(z, where=(z > 0), out=np.full_like(z, np.nan))

    # -------- Build Grid --------
    use_fast = fast_shape is not None and not force1d
    if use_fast:
        try:
            Z = z.reshape(fast_shape)
        except:
            use_fast = False

    if not use_fast:
        x_u, y_u = np.unique(x), np.unique(y)
        Xg, Yg = np.meshgrid(x_u, y_u)
        Z = np.full_like(Xg, np.nan)
        Z[np.searchsorted(y_u, y), np.searchsorted(x_u, x)] = z

    # -------- Centered Extent --------
    Lx = x.max() - x.min()
    Ly = y.max() - y.min()
    extent = [-Lx/2, Lx/2, -Ly/2, Ly/2]

    # -------- Plot --------
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(Z, cmap="plasma", origin="lower", extent=extent, aspect="auto")

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Log10 Counts" if flog else "Counts", weight="bold")

    if invxy:
        ax.invert_xaxis()
        ax.invert_yaxis()

    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")
    #ax.set_title(f"{id}: {os.path.basename(fpath)}")

    # -------- Reduce Tick Congestion --------
    ax.xaxis.set_major_locator(MaxNLocator(nticks))
    ax.yaxis.set_major_locator(MaxNLocator(nticks))

    plt.tight_layout()
    plt.show()
def plot_polarization(input, polar=True, mode='custom',
                      flog=False, normalize=False,
                      xi=0, yi=4,
                      use_actual_angle=True,
                      plot_style='scatter',
                      fit_dipole=True,
                      fit_npts=720,
                      minor_grids=True):
    """
    Polarization plot (polar or Cartesian) + optional dipolar fit.

    - Robustly reads MicroPL files with long headers + a non-# header line.
    - For mode='apd' (your file): columns are
        0 ReqPos(deg), 1 ActPos(deg), 2 Ch1, 3 Ch2, 4 Sum

    Dipolar fit uses: y(θ) = a + b*cos(2θ) + c*sin(2θ)
    """

    # -------- robust load: skip arbitrary header until numeric block ----------
    with open(input, "r", encoding="latin1", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if s[0].isdigit() or s[0] in "+-.":
            start = i
            break
    if start is None:
        raise ValueError("No numeric data found in file.")

    v = np.loadtxt(StringIO("".join(lines[start:])), unpack=True)

    # -------- choose columns ----------
    if mode == 'apd':
        x_index = 1 if use_actual_angle else 0  # ActPos or ReqPos (deg)
        y_index = 4                              # Sum counts
    elif mode == 'spec':
        x_index, y_index = (0, 5)
    elif mode == 'specw':
        x_index, y_index = (0, 6)
    else:
        x_index, y_index = xi, yi

    x_deg = v[x_index].astype(float)
    y = v[y_index].astype(float)

    # -------- preprocess y ----------
    y = y - np.min(y)

    if flog:
        y = np.log10(y + 1e-12)

    if normalize == 'max':
        m = np.max(y)
        if m != 0:
            y = y / m
    elif normalize == 'sum':
        s = np.sum(y)
        if s != 0:
            y = y / s
    elif normalize == 'minmax':
        ymin, ymax = np.min(y), np.max(y)
        if ymax != ymin:
            y = (y - ymin) / (ymax - ymin)

    # sort for clean plotting
    order = np.argsort(x_deg)
    x_deg = x_deg[order]
    y = y[order]

    x_rad = np.deg2rad(x_deg)

    # -------- plot ----------
    if polar:
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)

        if plot_style == 'line':
            ax.plot(x_rad, y, marker='o', lw=1)
        else:
            ax.scatter(x_rad, y, s=25, alpha=0.9)

    else:
        fig, ax = plt.subplots()

        if plot_style == 'line':
            ax.plot(x_deg, y, marker='o', lw=1)
        else:
            ax.scatter(x_deg, y, s=25, alpha=0.9)

        ax.set_xlabel("Theta (deg)")
        ax.set_ylabel("Normalized intensity" if normalize else "Counts (Arb.)")

        if minor_grids:
            ax.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    # -------- dipolar fit line (orange) ----------
    fit_info = None
    if fit_dipole:
        X = np.column_stack([np.ones_like(x_rad), np.cos(2 * x_rad), np.sin(2 * x_rad)])
        coeff, *_ = np.linalg.lstsq(X, y, rcond=None)
        a, b, c = coeff

        th = np.linspace(0, 2*np.pi, fit_npts)
        yfit = a + b*np.cos(2*th) + c*np.sin(2*th)

        if polar:
            ax.plot(th, yfit, lw=3, color='orange')
        else:
            ax.plot(np.rad2deg(th), yfit, lw=3, color='orange')

        A = 2.0 * np.hypot(b, c)
        theta0 = 0.5 * np.arctan2(c, b)
        B = a - A / 2.0
        fit_info = {
            "a": float(a), "b": float(b), "c": float(c),
            "A": float(A), "B": float(B),
            "theta0_deg_mod180": float(np.rad2deg(theta0) % 180)
        }

    # -------- styling: polar ticks/grids ----------
    if polar:
        # Angle labels every 45°
        major_deg = np.arange(0, 360, 45)
        ax.set_xticks(np.deg2rad(major_deg))
        ax.set_xticklabels([f"{d}°" for d in major_deg])
        ax.tick_params(axis='x', pad=30)  # push labels outward a bit

        # Remove radial tick labels completely (no "0", no "1")
        ax.set_yticklabels([])

        # Keep a reasonable radial range (auto if not normalized, but usually OK)
        # If you normalize='max' this will naturally be ~0..1
        if normalize in ('max', 'minmax'):
            ax.set_ylim(0, 1.05)

        # Minor grids
        if minor_grids:
            ax.set_xticks(np.deg2rad(np.arange(0, 360, 15)), minor=True)

            # minor radial circles (5 rings total)
            rmax = ax.get_ylim()[1]
            ax.set_yticks(np.linspace(0, rmax, 5), minor=True)

            ax.grid(True, which='major', linewidth=1.0, alpha=0.7)
            ax.grid(True, which='minor', linewidth=0.6, alpha=0.30)
        else:
            ax.grid(True)

    else:
        if minor_grids:
            ax.grid(True, which='major', alpha=0.7)
            ax.grid(True, which='minor', alpha=0.35)
        else:
            ax.grid(True)

    # remove title and legend
    ax.set_title("")
    leg = ax.get_legend()
    if leg is not None:
        leg.remove()

    return fig, ax, fit_info
def plot_trpl_log(fpath,
                  channel="Ch3",                 # "Ch3" | "Ch4" | "sum"
                  t_max_plot=20.0,               # ns
                  fit_end_ns=None,               # ns, None -> t_max_plot
                  start_at_frac_of_peak=0.70,    # fit starts when y <= frac*peak (after peak)
                  min_points_fit=60,             # require at least this many points
                  baseline_mode="tail_median",   # "tail_median" | "min" | "zero"
                  tail_fraction=0.15,            # fraction of fit window end for baseline estimate
                  min_counts_for_log=1.0,        # clip for log plot
                  raw_alpha=0.35,
                  raw_lw=1.2,
                  fit_lw=3.0):
    """
    Reads MicroPL histogram file and plots ONLY the semilogy TRPL with an exponential tail fit.

    Fit model (tail): y(t) = A * exp(-(t - t0)/tau) + C
    t0 is chosen automatically based on when the signal falls to start_at_frac_of_peak * peak.
    """

    # -------- robust load numeric block ----------
    with open(fpath, "r", encoding="latin1", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if s[0].isdigit() or s[0] in "+-.":
            start = i
            break
    if start is None:
        raise ValueError("No numeric data found in file.")

    data = np.loadtxt(StringIO("".join(lines[start:])))
    t = data[:, 0].astype(float)      # ns
    ch3 = data[:, 1].astype(float)
    ch4 = data[:, 2].astype(float)

    if channel.lower() == "ch3":
        y = ch3
        ch_label = "CH3"
    elif channel.lower() == "ch4":
        y = ch4
        ch_label = "CH4"
    elif channel.lower() == "sum":
        y = ch3 + ch4
        ch_label = "CH3+CH4"
    else:
        raise ValueError('channel must be "Ch3", "Ch4", or "sum"')

    # sort by time
    order = np.argsort(t)
    t = t[order]
    y = y[order]

    # plot window
    if t_max_plot is not None:
        mplot = t <= float(t_max_plot)
        t_plot = t[mplot]
        y_plot = y[mplot]
    else:
        t_plot, y_plot = t, y

    if t_plot.size < 50:
        raise ValueError("Not enough points in plot window. Increase t_max_plot.")

    # -------- pick peak and choose fit start based on fraction-of-peak ----------
    i_peak = int(np.argmax(y_plot))
    t_peak = float(t_plot[i_peak])
    y_peak = float(y_plot[i_peak])

    thr = float(start_at_frac_of_peak) * y_peak

    # find first index after peak where y drops below threshold
    post = np.arange(i_peak, len(y_plot))
    below = post[y_plot[post] <= thr]
    if below.size == 0:
        # fallback: start a bit after peak (1% of window)
        i0 = builtins.min(i_peak + builtins.max(1, int(0.01 * len(y_plot))), len(y_plot) - 1)
    else:
        i0 = int(below[0])

    t0 = float(t_plot[i0])

    # fit end
    t1 = float(t_plot[-1]) if fit_end_ns is None else float(fit_end_ns)

    mfit = (t_plot >= t0) & (t_plot <= t1)
    tf = t_plot[mfit]
    yf = y_plot[mfit]

    if tf.size < min_points_fit:
        raise ValueError(
            f"Fit window too small ({tf.size} pts). "
            f"Try increasing t_max_plot, lowering start_at_frac_of_peak, or lowering min_points_fit."
        )

    # -------- baseline C ----------
    n_tail = builtins.max(10, int(len(yf) * float(tail_fraction)))
    tail_vals = yf[-n_tail:]

    if baseline_mode == "tail_median":
        C = float(np.median(tail_vals))
    elif baseline_mode == "min":
        C = float(np.min(yf))
    elif baseline_mode == "zero":
        C = 0.0
    else:
        raise ValueError('baseline_mode must be "tail_median", "min", or "zero"')

    # subtract baseline and keep positive points
    y_corr = yf - C
    good = y_corr > 1e-12
    tf2 = tf[good]
    y2 = y_corr[good]

    if tf2.size < builtins.max(20, int(0.5 * min_points_fit)):
        raise ValueError(
            "Not enough positive points after baseline subtraction. "
            "Try baseline_mode='zero' or reduce tail_fraction."
        )

    # -------- fit ln(y) vs time ----------
    x = (tf2 - t0)
    ln_y = np.log(y2)

    xbar, ybar = x.mean(), ln_y.mean()
    Sxx = np.sum((x - xbar) ** 2)
    Sxy = np.sum((x - xbar) * (ln_y - ybar))
    slope = Sxy / Sxx
    intercept = ybar - slope * xbar

    tau = -1.0 / slope
    A = float(np.exp(intercept))

    # uncertainties (OLS)
    resid = ln_y - (intercept + slope * x)
    dof = builtins.max(1, len(x) - 2)
    s2 = np.sum(resid**2) / dof
    slope_se = np.sqrt(s2 / Sxx)
    tau_se = abs(slope_se / (slope ** 2))

    # fit curve over plot window
    t_fit = t_plot
    y_fit = A * np.exp(-(t_fit - t0) / tau) + C
    y_fit[t_fit < t0] = np.nan

    # -------- plot: ONLY semilogy ----------
    fig, ax = plt.subplots(1, 1, figsize=(7.0, 4.2), dpi=150, constrained_layout=True)

    y_plot_log = np.clip(y_plot, min_counts_for_log, None)
    ax.semilogy(t_plot, y_plot_log, lw=raw_lw, alpha=raw_alpha, label=f"Raw Counts ({ch_label})")

    y_fit_log = np.where(np.isfinite(y_fit), np.clip(y_fit, min_counts_for_log, None), np.nan)
    ax.semilogy(t_fit, y_fit_log, lw=fit_lw, color="orange",
                label=f"Fit (τ={tau:.2f}±{tau_se:.2f} ns)")

    ax.set_xlabel("Time (ns)")
    ax.set_ylabel(f"Counts ({ch_label}, log scale)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="upper right", frameon=True)

    fit_dict = {
        "channel": ch_label,
        "t_peak_ns": t_peak,
        "y_peak": y_peak,
        "t0_ns": t0,
        "fit_end_ns": t1,
        "A": float(A),
        "C": float(C),
        "tau_ns": float(tau),
        "tau_err_ns": float(tau_se),
        "n_fit_points": int(tf2.size),
        "start_at_frac_of_peak": float(start_at_frac_of_peak),
    }

    return fig, ax, fit_dict
def plot_parameters(xi,yi, xr,yr):
    xs=xi-xr/2
    print(f'xstart= {xs}')
    xe=xi+xr/2
    print(f'xend= {xe}')
    ys=yi-yr/2
    print(f'ystart= {ys}')
    ye=yi+yr/2
    print(f'yend= {ye}')
def start_kdc(SN="27257399", kdc=None, force=False):
    if kdc is not None:
        return kdc
    else:
        try:
            kdc = Thorlabs.KinesisMotor(SN)
            kdc.open()
            if force:
                print(f"Homing KDC motor SN: {SN}...")
                # sync=False allows the script to continue running so we can poll
                kdc.home(force=True, sync=False) 
                time.sleep(0.2) # Give the motor a moment to start moving
                
                # Poll position while homing
                try:
                    while kdc.is_moving():
                        curr_deg = kdc.get_position() / 1919.6418578623391
                        print(f"Homing... Current Position: {curr_deg:.2f}°", end='\r')
                        time.sleep(0.05)
                    print("\nHoming complete.")
                except Exception:
                    # Fallback if is_moving behaves as a property
                    while getattr(kdc, 'is_moving', False):
                        curr_deg = kdc.get_position() / 1919.6418578623391
                        print(f"Homing... Current Position: {curr_deg:.2f}°", end='\r')
                        time.sleep(0.05)
                    print("\nHoming complete.")
                    
            print(f"Connected to KDC motor SN: {SN}")
            return kdc
        except Exception as e:
            print(f"ERROR: Failed to connect to KDC motor: {e}")
            return None
def kdc_position_deg(kdc=None):
    kdc_local = False
    if kdc is None:
        kdc = start_kdc()
        kdc_local = True
        
    if kdc is None:
        print("ERROR: KDC motor is not initialized.")
        return 0.0

    current_steps = kdc.get_position()
    current_deg = current_steps / 1919.6418578623391
    
    if kdc_local and kdc:
        try:
            kdc.close()
        except Exception:
            pass
    return current_deg
def kdc_move_deg(deg, kdc=None, showcmd=True):
    """
    Moves the Thorlabs KDC rotation mount to the specified angle in degrees.
    
    Args:
        deg (float): Target angle in degrees.
        kdc (Thorlabs.KinesisMotor, optional): Existing KDC motor instance.
        showcmd (bool): If True, prints polling status. If False, moves silently.
    """
    kdc_local = False
    if kdc is None:
        kdc = start_kdc()
        kdc_local = True
        
    if kdc is None:
        if showcmd: print("ERROR: KDC motor is not initialized.")
        return

    step = deg * 1919.6418578623391
    kdc.move_to(step)
    
    time.sleep(0.05)
    
    # Poll position while moving
    try:
        while kdc.is_moving():
            if showcmd:
                curr_deg = kdc.get_position() / 1919.6418578623391
                print(f"Moving... Current Angle: {curr_deg:.2f}° (Target: {deg:.2f}°)", end='\r')
            time.sleep(0.05)
            
        if showcmd:
            final_deg = kdc.get_position() / 1919.6418578623391
            print(f"\nMovement complete. Final Angle: {final_deg:.2f}°")
            
    except Exception:
        # Fallback if is_moving behaves as a property
        while getattr(kdc, 'is_moving', False):
            if showcmd:
                curr_deg = kdc.get_position() / 1919.6418578623391
                print(f"Moving... Current Angle: {curr_deg:.2f}° (Target: {deg:.2f}°)", end='\r')
            time.sleep(0.05)
            
        if showcmd:
            final_deg = kdc.get_position() / 1919.6418578623391
            print(f"\nMovement complete. Final Angle: {final_deg:.2f}°")

    if kdc_local and kdc:
        try:
            kdc.close()
        except Exception:
            pass
def run_pl_polarization(start_deg=0, end_deg=360, step_deg=10, 
                        detector_config=2, out_dir_base=r'D:\Data_Python_PL\Polarization',
                        show_plot=True, force_home_kdc=False, kdc=None, amc=None, sn=None, d1=None, d2=None):
    """
    Performs a polarization-dependent PL measurement by sweeping a Thorlabs rotation mount.
    Features live real-time plotting and instant data-file saves.
    """
    kdc_local = False
    amc_local = False
    sn_local = False
    data_file_handle = None

    try:
        # === Initialize Devices ===
        if kdc is None:
            kdc = start_kdc(force=force_home_kdc)
            if kdc is None: raise ConnectionError("Failed to start Thorlabs KDC motor.")
            kdc_local = True

        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

        # === Setup Output Directory and Files ===
        out_dir = output_dir_folder(base_dir=out_dir_base)
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        data_file = os.path.join(out_dir, f'polarization_data_{timestamp}.txt')
        plot_file = os.path.join(out_dir, f'polarization_plot_{timestamp}.png')

        print(f'Saving polarization data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# Polarization PL Measurement - {timestamp}\n')
        data_file_handle.write('# Req_Angle(deg)\tAct_Angle(deg)\tCount1\tCount2\tTotal\n')

        angles = np.arange(start_deg, end_deg + step_deg, step_deg)
        actual_angles, ch1_counts, ch2_counts, totals = [], [], [], []

        print("\nStarting polarization sweep...")
        
        # === Setup Live Plot ===
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))
        line, = ax.plot([], [], 'bo-', lw=2, label='Total Counts')
        ax.set_xlabel('Polarizer Angle (deg)')
        ax.set_ylabel('Counts (cps)')
        ax.set_title(f'Polarization Dependence | {timestamp}')
        ax.grid(True)
        ax.legend(loc='upper right')
        
        # Pre-set X axis limits so the plot doesn't jump horizontally
        ax.set_xlim(start_deg - step_deg, end_deg + step_deg)

        # === Measurement Loop ===
        for angle in angles:
            # Move silently, then wait exactly 1 second
            kdc_move_deg(angle, kdc=kdc, showcmd=False)
            time.sleep(1.0)  
            
            # Take readings
            act_angle = kdc_position_deg(kdc=kdc)
            cnt = sn.getCountRates()
            c1, c2 = cnt[d1], cnt[d2]
            total = c1 + c2

            actual_angles.append(act_angle)
            ch1_counts.append(c1)
            ch2_counts.append(c2)
            totals.append(total)

            # Write to file and instantly flush the buffer to save it
            data_file_handle.write(f'{angle:.2f}\t{act_angle:.2f}\t{c1}\t{c2}\t{total}\n')
            data_file_handle.flush()
            
            print(f'Angle: {act_angle:.1f}° | Total Counts: {total}      ', end='\r')

            # Update Live Plot
            line.set_data(actual_angles, totals)
            ax.relim()
            ax.autoscale_view(scalex=False, scaley=True) # Only autoscale Y axis dynamically
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.01)

        print("\nPolarization sweep complete.")

        # === Finalize and Save ===
        plt.ioff()
        plt.tight_layout()
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")
        
        if show_plot: plt.show()
        else: plt.close(fig)

        return np.array(actual_angles), np.array(totals)

    except Exception as e:
        print(f"\nA critical error occurred during polarization scan: {e}")
        return None, None
    finally:
        print("\n--- Cleaning up polarization scan resources ---")
        if data_file_handle: 
            data_file_handle.close()
        if kdc_local and kdc:
            try: kdc.close(); print("KDC motor closed.")
            except Exception: pass
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)
DEFAULT_CRYO_IP = "192.168.0.2"
_global_cryo = None
def start_cryo(ip_address=DEFAULT_CRYO_IP, cryo=None):
    global _global_cryo
    if cryo is not None: return cryo
    if _global_cryo is not None: return _global_cryo
    try:
        _global_cryo = cryocore.CryoCore(ip_address)
        print(f"Connected to Montana CryoCore at {ip_address}")
        return _global_cryo
    except Exception as e:
        print(f"ERROR: Failed to connect to CryoCore: {e}")
        return None

def _get_cryo_val(res):
    return res[1] if isinstance(res, tuple) else res

def cryo_state(cryo=None):
    c = start_cryo(cryo=cryo)
    if not c: return "Unknown"
    try: return _get_cryo_val(c.get_system_state())
    except Exception: return "Unknown"

def cryo_goal(cryo=None):
    c = start_cryo(cryo=cryo)
    if not c: return "Unknown"
    try: return _get_cryo_val(c.get_system_goal())
    except Exception: return "Unknown"

def cryo_ensure_ready(cryo=None, timeout=30):
    c = start_cryo(cryo=cryo)
    if not c: return False
    goal, state = cryo_goal(c), cryo_state(c)
    if goal in ['None', None] and state == 'Ready': return True
        
    print(f"System busy (Goal: {goal}, State: {state}). Aborting current goal...")
    try: c.abort_goal()
    except Exception as e: print(f"Error aborting goal: {e}")
        
    start_time = time.time()
    while time.time() - start_time < timeout:
        if cryo_state(c) == 'Ready':
            print("System is now Ready.")
            return True
        time.sleep(1)
    print("WARNING: Timed out waiting for system to reach 'Ready' state.")
    return False

def cryo_pullvac(cryo=None):
    c = start_cryo(cryo=cryo)
    if not c: return
    if cryo_goal(c) == 'PullVacuum':
        print("System is already pulling vacuum.")
        return
    if cryo_ensure_ready(c):
        try:
            c.pull_vacuum()
            print("Vacuum pull initiated.")
        except Exception as e:
            print(f"Error pulling vacuum: {e}")

def cryo_vent(cryo=None):
    c = start_cryo(cryo=cryo)
    if not c: return
    if cryo_goal(c) == 'Vent':
        print("System is already venting.")
        return
    if cryo_ensure_ready(c):
        try:
            c.vent()
            print("Venting initiated.")
        except Exception as e:
            print(f"Error venting: {e}")

def cryo_set_temp(cryo=None, target_temp=10):
    c = start_cryo(cryo=cryo)
    if not c: return
    try:
        c.set_platform_target_temperature(target_temp)
        print(f"Platform target temperature set to: {target_temp} K")
    except Exception as e:
        print(f"Error setting platform temperature: {e}")

def cryo_start_cooldown(cryo=None, target_temp=10, bakeout=False, n2purge=False):
    c = start_cryo(cryo=cryo)
    if not c: return
    if cryo_goal(c) not in ['Cooldown', 'None', None]:
        cryo_ensure_ready(c)

    try:
        if hasattr(c, 'set_platform_bakeout_enabled'):
            try: c.set_platform_bakeout_enabled(bakeout)
            except TypeError: c.set_platform_bakeout_enabled = bakeout
            
        if hasattr(c, 'set_dry_nitrogen_purge_enabled'):
            try: c.set_dry_nitrogen_purge_enabled(n2purge)
            except TypeError: c.set_dry_nitrogen_purge_enabled = n2purge

        c.set_platform_target_temperature(target_temp)
        print(f"Platform target temperature set to: {target_temp} K")
        
        if cryo_goal(c) != 'Cooldown':
            c.cooldown()
            print(f"Cooldown sequence initiated. (Bakeout: {bakeout}, N2 Purge: {n2purge})")
        else:
            print("System is already in Cooldown mode. Target temperature updated.")
    except Exception as e:
        print(f"Error starting cooldown: {e}")

def cryo_get_temp_p1(cryo=None):
    c = start_cryo(cryo=cryo)
    if not c: return None
    try: return float(_get_cryo_val(c.get_platform_temperature()))
    except Exception as e:
        print(f"Error reading platform temperature: {e}")
        return None

def cryo_get_temp_u1(cryo=None):
    c = start_cryo(cryo=cryo)
    if not c: return None
    try: return float(_get_cryo_val(c.get_user1_temperature()))
    except Exception as e:
        print(f"Error reading user 1 temperature: {e}")
        return None

def cryo_waitfortemp_p1(req_temp, cryo=None, tolerance=1.0, poll_interval=2):
    c = start_cryo(cryo=cryo)
    if not c: return
    print(f"Waiting for platform temperature to reach {req_temp} K (tolerance: ±{tolerance}K)...")
    while True:
        current_temp = cryo_get_temp_p1(c)
        if current_temp is not None:
            diff = abs(current_temp - req_temp)
            print(f"Current Platform Temp: {current_temp:.2f} K (Target: {req_temp} K) | State: {cryo_state(c)}", end='\r')
            if diff <= tolerance:
                print(f"\nPlatform reached target temperature: {current_temp:.2f} K")
                break
        time.sleep(poll_interval)

def cryo_waitfortemp_u1(req_temp, cryo=None, tolerance=1.0, poll_interval=2):
    c = start_cryo(cryo=cryo)
    if not c: return
    print(f"Waiting for User 1 temperature to reach {req_temp} K (tolerance: ±{tolerance}K)...")
    while True:
        current_temp = cryo_get_temp_u1(c)
        if current_temp is not None:
            diff = abs(current_temp - req_temp)
            print(f"Current User 1 Temp: {current_temp:.2f} K (Target: {req_temp} K) | State: {cryo_state(c)}", end='\r')
            if diff <= tolerance:
                print(f"\nUser 1 reached target temperature: {current_temp:.2f} K")
                break
        time.sleep(poll_interval)

def cryo_waitforvac(target_pressure=0.1, cryo=None, timeout_s=1800, poll_interval=2):
    c = start_cryo(cryo=cryo)
    if not c: return False
    print("Waiting for vacuum target...")
    start_time = time.time()
    while time.time() - start_time < timeout_s:
        try:
            pressure = _get_cryo_val(c.get_sample_chamber_pressure())
            state = cryo_state(c)
            if pressure is not None:
                print(f"Current Pressure: {pressure:.4f} (Target: {target_pressure}) | State: {state}", end='\r')
                if pressure <= target_pressure:
                    print(f"\nVacuum target reached: {pressure:.4f}")
                    return True
        except Exception:
            pass
        time.sleep(poll_interval)
    print("\nWARNING: Timeout reached waiting for vacuum.")
    return False

def cryo_waitforvent(vent_pressure_threshold=700, cryo=None, timeout_s=600, poll_interval=2):
    c = start_cryo(cryo=cryo)
    if not c: return False
    print("Waiting for system to vent...")
    start_time = time.time()
    while time.time() - start_time < timeout_s:
        try:
            pressure = _get_cryo_val(c.get_sample_chamber_pressure())
            state = cryo_state(c)
            if pressure is not None:
                print(f"Current Pressure: {pressure:.1f} (Target: >={vent_pressure_threshold}) | State: {state}", end='\r')
                if pressure >= vent_pressure_threshold:
                    print(f"\nVenting complete. Current pressure: {pressure:.1f}")
                    return True
        except Exception:
            pass
        time.sleep(poll_interval)
    print("\nWARNING: Timeout reached waiting for vent.")
    return False


import sys
import os
import time

# === FIX FOR FORTRAN/MKL CTRL+C CRASH ===
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

import numpy as np
import matplotlib.pyplot as plt

# === Path Setup for QFLv4 ===
try:
    current_dir = os.path.dirname(__file__)
except NameError:
    current_dir = os.getcwd()

parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

pathe = r"D:\Gaurang\GitHub-QFL\tank-QFL\camera-thor\SDK\Python Toolkit\examples"
if pathe not in sys.path:
    sys.path.append(pathe)
    
import windows_setup
windows_setup.configure_path()

from QFLv4 import *
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK

def get_peak_intensity(image_array):
    """
    Collapses 3D arrays to 2D grayscale and finds the absolute brightest pixel.
    """
    if image_array.ndim == 3:
        gray_img = np.mean(image_array, axis=2)
    else:
        gray_img = image_array
        
    max_val = float(np.max(gray_img))
    max_coords = np.unravel_index(np.argmax(gray_img), gray_img.shape)
    
    return max_val, max_coords, gray_img

def run_camera_focus_sweep(center_f=None, f_size=10, step=0.1,
                           camera_serial="11484", exposure_ms=10, 
                           out_dir_base=r'D:\Data_Python_PL\Camera',
                           move_to_best=True, post_sweep_live_feed=True,
                           amc=None):
    amc_local = False
    data_file_handle = None
    best_f = None
    aborted = False
    exposure_us=exposure_ms*1000
    try:
        # === 1. Start AMC ===
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        fnow = center_f if center_f is not None else amc.move.getPosition(1) / 1000
        center_f = fnow
        best_f = center_f  

        # Setup Output Directories
        out_dir = output_dir_folder(base_dir=out_dir_base)

        # Setup Real-time Plotting
        plt.ion()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        f_start, f_end = center_f - (f_size / 2), center_f + (f_size / 2)
        f_pos = np.arange(f_start, f_end + step, step)
        intensity_data = np.zeros(len(f_pos), dtype=float)
        
        line1, = ax1.plot(f_pos, intensity_data, 'b-o', markersize=4)
        ax1.set_xlabel('F / Z (µm)')
        ax1.set_ylabel('Max Single-Pixel Intensity')
        ax1.set_title('Focus Sweep Curve')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        img_display = None
        ax2.set_title('Live Camera Feed')
        ax2.axis('off')
        fig.tight_layout()

        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'cam_focus_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'cam_focus_data_{timestamp}.txt')

        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# Camera Focus Sweep - {timestamp}\n# Center F: {center_f}\n')
        data_file_handle.write('# f_req\tf_act\tintensity\tmax_x\tmax_y\n')

        # === 2. Start Camera inside Context Managers ===
        with TLCameraSDK() as sdk:
            available_cameras = sdk.discover_available_cameras()
            if not available_cameras: raise ConnectionError("No Thorlabs cameras found!")
            
            target_serial = next((cam for cam in available_cameras if camera_serial in cam), available_cameras[0])
            
            with sdk.open_camera(target_serial) as camera:
                camera.exposure_time_us = exposure_us
                camera.frames_per_trigger_zero_for_unlimited = 1

                # === 3. THE DUMMY FRAME FIX ===
                print("\nClearing stale hardware buffers...")
                camera.arm(frames_to_buffer=1)
                camera.issue_software_trigger()
                time.sleep(0.2)
                _ = camera.get_pending_frame_or_null() # Throw away the bad first frame
                camera.disarm()
                time.sleep(0.1)

                max_int = -1
                total_points = len(f_pos)
                point_counter = 0

                print(f"--- Starting Sweep ({f_start:.2f} µm to {f_end:.2f} µm) ---")

                # === SWEEP LOOP ===
                for i, y in enumerate(f_pos):
                    amc.move.setControlTargetPosition(1, int(y * 1000))
                    wait_until_stable(amc, axis=1)
                    
                    f_act = amc.move.getPosition(1) / 1000
                    
                    camera.arm(frames_to_buffer=1)
                    camera.issue_software_trigger()
                    time.sleep(0.5) 
                    
                    frame = None
                    attempts = 0
                    while frame is None and attempts < 10:
                        time.sleep(0.1) 
                        frame = camera.get_pending_frame_or_null()
                        attempts += 1
                    
                    if frame is None:
                        print(f"Warning: Frame missing at Z={f_act:.2f} µm")
                        intensity, coords, process_img = 0, (0, 0), np.zeros((10, 10))
                    else:
                        imagem = np.asarray(frame.image_buffer)
                        intensity, coords, process_img = get_peak_intensity(imagem)
                    
                    camera.disarm()

                    intensity_data[i] = intensity
                    if intensity > max_int:
                        max_int, best_f = intensity, f_act

                    max_y, max_x = coords
                    data_file_handle.write(f'{y:.3f}\t{f_act:.3f}\t{intensity:.2f}\t{max_x}\t{max_y}\n')
                    data_file_handle.flush()

                    point_counter += 1
                    print(f'Scan: {point_counter}/{total_points} | Z: {f_act:.2f} | Peak: {intensity:.0f} at X:{max_x}, Y:{max_y}', end='\r')

                    line1.set_ydata(intensity_data)
                    ax1.relim()
                    ax1.autoscale_view()
                    ax1.set_title(f'Focus Sweep – Max: {max_int:.0f} @({best_f:.2f} µm)')
                    
                    # VISIBILITY IMPROVEMENT
                    if img_display is None:
                        img_display = ax2.imshow(process_img, cmap='gray', vmin=0)
                    else:
                        img_display.set_data(process_img)
                        # dynamically track the peak without washing out dim lasers
                        vmax_val = max(10, process_img.max()) 
                        img_display.set_clim(vmin=0, vmax=vmax_val)
                        
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                print("\n\nScan complete.")
                
                # === MOVE TO BEST FOCUS ===
                target_f = best_f if move_to_best else center_f
                print(f"Moving to target focus position: {target_f:.2f} µm...")
                amc.move.setControlTargetPosition(1, int(target_f * 1000))
                wait_until_stable(amc, axis=1)
                time.sleep(0.3)

                # === LIVE FEED ===
                if post_sweep_live_feed:
                    print(f"\n[LIVE FEED ACTIVE] Stage parked at {target_f:.2f} µm.")
                    print(">>> PRESS 'CTRL+C' IN THE TERMINAL TO STOP AND CLOSE <<<")
                    
                    ax1.set_title(f'Sweep Finished – Parked at {target_f:.2f} µm')
                    
                    try:
                        while True:
                            camera.arm(frames_to_buffer=1)
                            camera.issue_software_trigger()
                            
                            frame = None
                            attempts = 0
                            while frame is None and attempts < 10:
                                time.sleep(0.05)
                                frame = camera.get_pending_frame_or_null()
                                attempts += 1
                            
                            if frame is not None:
                                imagem = np.asarray(frame.image_buffer)
                                intensity, coords, process_img = get_peak_intensity(imagem)
                                
                                img_display.set_data(process_img)
                                vmax_val = max(10, process_img.max())
                                img_display.set_clim(vmin=0, vmax=vmax_val)
                                ax2.set_title(f'Live Camera | Peak: {intensity:.0f}')
                                
                                fig.canvas.draw()
                                fig.canvas.flush_events()
                                
                            camera.disarm()
                    except KeyboardInterrupt:
                        print("\nKeyboard Interrupt received. Closing live feed...")
                        aborted = True

    except Exception as e:
        print(f"\nA critical error occurred: {e}")
        aborted = True
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt received during sweep.")
        aborted = True
    finally:
        print("\n--- Cleaning up resources ---")
        plt.ioff()
        if not aborted:
            plt.savefig(plot_file)
            print(f"Plot saved to: {plot_file}")
            
        plt.close('all') 
        if data_file_handle: data_file_handle.close()
        if amc_local and amc:
            try: amc.close() 
            except AttributeError: pass


# %%
