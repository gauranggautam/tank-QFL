# ==========================================
# Imports
# ==========================================
import os, re, time, traceback, builtins
from datetime import datetime
from io import StringIO

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
import pyvisa

TAB20_COLORS = plt.colormaps['tab20'].colors

# Hardware-Specific Optional Imports
try: from attocube import AMC
except ImportError as e: print(e)

try: from snAPI.Main import *
except ImportError as e: print(e)

try: from taiko_driver import TaikoLaser
except ImportError as e: print(e)

try: import nidaqmx; from nidaqmx.constants import Edge
except ImportError as e: print(e)

try: import labview_buttons_v2 as lv
except ImportError as e: print(e)

try: from montana import cryocore
except ImportError as e: print(e)


# ==========================================
# 1. Hardware & System Classes
# ==========================================

class MontanaCryo:
    """Montana CryoCore Controller with state & goal management."""
    def __init__(self, ip_address="192.168.0.2"):
        self.ip_address = ip_address
        self.cryo = None
        self.connect()

    def connect(self):
        try:
            self.cryo = cryocore.CryoCore(self.ip_address)
            print(f"Connected to Montana CryoCore at {self.ip_address}")
        except Exception as e:
            print(f"ERROR: Failed to connect to CryoCore: {e}")

    def _get_val(self, res):
        return res[1] if isinstance(res, tuple) else res

    @property
    def state(self):
        return self._get_val(self.cryo.get_system_state()) if self.cryo else "Unknown"

    @property
    def goal(self):
        return self._get_val(self.cryo.get_system_goal()) if self.cryo else "Unknown"

    def ensure_ready(self, timeout=30):
        if not self.cryo: self.connect()
        if self.goal in ['None', None] and self.state == 'Ready': return True
        print(f"System busy (Goal: {self.goal}, State: {self.state}). Aborting current goal...")
        self.cryo.abort_goal()
        start = time.time()
        while time.time() - start < timeout:
            if self.state == 'Ready': return True
            time.sleep(1)
        return False

    def pull_vacuum(self):
        if self.goal == 'PullVacuum': return
        if self.ensure_ready(): self.cryo.pull_vacuum()

    def vent(self):
        if self.goal == 'Vent': return
        if self.ensure_ready(): self.cryo.vent()

    def set_temp(self, target_temp):
        if self.cryo: self.cryo.set_platform_target_temperature(target_temp)

    def start_cooldown(self, target_temp=10, bakeout=False, n2purge=False):
        if self.goal not in ['Cooldown', 'None', None]: self.ensure_ready()
        if hasattr(self.cryo, 'set_platform_bakeout_enabled'):
            try: self.cryo.set_platform_bakeout_enabled(bakeout)
            except TypeError: self.cryo.set_platform_bakeout_enabled = bakeout
        if hasattr(self.cryo, 'set_dry_nitrogen_purge_enabled'):
            try: self.cryo.set_dry_nitrogen_purge_enabled(n2purge)
            except TypeError: self.cryo.set_dry_nitrogen_purge_enabled = n2purge
        
        self.set_temp(target_temp)
        if self.goal != 'Cooldown': self.cryo.cooldown()

    def get_temp_p1(self):
        return float(self._get_val(self.cryo.get_platform_temperature())) if self.cryo else None

    def get_temp_u1(self):
        return float(self._get_val(self.cryo.get_user1_temperature())) if self.cryo else None

    def wait_for_temp_p1(self, req_temp, tolerance=1.0, poll_interval=2):
        print(f"Waiting for platform temp to reach {req_temp} K (±{tolerance}K)...")
        while True:
            t = self.get_temp_p1()
            if t is not None:
                print(f"Current P1: {t:.2f} K (Target: {req_temp} K) | State: {self.state}", end='\r')
                if abs(t - req_temp) <= tolerance:
                    print(f"\nTarget temperature reached: {t:.2f} K")
                    break
            time.sleep(poll_interval)

    def wait_for_temp_u1(self, req_temp, tolerance=1.0, poll_interval=2):
        print(f"Waiting for user 1 temp to reach {req_temp} K (±{tolerance}K)...")
        while True:
            t = self.get_temp_u1()
            if t is not None:
                print(f"Current U1: {t:.2f} K (Target: {req_temp} K) | State: {self.state}", end='\r')
                if abs(t - req_temp) <= tolerance:
                    print(f"\nUser 1 target reached: {t:.2f} K")
                    break
            time.sleep(poll_interval)


