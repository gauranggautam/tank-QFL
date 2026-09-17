# %%
from pyHegel import start_pyHegel
start_pyHegel()
import os
import re
import sys
import time
import traceback
import builtins
import serial
from datetime import datetime
from io import StringIO

# === Fix for FORTRAN/MKL CTRL+C Crash ===
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

# === Third-party ===
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
import pyvisa

# === PyHegel Setup ===
from pyHegel import start_pyHegel
start_pyHegel()

# === Matplotlib Configuration ===
plt.style.use('dark_background')
TAB20_COLORS = plt.colormaps['tab20'].colors
uhd_plots = False

# === Hardware-Specific Imports ===
try: from attocube import AMC
except ImportError as e: print(f"Attocube error: {e}")

try: from snAPI.Main import *
except ImportError as e: print(f"snAPI error: {e}")

try: import nidaqmx; from nidaqmx.constants import Edge
except ImportError as e: print(f"nidaqmx error: {e}")

try: import labview_buttons_v2 as lv
except ImportError as e: print(f"LabVIEW buttons error: {e}")

try: from pylablib.devices import Thorlabs
except ImportError as e: print(f"Thorlabs error: {e}")

try: from montana import cryocore
except ImportError as e: print(f"Montana error: {e}")

# === Camera Path Setup ===
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

try:
    import windows_setup
    windows_setup.configure_path()
    from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
except ImportError as e:
    print(f"Thorlabs Camera SDK error: {e}")

# ==========================================
# PLOTTING & UI HELPERS
# ==========================================

def set_4k():
    global uhd_plots
    mpl.rcParams['figure.dpi'] = 200
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['figure.figsize'] = [10, 6]
    mpl.rcParams['font.size'] = 14
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['lines.markersize'] = 6
    mpl.rcParams['axes.titlesize'] = 16
    mpl.rcParams['axes.labelsize'] = 14
    mpl.rcParams['xtick.labelsize'] = 12
    mpl.rcParams['ytick.labelsize'] = 12
    mpl.rcParams['legend.fontsize'] = 12
    uhd_plots = True

def set_size_poster(size=45):
    sz_small = size - 10
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = sz_small
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = size
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = sz_small
    plt.rcParams['legend.fontsize'] = sz_small - 10
    plt.rcParams['xtick.labelsize'] = sz_small
    plt.rcParams['ytick.labelsize'] = sz_small

def add_stop_button(fig, running_flag):
    def stop_loop(event):
        print("Stop button clicked. Halting loop.")
        running_flag[0] = False
    button_ax = fig.add_axes([0.8, 0.01, 0.1, 0.05])
    stop_button = Button(button_ax, 'Stop')
    stop_button.on_clicked(stop_loop)
    return stop_button

def output_dir_folder(base_dir=r'D:\Data_Python_PL'):
    datestamp = time.strftime('%Y_%m_%d')
    output_dir_base = os.path.join(base_dir, datestamp)
    os.makedirs(output_dir_base, exist_ok=True)
    return output_dir_base

# ==========================================
# DEVICE INITIALIZATION & CLEANUP
# ==========================================

def close_device_all(sn=None, amc=None, showcmd=True, daq=None, t_ch1=None, t_ch2=None, spectro=None, camera=None):
    try:
        if amc:
            amc.close()
            if showcmd: print("AMC closed.")
        if sn:
            sn.closeDevice(allDevices=True)
            sn.exitAPI()
            time.sleep(3)
            if showcmd: print("MH150 closed.")
        if daq:
            if t_ch1: t_ch1.stop()
            if t_ch2: t_ch2.stop()
            if showcmd: print("DAQ closed.") 
        if camera is not None:
            unload(camera)
        if spectro is not None:
            unload(spectro)
    except Exception as e:
        print(f"Nothing to close or error during close: {e}")
        return None

def start_attocube(amc_address='amc100num-a01-0248.local'):
    amc = None
    try:
        amc = AMC.Device(amc_address)
        amc.connect()
        for axis in [0, 1, 2]:
            amc.control.setControlOutput(axis, True)
            amc.control.setControlMove(axis, True)
        print(f"Using AMC : {amc_address}")
        return amc
    except Exception as e:
        print(f"ERROR: Failed to connect or initialize AMC controller: {e}")
        if amc: amc.close()
        return None

