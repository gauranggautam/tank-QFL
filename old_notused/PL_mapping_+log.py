import numpy as np, matplotlib.pyplot as plt, matplotlib.ticker as mticker
import time, os, AMC
from snAPI.Main import *

# === Config ===
X_START, X_END, Y_START, Y_END, STEP = -20, 20, -20, 20, 1
timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
out_dir = './PlotBasic/Output/PLmaps'
os.makedirs(out_dir, exist_ok=True)

# === Init Devices ===
sn = snAPI(libType=LibType.MH)
sn.closeDevice()
if not sn.getDevice(0): print('MH not found'); exit()
sn.setLogLevel(LogLevel.Device, False)
sn.setLogLevel(LogLevel.Api, False)
sn.initDevice(MeasMode.T2)

# === Detector Configuration ===
Detectors = 2
if Detectors == 1:
    d1, d2 = 1, 2
    sn.loadIniConfig(r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\Exciletas_MH.ini')
else:
    d1, d2 = 3, 4
    sn.loadIniConfig(r'C:\Users\iq-qfl\Documents\Gaurang\Codes\user_configs_snAPI\MPDs_MH.ini')

# === AMC Init ===
amc = AMC.Device('amc100num-a01-0248.local')
amc.connect()
for a in [0, 1, 2]: amc.control.setControlOutput(a, True); amc.control.setControlMove(a, True)
#amc.control.setControlOutput(1, False); amc.control.setControlMove(1, False)

# === Grid Setup ===
x_pos = np.arange(X_START, X_END + STEP, STEP)
y_pos = np.arange(Y_START, Y_END + STEP, STEP)
Z = np.zeros((len(y_pos), len(x_pos)), dtype=float)
Zlog = np.zeros_like(Z)
extent = [X_START, X_END, Y_START, Y_END]

# === Plot Init ===
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

img1 = ax1.imshow(Z, cmap='plasma', origin='lower', extent=extent, aspect='auto', vmin=0, vmax=1)
img2 = ax2.imshow(Zlog, cmap='plasma', origin='lower', extent=extent, aspect='auto', vmin=0, vmax=1)

cb1 = fig.colorbar(img1, ax=ax1, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))
cb2 = fig.colorbar(img2, ax=ax2, format=mticker.FuncFormatter(lambda x, _: f'{x / 1000:.1f}k' if x >= 1000 else str(int(x))))

for ax in [ax1, ax2]:
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    ax.set_xlim(X_START, X_END)
    ax.set_ylim(Y_START, Y_END)
    ax.invert_xaxis()
    ax.invert_yaxis()

ax1.set_title('PL map - Raw counts')
ax2.set_title('PL map - Log counts')

# === Output Files ===
plot_file = os.path.join(out_dir, f'plmap_plot_{timestamp}.png')
data_file = os.path.join(out_dir, f'plmap_data_{timestamp}.txt')

#os.system('cls' if os.name == 'nt' else 'clear')
print(f'using file name: {data_file}')
      
with open(data_file, 'w') as f:
    f.write(f'# PL Mapping - {timestamp}\n')
    f.write('# x_req\ty_req\tx_act\ty_act\tcount1\tcount2\ttotal\n')
# === Wait Helper ===
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
# === Scan ===
max_int, best_x, best_y = 0, X_START, Y_START
global_max = 1
total_points = len(x_pos) * len(y_pos)
point_counter = 0
start_time = time.time()

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
            Zlog[j, i] = np.log10(total + 1)

            if total > max_int:
                max_int, best_x, best_y = total, x_act, y_act
            # === Write to tab-delimited file ===
            with open(data_file, 'a') as f:
                f.write(f'{x:.3f}\t{y:.3f}\t{x_act:.3f}\t{y_act:.3f}\t{cnt[d1]}\t{cnt[d2]}\t{total}\n')

            # === Global max color scaling ===
            global_max = max(global_max, total)
            global_log_max = np.log10(global_max + 1)

            img1.set_data(Z)
            img2.set_data(Zlog)
            img1.set_clim(vmin=0, vmax=global_max)
            img2.set_clim(vmin=0, vmax=global_log_max)
            cb1.update_normal(img1)
            cb2.update_normal(img2)
            ax1.set_title(f'PL Map (Linear) – Max: {max_int:.0f} at ({best_x:.2f}, {best_y:.2f})')
            plt.pause(0.01)
            # === ETA ===
            point_counter += 1
            elapsed = time.time() - start_time
            avg_time = elapsed / point_counter
            rem = avg_time * (total_points - point_counter)
            mins, secs = divmod(int(rem), 60)
            print(f'Scan progress: {point_counter}/{total_points} | ETA: {mins}m {secs}s', end='\r')
        except Exception as e:
            print(f'\nError at ({x:.2f}, {y:.2f}): {e}')
# === Finish ===
plt.ioff()
plt.savefig(plot_file)
plt.show()
sn.closeDevice(0)
for a in [0, 1, 2]:
    amc.control.setControlOutput(a, True)
    amc.control.setControlMove(a, True)
amc.close()