class AttocubeStage:
    """Attocube AMC Controller."""
    def __init__(self, address='amc100num-a01-0248.local'):
        self.address = address
        self.amc = None

    def connect(self):
        self.amc = AMC.Device(self.address)
        self.amc.connect()
        for ax in [0, 1, 2]:
            self.amc.control.setControlOutput(ax, True)
            self.amc.control.setControlMove(ax, True)
        print(f"Connected to AMC: {self.address}")

    def wait_stable(self, axis, timeout=10):
        start = time.time()
        while True:
            if self.amc.status.getStatusMoving(axis) == 0 and self.amc.status.getStatusTargetRange(axis):
                break
            self.amc.control.setControlOutput(axis, True)
            self.amc.control.setControlMove(axis, True)
            if time.time() - start > timeout: break
            time.sleep(0.01)

    def move_axis(self, axis, pos_um):
        if not self.amc: self.connect()
        self.amc.move.setControlTargetPosition(axis, int(pos_um * 1000))
        self.wait_stable(axis)

    def get_pos(self, axis):
        if not self.amc: self.connect()
        return self.amc.move.getPosition(axis) / 1000.0

    def close(self):
        if self.amc:
            self.amc.close()
            self.amc = None


class APDDetector:
    """PicoQuant snAPI APD Interface."""
    def __init__(self, config=2, serial="1043897"):
        self.config = config
        self.serial = serial
        self.sn = None
        self.d1 = 3 if config == 2 else 1
        self.d2 = 4 if config == 2 else 2

    def connect(self):
        self.sn = snAPI()
        self.sn.getDevice(self.serial)
        if not self.sn.initDevice(): raise ConnectionError('MH150 initialization failed.')
        cfg = r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\MPDs_MH.ini' if self.config == 2 else r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\Exciletas_MH.ini'
        self.sn.loadIniConfig(cfg)

    def get_counts(self):
        if not self.sn: self.connect()
        cnt = self.sn.getCountRates()
        return cnt[self.d1], cnt[self.d2], cnt[self.d1] + cnt[self.d2]

    def close(self):
        if self.sn:
            self.sn.closeDevice(allDevices=True)
            self.sn.exitAPI()
            self.sn = None


# Global Hardware Singletons
_global_cryo = None
_global_stage = None
_global_apd = None


# ==========================================
# 2. Montana CryoCore Functions
# ==========================================

def start_cryo(ip="192.168.0.2"):
    global _global_cryo
    if _global_cryo is None:
        _global_cryo = MontanaCryo(ip)
    return _global_cryo

def cryo_pullvac():
    start_cryo().pull_vacuum()

def cryo_vent():
    start_cryo().vent()

def cryo_set_temp(target_temp):
    start_cryo().set_temp(target_temp)

def cryo_start_cooldown(target_temp=10, bakeout=False, n2purge=False):
    start_cryo().start_cooldown(target_temp=target_temp, bakeout=bakeout, n2purge=n2purge)

def cryo_get_temp_p1():
    return start_cryo().get_temp_p1()

def cryo_get_temp_u1():
    return start_cryo().get_temp_u1()

def cryo_waitfortemp_p1(req_temp, tolerance=1.0):
    start_cryo().wait_for_temp_p1(req_temp, tolerance=tolerance)

def cryo_waitfortemp_u1(req_temp, tolerance=1.0):
    start_cryo().wait_for_temp_u1(req_temp, tolerance=tolerance)


# ==========================================
# 3. Attocube Stage & Motion Functions
# ==========================================

