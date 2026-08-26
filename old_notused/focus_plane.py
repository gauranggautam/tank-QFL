import numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as mticker
import time, os, AMC
from snAPI.Main import *

# === Focus scan CONFIG ===
FOCUS_STEP = 0.1         # Focus scan step in µm
FOCUS_RANGE = 5 # ± range from current focus

timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
out_dir = './PlotBasic/Output/FocusPlane'
os.makedirs(out_dir, exist_ok=True)

# === AMC Init ===
amc = AMC.Device('amc100num-a01-0248.local')
amc.connect()
for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)

x_now = amc.move.getPosition(0) / 1000
y_now = amc.move.getPosition(2) / 1000
f_now = amc.move.getPosition(1) / 1000

(x1,y1,f1) = (0,0,f_now)
(x2,y2,f2) = (0,0,f_now)
(x3,y3,f3) = (0,0,f_now)

#F range
f_START, f_END = f_now - FOCUS_RANGE, f_now + FOCUS_RANGE

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

# === Wait Until Stable ===
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
        
   
        
# Best focus at three points:

focus_range = np.arange(f_now - FOCUS_RANGE, f_now + FOCUS_RANGE + FOCUS_STEP, FOCUS_STEP)
counts = []
max_cf1, best_f1= 0, f_now


fig, ax = plt.subplots()
plt.figure(figsize=(6, 4))
plt.title("Focus sweep")
plt.xlabel("Focus (µm)")
plt.ylabel("Counts")
plt.grid(True)
plt.tight_layout()
plt.show()


mark=1
print("\nMoving to mark 1...")
amc.move.setControlTargetPosition(0, int(x1 * 1000))
amc.move.setControlTargetPosition(0, int(y1 * 1000))
wait_until_stable()
print("\nSweeping focus at mark 1...")

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
        print(f'Best Focus mark 1{mark}: {best_f:.2f}') 
        

mark=2
ax_cf2, best_f2= 0, f_now
print("\nMoving to mark 2...")
amc.move.setControlTargetPosition(0, int(x1 * 1000))
amc.move.setControlTargetPosition(0, int(y1 * 1000))
wait_until_stable()
print("\nSweeping focus at mark 2...")


for f in focus_range:
    amc.move.setControlTargetPosition(1, int(f * 1000))
    wait_until_stable()
    cnt = sn.getCountRates()
    
    total = cnt[d1] + cnt[d2]
    plt.plot(focus_range, counts, marker='o', color='blue')
    f_act= amc.move.getPosition(1) / 1000
    #print(f'Focus {f:.2f} µm -> {total} cps')
    
    if total > max_cf:
        max_cf, best_f= total, f_act
        print(f'Best Focus for mark {mark}: {best_f:.2f}') 


mark=3
max_cf3, best_f3= 0, f_now
print("\nMoving to mark 3...")
amc.move.setControlTargetPosition(0, int(x3 * 1000))
amc.move.setControlTargetPosition(0, int(y3 * 1000))
wait_until_stable()
print("\nSweeping focus at mark 3...")
for f in focus_range:
    amc.move.setControlTargetPosition(1, int(f * 1000))
    wait_until_stable()
    cnt = sn.getCountRates()
    total = cnt[d1] + cnt[d2]
    ax.plot(focus_range, counts, marker='o', color='green', label='')
    f_act= amc.move.getPosition(1) / 1000
    #print(f'Focus {f:.2f} µm -> {total} cps')
    
    if total > max_cf:
        max_cf, best_f= total, f_act
        print(f'Best Focus mark 1{mark}: {best_f:.2f}') 