def start_apds(detector_config=2, read_counts=False, graph_counts=False):
    config_path_1_det = r'C:\Codes\Picoquant\user_configs_snAPI\Exciletas_MH.ini'
    config_path_2_det = r'C:\Codes\Picoquant\user_configs_snAPI\MPDs_MH.ini'
    config_path_3_det = r'C:\Codes\Picoquant\user_configs_snAPI\MPDs_MH_TRPL.ini'

    sn = None
    try:
        sn = snAPI()
        sn.getDevice("1043897")
        if not sn.initDevice():
            raise ConnectionError('MH150 device initialization failed.')

        if detector_config == 1:
            d1, d2 = 1, 2
            sn.loadIniConfig(config_path_1_det)
            print(f'Using Exciletas: {sn.deviceConfig["ID"]}')
        elif detector_config == 3:
            d0, d1, d2 = 0, 1, 2
            sn.loadIniConfig(config_path_3_det)
            print(f'Using Exciletas TRPL: {sn.deviceConfig["ID"]}')
        else: 
            d1, d2 = 3, 4
            sn.loadIniConfig(config_path_2_det)
            print(f'Using MPDs: {sn.deviceConfig["ID"]}')

        if read_counts:
            print("Current count rates:", sn.getCountRates())

        if graph_counts:
            print("Starting live count graph... Press Ctrl+C to exit.")
            fig = None
            try:
                start_time = time.time()
                times, counts1, counts2, totals = [], [], [], []
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
                    c1, c2 = int(cnt[d1]), int(cnt[d2])
                    total = c1 + c2
                    times.append(time.time() - start_time)
                    counts1.append(c1)
                    counts2.append(c2)
                    totals.append(total)

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
                return None, None, None

        if detector_config == 3:
            return sn, d0, d1, d2
        else:
            return sn, d1, d2

    except Exception as e:
        print(f"An error occurred in start_apds: {e}")
        if sn is not None:
             close_device_all(sn=sn)
        return None, None, None

def start_daq(device='Dev1', ch1='PFI8', ch2='PFI9'):
    PFI_CH1 = f"/{device}/{ch1}"
    PFI_CH2 = f"/{device}/{ch2}"
    daq = nidaqmx
    
    t_ch1 = daq.Task()
    t_ch1.ci_channels.add_ci_count_edges_chan(
        counter=f"{device}/ctr0",
        edge=Edge.RISING,
        initial_count=0
    )
    t_ch1.ci_channels.all.ci_count_edges_term = PFI_CH1
    
    t_ch2 = daq.Task()
    t_ch2.ci_channels.add_ci_count_edges_chan(
        counter=f"{device}/ctr1",
        edge=Edge.RISING,
        initial_count=0
    )
    t_ch2.ci_channels.all.ci_count_edges_term = PFI_CH2
    
    print('Using MPD with DAQ')
    return daq, t_ch1, t_ch2

def start_kdc(SN="27257399", kdc=None, force=False):
    if kdc is not None:
        return kdc
    else:
        try:
            kdc = Thorlabs.KinesisMotor(SN)
            kdc.open()
            if force:
                print(f"Homing KDC motor SN: {SN}...")
                kdc.home(force=True, sync=False) 
                time.sleep(0.2) 
                try:
                    while kdc.is_moving():
                        curr_deg = kdc.get_position() / 1919.6418578623391
                        print(f"Homing... Current Position: {curr_deg:.2f}°", end='\r')
                        time.sleep(0.05)
                    print("\nHoming complete.")
                except Exception:
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

def start_spectro(spectro_set_cw=484, shutter_init=True, waitfortemp=True, showrange=True):
    spectro = instruments.andor_kymera()
    set(spectro.wavelength_nm, spectro_set_cw)
    time.sleep(5)
    camera = instruments.andor_iDus(spectro_instr=spectro, cooler_temp=-80, shutter_init=shutter_init)
    camera.conf(read_mode='full_vertical_binning', exposure_time=5, acq_mode="accumulate", acc_N=2)
    set(camera.cosmic_filter_en, True)
    if waitfortemp:
        camera.wait_for_cooler_stable(-80)
    minw = int(get(spectro.sensor_wavelengths_nm)[0])
    maxw = int(get(spectro.sensor_wavelengths_nm)[-1])
    if showrange:
        print(f"Current wavelength range : {minw}nm to {maxw}nm")
    return spectro, camera        

def close_spectro(spectro=None, camera=None):
    if camera is not None: unload(camera)
    if spectro is not None: unload(spectro)

# ==========================================
# HARDWARE CONTROL (SERIAL, SWITCHES, MOTORS)
# ==========================================

def amc_disable():
    amc = start_attocube()
    for axis in [0, 1, 2]:
        amc.control.setControlMove(axis, False)
        print(f"Disabled: Axis {axis}")
    amc.close()

def wait_until_stable(amc_dev, axis):
    timeout = 10
    start = time.time()
    while True:
        if amc_dev.status.getStatusMoving(axis) == 0 and amc_dev.status.getStatusTargetRange(axis):
            break
        amc_dev.control.setControlOutput(axis, True)
        amc_dev.control.setControlMove(axis, True)
        if time.time() - start > timeout:
            print(f"Timeout waiting for stage axis {axis}")
            break
        time.sleep(0.01)

def amc_move(amc=None, axis=None, d=None):
    if amc is None: amc = start_attocube()
    amc.move.setControlTargetPosition(axis, int(d * 1000)); wait_until_stable(amc, axis)

