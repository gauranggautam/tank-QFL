from pyHegel.commands import * 
import builtins
from datetime import datetime
from io import StringIO
import os
import re
import time
import traceback

# Third-party libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pyvisa

# Matplotlib configuration
plt.style.use('dark_background')
TAB20_COLORS = plt.colormaps['tab20'].colors

# Hardware-Specific Imports & Flags
uhd_plots = False

try:
    from attocube import AMC
except ImportError as e:
    print(e)

try:
    from snAPI.Main import *
except ImportError as e:
    print(e)

# try: from taiko_driver import TaikoLaser, PicoQuantException
# except ImportError as e: print(e)

try:
    import nidaqmx
    from nidaqmx.constants import Edge
except ImportError as e:
    print(e)

try:
    import labview_buttons_v2 as lv
except ImportError as e:
    print(e)

try:
    from pylablib.devices import Thorlabs
except ImportError as e:
    print(e)

try:
    from montana import cryocore
except ImportError as e:
    print(e)




import os, re, time, traceback, builtins
from datetime import datetime
from io import StringIO
# Third-party
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('dark_background')
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


# Assuming instruments, set, and get are imported/defined in your environment

def set_laser(power=None, pulsed=False, laser=None, freq_khz=10000, softlock=False, engaged=True):
    """
    Controls and manages a Taiko laser connection.
    Automatically disables the softlock (softlock=False) to allow emission.
    
    Args:
        power (float, optional): Sets CW/Pulsed power as a percentage (0-100). Defaults to None.
        pulsed (bool): If True, sets to pulsed mode. If False, sets to CW mode. Defaults to False.
        laser (object, optional): Existing laser object. Defaults to None.
        freq_khz (float): Pulse frequency in kHz. Defaults to 20000.
        softlock (bool): Enables the software lock. Defaults to False (unlocked).
        engaged (bool): If True, returns the connection. If False, returns None.
    """
    if laser is None:
        try:
            laser = instruments.picoQuant.PicoQuant_Taiko_PDL_M1()
        except Exception as e:
            print(f"Failed to connect to laser: {e}")
            return None

    # === 1. Unlock Laser ===
    if softlock is not None:
        set(laser.softlock_en, softlock)
        print(f"\nLaser softlock state : {get(laser.softlock_en)}")

    # === 2. Apply Power & Mode Settings ===
    if power is not None:
        pwr_permille = int(power * 10) # Convert % to permille (0-1000)
        
        if pulsed:
            print("Setting Pulsed mode...")
            set(laser.laser_mode, "pulsed")
            
            freq_hz = int(freq_khz * 1000)
            print(f"Setting Frequency to {freq_hz} Hz ({freq_khz} kHz)...")
            set(laser.pulse_burst_freq_Hz, freq_hz)
            
            print(f"Setting power to {power}%...")
            set(laser.pulse_burst_power_permille, pwr_permille)
            
        else:
            print("Setting CW mode...")
            set(laser.laser_mode, "cw")
            
            print(f"Setting power to {power}%...")
            set(laser.cw_power_permille, pwr_permille)
        close_device_all(laser=laser)

def get_laser(laser=None):
    """
    Queries and prints current Taiko laser parameters.
    
    Returns:
        tuple: (mode, cw_power_permille, cw_power_W, pulse_power_permille, pulse_power_W, freq_hz)
    """
    laser_local = False
    if laser is None:
        try:
            laser = instruments.picoQuant.PicoQuant_Taiko_PDL_M1()
            laser_local = True
        except Exception as e:
            print(f"Failed to connect to laser: {e}")
            return None

    try:
        mode = get(laser.laser_mode)
        pwr_cw_p = get(laser.cw_power_permille) / 10.0      # Converted to %
        pwr_cw_w = get(laser.cw_power_W)
        hz = get(laser.pulse_burst_freq_Hz)
        pwr_pulse_p = get(laser.pulse_burst_power_permille) / 10.0 # Converted to %
        pwr_pulse_w = get(laser.pulse_burst_power_W)
        
        print("\n--- Taiko Laser Status ---")
        print(f"  Mode           : {mode}")
        print(f"  CW Power       : {pwr_cw_p}% ({pwr_cw_w} W)")
        print(f"  Pulse Power    : {pwr_pulse_p}% ({pwr_pulse_w} W)")
        print(f"  Frequency      : {hz} Hz ({hz / 1e6} MHz)")
        print("-" * 28)

    finally:
        if laser_local and laser:
            close_device_all(laser=laser)
            
    return mode, pwr_cw_p, pwr_cw_w, pwr_pulse_p, pwr_pulse_w, hz
def set_laser_softlock(laser=None, engaged=True):
    """
    Safely zeroes the laser power and enables the software lock.
    """
    if laser is None:
        try:
            laser = instruments.picoQuant.PicoQuant_Taiko_PDL_M1()
        except Exception as e:
            print(f"Failed to connect to laser for softlocking: {e}")
            return None
            
    print("\nEnabling Laser Softlock (Zeroing power)...")
    set(laser.cw_power_permille, 0)
    set(laser.pulse_burst_power_permille, 0)
    set(laser.softlock_en, True)
    close_device_all(laser=laser)


import time
import matplotlib.pyplot as plt

def start_apds(detector_config=2, trpl=False, read_counts=True, graph_counts=False):
    """
    Initializes the MH150. Validates that total count rates > 200 cps before 
    returning the device handle. Retries up to 3 times, polling for 10 seconds 
    per attempt.
    """
    config_path_1_det = r"C:\Codes\Picoquant\snAPI_configs\Exciletas_MH.ini"
    config_path_2_det = r"C:\Codes\Picoquant\snAPI_configs\MPDs_MH.ini"
    config_path_3_det = r"C:\Codes\Picoquant\snAPI_configs\MPDs_MH_TRPL.ini"

    d0 = 0  # Sync channel is standardly 0

    for attempt in range(3):
        sn = None  
        d1, d2 = None, None
        
        try:
            print(f"\n--- APD Initialization Attempt {attempt + 1}/3 ---")
            
            # --- 1. Initialize snAPI Detector ---
            sn = snAPI()
            sn.getDevice("1043897") 
            
            if not sn.initDevice():
                raise ConnectionError('MH150 device initialization failed.')

            # --- 2. Configuration Routing ---
            if detector_config == 1:
                d1, d2 = 1, 2
                sn.loadIniConfig(config_path_1_det)
                print(f'Using Exciletas: {sn.deviceConfig["ID"]}')
                
            elif detector_config == 2:
                d1, d2 = 3, 4
                if trpl:
                    sn.loadIniConfig(config_path_3_det)
                    print(f'Using MPDs for TRPL: {sn.deviceConfig["ID"]}')
                else:
                    sn.loadIniConfig(config_path_2_det)
                    print(f'Using MPDs (Standard): {sn.deviceConfig["ID"]}')
                    
            elif detector_config == 3:
                d1, d2 = 3, 4
                sn.loadIniConfig(config_path_3_det)
                print(f'Using MPDs for TRPL (Config 3 direct): {sn.deviceConfig["ID"]}')
                trpl = True 
            else:
                raise ValueError(f"Invalid detector_config: {detector_config}")

            # --- 3. Verification: Poll for 10 seconds ensuring Total > 200 ---
            counts_passed = False
            print("Polling APD count rates for up to 10 seconds (Requires Total > 200 cps)...")
            
            for sec in range(1, 11): # 1 to 10 seconds
                time.sleep(1) # Let hardware accumulate
                cnts = sn.getCountRates()

                c1, c2 = int(cnts[d1]), int(cnts[d2])
                total = c1 + c2
                
                if read_counts:
                    print(f"  [T+{sec}s] Ch {d1}: {c1} | Ch {d2}: {c2} | Total: {total} cps")
                    
                if total > 200:
                    counts_passed = True
                    print("Verification passed! Handing over instrument.")
                    break # Exit the polling loop early
            
            if not counts_passed:
                print("Verification failed: Total counts did not exceed 200 cps within 10 seconds.")
                print("Closing device and triggering restart...")
                close_device_all(sn=sn)
                time.sleep(1.5) # Brief cooldown before the next attempt
                continue # Jump to the next iteration of the 3-attempt loop

            # --- 4. Graph Counts Functionality (If Verification Passed) ---
            if graph_counts:
                print("Starting live count graph... Press Ctrl+C to exit.")
                fig = None 
                try:
                    start_time = time.time()
                    times, counts1, counts2 = [], [], []
                    running = [True] 

                    plt.ion()
                    fig, ax = plt.subplots()
                    
                    ax.set_title('Live Detector Counts')
                    ax.set_xlabel('Elapsed Time (s)'); ax.set_ylabel('Counts (cps)')
                    line1, = ax.plot([], [], 'r.-', label=f'Channel {d1}')
                    line2, = ax.plot([], [], 'b.-', label=f'Channel {d2}')
                    ax.legend(loc='upper left')
                    plt.show(block=False)

                    while running[0]:
                        cnt = sn.getCountRates()
                        tc1, tc2 = int(cnt[d1]), int(cnt[d2])
                        
                        times.append(time.time() - start_time)
                        counts1.append(tc1)
                        counts2.append(tc2)

                        line1.set_data(times, counts1)
                        line2.set_data(times, counts2)
                        
                        ax.relim(); ax.autoscale_view()
                        fig.canvas.draw(); fig.canvas.flush_events()
                        plt.pause(0.1)

                except KeyboardInterrupt:
                    print("\nGraphing stopped by user.")
                finally:
                    if fig and plt.fignum_exists(fig.number):
                        plt.ioff()
                        plt.close(fig)
                    print("Closing device after graphing.")
                    close_device_all(sn=sn)
                    return (None, None, None, None) if trpl else (None, None, None)

            # --- 5. Successful Standard Return ---
            if trpl:
                return sn, d0, d1, d2
            else:
                return sn, d1, d2

        except Exception as e:
            print(f"An error occurred during attempt {attempt + 1}: {e}")
            if sn is not None:
                try: close_device_all(sn=sn)
                except: pass
            time.sleep(1.5) # Cooldown before next attempt

    # --- Exhausted all 3 attempts ---
    print("\nCritical Error: Failed to start APDs with > 200 cps after 3 attempts.")
    return (None, None, None, None) if trpl else (None, None, None)

