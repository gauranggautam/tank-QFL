import numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as mticker
import time, os, AMC
from snAPI.Main import *

# === AMC Init ===
amc = AMC.Device('amc100num-a01-0248.local')
amc.connect()
for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
def wait_until_stable(timeout=10):
    import time
    start = time.time()
    while True:
        if all(amc.status.getStatusMoving(a) == 0 for a in [0, 1, 2]) and \
        all(amc.status.getStatusTargetRange(a) for a in [0, 1, 2]):
            break
        for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
        if time.time() - start > timeout:
            break
        time.sleep(0.01)
wait_until_stable
x_now = amc.move.getPosition(0) / 1000
y_now = amc.move.getPosition(2) / 1000
f_now = amc.move.getPosition(1) / 1000

#Three markers
(ax,ay) = (0,0) 
(bx,by) = (0,0)
(cx,cy) = (0,0)
(af,bf,cf)=(0,0,0)

# === snAPI Init ===
sn = snAPI(libType=LibType.MH)
sn.closeDevice()
if not sn.getDevice(0): print('MH not found'); exit()
sn.setLogLevel(LogLevel.Device, False)
sn.setLogLevel(LogLevel.Api, False)
sn.initDevice(MeasMode.T2)

# === Detector Config ===
Detectors = 2
if Detectors == 1:
    d1, d2 = 1, 2
    sn.loadIniConfig(r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\Exciletas_MH.ini')
else:
    d1, d2 = 3, 4
    sn.loadIniConfig(r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\MPDs_MH.ini')
#focus sweep at three positions
FOCUS_STEP = 0.1         # Focus scan step in µm
FOCUS_RANGE = 5 # ± range from current focus
focus_range = np.arange(f_now - FOCUS_RANGE, f_now + FOCUS_RANGE + FOCUS_STEP, FOCUS_STEP)
counts = []
max_cf1, best_f1= 0, f_now


print("\nMoving to mark 1...")
amc.move.setControlTargetPosition(0, int(ax * 1000))
amc.move.setControlTargetPosition(0, int(ay * 1000))
wait_until_stable()
print("\nSweeping focus at mark 1...")
focus_range = np.arange(af - FOCUS_RANGE, af + FOCUS_RANGE + FOCUS_STEP, FOCUS_STEP)
for f in focus_range:
    amc.move.setControlTargetPosition(1, int(f * 1000))
    wait_until_stable()
    cnt = sn.getCountRates()
    total = cnt[d1] + cnt[d2]
    plt.plot(focus_range, counts, marker='o', color='red')
    f_act= amc.move.getPosition(1) / 1000
    #print(f'Focus {f:.2f} µm -> {total} cps')
    
    if total > max_cf:
        max_cf, best_f= total, f_act
        print(f'Best Focus mark 1: {best_f:.2f}') 

def calc_plane(ax, ay, az, bx, by, bz, cx, cy, cz):
    abx = bx - ax
    aby = by - ay
    abz = bz - az
    acx = cx - ax
    acy = cy - ay
    acz = cz - az
    nx = aby * acz - abz * acy
    ny = abz * acx - abx * acz
    nz = abx * acy - aby * acx
    if nx==0 and ny==0 and nz==0:
        return None                 #collinear points case
    return (nx, ny, nz, -nx*ax-ny*ay-nz*az)
print(calc_plane(1,0,0,0,1,0,0,0,1))
print(calc_plane(1,-2,1,4,-2,-2,4,1,4))