def amc_movexyz(x, y, f, amc=None):
    if amc is None: amc = start_attocube()
    amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, 0)
    amc.move.setControlTargetPosition(1, int(f * 1000)); wait_until_stable(amc, 1)
    amc.move.setControlTargetPosition(2, int(y * 1000)); wait_until_stable(amc, 2)       

def getposall():
    amc = start_attocube()
    print(f"x = {amc.move.getPosition(0) / 1000}")
    print(f"y = {amc.move.getPosition(2) / 1000}")
    print(f"f = {amc.move.getPosition(1) / 1000}")  
    close_device_all(amc=amc)

def gohome(amc=None):
    if amc is None: amc = start_attocube()
    for ax in [0, 1, 2]:
        amc_move(amc=amc, axis=ax, d=0)
    getposall()

def wobble(size=2, speed=1, fbase=None):
    amc = start_attocube()
    if fbase is not None:
        f_now = fbase
    else:
        f_now = amc.move.getPosition(1) / 1000
    print(f"wobble around = {f_now}")
    wobble_range = np.arange(f_now - size, f_now + size, speed)
    rev_wobble_range = np.arange(f_now + size, f_now - size, -speed)

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
        try: kdc.close()
        except Exception: pass
    return current_deg

def kdc_move_deg(deg, kdc=None, showcmd=True):
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
        while getattr(kdc, 'is_moving', False):
            if showcmd:
                curr_deg = kdc.get_position() / 1919.6418578623391
                print(f"Moving... Current Angle: {curr_deg:.2f}° (Target: {deg:.2f}°)", end='\r')
            time.sleep(0.05)
        if showcmd:
            final_deg = kdc.get_position() / 1919.6418578623391
            print(f"\nMovement complete. Final Angle: {final_deg:.2f}°")

    if kdc_local and kdc:
        try: kdc.close()
        except Exception: pass

def detector_switch(moveto='camera', ESP_address="GPIB1::7::INSTR", showcmd=False):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    
    targets = {'apd': "3PA0", 'spectro': "3PA-49", 'camera': "3PA47.5"}
    names = {'apd': "0mm for APDs", 'spectro': "-49mm for Spectrometer", 'camera': "47.5mm for Camera"}
    
    if moveto in targets:
        try:
            if showcmd: print(f"Detection axis moving to {names[moveto]}")
            esp.write(targets[moveto])
            time.sleep(5)
            pos_now = esp.query("3TP?")
            if showcmd: print("Detection axis Position:", pos_now.strip(), "mm")
        except: return None
    return esp

def filter_switch(moveto, ESP_address="GPIB1::7::INSTR", showcmd=False):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    
    targets = {'no': "2PA-24", 'n405': "2PA0", 'n533': "2PA25"}
    names = {'no': "-24mm for No Filter", 'n405': "0mm for Notch 405nm", 'n533': "25mm for Notch 533nm"}
    
    if moveto in targets:
        try:
            if showcmd: print(f"Filter axis moving to {names[moveto]}")
            esp.write(targets[moveto])
            time.sleep(5)
            pos_now = esp.query("2TP?")
            if showcmd: print("Filter axis Position:", pos_now.strip(), "mm")
        except: return None
    return esp

def send_cmd(drive, command):
    drive.write(f"{command}\r".encode('ascii'))
    return drive.read_until(b'\r').decode('ascii').strip()

def Power_apds(drive, state):
    send_cmd(drive, "IL1" if state else "IH1")

def power_whitelight(drive, state):
    send_cmd(drive, "IL1") 
    if state:
        time.sleep(1) 
        send_cmd(drive, "IL2")
    else:
        send_cmd(drive, "IH2")

def seek_home_precise(drive):
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
    if slot < 0 or slot > 14: return
    target_steps = int(-(slot + offset) * 1400)
    
    try:
        with serial.Serial(port='COM4', baudrate=38400, timeout=1) as drive:
            power_whitelight(drive, False)
            Power_apds(drive, False)
            
            if home_first:
                seek_home_precise(drive)

            send_cmd(drive, "VE1.0") 
            send_cmd(drive, f"FP{target_steps}")
            
            time.sleep(0.2)
            while True:
                if "0009" in send_cmd(drive, "SC"): break
                time.sleep(0.05)
            
            Power_apds(drive, apd_final_state)
            if not apd_final_state:
                power_whitelight(drive, wlight_final_state)
                
    except serial.SerialException:
        pass

def set_detection(state, Homefirst=False, apd_final_state=False, wlight_final_state=False, offset=11.224):
    if state == "camera":
        filterwheel(0, offset=offset, home_first=Homefirst, apd_final_state=apd_final_state, wlight_final_state=wlight_final_state)
        filter_switch(moveto="no")
        detector_switch(moveto="camera")
    elif state == "apd":
        filterwheel(10, offset=offset, home_first=Homefirst, apd_final_state=apd_final_state, wlight_final_state=False)
        filter_switch(moveto="n405")
        detector_switch(moveto="apd")
    elif state == "spectro":
        filterwheel(1, offset=offset, home_first=Homefirst, apd_final_state=apd_final_state, wlight_final_state=False)
        filter_switch(moveto="n405")
        detector_switch(moveto="spectro")