def start_apds_trpl():
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
    config_path_3_det = r'C:\Codes\Picoquant\user_configs_snAPI\MPDs_MH_TRPL.ini'

    sn = None  # Initialize sn to None for robust error handling
    try:
        # --- Initialize snAPI Detector ---
        sn = snAPI()
        sn.getDevice("1043897") # Register the device by serial number.
        

        if not sn.initDevice(MeasMode.Histogram):
            raise ConnectionError('MH150 device initialization failed.')
    
        d0, d1, d2 =0, 3, 4
        sn.loadIniConfig(config_path_3_det)
        print(f'Using MPDs for TRPL: {sn.deviceConfig["ID"]}')

        return sn, d0, d1, d2

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


import serial
import time
import pyvisa

# ==========================================
# 1. Serial Device (Filter Wheel & Lights)
# ==========================================

def send_cmd(drive, command, delay=0.05):
    """Sends a command and reads the response, with a small safety delay."""
    drive.write(f"{command}\r".encode('ascii'))
    time.sleep(delay)
    return drive.read_until(b'\r').decode('ascii').strip()

def power_apds(drive, state):
    """Robust APD power toggle. Sends command twice to ensure it registers."""
    cmd = "IL1" if state else "IH1"
    send_cmd(drive, cmd)
    time.sleep(0.1)
    send_cmd(drive, cmd) # Double-send for hardware robustness

def power_whitelight(drive, state):
    """Toggles white light without accidentally triggering APD commands."""
    if state:
        send_cmd(drive, "IL2")
    else:
        send_cmd(drive, "IH2")

def seek_home_precise(drive):
    """Micro-steps to the sensor edge and sets it as absolute zero (SP0)."""
    send_cmd(drive, "SK")
    time.sleep(0.1)
    send_cmd(drive, "VE10.0")
    
    while True:
        bits = send_cmd(drive, "IS").replace("IS=", "")
        if len(bits) >= 4 and bits[3] == '0':
            break
        send_cmd(drive, "DI10")
        send_cmd(drive, "FL")
        time.sleep(0.01)
        
    send_cmd(drive, "SP0")
    time.sleep(0.1)

def filterwheel(slot, offset=11.224, home_first=False, apd_final_state=False, wlight_final_state=False):
    """Moves the filter wheel and returns a state dictionary."""
    if slot < 0 or slot > 14:
        return {"status": "Error", "msg": "Invalid slot"}
        
    target_steps = int(-(slot + offset) * 1400)
    
    try:
        with serial.Serial(port='COM4', baudrate=38400, timeout=1) as drive:
            # Power down sensitive equipment during move
            power_whitelight(drive, False)
            power_apds(drive, False)
            
            if home_first:
                seek_home_precise(drive)

            send_cmd(drive, "VE1.0") 
            send_cmd(drive, f"FP{target_steps}")
            
            time.sleep(0.2)
            while True:
                if "0009" in send_cmd(drive, "SC", delay=0.1):
                    break
            
            # Restore desired states after move
            power_apds(drive, apd_final_state)
            if not apd_final_state:
                power_whitelight(drive, wlight_final_state)
                
            return {
                "Slot": slot,
                "APD_Power": "ON" if apd_final_state else "OFF",
                "White_Light": "ON" if (wlight_final_state and not apd_final_state) else "OFF"
            }
            
    except serial.SerialException as e:
        print(f"Serial connection failed: {e}")
        return {"Slot": "Unknown", "APD_Power": "Unknown", "White_Light": "Unknown"}

# ==========================================
# 2. ESP Controller (Detection & Filters)
# ==========================================

def move_esp_axis(esp, axis, target_pos, axis_name, showcmd=False):
    """Smart polling function that moves an axis and waits exactly until it arrives."""
    try:
        if showcmd:
            print(f"{axis_name} axis moving to {target_pos}mm...")
        
        esp.write(f"{axis}PA{target_pos}")
        
        # Smart Polling Loop instead of time.sleep(5)
        timeout = 15.0 
        start_time = time.time()
        pos_now = 0.0
        
        while time.time() - start_time < timeout:
            response = esp.query(f"{axis}TP?").strip()
            if response:
                pos_now = float(response)
                # If we are within 0.01mm of target, we have arrived
                if abs(pos_now - target_pos) < 0.01:
                    break
            time.sleep(0.2) # Check 5 times a second
            
        if showcmd:
            print(f"{axis_name} axis arrived at: {pos_now} mm")
        return pos_now
        
    except Exception as e:
        print(f"ESP communication error on {axis_name}: {e}")
        return "Error"

def detector_switch(esp, moveto='camera', showcmd=False):
    targets = {'apd': 0.0, 'spectro': -49.0, 'camera': 47.5}
    if moveto not in targets: return "Invalid"
    return move_esp_axis(esp, axis=3, target_pos=targets[moveto], axis_name="Detection", showcmd=showcmd)

def filter_switch(esp, moveto='no', showcmd=False):
    targets = {'no': -24.0, 'n405': 0.0, 'n533': 25.0}
    if moveto not in targets: return "Invalid"
    return move_esp_axis(esp, axis=2, target_pos=targets[moveto], axis_name="Filter", showcmd=showcmd)

# ==========================================
# 3. Master Integration
# ==========================================

def set_detection(state, home_first=False, apd_final_state=False, wlight_final_state=False, offset=11.224):
    """
    Coordinates all hardware and prints a complete state output table.
    """
    print(f"\n--- Initiating Hardware Shift to: [{state.upper()}] ---")
    
    # 1. Manage Serial Filter Wheel & Lights
    configs = {
        "camera":  {"slot": 0,  "filter": "no",   "detector": "camera"},
        "apd":     {"slot": 10, "filter": "n405", "detector": "apd"},
        "spectro": {"slot": 1,  "filter": "n405", "detector": "spectro"},
        "apd-435": {"slot": 5, "filter": "n405", "detector": "apd"}
    }
    
    if state not in configs:
        print("Error: Unknown detection state requested.")
        return
        
    cfg = configs[state]
    
    serial_status = filterwheel(
        slot=cfg["slot"], 
        offset=offset, 
        home_first=home_first, 
        apd_final_state=apd_final_state, 
        wlight_final_state=wlight_final_state
    )
    
    # 2. Manage ESP Axes
    det_pos, filt_pos = "Unknown", "Unknown"
    
    try:
        rm = pyvisa.ResourceManager()
        esp = rm.open_resource("GPIB1::7::INSTR")
        esp.timeout = 2000 # Set 2s timeout for reliable queries
        
        filt_pos = filter_switch(esp, moveto=cfg["filter"], showcmd=False)
        det_pos = detector_switch(esp, moveto=cfg["detector"], showcmd=False)
        
        esp.close()
    except Exception as e:
        print(f"Warning: Could not connect to ESP Controller. {e}")

    # 3. Output Final Hardware State
    print("\n" + "="*45)
    print("      CURRENT HARDWARE SYSTEM STATE      ")
    print("="*45)
    print(f" Target Mode        : {state.upper()}")
    print(f" Filter Wheel Slot  : {serial_status['Slot']}")
    print(f" Filter Axis Pos    : {filt_pos} mm")
    print(f" Detection Axis Pos : {det_pos} mm")
    print(f" APD Power State    : {serial_status['APD_Power']}")
    print(f" White Light State  : {serial_status['White_Light']}")
    print("="*45 + "\n")
    

#def home_attocube(axis,amc=None):
    #if amc is None:
    #    amc = start_attocube()
    #if axis is None:
        #for ax in [0,1,2]:
            #amc.control.setControlOutput(ax, True)
            #amc.control.setControlMove(ax, True)
            #amc.control.setControlAutoReset(ax)
            #amc.control.searchReferencePosition(ax)
            #amc.control.setCon
    

def start_attocube(amc_address='amc100num-a01-0248.local',showcmd=False):
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
            
        if showcmd: 
            print(f"Using AMC : {amc_address}")
        # Return the connected device object so it can be used later
        return amc
    

    except Exception as e:
        print(f"ERROR: Failed to connect or initialize AMC controller: {e}")
        # Clean up by closing the connection if an error occurs
        if amc:
            amc.close()
        return None
