import os
import time
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

# Make sure this import is available in your main script
from QFLv5 import start_apds

def g2_measure(time_m=300, save_figure=True, sn=None, detector_config=2, det_ch1=None, det_ch2=None, binsize_ps=100, windowsize_ps=100000):
    """
    Performs a live g(2) cross-correlation measurement.
    Wrapped in a kernel-safe structure to prevent memory leaks and DLL locks.
    """
    sn_local = False
    succ = False
    end_time = time.time() # Fallback
    start_time = time.time()
    
    try:
        # === 1. Device Initialization ===
        if sn is None:
            # detector_config = 1 for Excieltas and 2 for MPDs
            result = start_apds(detector_config=detector_config)
            if result[0] is None: 
                raise ConnectionError("Failed to start APDs.")
            
            sn = result[0]
            a = result[1]
            b = result[2]
            sn_local = True
        else:
            # If an existing sn object is passed, use the provided channels
            a = det_ch1
            b = det_ch2
            if a is None or b is None:
                raise ValueError("If passing an existing 'sn', you must specify det_ch1 and det_ch2.")

        mt = time_m 
        
        # === 2. File Setup ===
        output_dir = r'D:\Data_Python_PL\G2data'
        os.makedirs(output_dir, exist_ok=True)
        dtnow = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        ptuo = f'g2data_{mt:.0f}s_{dtnow}.ptu' 
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
        
        # Pre-allocate plot lines (avoids using .clear() and leaking memory)
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
                time.sleep(0.5) 
                
                try:
                    finished = sn.correlation.isFinished()
                    g2, lagtimes = sn.correlation.getG2Data()
                except Exception:
                    continue # Skip loop safely if hardware is busy
                    
                lagtimes_ns = np.array(lagtimes) * 1e9
                
                if len(g2) == 0:
                    if finished: break
                    continue
                    
                g2_zero = np.min(g2)
                
                # Fetch count rates
                cnts = sn.getCountRates()
                cntss = cnts[a] + cnts[b]
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
                    
                    axes[0].relim()
                    axes[0].autoscale_view(True, True, True)
                    axes[0].set_ylim(0, max(0.1, np.max(g2) * 1.1))
                    axes[0].set_title(f'g2(t) Correlation (BinWidth = {d} ps & WindowSize = {int(c/1000):.0f} ns) g2(0)={g2_zero: .2f}')
                    
                    axes[1].relim()
                    axes[1].autoscale_view(True, True, True)
                    axes[1].set_ylim(0, max(max(ch1_counts, default=1), max(ch2_counts, default=1)) * 1.2)
                    
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
    finally:
        if sn is not None:
            try:
                sn.correlation.stopMeasure()
                print("Measurement stopped")
            except Exception as stop_err:
                print(f"Warning during stopMeasure: {stop_err}")
        if sn_local and sn is not None:
            try:
                sn.closeDevice(allDevices=True)
                print("Device closed successfully.")
            except Exception as e:
                print(f"Error closing device: {e}")
        plt.ioff()
        plt.show()