def set_laser(power, laser=None, cw=True, softlock=None, engaged=False, close=False, read_power=False):
    if laser is None:
        laser = instruments.picoQuant.PicoQuant_Taiko_PDL_M1()
    if power is not None:
        print(f"\nSetting CW power to {power}%...")
        pwr = power * 10
        set(laser.cw_power_permille, int(pwr))
        print(f"CW power is now: {power}%")
    if softlock is not None:
        set(laser.softlock_en, softlock)
        print(f"Laser softlock state : {get(laser.softlock_en)}.")
    if cw:
        set(laser.laser_mode, "cw")    
    return laser

# ==========================================
# CRYOSTAT CONTROL
# ==========================================

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
    print("Waiting for platform temperature to stabalize...")
    while True:
        current_temp = cryo_get_temp_p1(cryo)
        if cryo.get_system_state() == 'StableAtTarget':
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


# ==========================================
# SCANS, SWEEPS & MEASUREMENTS
# ==========================================

def run_focus_sweep(fbase=None, fstep=0.1, fsize=30, movetobest=True, showplt=True, engaged=False, 
                    sn=None, d1=None, d2=None, amc=None, detector_config=2,
                    out_dir_base=r'D:\Data_Python_PL\FocusSweeps'):
    """
    Performs a Z-axis sweep to find the optimal focus.
    Saves the data and plot to a file.
    """
    amc_local = sn_local = False
    data_file_handle = None
    fnow = fbase

    try:
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

        if fbase is None:
            fnow = amc.move.getPosition(1) / 1000
        else:
            fnow = fbase
            
        fstart, fend = fnow - (fsize / 2), fnow + (fsize / 2)
        frange = np.arange(fstart, fend + fstep, fstep)
        focus, totals, ch1s, ch2s = [], [], [], []
        maxc, bestf = -1, fnow

        out_dir = output_dir_folder(base_dir=out_dir_base)
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        data_file = os.path.join(out_dir, f'focus_sweep_{timestamp}.txt')
        plot_file = os.path.join(out_dir, f'focus_sweep_{timestamp}.png')
        
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# APD Focus Sweep - {timestamp}\n')
        data_file_handle.write(f'# Base Focus: {fnow:.2f}, Size: {fsize}, Step: {fstep}\n')
        data_file_handle.write('Focus(um)\tCh1(cps)\tCh2(cps)\tTotal(cps)\n')

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
            
            focus.append(f); ch1s.append(ch1); ch2s.append(ch2); totals.append(total)

            if total > maxc:
                bestf, maxc = f, total
                
            data_file_handle.write(f'{f:.3f}\t{ch1}\t{ch2}\t{total}\n')

            line_ch1.set_data(focus, ch1s)
            line_ch2.set_data(focus, ch2s)
            line_total.set_data(focus, totals)
            ax.set_title(f'Focus Sweep | Best F: {bestf:.2f} µm')
            ax.relim(); ax.autoscale_view(True, True, True)
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
        print(f"Keyboard interrupt : {k}\nMoving to initial position ---")
        amc.move.setControlTargetPosition(1, int(fnow * 1000)); wait_until_stable(amc, 1)
        return fnow
    finally:
        if data_file_handle: data_file_handle.close()
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)
        
def run_pl_scan(center_x=None, center_y=None, center_f=None,
                focus_sweep=False, f_size=50,
                x_size=5, y_size=5, step=0.1,
                detector_config=2,
                logz=False,
                out_dir_base=r'D:\Data_Python_PL\PLmaps',
                show_plot=True, waits=0,
                amc=None, sn=None, d1=None, d2=None):
    amc_local = sn_local = False
    data_file_handle = None

    try:
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

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

        max_int, best_x, best_y = -1, x_start, y_start
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()

        amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(y_start * 1000)); wait_until_stable(amc, axis=2)

        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)); wait_until_stable(amc, axis=2)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1]

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
        print(f"Keyboard interrupt : {k}\nMoving to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(center_y * 1000)); wait_until_stable(amc, axis=2)
        return None, None, None    
    finally:
        print("\n--- Cleaning up PL scan resources ---")
        if data_file_handle:
            data_file_handle.close(); print("Data file closed.")
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)

    return best_x, best_y, center_f