def amc_disable(amc=None):
    if amc is None:
        amc = start_attocube()
    for axis in [0, 1, 2]:
        #amc.control.setControlOutput(axis, False)
        amc.control.setControlMove(axis, False)
        print(f"Disabled: Axis {axis}")
    amc.close()
def close_device_all(sn=None, amc=None,showcmd=True, daq=None, t_ch1=None, t_ch2=None, spectro=None, camera=None,laser=None):
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
        if camera:
            unload(camera)
            print("iDus closed.")
        if spectro:
            unload(spectro)
            print("Kymera closed.")
        if laser:
            unload(laser)
            print("laser closed.")
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
def amc_movexyz(x=None,y=None,f=None,amc=None,output=False):
    try:
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True
        x0,y0,f0 = getposall(amc=amc)
        if x is not None:
            amc.move.setControlTargetPosition(0, int(x * 1000));wait_until_stable(amc, 0)
        if f is not None:
            amc.move.setControlTargetPosition(1, int(f * 1000));wait_until_stable(amc, 1)
        if y is not None: 
            amc.move.setControlTargetPosition(2, int(y * 1000));wait_until_stable(amc, 2)
        x,y,f = getposall(amc=amc) 
        if output:
            return x,y,f 
    except Exception as e:
        print(f"An error occurred during amc_move: {e}")
        amc.move.setControlTargetPosition(0, int(x0 * 1000));wait_until_stable(amc, 0)
        amc.move.setControlTargetPosition(1, int(f0 * 1000));wait_until_stable(amc, 1)
        amc.move.setControlTargetPosition(2, int(y0 * 1000));wait_until_stable(amc, 2)
        return x0,y0,f0 
    finally:
        if amc_local and amc: close_device_all(amc=amc,showcmd=False)
        
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
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def run_pl_scan(center_x=None, center_y=None, center_f=None,
                focus_sweep=False, f_size=50,
                x_size=5, y_size=5, step=0.1,
                detector_config=2, min_signal=100,
                logz=False,
                ide=None,
                out_dir_base=r'D:\Data_Python_PL\PLmaps',
                show_plot=True,
                waits=0,
                amc=None, sn=None, d1=None, d2=None):
    """
    Performs a 2D photoluminescence scan. Manages its own device lifecycle
    and includes a 10-second APD health pre-check to prevent dead scans.
    """
    amc_local = False
    sn_local = False
    data_file_handle = None

    try:
        # === 1. Initialize Devices (if not provided) ===
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

        # === 3. Setup Scan Area, Output, and Focus ===
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
            best_f = run_focus_sweep(fbase=fnow, sn=sn, amc=amc, d1=d1, d2=d2,
                                     movetobest=True, showplt=False, fsize=f_size, engaged=True)
            fnow = best_f
            time.sleep(5)
            
        center_f = fnow 
        print(f"Initial pos (x,y,z) :  ({center_x:.2f}, {center_y:.2f}, {center_f:.2f}) µm")
        
        # === 4. Setup Plot and Data File ===
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
        plot_file = os.path.join(out_dir, f'plmap_plot{f"_{ide}" if ide is not None else ""}_{timestamp}.png')
        data_file = os.path.join(out_dir, f'plmap_data{f"_{ide}" if ide is not None else ""}_{timestamp}.txt')

        print(f'Saving data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# PL Mapping - {timestamp}\n# Center X: {center_x}, Y: {center_y}, F: {center_f}\n')
        data_file_handle.write(f'# readback numpy shape for line part: {len(x_pos)}, {len(y_pos)} \n')
        data_file_handle.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')

        # === 5. Start Scan Loop ===
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
        return None, None, None
    except KeyboardInterrupt as k:
        print(f"\nKeyboard interrupt : {k}")
        print(f"Moving to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(center_y * 1000)); wait_until_stable(amc, axis=2)
        return None, None, None    
    finally:
        # === 6. Cleanup Resources ===
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


def run_pl_position_optimizer(scan_size=2, scan_step=0.1, movetoxy=True, run_focus_sweep=False, show_plot=True,
                              sn=None, d1=None, d2=None, ide=None, amc=None, detector_config=2):
    """
    Runs a PL scan to find the brightest spot. 
    Delegates the heavy lifting and hardware safety checks to run_pl_scan.
    """
    sn_local = False
    amc_local = False
    bx, by, bf = None, None, None

    try:
        # --- 1. Device Initialization ---
        if sn is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Optimizer failed to start APDs.")
            sn_local = True
        elif d1 is None or d2 is None:
            # Fallback if an existing sn is passed without channels specified
            d1, d2 = 3, 4 
            
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Optimizer failed to start Attocube.")
            amc_local = True

        x_now = amc.move.getPosition(0) / 1000
        y_now = amc.move.getPosition(2) / 1000
        f_now = amc.move.getPosition(1) / 1000

        # --- 2. Execute PL Scan ---
        print("\nStarting position optimization...")
        
        # run_pl_scan will handle the 10-second APD check internally
        bx, by, bf = run_pl_scan(
            center_x=x_now, center_y=y_now, center_f=f_now,
            x_size=scan_size, y_size=scan_size, step=scan_step,
            focus_sweep=run_focus_sweep, show_plot=show_plot,
            sn=sn, d1=d1, d2=d2, amc=amc, ide=ide
        )

        # --- 3. Move to Best Position ---
        if movetoxy and bx is not None:
            print("\nMoving to best X-Y position...")
            amc.move.setControlTargetPosition(0, int(bx * 1000))
            wait_until_stable(amc, 0)
            amc.move.setControlTargetPosition(2, int(by * 1000))
            wait_until_stable(amc, 2)
            print("Move complete.")
            
    finally:
        # --- 4. Cleanup Locally Opened Devices ---
        if sn_local and sn is not None: 
            try: close_device_all(sn=sn)
            except Exception: pass
        if amc_local and amc is not None: 
            try: close_device_all(amc=amc)
            except Exception: pass
            
    return bx, by, bf

def g2_measure(time_m=300, save_figure=True, sn=None, detector_config=2, ide=None,det_ch1=None, det_ch2=None, binsize_ps=100, windowsize_ps=100000):
    """
    Performs a live g(2) cross-correlation measurement.
    Wrapped in a kernel-safe structure to prevent memory leaks and DLL locks.
    """
    sn_local = False
    succ = False
    end_time = time.time() 
    start_time = time.time()
    
    try:
        # === 1. Device Initialization ===
        if sn is None:
            # Assuming start_apds returns (sn, d1, d2) when trpl=False
            result = start_apds(detector_config=detector_config)
            if result[0] is None: 
                raise ConnectionError("Failed to start APDs.")
            
            sn = result[0]
            a = result[1]
            b = result[2]
            sn_local = True
        else:
            a = det_ch1
            b = det_ch2
            if a is None or b is None:
                raise ValueError("If passing an existing 'sn', you must specify det_ch1 and det_ch2.")

        mt = time_m 
        
        # === 2. File Setup ===
        output_dir = r'D:\Data_Python_PL\G2data'
        os.makedirs(output_dir, exist_ok=True)
        dtnow = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        ptuo = f'g2data_{mt:.0f}s{f"_{ide}" if ide is not None else ""}_{dtnow}.ptu' 
        g2_filename = os.path.join(output_dir, ptuo)
        sn.setPTUFilePath(g2_filename)
        details_filename = os.path.join(output_dir, f"g2details_{mt:.0f}s_{dtnow}.txt")
        
        # === 3. Measurement Parameters ===
        d = binsize_ps          # in ps
        c = windowsize_ps       # in ps

        sn.correlation.setG2Parameters(a, b, c, d)
            
        # Start measurement
        sn.correlation.measure(int(mt * 1000), savePTU=True)
        start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'MH Device : ({sn.deviceConfig["ID"]}) initialized.')
        print(f'Starting a measurement for {mt} s...')
        print(f'Using file name: {g2_filename}')
        
        # Tracking variables
        elapsed_time_list = []
        ch1_counts = []
        ch2_counts = []
        total_counts = []
        timestamps = []
        g2_zero_values = []

        start_time = time.time()

        # === 4. High-Performance Graphing Setup ===
        plt.ion()
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))
        
        line_g2, = axes[0].plot([], [], label=f'{os.path.basename(g2_filename)}', linewidth=0.5)
        axes[0].set_xlabel('Time delay (ns)')
        axes[0].set_ylabel('g2(t)')
        axes[0].legend(loc='upper right')
        
        line_ch1, = axes[1].plot([], [], label="Channel 1", color='b', linewidth=0.5, linestyle='--', marker='o')
        line_ch2, = axes[1].plot([], [], label="Channel 2", color='r', linewidth=0.5, linestyle='--', marker='s')
        axes[1].set_xlabel('Elapsed Time (s)')
        axes[1].set_ylabel('Count Rate')
        axes[1].legend(loc='upper right')

        # === 5. Main Measurement Loop ===
        with open(details_filename, 'w') as file:
            file.write(f"# Measurement Details\n")
            file.write(f"# Channel 1 = {a}, Channel 2 = {b}, Windows Size = {c} ps, Bin Width = {d} ps\n")
            file.write(f"# Measurement Time (mt) = {mt} s\n")
            file.write(f"# Measurement Start Time: {start_timestamp}\n#\n")
            file.write(f"# Current Time\tElapsed Time (s)\tChannel 1 Counts\tChannel 2 Counts\tTotal Counts\tg2(0)\n")

            last_plot_time = time.time()

            while True:
                # Replaced time.sleep with plt.pause to keep GUI responsive
                plt.pause(0.5) 
                
                try:
                    finished = sn.correlation.isFinished()
                    g2, lagtimes = sn.correlation.getG2Data()
                except Exception:
                    continue # Skip loop safely if hardware is busy
                    
                lagtimes_ns = np.array(lagtimes) * 1e9
                
                # Check if arrays are valid before operating on them
                if not isinstance(g2, np.ndarray) or len(g2) == 0:
                    if finished: break
                    continue
                    
                g2_zero = float(np.min(g2))
                
                # Fetch count rates safely
                try:
                    cnts = sn.getCountRates()
                    cntss = cnts[a] + cnts[b]
                except IndexError:
                    print(f"Error: Channels ({a}, {b}) exceed hardware count array length.")
                    break
                    
                elapsed_t = time.time() - start_time
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Store data
                timestamps.append(current_time)
                elapsed_time_list.append(elapsed_t)
                ch1_counts.append(cnts[a])
                ch2_counts.append(cnts[b])
                total_counts.append(cntss)
                g2_zero_values.append(g2_zero)
                
                file.write(f"{current_time}\t{elapsed_t:.2f}\t{cnts[a]}\t{cnts[b]}\t{cntss}\t{g2_zero:.2f}\n")
                file.flush() 
                
                c_percent = (elapsed_t * 100) / mt

                # Update plots smoothly
                if time.time() - last_plot_time >= 1.0 or finished:
                    line_g2.set_data(lagtimes_ns, g2)
                    line_ch1.set_data(elapsed_time_list, ch1_counts)
                    line_ch2.set_data(elapsed_time_list, ch2_counts)
                    
                    # --- PYLAB FIX: Using np.maximum instead of max() ---
                    axes[0].relim()
                    axes[0].autoscale_view(True, True, True)
                    axes[0].set_ylim(0, np.maximum(0.1, np.max(g2) * 1.1))
                    axes[0].set_title(f'g2(t) Correlation (BinWidth = {d} ps & WindowSize = {int(c/1000):.0f} ns) g2(0)={g2_zero: .2f}')
                    
                    axes[1].relim()
                    axes[1].autoscale_view(True, True, True)
                    # Safely handle the double max for the count arrays
                    max_ch1 = np.max(ch1_counts) if ch1_counts else 1
                    max_ch2 = np.max(ch2_counts) if ch2_counts else 1
                    axes[1].set_ylim(0, np.maximum(max_ch1, max_ch2) * 1.2)
                    # ----------------------------------------------------
                    
                    if elapsed_t < mt:
                        axes[1].set_title(f'Time trace : {c_percent: .0f}% done (Run-time = {elapsed_t: .0f} / {mt: .0f} s)')
                    else: 
                        axes[1].set_title(f'Time trace : Completed (Total Run-time = {mt: .0f} s)')
                    
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    last_plot_time = time.time()
                
                if finished:
                    end_time = time.time()
                    succ = True
                    break
                    
            end_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            total_runtime = end_time - start_time        
            
            # Footer information
            file.write("#\n")
            file.write(f"# Measurement End Time: {end_timestamp}\n")
            file.write(f"# Total Runtime: {total_runtime:.2f} s\n")
            if succ:
                file.write(f"# Completion = {succ} \n")        
                
            if save_figure:
                figpath = os.path.join(output_dir, f'g2plot_{mt}s_{dtnow}.png')
                try:
                    fig.savefig(figpath)
                    print(f"Figure saved as {figpath}")
                except Exception as e:
                    print(f"Error saving figure: {e}")

    # === 6. Guaranteed Cleanup ===
    except Exception as e:
        print(f"\nA critical error occurred: {e}")
        traceback.print_exc() # Added to reveal hidden bugs
    finally:
        # Added sleep for safe C-DLL thread shutdown
        if sn is not None:
            try:
                sn.correlation.stopMeasure()
                print("Measurement stopped, clearing buffers...")
                time.sleep(0.5) 
            except Exception as stop_err:
                print(f"Warning during stopMeasure: {stop_err}")
        if sn_local and sn is not None:
            try:
                # If your close function requires 'sn' as a kwarg like before, update this to:
                # close_device_all(sn=sn)
                sn.closeDevice(allDevices=True) 
                print("Device closed successfully.")
            except Exception as e:
                print(f"Error closing device: {e}")
        plt.ioff()
        plt.show()       
        
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