def start_attocube(amc_address='amc100num-a01-0248.local'):
    global _global_stage
    if _global_stage is None or _global_stage.amc is None:
        _global_stage = AttocubeStage(amc_address)
        _global_stage.connect()
    return _global_stage.amc

def amc_move(axis, d, amc=None):
    stage = _global_stage or AttocubeStage()
    stage.move_axis(axis, d)

def amc_movexyz(x, y, f, amc=None):
    stage = _global_stage or AttocubeStage()
    stage.move_axis(0, x)
    stage.move_axis(2, y)
    stage.move_axis(1, f)

def getposall():
    stage = _global_stage or AttocubeStage()
    print(f"x = {stage.get_pos(0)}")
    print(f"y = {stage.get_pos(2)}")
    print(f"f = {stage.get_pos(1)}")

def gohome():
    stage = _global_stage or AttocubeStage()
    for ax in [0, 1, 2]: stage.move_axis(ax, 0)
    getposall()


# ==========================================
# 4. Laser, APD, Optomech & DAQ Functions
# ==========================================

def start_apds(detector_config=2, read_counts=False):
    global _global_apd
    _global_apd = APDDetector(config=detector_config)
    _global_apd.connect()
    if read_counts:
        c1, c2, tot = _global_apd.get_counts()
        print(f"Ch{_global_apd.d1}: {c1}, Ch{_global_apd.d2}: {c2}, Total: {tot}")
    return _global_apd.sn, _global_apd.d1, _global_apd.d2

def start_laser(power=None, cw=True, softlock=False, close=False, engaged=False):
    laser = TaikoLaser()
    laser.open()
    if close:
        laser.cw_power_permille = 0
        laser.softlock = True
        laser.close()
        return None
    if softlock: laser.softlock = True
    if power is not None: laser.cw_power_permille = int(power * 10)
    if cw: laser.laser_mode = 'cw'
    if engaged: return laser
    laser.close()
    return None

def detector_switch(moveto='camera', ESP_address="GPIB1::7::INSTR"):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    pos_map = {'apd': 0, 'spectro': -49, 'camera': 47.5}
    if moveto in pos_map:
        esp.write(f"3PA{pos_map[moveto]}")
        time.sleep(5)
    return esp

def filter_switch(moveto='no', ESP_address="GPIB1::7::INSTR"):
    rm = pyvisa.ResourceManager()
    esp = rm.open_resource(ESP_address)
    pos_map = {'no': -24, 'n405': 0, 'n533': 25}
    if moveto in pos_map:
        esp.write(f"2PA{pos_map[moveto]}")
        time.sleep(5)
    return esp

def close_device_all(sn=None, amc=None, daq=None):
    global _global_apd, _global_stage
    if _global_apd: _global_apd.close(); _global_apd = None
    if _global_stage: _global_stage.close(); _global_stage = None
    print("All devices closed.")


# ==========================================
# 5. Measurement Routines
# ==========================================

def output_dir_folder(base_dir=r'D:\Data_Python_PL'):
    out_dir = os.path.join(base_dir, time.strftime('%Y_%m_%d'))
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

def run_focus_sweep(fbase=None, fstep=0.1, fsize=30, movetobest=True, showplt=True, detector_config=2):
    stage = _global_stage or AttocubeStage()
    apd = _global_apd or APDDetector(config=detector_config)
    
    fnow = fbase if fbase is not None else stage.get_pos(1)
    fstart, fend = fnow - (fsize / 2), fnow + (fsize / 2)
    frange = np.arange(fstart, fend + fstep, fstep)

    focus, totals, ch1s, ch2s = [], [], [], []
    maxc, bestf = -1, fnow

    plt.ion()
    fig, ax = plt.subplots()
    line_total, = ax.plot([], [], 'b.-', label='Total Counts')
    ax.set_xlim(fstart, fend)

    for f in frange:
        stage.move_axis(1, f)
        c1, c2, total = apd.get_counts()
        focus.append(f); totals.append(total)
        if total > maxc: bestf, maxc = f, total
        line_total.set_data(focus, totals)
        ax.relim(); ax.autoscale_view()
        fig.canvas.draw(); fig.canvas.flush_events()

    if movetobest: stage.move_axis(1, bestf)
    plt.ioff()
    if showplt: plt.show()
    else: plt.close(fig)
    return bestf