def run_edge_sweep(center_x=None, center_f=None, f_size=5,
                x_size=5, step=1, detector_config=2, logz=False,
                out_dir_base=r'D:\Data_Python_PL\PLmaps',
                show_plot=True, amc=None, sn=None, d1=None, d2=None):
    amc_local = sn_local = False
    data_file_handle = None

    try:
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
        center_f = fnow 

        x_start, x_end = center_x - (x_size / 2), center_x + (x_size / 2)
        f_start, f_end = center_f - (f_size / 2), center_f + (f_size / 2)
        out_dir = output_dir_folder(base_dir=out_dir_base)

        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(center_f * 1000)); wait_until_stable(amc, axis=1)
        
        print(f"Initial pos (x,f) :  ({center_x:.2f}, {center_f:.2f}) µm")
        
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

        max_int, best_x, best_y = -1, x_start, f_start
        total_points = len(x_pos) * len(f_pos)
        point_counter = 0
        start_time = time.time()

        amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(f_start * 1000)); wait_until_stable(amc, axis=1)

        for i, y in enumerate(f_pos):
            amc.move.setControlTargetPosition(1, int(y * 1000)); wait_until_stable(amc, axis=1)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1] 

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, axis=0)

                x_act, f_act = amc.move.getPosition(0)/1000, amc.move.getPosition(1)/1000
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]

                Z[i, j] = np.log10(total + 1) if logz else total

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
        print(f"Keyboard interrupt : {k}\nMoving to initial position ---")
        amc.move.setControlTargetPosition(0, int(center_x * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(1, int(center_f * 1000)); wait_until_stable(amc, axis=1)
        return None, None, None    
    finally:
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
    amc_local = daq_local = False
    data_file_handle = None

    try:
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if daq is None or ch1 is None or ch2 is None:
            daq, ch1, ch2 = start_daq()
            if daq is None: raise ConnectionError("Failed to start DAQ-APDs.")
            daq_local = True

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
        
        center_f = fnow 
        print(f"Initial pos (x,y,z) :  ({center_x:.2f}, {center_y:.2f}, {center_f:.2f}) µm")
        
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

        max_int, best_x, best_y = -1, x_start, y_start
        total_points = len(x_pos) * len(y_pos)
        point_counter = 0
        start_time = time.time()

        amc.move.setControlTargetPosition(0, int(x_start * 1000)); wait_until_stable(amc, axis=0)
        amc.move.setControlTargetPosition(2, int(y_start * 1000)); wait_until_stable(amc, axis=2)
        ch1.start()
        ch2.start()

        pr1 = ch1.read()
        pr2 = ch2.read()
        
        for i, y in enumerate(y_pos):
            amc.move.setControlTargetPosition(2, int(y * 1000)); wait_until_stable(amc, axis=2)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1] 

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                amc.move.setControlTargetPosition(0, int(x * 1000)); wait_until_stable(amc, axis=0)

                x_act, y_act = amc.move.getPosition(0)/1000, amc.move.getPosition(2)/1000
                pr1, pr2 = ch1.read(), ch2.read()
                time.sleep(t_acq)
                cnt1, cnt2 = ch1.read(), ch2.read()
                cnt1_n = cnt1 - pr1
                cnt2_n = cnt2 - pr2
                total = cnt1_n + cnt2_n

                Z[i, j] = np.log10(total + 1) if logz else total

                if total > max_int:
                    max_int, best_x, best_y = total, x_act, y_act

                data_file_handle.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt1_n}\t{cnt2_n}\t{total}\n')

                point_counter += 1
                elapsed = time.time() - start_time
                rem_time = (elapsed / point_counter) * (total_points - point_counter)
                mins, secs = divmod(int(rem_time), 60)
                print(f'Scan: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')

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
        print("\n--- Cleaning up PL scan resources ---")
        if data_file_handle:
            data_file_handle.close(); print("Data file closed.")
        if daq_local and daq: close_device_all(daq=daq, t_ch1=ch1, t_ch2=ch2)
        if amc_local and amc: close_device_all(amc=amc)

    return best_x, best_y, center_f

def multi_run_plscan():
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
                            sn=None, d1=None, d2=None, amc=None, detector_config=2):
    sn_local = amc_local = False
    bx, by, bf = None, None, None

    try:
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
        
        bx, by, bf = run_pl_scan(
            center_x=x_now, center_y=y_now, center_f=f_now,
            x_size=scan_size, y_size=scan_size, step=scan_step,
            focus_sweep=run_focus_sweep,
            show_plot=show_plot,
            sn=sn, d1=d1, d2=d2, amc=amc
        )

        if movetoxy and bx is not None:
            print("Moving to best X-Y position...")
            amc.move.setControlTargetPosition(0, int(bx * 1000)); wait_until_stable(amc, 0)
            amc.move.setControlTargetPosition(2, int(by * 1000)); wait_until_stable(amc, 2)
            print("Move complete.")
            
    finally:
        if sn_local: close_device_all(sn=sn)
        if amc_local: close_device_all(amc=amc)
            
    return bx, by, bf