def trpl_measure(time_m=600, sync_offset=20, save_figure=True, sn=None, 
                 detector_config=3, frequency_mhz=10, update_hz_laser=False, 
                 laser=None, binsize_ps=10, 
                 output_dir=r'D:\Data_Python_PL\TRPLdata',ide=None):
    """
    Performs a Dual-Channel Time-Resolved Photoluminescence (TRPL) measurement.
    Dynamically scales binnums based on laser frequency and locks X-axis windows.
    sync_offset = in ns
    """
    sn_local = False
    laser_local = False
    succ = False
    start_time = time.time()
    ide_suffix = f"_{ide}" if ide is not None else ""
    
    # === 1. Handle Frequency Source ===
    if update_hz_laser:
        print("Querying laser for current pulse frequency...")
        if laser is None:
            try:
                laser = instruments.picoQuant.PicoQuant_Taiko_PDL_M1()
                laser_local = True
            except Exception as e:
                print(f"Warning: Could not connect to laser to fetch frequency: {e}")
                
        if laser is not None:
            try:
                freq_hz = get(laser.pulse_burst_freq_Hz)
                frequency_mhz = freq_hz / 1e6 # Convert Hz to MHz
                print(f"Successfully fetched frequency from laser: {frequency_mhz:.2f} MHz")
            except Exception as e:
                print(f"Warning: Failed to read frequency from laser object: {e}. Falling back to {frequency_mhz} MHz.")
                
        if laser_local and laser:
            try: close_device_all(laser=laser)
            except Exception: pass
            laser_local = False

    # === 2. Dynamic Bin Calculation ===
    period_ps = 1e6 / frequency_mhz
    binnums = int(period_ps / binsize_ps)
    print(f"Active Laser Frequency: {frequency_mhz:.1f} MHz | Window: {period_ps / 1000:.1f} ns | Binnums: {binnums}")

    sync_ch, det_ch1, det_ch2 = 0, 3, 4 
    
    try:
        # === 3. Device Initialization ===
        if sn is None:
            sn, sync_ch, det_ch1, det_ch2 = start_apds(detector_config=detector_config, trpl=True)
            if sn is None: 
                raise ConnectionError("Failed to start APDs.")
            sn_local = True
            
        # === 4. File Setup (TEXT ONLY) ===
        os.makedirs(output_dir, exist_ok=True)
        dtnow = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        
        # === 5. Start Measurement ===
        sn.histogram.setRefChannel(sync_ch)
        sn.histogram.setBinWidth(binsize_ps)
        sn.histogram.setNumBins(binnums) 
        sn.device.setSyncChannelOffset(int(sync_offset*1000))
        
        # FIX: savePTU=False prevents the 45GB file dump. Data stays in RAM.
        sn.histogram.measure(int(time_m * 1000), waitFinished=False, savePTU=False)

        print(f'Starting dual-channel TRPL measurement for {time_m} s at {frequency_mhz:.1f} MHz...')

        # === 6. High-Performance Graphing Setup ===
        plt.ion()
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # FIX: Added marker='.' and set linewidth to draw only the top points
        line_hist1, = axes[0].plot([], [], label=f'Ch {det_ch1}', linewidth=1.0, color='blue', marker='.', markersize=2)
        axes[0].set_xlabel('Time (ns)')
        axes[0].set_ylabel('Counts (Log)')
        axes[0].set_yscale('log')
        axes[0].set_xlim(left=0, right=period_ps / 1000) 
        axes[0].grid(True, which='both', alpha=0.3)
        axes[0].legend(loc='upper right')

        line_hist2, = axes[1].plot([], [], label=f'Ch {det_ch2}', linewidth=1.0, color='red', marker='.', markersize=2)
        axes[1].set_xlabel('Time (ns)')
        axes[1].set_ylabel('Counts (Log)')
        axes[1].set_yscale('log')
        axes[1].set_xlim(left=0, right=period_ps / 1000) 
        axes[1].grid(True, which='both', alpha=0.3)
        axes[1].legend(loc='upper right')
        
        fig.tight_layout()
        fig.subplots_adjust(top=0.88)

        # === 7. Main Measurement Loop ===
        last_plot_time = time.time()

        while True:
            plt.pause(2) 
            
            try:
                finished = sn.histogram.isFinished()
                hist_all_channels, time_bins = sn.histogram.getData()
            except Exception:
                continue
            
            try:
                if not isinstance(hist_all_channels, np.ndarray) or hist_all_channels.ndim < 2:
                    continue 
                    
                max_idx = hist_all_channels.shape[0] - 1
                if det_ch1 > max_idx or det_ch2 > max_idx:
                    print(f"Warning: Channels ({det_ch1}, {det_ch2}) exceed data shape")
                    break
                    
                hist_data1 = hist_all_channels[det_ch1]
                hist_data2 = hist_all_channels[det_ch2]
            except Exception as e:
                print(f"Data extraction error: {e}")
                break

            time_bins_ns = np.array(time_bins) / 1000.0 
            elapsed_t = time.time() - start_time
            
            if time.time() - last_plot_time >= 2.0 or finished:
                line_hist1.set_data(time_bins_ns, np.clip(hist_data1, 1, None))
                line_hist2.set_data(time_bins_ns, np.clip(hist_data2, 1, None))
                
                try: tau1 = estimate_lifetime(time_bins_ns, hist_data1)
                except Exception: tau1 = 0.0
                try: tau2 = estimate_lifetime(time_bins_ns, hist_data2)
                except Exception: tau2 = 0.0
                
                axes[0].relim()
                axes[0].autoscale_view(True, True, True)
                axes[0].set_ylim(1, np.maximum(10, np.max(hist_data1) * 2))
                axes[0].set_title(f'Ch {det_ch1} TRPL | $\\tau \\approx$ {tau1:.2f} ns')
                
                axes[1].relim()
                axes[1].autoscale_view(True, True, True)
                axes[1].set_ylim(1, np.maximum(10, np.max(hist_data2) * 2))
                axes[1].set_title(f'Ch {det_ch2} TRPL | $\\tau \\approx$ {tau2:.2f} ns')
                
                title_text = 'TRPL Measurement Completed' if finished else f'Live TRPL ({elapsed_t:.0f} / {time_m} s)'
                fig.suptitle(title_text, fontsize=14, fontweight='bold')
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                last_plot_time = time.time()
                
            if finished:
                succ = True
                break
                
        # === 8. Export Data ===
        if succ:
            txt_filename = os.path.join(output_dir, f"trpldata_{frequency_mhz:.1f}MHz_{time_m:.0f}s{ide_suffix}_{dtnow}.txt")
            
            # FIX: This perfectly matches your request. Col 0 is Bins, Col 1 is Ch1, Col 2 is Ch2.
            np.savetxt(txt_filename, np.column_stack((time_bins, hist_data1, hist_data2)), 
                       delimiter='\t', header=f"Time(ps)\tCh{det_ch1}_Counts\tCh{det_ch2}_Counts")
            print(f"Final histogram data saved to: {os.path.basename(txt_filename)}")

        if save_figure:
            figpath = os.path.join(output_dir, f'trplplot_{frequency_mhz:.1f}MHz_{time_m}s{ide_suffix}_{dtnow}.png')
            try: fig.savefig(figpath)
            except Exception: pass
                
    except Exception as e:
        print(f"\nA critical error occurred: {e}")
        traceback.print_exc() 
    finally:
        if sn is not None:
            try:
                sn.histogram.stopMeasure()
                time.sleep(0.5) 
            except Exception: pass
                
        if sn_local and sn:
            try: close_device_all(sn=sn)
            except Exception: pass
                
        plt.ioff()
        plt.show()
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
def getposall(amc=None):
    if amc is None:
        amc = start_attocube()
    x = amc.move.getPosition(0) / 1000
    y = amc.move.getPosition(2) / 1000
    f = amc.move.getPosition(1) / 1000
    return x,y,f
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
    #try:
    #    spectro = instruments.andor_kymera()
    #    camera = instruments.andor_iDus()
    #except: pass
    #time.sleep(1)
    #try:
    #    unload(camera)
    #    unload(spectro)
    #except: pass
    #time.sleep(10)
    spectro = instruments.andor_kymera()
    set(spectro.wavelength_nm, spectro_set_cw)
    time.sleep(1)
    camera = instruments.andor_iDus(spectro_instr=spectro,cooler_temp=-80,shutter_init=shutter_init)
    time.sleep(5)
    camera.conf(read_mode='full_vertical_binning',exposure_time=5,acq_mode="accumulate", acc_N=2)
    set(camera.cosmic_filter_en, True)
    vbg=None
    if waitfortemp:
        camera.wait_for_cooler_stable(-80)
    minw = int(get(spectro.sensor_wavelengths_nm)[0])
    maxw = int(get(spectro.sensor_wavelengths_nm)[-1])
    if showrange:
        print(f"Current wavelength range : {minw}nm to {maxw}nm")
    return spectro, camera        