def run_pl_scan(center_x=None, center_y=None, center_f=None, x_size=5, y_size=5, step=0.1, 
                focus_sweep=False, f_size=50, detector_config=2, logz=False, 
                out_dir_base=r'D:\Data_Python_PL\PLmaps', show_plot=True):
    stage = _global_stage or AttocubeStage()
    apd = _global_apd or APDDetector(config=detector_config)

    center_x = center_x if center_x is not None else stage.get_pos(0)
    center_y = center_y if center_y is not None else stage.get_pos(2)
    if center_f is not None: stage.move_axis(1, center_f)
    fnow = center_f if center_f is not None else stage.get_pos(1)

    stage.move_axis(0, center_x); stage.move_axis(2, center_y)
    if focus_sweep:
        center_f = run_focus_sweep(fbase=fnow, fsize=f_size, movetobest=True, showplt=False, detector_config=detector_config)

    x_start, x_end = center_x - (x_size / 2), center_x + (x_size / 2)
    y_start, y_end = center_y - (y_size / 2), center_y + (y_size / 2)
    x_pos, y_pos = np.arange(x_start, x_end + step, step), np.arange(y_start, y_end + step, step)
    Z = np.zeros((len(y_pos), len(x_pos)), dtype=float)

    out_dir = output_dir_folder(base_dir=out_dir_base)
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')

    plt.ion()
    fig, ax = plt.subplots()
    extent = [x_start, x_end, y_start, y_end]
    img = ax.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto')
    fig.colorbar(img, ax=ax)
    
    max_int, best_x, best_y = -1, x_start, y_start

    with open(data_file, 'w') as f_out:
        f_out.write(f'# PL Mapping - Center X: {center_x}, Y: {center_y}, F: {center_f}\n')
        f_out.write(f'# readback numpy shape for line part: {len(x_pos)}, {len(y_pos)} \n')
        f_out.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')

        for i, y in enumerate(y_pos):
            stage.move_axis(2, y)
            x_scan_pos = x_pos if i % 2 == 0 else x_pos[::-1]

            for j_scan, x in enumerate(x_scan_pos):
                j = j_scan if i % 2 == 0 else len(x_pos) - 1 - j_scan
                stage.move_axis(0, x)

                x_act, y_act = stage.get_pos(0), stage.get_pos(2)
                c1, c2, total = apd.get_counts()
                Z[i, j] = np.log10(total + 1) if logz else total

                if total > max_int: max_int, best_x, best_y = total, x_act, y_act
                f_out.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{c1}\t{c2}\t{total}\n')

            img.set_data(Z); img.set_clim(vmin=Z.min(), vmax=Z.max())
            ax.set_title(f'PL Map – Max: {max_int:.0f} @({best_x:.2f},{best_y:.2f})')
            fig.canvas.draw(); fig.canvas.flush_events()

    plt.ioff()
    if show_plot: plt.show()
    else: plt.close(fig)
    return best_x, best_y, center_f