def run_g2(measure_time_s=600, bin_ps=100, window_ps=100000, detector_config=2, inp_hyst = 0, optimize_position=False, save_data=True, output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/acquired', sn=None, d1=None, d2=None, amc=None):
    sn_local = amc_local = False
    main_fig = None

    try:
        if sn is None or d1 is None or d2 is None:
            print("Initializing APDs...")
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True
        a, b = d1, d2

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

        plt.ion()
        main_fig, (ax_g2, ax_trace) = plt.subplots(1, 2, figsize=(12, 5.5))
        main_fig.suptitle("g\u00b2(\u03c4) Measurement", fontsize=16)

        stop_button_ax = main_fig.add_axes([0.9, 0.01, 0.08, 0.04])
        stop_button = Button(stop_button_ax, 'Stop', hovercolor='0.975')
        stop_button.on_clicked(lambda event: (print("Stop command sent."), sn.correlation.stopMeasure()))

        dt_now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        details_filename = "g2_details_temp.txt" 
        if save_data:
            os.makedirs(output_dir, exist_ok=True)
            ptu_filename = os.path.join(output_dir, f'g2data_{measure_time_s}s_{dt_now}.ptu')
            details_filename = os.path.join(output_dir, f"g2details_{measure_time_s}s_{dt_now}.txt")
            sn.setPTUFilePath(ptu_filename)
            print(f'\nSaving PTU data to: {os.path.basename(ptu_filename)}')

        sn.correlation.setG2Parameters(a, b, window_ps, bin_ps)
        sn.correlation.measure(int(measure_time_s * 1000), savePTU=save_data)
        start_time = time.time()
        start_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Starting g(2) measurement for {measure_time_s} s...')

        ax_g2.set_xlabel('Time Delay (ns)'); ax_g2.set_ylabel('$g^{(2)}(\\tau)$'); 
        line_g2, = ax_g2.plot([], [], lw=0.5, animated=True)
        ax_g2.set_ylim(0, 2.5)
        
        ax_trace.set_xlabel('Elapsed Time (s)'); ax_trace.set_ylabel('Count Rate (cps)'); 
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
                    ax_g2.set_ylim(0, g2_max * 1.1)  
                else:
                    ax_g2.set_ylim(0, 1.5) 
                
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

            if save_data and final_g2 is not None:
                f.write("\n\n# Final g2 data (Time_ps\tNorm_Counts)\n")
                np.savetxt(f, np.column_stack((final_lagtimes, final_g2)), delimiter='\t')
                
                fig_path = os.path.join(output_dir, f'g2plot_{measure_time_s}s_{dt_now}.png')
                line_g2.set_animated(False); line_ch1.set_animated(False); line_ch2.set_animated(False)
                main_fig.canvas.draw()
                main_fig.savefig(fig_path, dpi=150)
                print(f"Final plot saved to: {os.path.basename(fig_path)}")
        
        plt.ioff()
        print("Script finished. The plot window is now static. Close it to exit.")
        ax_trace.set_title(f'Time Trace | Measurement Complete')
        plt.show()

    except Exception as e:
        print(f"An error occurred in run_g2: {e}")
        traceback.print_exc()
    finally:
        if sn_local and sn:
            close_device_all(sn=sn)
            print("MH150 closed")
        if amc_local and amc:
            close_device_all(amc=amc)
            print("AMC closed")

def run_g2_from_file(input_file, detector_config=2, output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/fildevice', save_data=True, bin=100, window=100000):
    sn = snAPI()
    try:
        if detector_config==1:
            a,b = 1,2
        else:
            a, b = 3, 4
        sn.getFileDevice(input_file)
        print(f"Data from {os.path.basename(input_file)} loaded successfully")
        sn.correlation.setG2Parameters(a, b, window, bin)
        sn.correlation.measure(waitFinished=True)

        fig, ax = plt.subplots()
        g2, lagtimes = sn.correlation.getG2Data()

        ax.plot(lagtimes, g2, label=f'{os.path.basename(input_file)}', linewidth=0.5)
        ax.set_xlabel('Delay (s)')
        ax.set_ylabel('g(2)')
        ax.set_title(f'g(2) Correlation (Bin = {bin} ps & Window = {window} ps)')
        ax.legend(loc='upper right')

        if save_data:
            base_name = os.path.basename(input_file).replace('.ptu', '')
            dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            plot_filename = f'g2_filedevice_plot_{base_name}_{dt_now}.png'
            plot_path = os.path.join(output_dir, plot_filename)
            try:
                fig.savefig(plot_path, dpi=150)
                print(f"Plot saved as {plot_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")

            data_filename = f'g2_filedevice_data_{base_name}_{dt_now}.txt'
            data_path = os.path.join(output_dir, data_filename)
            try:
                data_to_save = np.column_stack((lagtimes, g2))
                np.savetxt(data_path, data_to_save, delimiter='\t', header='Lag Time (ps)\tg2(tau)', comments='# ')
                print(f"Data saved as {data_path}")
            except Exception as e:
                print(f"Error saving data: {e}")

        plt.show()

    finally:
        if sn:
            close_device_all(sn=sn)

def run_spectrum_focus_sweep(camera, spectro, fbase=None, fstep=0.1, fsize=30, movetobest=True, 
                             showplt=True, engaged=False, amc=None,
                             wl_min=None, wl_max=None, vbg=None,
                             out_dir_base=r'D:\Data_Python_PL\FocusSweeps'):
    amc_local = False
    data_file_handle = None
    fnow = fbase 

    try:
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
        print(f"Keyboard interrupt : {k}\nMoving to initial position ---")
        amc.move.setControlTargetPosition(1, int(fnow * 1000)); wait_until_stable(amc, 1)
        return fnow
    finally:
        if data_file_handle:
            data_file_handle.close()
        if amc_local and amc: close_device_all(amc=amc)    

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

def take_live_spectrum(camera, spectro, exposure_time=1, grating=1):
    if grating == 2:
        wl=461
        print("Grating 2 selected")
    else:
        wl=484
        print("Grating 1 selected (Default)")
    set_spectrum(camera=camera, spectro=spectro, acq_mode="single_scan", cosmic_filter=False, exposure_time=exposure_time, wl=wl, grating=grating)
    scope(camera.readval)
    
def take_spectrum(bg=True, vbg=None, data_only=False, show_plot=True, camera=None, sav_data=True, ide=None, idex=None):
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

    if show_plot:
        _, ax = plt.subplots()
        ax.plot(v[0], v[1]) 
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

def run_pl_polarization_spectrum(start_deg=0, end_deg=360, step_deg=10, 
                        detector_config=2, out_dir_base=r'D:\Data_Python_PL\Polarization',
                        show_plot=True, force_home_kdc=False, kdc=None, amc=None, 
                        camera=None, bg=True, vbg=None, ide=None, idex=None):
    kdc_local = False
    amc_local = False

    try:
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

        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        folder_suffix = f"{f'_{ide}' if ide is not None else ''}{f'_{idex}' if idex is not None else ''}"
        sub_folder_name = f"{timestamp}{folder_suffix}"
        out_dir = os.path.join(out_dir_base, sub_folder_name)
        os.makedirs(out_dir, exist_ok=True)

        print(f'Saving polarization spectra to directory: {out_dir}')

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
            kdc_move_deg(angle, kdc=kdc)
            time.sleep(0.2)  
            
            act_angle = kdc_position_deg(kdc=kdc)
            actual_angles.append(act_angle)

            deg_str = f"deg_{act_angle:.1f}".replace('.', '_')
            data_file = os.path.join(out_dir, f'spectrum_data{folder_suffix}_{deg_str}_{timestamp}.txt')

            print(f"Taking Spectrum at {act_angle:.1f}°...")
            v = get(camera.readval, filename=data_file)
            all_spectra.append(v)

        print("\nPolarization spectrum sweep complete.")

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


# ==========================================
# EXTRA PLOTTING UTILITIES
# ==========================================

def plot_plmap_poster(
    fpath, mode="apd", flog=False, id="PL map", invxy=False, force1d=False,
    encoding="latin1", figsize=(9, 7), poster=True, nticks=5, size=45
):
    if poster:
        sz = size
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

    Lx = x.max() - x.min()
    Ly = y.max() - y.min()
    extent = [-Lx/2, Lx/2, -Ly/2, Ly/2]

    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(Z, cmap="plasma", origin="lower", extent=extent, aspect="auto")

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Log10 Counts" if flog else "Counts", weight="bold")

    if invxy:
        ax.invert_xaxis()
        ax.invert_yaxis()

    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")

    ax.xaxis.set_major_locator(MaxNLocator(nticks))
    ax.yaxis.set_major_locator(MaxNLocator(nticks))

    plt.tight_layout()
    plt.show()

def plot_polarization(input, polar=True, mode='custom', flog=False, normalize=False,
                      xi=0, yi=4, use_actual_angle=True, plot_style='scatter',
                      fit_dipole=True, fit_npts=720, minor_grids=True):
    with open(input, "r", encoding="latin1", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s: continue
        if s[0].isdigit() or s[0] in "+-.":
            start = i
            break
    if start is None:
        raise ValueError("No numeric data found in file.")

    v = np.loadtxt(StringIO("".join(lines[start:])), unpack=True)

    if mode == 'apd':
        x_index = 1 if use_actual_angle else 0  
        y_index = 4                              
    elif mode == 'spec':
        x_index, y_index = (0, 5)
    elif mode == 'specw':
        x_index, y_index = (0, 6)
    else:
        x_index, y_index = xi, yi

    x_deg = v[x_index].astype(float)
    y = v[y_index].astype(float)
    y = y - np.min(y)

    if flog:
        y = np.log10(y + 1e-12)

    if normalize == 'max':
        m = np.max(y)
        if m != 0: y = y / m
    elif normalize == 'sum':
        s = np.sum(y)
        if s != 0: y = y / s
    elif normalize == 'minmax':
        ymin, ymax = np.min(y), np.max(y)
        if ymax != ymin: y = (y - ymin) / (ymax - ymin)

    order = np.argsort(x_deg)
    x_deg = x_deg[order]
    y = y[order]
    x_rad = np.deg2rad(x_deg)

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

    if polar:
        major_deg = np.arange(0, 360, 45)
        ax.set_xticks(np.deg2rad(major_deg))
        ax.set_xticklabels([f"{d}°" for d in major_deg])
        ax.tick_params(axis='x', pad=30) 
        ax.set_yticklabels([])

        if normalize in ('max', 'minmax'):
            ax.set_ylim(0, 1.05)

        if minor_grids:
            ax.set_xticks(np.deg2rad(np.arange(0, 360, 15)), minor=True)
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

    ax.set_title("")
    leg = ax.get_legend()
    if leg is not None: leg.remove()

    return fig, ax, fit_info

def plot_trpl_log(fpath, channel="Ch3", t_max_plot=20.0, fit_end_ns=None, start_at_frac_of_peak=0.70, 
                  min_points_fit=60, baseline_mode="tail_median", tail_fraction=0.15, 
                  min_counts_for_log=1.0, raw_alpha=0.35, raw_lw=1.2, fit_lw=3.0):

    with open(fpath, "r", encoding="latin1", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s: continue
        if s[0].isdigit() or s[0] in "+-.":
            start = i
            break
    if start is None:
        raise ValueError("No numeric data found in file.")

    data = np.loadtxt(StringIO("".join(lines[start:])))
    t = data[:, 0].astype(float)      
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

    order = np.argsort(t)
    t = t[order]
    y = y[order]

    if t_max_plot is not None:
        mplot = t <= float(t_max_plot)
        t_plot = t[mplot]
        y_plot = y[mplot]
    else:
        t_plot, y_plot = t, y

    if t_plot.size < 50:
        raise ValueError("Not enough points in plot window. Increase t_max_plot.")

    i_peak = int(np.argmax(y_plot))
    t_peak = float(t_plot[i_peak])
    y_peak = float(y_plot[i_peak])

    thr = float(start_at_frac_of_peak) * y_peak

    post = np.arange(i_peak, len(y_plot))
    below = post[y_plot[post] <= thr]
    if below.size == 0:
        i0 = builtins.min(i_peak + builtins.max(1, int(0.01 * len(y_plot))), len(y_plot) - 1)
    else:
        i0 = int(below[0])

    t0 = float(t_plot[i0])
    t1 = float(t_plot[-1]) if fit_end_ns is None else float(fit_end_ns)

    mfit = (t_plot >= t0) & (t_plot <= t1)
    tf = t_plot[mfit]
    yf = y_plot[mfit]

    if tf.size < min_points_fit:
        raise ValueError(f"Fit window too small ({tf.size} pts). ")

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

    y_corr = yf - C
    good = y_corr > 1e-12
    tf2 = tf[good]
    y2 = y_corr[good]

    if tf2.size < builtins.max(20, int(0.5 * min_points_fit)):
        raise ValueError("Not enough positive points after baseline subtraction.")

    x = (tf2 - t0)
    ln_y = np.log(y2)

    xbar, ybar = x.mean(), ln_y.mean()
    Sxx = np.sum((x - xbar) ** 2)
    Sxy = np.sum((x - xbar) * (ln_y - ybar))
    slope = Sxy / Sxx
    intercept = ybar - slope * xbar

    tau = -1.0 / slope
    A = float(np.exp(intercept))

    resid = ln_y - (intercept + slope * x)
    dof = builtins.max(1, len(x) - 2)
    s2 = np.sum(resid**2) / dof
    slope_se = np.sqrt(s2 / Sxx)
    tau_se = abs(slope_se / (slope ** 2))

    t_fit = t_plot
    y_fit = A * np.exp(-(t_fit - t0) / tau) + C
    y_fit[t_fit < t0] = np.nan

    fig, ax = plt.subplots(1, 1, figsize=(7.0, 4.2), dpi=150, constrained_layout=True)

    y_plot_log = np.clip(y_plot, min_counts_for_log, None)
    ax.semilogy(t_plot, y_plot_log, lw=raw_lw, alpha=raw_alpha, label=f"Raw Counts ({ch_label})")

    y_fit_log = np.where(np.isfinite(y_fit), np.clip(y_fit, min_counts_for_log, None), np.nan)
    ax.semilogy(t_fit, y_fit_log, lw=fit_lw, color="orange", label=f"Fit (τ={tau:.2f}±{tau_se:.2f} ns)")

    ax.set_xlabel("Time (ns)")
    ax.set_ylabel(f"Counts ({ch_label}, log scale)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="upper right", frameon=True)

    fit_dict = {
        "channel": ch_label, "t_peak_ns": t_peak, "y_peak": y_peak, "t0_ns": t0, "fit_end_ns": t1,
        "A": float(A), "C": float(C), "tau_ns": float(tau), "tau_err_ns": float(tau_se),
        "n_fit_points": int(tf2.size), "start_at_frac_of_peak": float(start_at_frac_of_peak),
    }

    return fig, ax, fit_dict

def plot_parameters(xi, yi, xr, yr):
    print(f'xstart= {xi - xr/2}')
    print(f'xend= {xi + xr/2}')
    print(f'ystart= {yi - yr/2}')
    print(f'yend= {yi + yr/2}')


# %%