def close_spectro(spectro=None,camera=None):
    if camera is not None:
        unload(camera)
    if spectro is not None:
        unload(spectro)
def take_spectrum_bg(camera=None, sav_data=True, ide=None, idex=None):
    out_dir = output_dir_folder(base_dir=r"D:\Data_Python_PL\Spectrum")
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    data_file_bg = os.path.join(out_dir, f'spectrum_data_BG{f"_{ide}" if ide is not None else ""}{f"_{idex}" if idex is not None else ""}_{timestamp}.txt') 
    set(camera.shutter, False)
    time.sleep(1)
    print("Taking BG...")
    print(f"Using Filename : {data_file_bg}")
    vbg = get(camera.readval, filename=data_file_bg if sav_data else None)
    set(camera.shutter, True)
    time.sleep(1)
    return vbg

def take_live_spectrum(camera,spectro,exposure_time=1,grating=1):
    if grating ==2:
        wl=461
        print("Grating 2 selected")
    else:
        wl=484
        print("Grating 1 selected (Default)")
    set_spectrum(camera=camera, spectro=spectro, acq_mode="single_scan", cosmic_filter=False, exposure_time=exposure_time,wl=wl,grating=grating)
    scope(camera.readval)
    
def take_spectrum(bg=True, vbg=None,
                  data_only=False,
                  show_plot=True,
                  camera=None,sav_data=True,ide=None,idex=None):
    if camera is None:
        print("No Camera")
        return None
    out_dir = output_dir_folder(base_dir=r"D:\Data_Python_PL\Spectrum")
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    data_file_bg = os.path.join(out_dir, f'spectrum_data_BG{f"_{ide}" if ide is not None else ""}{f"_{idex}" if idex is not None else ""}_{timestamp}.txt') 
    data_file = os.path.join(out_dir, f'spectrum_data{f"_{ide}" if ide is not None else ""}{f"_{idex}" if idex is not None else ""}_{timestamp}.txt') 
    if bg:
        if vbg is None:
            set(camera.shutter, False)
            time.sleep(1)
            print("Taking BG...")
            print(f"Using Filename : {data_file_bg}")
            vbg = get(camera.readval, filename=data_file_bg if sav_data else None)
            set(camera.shutter, True)
            time.sleep(1)
        print("Taking Spectrum...")
        print(f"Using Filename : {data_file}")
        v = get(camera.readval, bkg_rem=vbg[1], filename=data_file if sav_data else None)
    else:
        print("Taking Spectrum...")
        print(f"Using Filename : {data_file}")
        v = get(camera.readval, filename=data_file if sav_data else None)
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