def run_g2(measure_time_s=600, bin_ps=100, window_ps=100000, detector_config=2, save_data=True, 
           output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/Output/g2/acquired'):
    apd = _global_apd or APDDetector(config=detector_config)
    if not apd.sn: apd.connect()

    os.makedirs(output_dir, exist_ok=True)
    dt_now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    ptu_file = os.path.join(output_dir, f'g2data_{measure_time_s}s_{dt_now}.ptu')
    txt_file = os.path.join(output_dir, f'g2details_{measure_time_s}s_{dt_now}.txt')

    if save_data: apd.sn.setPTUFilePath(ptu_file)
    apd.sn.correlation.setG2Parameters(apd.d1, apd.d2, window_ps, bin_ps)
    apd.sn.correlation.measure(int(measure_time_s * 1000), savePTU=save_data)

    plt.ion()
    fig, (ax_g2, ax_trace) = plt.subplots(1, 2, figsize=(12, 5.5))
    line_g2, = ax_g2.plot([], [], lw=0.5)
    line_ch1, = ax_trace.plot([], [], 'r-')
    line_ch2, = ax_trace.plot([], [], 'g-')

    start_time = time.time()
    times, counts1, counts2 = [], [], []

    with open(txt_file, 'w') as f:
        while not apd.sn.correlation.isFinished():
            g2, lagtimes = apd.sn.correlation.getG2Data()
            c1, c2, _ = apd.get_counts()
            if g2 is None or len(g2) < 1:
                plt.pause(0.1); continue

            elapsed = time.time() - start_time
            times.append(elapsed); counts1.append(c1); counts2.append(c2)
            f.write(f"{elapsed:.2f}\t{c1}\t{c2}\t{np.min(g2):.4f}\n")

            line_g2.set_data(np.array(lagtimes) / 1000.0, g2)
            line_ch1.set_data(times, counts1)
            line_ch2.set_data(times, counts2)
            ax_g2.relim(); ax_g2.autoscale_view()
            ax_trace.relim(); ax_trace.autoscale_view()
            fig.canvas.draw(); fig.canvas.flush_events()
            plt.pause(0.01)

    plt.ioff(); plt.show()


# ==========================================
# 6. Plotting Utilities
# ==========================================

def set_4k():
    mpl.rcParams.update({
        'figure.dpi': 200, 'savefig.dpi': 300, 'figure.figsize': [10, 6],
        'font.size': 14, 'lines.linewidth': 2, 'lines.markersize': 6,
        'axes.titlesize': 16, 'axes.labelsize': 14, 'xtick.labelsize': 12,
        'ytick.labelsize': 12, 'legend.fontsize': 12
    })

def set_size_poster(size=45):
    sz_small = size - 10
    mpl.rcParams.update({
        'font.family': 'Times New Roman', 'font.size': sz_small,
        'font.weight': 'bold', 'axes.labelweight': 'bold',
        'axes.titlesize': size, 'axes.titleweight': 'bold',
        'axes.labelsize': sz_small, 'legend.fontsize': sz_small - 10,
        'xtick.labelsize': sz_small, 'ytick.labelsize': sz_small
    })

def plot_spectrum(input_path, compare=False, fig_num=11, plot_id='Plot'):
    v = np.loadtxt(input_path, unpack=True, encoding='latin1')
    fig, ax = plt.subplots() if not compare else (plt.figure(fig_num), plt.gca())
    ax.plot(v[1], v[2], label=f'{plot_id}_{os.path.basename(input_path)}')
    ax.set_xlabel('Wavelength (nm)'); ax.set_ylabel('Counts (Arb.)')
    ax.grid(True); ax.legend()
    plt.show()

def plot_polarization(input_path, polar=True, fit_dipole=True):
    with open(input_path, "r", encoding="latin1", errors="ignore") as f:
        lines = [line for line in f.readlines() if line.strip() and (line.strip()[0].isdigit() or line.strip()[0] in "+-.")]
    v = np.loadtxt(StringIO("".join(lines)), unpack=True)
    x_rad, y = np.deg2rad(v[1]), v[4] - np.min(v[4])

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True) if polar else fig.add_subplot(111)
    ax.scatter(x_rad if polar else np.rad2deg(x_rad), y, s=25)

    if fit_dipole:
        X = np.column_stack([np.ones_like(x_rad), np.cos(2 * x_rad), np.sin(2 * x_rad)])
        a, b, c = np.linalg.lstsq(X, y, rcond=None)[0]
        th = np.linspace(0, 2 * np.pi, 720)
        yfit = a + b * np.cos(2 * th) + c * np.sin(2 * th)
        ax.plot(th if polar else np.rad2deg(th), yfit, lw=3, color='orange')

    plt.show()