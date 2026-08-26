import numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as mticker
import time, os, AMC
from snAPI.Main import *

# === CONFIG ===
FOCUS_ONLY_MODE = True  # Set to True to skip scan and only do focus sweep
SC_SIZE = 1              # Scan area half-size in µm
STEP = 0.1               # Scan step in µm
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

X_START, X_END = x_now - SC_SIZE, x_now + SC_SIZE
Y_START, Y_END = y_now - SC_SIZE, y_now + SC_SIZE

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
def wait_until_stable(axx=None):
    timeout=10
    start = time.time()
    while True:
        if amc.status.getStatusMoving(axx) == 0 and \
           amc.status.getStatusTargetRange(axx):
            break
        amc.control.setControlOutput(axx, True); amc.control.setControlMove(axx, True)
        if time.time() - start > timeout:
            print("Timeout waiting for stage"); break
        time.sleep(0.01)
# === Full Mapping Mode ===
if not FOCUS_ONLY_MODE:
    x_pos = np.arange(X_START, X_END + STEP, STEP)
    y_pos = np.arange(Y_START, Y_END + STEP, STEP)
    Z = np.zeros((len(y_pos), len(x_pos)), dtype=float)
    extent = [X_START, X_END, Y_START, Y_END]
    global_max = 1
    max_int, max_cf, best_x, best_y = 0, 0, X_START, Y_START

    # === Plot Init ===
    plt.ion()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    img = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto', vmin=0, vmax=1)
    cb = fig.colorbar(img, ax=ax1, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))
    ax1.set_title("PL Mapping – Raw Counts")
    ax1.set_xlabel("X (µm)"); ax1.set_ylabel("Y (µm)")

    data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')
    with open(data_file, 'w') as f:
        f.write(f'# PL Mapping - {timestamp}\n')
        f.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')

    total_points = len(x_pos) * len(y_pos)
    point_counter = 0
    start_time = time.time()

    # === Start Scan ===
    for i, x in enumerate(x_pos):
        amc.move.setControlTargetPosition(0, int(x * 1000))
        wait_until_stable(axx=0)
        for j, y in enumerate(y_pos):
            try:
                amc.move.setControlTargetPosition(2, int(y * 1000))
                wait_until_stable(axx=2)

                x_act = amc.move.getPosition(0) / 1000
                y_act = amc.move.getPosition(2) / 1000
                cnt = sn.getCountRates()
                total = cnt[d1] + cnt[d2]
                Z[j, i] = total

                if total > max_int:
                    max_int, best_x, best_y = total, x_act, y_act

                with open(data_file, 'a') as f:
                    f.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

                # Update plot
                global_max = max(global_max, total)
                img.set_data(Z)
                img.set_clim(vmin=0, vmax=global_max)
                cb.update_normal(img)
                ax1.set_title(f'PL Map – Max: {max_int:.0f} at ({best_x:.2f}, {best_y:.2f})')
                plt.pause(0.01)

                # ETA
                point_counter += 1
                elapsed = time.time() - start_time
                rem = (elapsed / point_counter) * (total_points - point_counter)
                m, s = divmod(int(rem), 60)
                print(f'{point_counter}/{total_points} pts | ETA: {m}m {s}s', end='\r')

            except Exception as e:
                print(f'\nError at ({x:.2f}, {y:.2f}): {e}')
        

    amc.move.setControlTargetPosition(0, int(best_x * 1000))
    amc.move.setControlTargetPosition(2, int(best_y * 1000))
    wait_until_stable()
    print(f'\nMoved to max point: ({best_x:.2f}, {best_y:.2f})')
    plt.ioff()
    plt.savefig(os.path.join(out_dir, f'plmap_plot_{timestamp}.png'))
    plt.show()

else:
    best_x, best_y = x_now, y_now
    amc.move.setControlTargetPosition(0, int(best_x * 1000))
    amc.move.setControlTargetPosition(2, int(best_y * 1000))
    wait_until_stable([0,1,2])
    print(f'\nFocus-only mode at current pos: ({best_x:.2f}, {best_y:.2f})')

# === FOCUS SWEEP ===
for a in [1]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
for a in [0, 2]: amc.control.setControlMove(a, False)
focus_range = np.arange(f_now - FOCUS_RANGE, f_now + FOCUS_RANGE + FOCUS_STEP, FOCUS_STEP)
counts = []
max_cf, best_f= 0, f_now

print("\nSweeping focus...")
for f in focus_range:
    amc.move.setControlTargetPosition(1, int(f * 1000))
    wait_until_stable(axx=1)
    cnt = sn.getCountRates()
    total = cnt[d1] + cnt[d2]
    counts.append(total)
    f_act= amc.move.getPosition(1) / 1000
    #print(f'Focus {f:.2f} µm -> {total} cps')
    
    if total > max_cf:
        max_cf, best_f= total, f_act
        print(f'Best Focus: {best_f:.2f}')    

amc.move.setControlTargetPosition(1, int(best_f * 1000))
print(f'Moved to Focus: {best_f:.2f}')    

focus_file = os.path.join(out_dir, f'focus_sweep_{timestamp}.txt')
with open(focus_file, 'w') as f:
    f.write('# Focus\tCount\n')
    for fval, c in zip(focus_range, counts):
        f.write(f'{fval:.3f}\t{c}\n')

# === Plot Focus Curve ===
plt.figure(figsize=(6, 4))
plt.plot(focus_range, counts, marker='o', color='purple')
plt.title("Focus Optimization")
plt.xlabel("Focus (µm)")
plt.ylabel("Counts")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, f'focus_curve_{timestamp}.png'))
plt.show()

# === Clean Exit ===
sn.closeDevice(0)
amc.close()
print("\nAll done.")