def run_focus_sweep_save(fbase=None, fstep=0.1, fsize=30, movetobest=True, showplt=True, engaged=False, 
                    sn=None, d1=None, d2=None, amc=None, detector_config=2,
                    out_dir_base=r'D:\Data_Python_PL\FocusSweeps'):
    """
    Performs a Z-axis sweep to find the optimal focus.
    Saves the data and plot to a file.
    """
    amc_local = False
    sn_local = False
    data_file_handle = None
    fnow = fbase # Keep track of initial focus for error case

    try:
        # --- Device Initialization ---
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

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

        # --- File Saving Setup ---
        out_dir = output_dir_folder(base_dir=out_dir_base) # Ensure output_dir_folder exists
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        data_file = os.path.join(out_dir, f'focus_sweep_{timestamp}.txt')
        plot_file = os.path.join(out_dir, f'focus_sweep_{timestamp}.png')
        
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# APD Focus Sweep - {timestamp}\n')
        data_file_handle.write(f'# Base Focus: {fnow:.2f}, Size: {fsize}, Step: {fstep}\n')
        data_file_handle.write('Focus(um)\tCh1(cps)\tCh2(cps)\tTotal(cps)\n')

        # --- Plot Setup ---
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
                
            # Write point to file
            data_file_handle.write(f'{f:.3f}\t{ch1}\t{ch2}\t{total}\n')

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
        plt.savefig(plot_file)
        if showplt: plt.show()
        else: plt.close(fig)

        return bestf

    except Exception as e:
        print(f"An error occurred during focus sweep: {e}")
        return fnow # Return original focus on error
    except KeyboardInterrupt as k:
        print(f"Keyboard interrupt : {k}")
        print(f"Moving to initial position ---")
        amc.move.setControlTargetPosition(1, int(fnow * 1000)); wait_until_stable(amc, 1)
        return fnow
    finally:
        # --- Cleanup ---
        if data_file_handle:
            data_file_handle.close()
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)		
def run_spectrum_focus_sweep(camera, spectro, fbase=None, fstep=0.1, fsize=30, movetobest=True, 
                             showplt=True, engaged=False, amc=None,
                             wl_min=None, wl_max=None, vbg=None,
                             out_dir_base=r'D:\Data_Python_PL\FocusSweeps'):
    """
    Performs a Z-axis sweep using a spectrograph.
    Saves the full spectrum at each focus step to a text file.
    Finds best focus based on the sum of intensities between wl_min and wl_max.
    """
    amc_local = False
    data_file_handle = None
    fnow = fbase 

    try:
        # --- Device Initialization ---
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if engaged:
            amc_local = False

        if fbase is None:
            fnow = amc.move.getPosition(1) / 1000
        else:
            fnow = fbase
            
        fstart, fend = fnow - (fsize / 2), fnow + (fsize / 2)
        frange = np.arange(fstart, fend + fstep, fstep)
        focus, totals = [], []
        maxc, bestf = -1, fnow

        # --- Get Wavelength Array & Mask ---
        print("Taking initial dummy spectrum to calibrate wavelengths...")
        if vbg is not None:
            v_init = get(camera.readval, bkg_rem=vbg[1])
        else:
            v_init = get(camera.readval)
        
        wavelengths = v_init[0]
        if wl_min is None: wl_min = wavelengths[0]
        if wl_max is None: wl_max = wavelengths[-1]
        wl_mask = (wavelengths >= wl_min) & (wavelengths <= wl_max)
        
        print(f"Plotting and optimizing sum of intensities between {wl_min:.1f} nm and {wl_max:.1f} nm.")

        # --- File Saving Setup ---
        out_dir = output_dir_folder(base_dir=out_dir_base)
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        data_file = os.path.join(out_dir, f'focus_sweep_spectro_{timestamp}.txt')
        plot_file = os.path.join(out_dir, f'focus_sweep_spectro_{timestamp}.png')
        
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# Spectro Focus Sweep - {timestamp}\n')
        data_file_handle.write(f'# Base Focus: {fnow:.2f}, Size: {fsize}, Step: {fstep}\n')
        data_file_handle.write(f'# Integrated Range for Plotting: {wl_min} to {wl_max} nm\n')
        wl_headers = "\t".join([f"{w:.2f}" for w in wavelengths])
        data_file_handle.write(f'Focus(um)\t{wl_headers}\n')

        # --- Plot Setup ---
        plt.ion()
        fig, ax = plt.subplots()
        line_total, = ax.plot([], [], 'b.-', label=f'Sum ({wl_min:.1f}-{wl_max:.1f}nm)')
        ax.legend(loc='upper left')
        ax.set_xlabel('Focus (µm)'); ax.set_ylabel('Counts (Arb.)')
        ax.set_xlim(fstart, fend)

        print("Starting spectro focus sweep...")
        for f in frange:
            amc.move.setControlTargetPosition(1, int(f * 1000))
            wait_until_stable(amc, 1)

            # --- Read Spectrum ---
            if vbg is not None:
                v = get(camera.readval, bkg_rem=vbg[1])
            else:
                v = get(camera.readval)
            intensities = v[1]
            
            filtered_sum = np.sum(intensities[wl_mask])
            
            focus.append(f)
            totals.append(filtered_sum)

            if filtered_sum > maxc:
                bestf, maxc = f, filtered_sum
                
            # Write exact point data to file
            int_data_str = "\t".join([f"{count:.2f}" for count in intensities])
            data_file_handle.write(f'{f:.3f}\t{int_data_str}\n')

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
        plt.savefig(plot_file)
        if showplt: plt.show()
        else: plt.close(fig)

        return bestf

    except Exception as e:
        print(f"An error occurred during focus sweep: {e}")
        return fnow 
    except KeyboardInterrupt as k:
        print(f"Keyboard interrupt : {k}")
        print(f"Moving to initial position ---")
        # Notice I fixed the axis to 1 below, in the original script it had a typo as axis=0
        amc.move.setControlTargetPosition(1, int(fnow * 1000)); wait_until_stable(amc, 1)
        return fnow
    finally:
        # --- Cleanup ---
        if data_file_handle:
            data_file_handle.close()
        if amc_local and amc: close_device_all(amc=amc)	


#set_spectrum(camera=camera, spectro=spectro, wl=484, grating=1) for default 420 to 547
#set_spectrum(camera=camera, spectro=spectro, wl=461, grating=2) for HR 430 to 490
try: 
    from pylablib.devices import Thorlabs
except ImportError as e: 
    print(e)

# --- Thorlabs KDC Controller Functions ---

def start_kdc(SN="27257399", kdc=None, force=True):
    """
    Initializes and connects to a Thorlabs Kinesis Motor (rotation mount).
    
    Args:
        SN (str): Serial number of the motor. Defaults to "27257399".
        kdc (Thorlabs.KinesisMotor, optional): Existing KDC motor instance.
        force (bool): If True, forces the motor to home upon starting. Defaults to False.
        
    Returns:
        Thorlabs.KinesisMotor: The connected motor object.
    """
    if kdc is not None:
        return kdc
    else:
        try:
            kdc = Thorlabs.KinesisMotor(SN)
            kdc.open()
            print(f"Homing KDC motor SN: {SN}...")
            kdc.home(force=force)
            print(f"Connected to KDC motor SN: {SN}")
            return kdc
        except Exception as e:
            print(f"ERROR: Failed to connect to KDC motor: {e}")
            return None


def kdc_position_deg(kdc=None):
    """
    Reads the current position of the Thorlabs KDC rotation mount in degrees.
    
    Args:
        kdc (Thorlabs.KinesisMotor, optional): Existing KDC motor instance.
        
    Returns:
        float: Current position in degrees.
    """
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


def run_pl_polarization(start_deg=0, end_deg=360, step_deg=2, 
                        detector_config=2, out_dir_base=r'D:\Data_Python_PL\PolarizationAPD',
                        show_plot=True, normalize_plot=False, movetobest=False, force_home_kdc=False, 
                        kdc=None,sn=None, d1=None, d2=None, ide=None, idex=None):
    """
    Performs a polarization-dependent PL measurement by sweeping a Thorlabs rotation mount,
    plotting total APD counts (d1 + d2) in real-time (optionally normalized), and optionally 
    moving to the best polarization angle if movetobest=True.
    """
    kdc_local = False
    sn_local = False
    actual_angles = []
    total_counts_list = []
    ch1_counts_list = []
    ch2_counts_list = []

    try:
        # === 1. Initialize Devices ===
        if kdc is None:
            kdc = start_kdc(force=force_home_kdc)
            if kdc is None: raise ConnectionError("Failed to start Thorlabs KDC motor.")
            kdc_local = True

        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

        # === 2. Setup Output Directory and Files ===
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        #folder_suffix = f"{f'_{ide}' if ide is not None else ''}{f'_{idex}' if idex is not None else ''}"
        #sub_folder_name = f"{timestamp}{folder_suffix}"
        #out_dir = os.path.join(out_dir_base, sub_folder_name)
        out_dir = output_dir_folder(base_dir=out_dir_base)
        os.makedirs(out_dir, exist_ok=True)

        data_file = os.path.join(out_dir, f'polarization_apd_data{f"_{ide}" if ide is not None else ""}_{timestamp}.txt')
        print(f'Saving polarization APD data to: {data_file}')

        # === 3. Real-Time Graphing Setup ===
        angles = np.arange(start_deg, end_deg + step_deg, step_deg)
        total_angles = len(angles)
        
        plt.ion() # Enable interactive mode for live plotting
        fig, ax = plt.subplots(figsize=(8, 5))
        line_tot, = ax.plot([], [], marker='o', color='purple', linewidth=1.5, label='Total Counts (Ch1 + Ch2)')
        
        ax.set_xlabel('Polarization Angle (Degrees)')
        
        if normalize_plot:
            ax.set_ylabel('Normalized Intensity (Arb. U.)')
        else:
            ax.set_ylabel('Count Rate (cps)')
            
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Live PL Polarization APD Counts | {timestamp}')
        ax.legend(loc='upper right')
        fig.tight_layout()

        print(f"\nStarting real-time polarization APD sweep ({total_angles} points)...")
        start_time = time.time()
        
        with open(data_file, 'w') as f:
            f.write(f"# PL Polarization APD Scan - {timestamp}\n")
            f.write(f"# Channel 1: {d1}, Channel 2: {d2}\n")
            f.write("# Angle_Req(deg)\tAngle_Act(deg)\tCh1_Counts\tCh2_Counts\tTotal_Counts\n")

            for idx, angle in enumerate(angles):
                # Move polarization stage
                kdc_move_deg(angle, kdc=kdc)
                
                # Read back actual position
                act_angle = kdc_position_deg(kdc=kdc)
                actual_angles.append(act_angle)

                # Read APD count rates
                time.sleep(1)  # Allow APDs to settle
                cnts = sn.getCountRates()
                c1 = int(cnts[d1]) if len(cnts) > d1 else 0
                c2 = int(cnts[d2]) if len(cnts) > d2 else 0
                tot = c1 + c2

                ch1_counts_list.append(c1)
                ch2_counts_list.append(c2)
                total_counts_list.append(tot)

                # Write point to file (ALWAYS RAW DATA)
                f.write(f"{angle:.2f}\t{act_angle:.2f}\t{c1}\t{c2}\t{tot}\n")
                f.flush()

                # === Update Live Plot ===
                if normalize_plot and len(total_counts_list) > 0:
                    max_tot = max(total_counts_list)
                    plot_data = [c / max_tot for c in total_counts_list] if max_tot > 0 else total_counts_list
                else:
                    plot_data = total_counts_list
                    
                line_tot.set_data(actual_angles, plot_data)
                
                ax.relim()
                ax.autoscale_view(True, True, True)
                fig.canvas.draw()
                fig.canvas.flush_events()

                # Progress & ETA calculation
                elapsed = time.time() - start_time
                rem_time = (elapsed / (idx + 1)) * (total_angles - (idx + 1))
                mins, secs = divmod(int(rem_time), 60)
                print(f"Progress: {idx+1}/{total_angles} | Angle: {act_angle:.1f}° | Total: {tot} cps | ETA: {mins}m {secs}s", end='\r')

        print("\nPolarization APD sweep complete.")

        # === 4. Find Best Angle & Move if Requested ===
        best_idx = np.argmax(total_counts_list)
        best_angle = actual_angles[best_idx]
        best_counts = total_counts_list[best_idx]
        print(f"Peak Polarization Found: {best_counts} cps at {best_angle:.1f}°")

        if movetobest:
            print(f"Moving KDC motor to peak polarization angle: {best_angle:.1f}°...")
            kdc_move_deg(best_angle, kdc=kdc)
            time.sleep(0.3)
            print(f"Current KDC position: {kdc_position_deg(kdc=kdc):.1f}°")

        # === 5. Finalize and Save Plot ===
        plt.ioff() # Disable interactive mode
        if show_plot and len(actual_angles) > 0:
            plot_file = os.path.join(out_dir, f'polarization_apd_plot{f"_{ide}" if ide is not None else ""}_{timestamp}.png')
            fig.savefig(plot_file)
            print(f"Summary plot saved to: {plot_file}")
            plt.show()
        else:
            plt.close(fig)

        return np.array(actual_angles), np.array(total_counts_list)

    except Exception as e:
        print(f"\nA critical error occurred during polarization scan: {e}")
        traceback.print_exc()
        return None, None
        
    finally:
        plt.ioff()
        print("\n--- Cleaning up polarization scan resources ---")
        if kdc_local and kdc:
            if not movetobest:
                kdc_move_deg(0,kdc=kdc)
            try:
                kdc.close()
                print("KDC motor closed.")
            except Exception:
                pass
        if sn_local and sn:
            try:
                close_device_all(sn=sn)
                print("APDs closed.")
            except Exception:
                pass
            
            
