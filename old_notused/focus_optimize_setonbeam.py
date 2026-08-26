import numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as mticker
import time, os, AMC
from snAPI.Main import *

# === CONFIG ===
FOCUS_ONLY_MODE = True  # Set to True to skip scan and only do focus sweep
FOCUS_STEP = 0.1         # Focus scan step in µm
FOCUS_RANGE = 20          # ± range from current focus

timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
out_dir = './PlotBasic/Output/PLmaps'
os.makedirs(out_dir, exist_ok=True)

# === AMC Init ===
amc = AMC.Device('amc100num-a01-0248.local')
amc.connect()
for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)

x_now = amc.move.getPosition(0) / 1000
y_now = amc.move.getPosition(2) / 1000
f_now = amc.move.getPosition(1) / 1000

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

# === Helper: Wait Until Stable ===
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
        
# === FOCUS SWEEP ===
for a in [1]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
#for a in [0, 2]: amc.control.setControlMove(a, False)
focus_range = np.arange(f_now - FOCUS_RANGE, f_now + FOCUS_RANGE + FOCUS_STEP, FOCUS_STEP)
counts = []
max_cf, best_f= 0, f_now




fig, ax = plt.subplots()

ax.set_title('Focus sweep')
ax.set_xlabel('Focus (um)')
ax.set_ylabel('Counts (a.u.)')


print("\nSweeping focus...")
for f in focus_range:
    amc.move.setControlTargetPosition(1, int(f * 1000))
    wait_until_stable()
    cnt = sn.getCountRates()
    total = cnt[d1] + cnt[d2]
    ax.plot(f, total, marker='o', color='red')
    f_act= amc.move.getPosition(1) / 1000
    plt.pause(0.1)
    if total > max_cf:
        max_cf, best_f= total, f_act
        print(f'Best Focus: {best_f:.2f}')    

amc.move.setControlTargetPosition(1, int(best_f * 1000))
print(f'Moved to Focus: {best_f:.2f}')    
plt.show()
# === Clean Exit ===
sn.closeDevice(0)