def run_pl_polarization_spectrum(start_deg=0, end_deg=360, step_deg=5, out_dir_base=r'D:\Data_Python_PL\Polarization',
                        show_plot=True, force_home_kdc=False, kdc=None, amc=None, 
                        camera=None, bg=True, vbg=None, ide=None, idex=None):
    """
    Performs a polarization-dependent PL measurement by sweeping a Thorlabs rotation mount 
    and recording a full spectrum at each angle using the camera/spectrometer.
    
    Args:
        start_deg (float): Starting angle in degrees.
        end_deg (float): Ending angle in degrees.
        step_deg (float): Angle increment step in degrees.
        detector_config (int): Detector configuration.
        out_dir_base (str): Base directory to save output data and plots.
        show_plot (bool): If True, displays the plot after completion.
        force_home_kdc (bool): If True, passes force=True to start_kdc.
        kdc, amc, camera: Externally managed device handles (optional).
        bg (bool): If True, takes background subtraction before scanning.
        vbg (tuple): Pre-acquired background data.
        ide, idex: Optional identifiers used in folder and filenames.
        
    Returns:
        tuple: (actual_angles, all_spectra) arrays/lists.
    """
    kdc_local = False
    amc_local = False

    try:
        # === Initialize Devices ===
        if kdc is None:
            kdc = start_kdc(force=force_home_kdc)
            if kdc is None: raise ConnectionError("Failed to start Thorlabs KDC motor.")
            kdc_local = True

        if amc is None:
            try:
                amc = start_attocube()
                amc_local = True
            except NameError:
                pass

        if camera is None:
            print("No Camera provided.")
            return None, None

        # === Setup Output Directory and Subfolder with Timestamp and Identifiers ===
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        folder_suffix = f"{f'_{ide}' if ide is not None else ''}{f'_{idex}' if idex is not None else ''}"
        sub_folder_name = f"{timestamp}{folder_suffix}"
        out_dir = os.path.join(out_dir_base, sub_folder_name)
        os.makedirs(out_dir, exist_ok=True)

        print(f'Saving polarization spectra to directory: {out_dir}')

        # === Optional Background Acquisition ===
        if bg and vbg is None:
            try:
                set(camera.shutter, False)
                time.sleep(1)
                data_file_bg = os.path.join(out_dir, f'spectrum_data_BG{folder_suffix}_{timestamp}.txt')
                print("Taking BG...")
                print(f"Using Filename : {data_file_bg}")
                vbg = get(camera.readval, filename=data_file_bg)
                set(camera.shutter, True)
                time.sleep(1)
            except Exception as e:
                print(f"Warning: Could not take background automatically: {e}")
                vbg = None

        angles = np.arange(start_deg, end_deg + step_deg, step_deg)
        actual_angles = []
        all_spectra = []

        print("\nStarting polarization spectrum sweep...")
        for angle in angles:
            # Move polarization stage
            kdc_move_deg(angle, kdc=kdc)
            time.sleep(0.2)  # Allow stage to settle
            
            # Read back actual position
            act_angle = kdc_position_deg(kdc=kdc)
            actual_angles.append(act_angle)

            # Construct filename including the KDC position degree
            deg_str = f"deg_{act_angle:.1f}".replace('.', '_')
            data_file = os.path.join(out_dir, f'spectrum_data{folder_suffix}_{deg_str}_{timestamp}.txt')

            # Take spectrum using camera logic
            # if bg and vbg is not None and len(vbg) > 1:
            #     print(f"Taking Spectrum at {act_angle:.1f}°...")
            #     v = get(camera.readval, bkg_rem=vbg[1], filename=data_file)
            # else:
            print(f"Taking Spectrum at {act_angle:.1f}°...")
            v = get(camera.readval, filename=data_file)

            all_spectra.append(v)

        print("\nPolarization spectrum sweep complete.")

        # === Plot Results ===
        if show_plot:
            fig, ax = plt.subplots(figsize=(8, 6))
            for i, (ang, v) in enumerate(zip(actual_angles, all_spectra)):
                ax.plot(v[0], v[1], label=f'{ang:.1f}°')
            
            ax.set_xlim(np.min(all_spectra[0][0]), np.max(all_spectra[0][0]))
            ax.set_xlabel('Wavelength (nm)')
            ax.set_ylabel('Counts (Arb.)')
            ax.grid(True)
            ax.set_title(f'PL Polarization Spectra | {timestamp}')
            
            if len(angles) <= 12:
                ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
                
            plt.tight_layout()
            plot_file = os.path.join(out_dir, f'polarization_summary_plot_{timestamp}.png')
            plt.savefig(plot_file)
            print(f"Summary plot saved to: {plot_file}")
            plt.show()
        else:
            plt.close('all')

        return np.array(actual_angles), all_spectra

    except Exception as e:
        print(f"\nA critical error occurred during polarization scan: {e}")
        return None, None
    finally:
        print("\n--- Cleaning up polarization scan resources ---")
        if kdc_local and kdc:
            kdc_move_deg(0,kdc=kdc)
            try:
                kdc.close()
                print("KDC motor closed.")
            except Exception:
                pass
        if amc_local and amc:
            try:
                close_device_all(amc=amc)
            except Exception:
                pass

def set_spectrum(
    camera=None,
    spectro=None,
    wl=None,
    grating=2,
    exposure_time=5,
    acq_mode="accumulate",
    acc_N=2,
    cosmic_filter=True,
):
  if spectro is not None and wl is not None:
    set(spectro.active_grating, int(grating))
    set(spectro.wavelength_nm, int(wl))
    minw = int(get(spectro.sensor_wavelengths_nm)[0])
    maxw = int(get(spectro.sensor_wavelengths_nm)[-1])
    print(f"Current wavelength range : {minw}nm to {maxw}nm")

  # Configure camera settings if provided
  if camera is not None:
    conf_args = {
        "read_mode": "full_vertical_binning",
        "exposure_time": exposure_time,
        "acq_mode": acq_mode,
    }
    if acq_mode == "accumulate" and acc_N is not None:
      conf_args["acc_N"] = acc_N

    camera.conf(**conf_args)
    set(camera.cosmic_filter_en, cosmic_filter)
    print(camera.conf())

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

def cryo_waitforstable(cryo=None, poll_interval=2):
    cryo = start_cryo(cryo=cryo)
    if not cryo: return
    print(f"Waiting for platform temperature to stabalize...")
    while True:
        current_temp = cryo_get_temp_p1(cryo)
        if cryo.get_system_state() == 'StableAtTarget' :
            print(f"Platform reached stability temperature: {current_temp:.2f} K")
            break
        time.sleep(poll_interval)



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


# === FIX FOR FORTRAN/MKL CTRL+C CRASH ===
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

# Assuming the SDK is in your active environment or working directory
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
from thorlabs_tsi_sdk.tl_camera_enums import OPERATION_MODE

def get_peak_intensity_fast(image_array):
    """Checks the absolute single-pixel maximum on the raw grayscale array."""
    max_val = float(np.max(image_array))
    max_coords = np.unravel_index(np.argmax(image_array), image_array.shape)
    return max_val, max_coords

def run_camera_focus_sweep(center_f=None, f_size=50, step=0.1,
                           camera_serial="11484", ide=None, exposure_ms=200, 
                           out_dir=r'D:\Data_Python_PL\Camera',
                           move_to_best=True, amc=None):
    
    if amc is None:
        try:
            amc = start_attocube()
            amc_local = True
        except NameError:
            pass

    exposure_us = int(float(exposure_ms) * 1000) 
    aborted = False
    data_file_handle = None
    points_collected = 0
    
    # Trackers for dropped frames
    last_valid_intensity = 0.0
    last_valid_image = np.zeros((1080, 1440), dtype=np.uint16)
    last_coords = (0, 0)
    
    # 1. Establish Initial Positions
    fnow = center_f if center_f is not None else float(amc.move.getPosition(1)) / 1000.0
    best_f = fnow
    max_int = -1

    # 2. Setup Output Files
    os.makedirs(out_dir, exist_ok=True)
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    plot_file = os.path.join(out_dir, f'cam_focus_plot_{timestamp}.png')
    data_file = os.path.join(out_dir, f'cam_focus_data_{timestamp}.txt')

    data_file_handle = open(data_file, 'w')
    data_file_handle.write(f'# Camera Focus Sweep - {timestamp}\n# Initial Center F: {fnow:.3f}\n')
    data_file_handle.write('# f_req\tf_act\tintensity\tmax_y\tmax_x\n')

    # 3. Setup High-Speed GUI
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    f_start, f_end = fnow - (f_size / 2), fnow + (f_size / 2)
    f_pos = np.arange(f_start, f_end + step, step)
    
    # Initialize with all zeros
    intensity_data = np.zeros(len(f_pos), dtype=float)
    
    line1, = ax1.plot(f_pos, intensity_data, 'b-o', markersize=4)
    ax1.set_xlabel('Z Position (µm)')
    ax1.set_ylabel('Peak Intensity')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # cmap='inferno' provides the color mapping for the live view
    img_display = ax2.imshow(last_valid_image, cmap='inferno', vmin=0, vmax=65535)
    ax2.axis('off')
    fig.tight_layout()

    try:
        with TLCameraSDK() as sdk:
            cameras = sdk.discover_available_cameras()
            target_serial = next((cam for cam in cameras if camera_serial in cam), cameras[0])
            
            with sdk.open_camera(target_serial) as camera:
                camera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
                camera.exposure_time_us = exposure_us
                camera.frames_per_trigger_zero_for_unlimited = 1
                
                # Clear stale hardware buffer
                camera.arm(1)
                camera.issue_software_trigger()
                time.sleep(0.1)
                _ = camera.get_pending_frame_or_null()
                camera.disarm()

                print(f"--- Starting Sweep ({f_start:.2f} µm to {f_end:.2f} µm) ---")

                for i, target_z in enumerate(f_pos):
                    if not plt.fignum_exists(fig.number):
                        print("\nPlot closed by user. Aborting!")
                        aborted = True
                        break

                    # Move Stage
                    amc.move.setControlTargetPosition(1, int(float(target_z) * 1000))
                    time.sleep(0.1) 
                    
                    f_act = float(amc.move.getPosition(1)) / 1000.0

                    # Capture Frame
                    camera.arm(1)
                    camera.issue_software_trigger()
                    
                    frame = None
                    attempts = 0
                    while frame is None and attempts < 20: 
                        time.sleep(0.02)
                        frame = camera.get_pending_frame_or_null()
                        attempts += 1
                        
                    camera.disarm()
                        
                    # Handle Frame Data (Fallback to last valid if dropped)
                    if frame is not None:
                        image_array = np.asarray(frame.image_buffer)
                        intensity, coords = get_peak_intensity_fast(image_array)
                        
                        # Cache for future dropped frames
                        last_valid_intensity = intensity
                        last_valid_image = image_array
                        last_coords = coords
                    else:
                        print(f"\nWarning: Frame dropped at Z={f_act:.2f}. Reusing last value.")
                        intensity = last_valid_intensity
                        image_array = last_valid_image
                        coords = last_coords

                    max_y, max_x = coords
                    intensity_data[i] = intensity
                    
                    if intensity > max_int:
                        max_int, best_f = intensity, f_act

                    # Write Data
                    data_file_handle.write(f'{target_z:.3f}\t{f_act:.3f}\t{intensity:.2f}\t{max_y}\t{max_x}\n')
                    data_file_handle.flush()
                    points_collected += 1

                    # --- PURE MATPLOTLIB UPDATE BLOCK ---
                    line1.set_ydata(intensity_data)
                    ax1.relim()
                    ax1.autoscale_view()
                    
                    # Update image data; cmap handles the coloring automatically
                    img_display.set_data(image_array)
                    
                    vmax_val = int(intensity) if intensity > 10 else 10
                    img_display.set_clim(vmin=0, vmax=vmax_val)
                    ax1.set_title(f'Max: {max_int:.0f} @ {best_f:.2f} µm')
                    
                    # Force GUI update
                    plt.pause(0.01)
                    # ------------------------------------
                        
                    print(f'Scan: {i+1}/{len(f_pos)} | Z: {f_act:.2f} | Peak: {intensity:.0f}', end='\r')

        print("\nSweep Complete.")

    except KeyboardInterrupt:
        print("\nSweep interrupted by user.")
        aborted = True
    except Exception as e:
        print("\n--- CRITICAL ERROR TRACEBACK ---")
        traceback.print_exc()
        print("--------------------------------")
        aborted = True
    finally:
        plt.ioff()
        if data_file_handle:
            data_file_handle.close()
            
        if amc is not None:
            park_pos = fnow if aborted else (best_f if move_to_best else fnow)
            print(f"Parking stage at {park_pos:.2f} µm...")
            try:
                amc.move.setControlTargetPosition(1, int(float(park_pos) * 1000))
            except Exception as e:
                print(f"Failed to park stage: {e}")
            if amc_local and amc:
                try:
                    close_device_all(amc=amc)
                except Exception:
                    pass
                
        if points_collected > 0 and plt.fignum_exists(fig.number):
            plt.savefig(plot_file)
            print(f"Data saved to: {out_dir}")
            
        plt.show()

def run_live_camera(camera_serial="11484", exposure_ms=10):
    exposure_us = int(float(exposure_ms) * 1000)
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 1. Pre-allocate display memory with a dummy 2D array
    # Using 'inferno' provides the false-color view for the laser spot
    dummy_img = np.zeros((1080, 1440), dtype=np.uint16)
    img_display = ax.imshow(dummy_img, cmap='inferno', vmin=0, vmax=65535)
    ax.set_title("Live Camera Feed")
    ax.axis('off')
    fig.tight_layout()
    
    try:
        with TLCameraSDK() as sdk:
            available_cameras = sdk.discover_available_cameras()
            if not available_cameras:
                raise ConnectionError("No Thorlabs cameras found!")
            
            target_serial = next((cam for cam in available_cameras if camera_serial in cam), available_cameras[0])
            
            with sdk.open_camera(target_serial) as camera:
                camera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
                camera.exposure_time_us = exposure_us
                camera.frames_per_trigger_zero_for_unlimited = 1
                
                # Clear stale hardware buffer
                camera.arm(1)
                camera.issue_software_trigger()
                time.sleep(0.1)
                _ = camera.get_pending_frame_or_null()
                camera.disarm()
                
                print(f"\n[LIVE FEED ACTIVE] Using camera: {target_serial}")
                print(">>> CLOSE THE PLOT WINDOW OR PRESS 'CTRL+C' TO EXIT <<<")
                
                while plt.fignum_exists(fig.number):
                    camera.arm(1)
                    camera.issue_software_trigger()
                    
                    frame = None
                    attempts = 0
                    
                    # BYPASS HIJACKED MAX()
                    sleep_time = exposure_ms / 1000.0 / 5.0
                    actual_sleep = sleep_time if sleep_time > 0.01 else 0.01
                    
                    while frame is None and attempts < 20:
                        time.sleep(actual_sleep) 
                        frame = camera.get_pending_frame_or_null()
                        attempts += 1
                        
                    camera.disarm()
                    
                    if frame is not None:
                        # Extract the raw 2D grayscale array
                        image_array = np.asarray(frame.image_buffer)
                        
                        # Find the peak intensity
                        peak_val = float(np.max(image_array))
                        
                        # 2. Update display data in memory (Fast)
                        img_display.set_data(image_array)
                        
                        # 3. Safe integer cast for Matplotlib limits
                        vmax_val = int(peak_val) if peak_val > 10 else 10
                        img_display.set_clim(vmin=0, vmax=vmax_val)
                        
                        ax.set_title(f"Live Camera Feed | Peak: {peak_val:.0f}")
                        
                        # 4. Pure Matplotlib safe refresh
                        plt.pause(0.01)
                        
    except KeyboardInterrupt:
        print("\nLive feed stopped by user.")
    except Exception as e:
        import traceback
        print("\n--- CRITICAL ERROR TRACEBACK ---")
        traceback.print_exc()
        print("--------------------------------")
    finally:
        plt.ioff()
        plt.close('all')
        print("Camera disconnected and plot closed.")