from QFLv5 import *
def estimate_lifetime(time_bins_ns, hist_data):
    """
    Estimates the photoluminescence lifetime (tau) using a simple 
    monoexponential tail fit: y(t) = A * exp(-t / tau) + C
    """
    if len(hist_data) < 100 or np.max(hist_data) < 10:
        return 0.0
    
    i_peak = int(np.argmax(hist_data))
    y_peak = float(hist_data[i_peak])
    
    # 1. Avoid Instrument Response Function (IRF) by starting the fit 
    # after the peak has dropped to 70% of its maximum value.
    thr = 0.7 * y_peak
    post_peak_indices = np.arange(i_peak, len(hist_data))
    below_thresh = post_peak_indices[hist_data[post_peak_indices] <= thr]
    
    i0 = int(below_thresh[0]) if len(below_thresh) > 0 else i_peak + 1
    if i0 >= len(hist_data): return 0.0
    
    # 2. Estimate the background (C) using the median of the tail end (last 15%)
    n_tail = max(10, int(len(hist_data) * 0.15))
    C = np.median(hist_data[-n_tail:])
    
    # 3. Extract the fitting region and subtract the background
    t_fit = time_bins_ns[i0:]
    y_fit = hist_data[i0:] - C
    
    # 4. Keep only strictly positive values for logarithms
    valid_mask = y_fit > 1e-12
    if np.sum(valid_mask) < 10: return 0.0
    
    x = t_fit[valid_mask]
    x = x - x[0] # Shift time to start at 0 for the fit
    ln_y = np.log(y_fit[valid_mask])
    
    # 5. Calculate Linear Regression: ln(y) = (-1/tau) * x + ln(A)
    xbar, ybar = x.mean(), ln_y.mean()
    Sxx = np.sum((x - xbar)**2)
    Sxy = np.sum((x - xbar)*(ln_y - ybar))
    
    if Sxx == 0: return 0.0
    slope = Sxy / Sxx
    
    if slope >= 0: return 0.0 # Prevent negative lifetimes if curve is rising
    
    tau = -1.0 / slope
    return tau

def trpl_measure(time_m=60, sync_offset=0,save_figure=True, sn=None, detector_config=3, binnums=65536,binsize_ps=5):
    """
    Performs a Dual-Channel Time-Resolved Photoluminescence (TRPL) measurement.
    Plots histograms side-by-side with live lifetime estimations.
    """
    sn_local = False
    succ = False
    start_time = time.time()
    
    try:
        # === 1. Device Initialization ===
        if sn is None:
            result = start_apds(detector_config=detector_config)
            if result[0] is None: raise ConnectionError("Failed to start APDs.")
            
            sn = result[0]
            if len(result) == 4:
                _, sync_ch, det_ch1, det_ch2 = result 
            sn_local = True
            
        mt = time_m 
        
        # === 2. File Setup ===
        output_dir = r'D:\Data_Python_PL\TRPLdata'
        os.makedirs(output_dir, exist_ok=True)
        dtnow = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        ptuo = f'trpldata_{mt:.0f}s_{dtnow}.ptu'
        trpl_filename = os.path.join(output_dir, ptuo)
        sn.setPTUFilePath(trpl_filename)
        
        # === 3. Start Measurement ===
        sn.histogram.setRefChannel(sync_ch)
        sn.histogram.setBinWidth(binsize_ps)
        sn.histogram.setNumBins(binnums)
        sn.device.setSyncChannelOffset(sync_offset)
        # Leaving NumBins at default (65536) to prevent 'False' rejection
        
        sn.histogram.measure(int(mt * 1000), waitFinished=False,savePTU=True)

        print(f'MH Device : ({sn.deviceConfig["ID"]}) initialized.')
        print(f'Starting dual-channel TRPL measurement for {mt} s...')

        # === 4. High-Performance Graphing Setup ===
        plt.ion()
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Channel 1 Plot
        line_hist1, = axes[0].plot([], [], label=f'Ch {det_ch1}', linewidth=1.2, color='blue')
        axes[0].set_xlabel('Time (ns)')
        axes[0].set_ylabel('Counts (Log)')
        axes[0].set_yscale('log')
        axes[0].grid(True, which='both', alpha=0.3)
        axes[0].legend(loc='upper right')

        # Channel 2 Plot
        line_hist2, = axes[1].plot([], [], label=f'Ch {det_ch2}', linewidth=1.2, color='red')
        axes[1].set_xlabel('Time (ns)')
        axes[1].set_ylabel('Counts (Log)')
        axes[1].set_yscale('log')
        axes[1].grid(True, which='both', alpha=0.3)
        axes[1].legend(loc='upper right')
        
        fig.tight_layout()
        fig.subplots_adjust(top=0.88) # Make room for main title

        # === 5. Main Measurement Loop ===
        last_plot_time = time.time()

        while True:
            time.sleep(0.5) 
            finished = sn.histogram.isFinished()
            hist_all_channels, time_bins = sn.histogram.getData()
            try:
                # hist_all_channels shape is (5, numBins). Slice out our specific channels.
                hist_data1 = hist_all_channels[det_ch1]
                hist_data2 = hist_all_channels[det_ch2]
            except IndexError:
                print(f"Error: Channels out of bounds.")
                break

            time_bins_ns = np.array(time_bins) / 1000.0 
            elapsed_t = time.time() - start_time
            
            if time.time() - last_plot_time >= 2.0 or finished:
                # Update data
                line_hist1.set_data(time_bins_ns, np.clip(hist_data1, 1, None))
                line_hist2.set_data(time_bins_ns, np.clip(hist_data2, 1, None))
                
                # Estimate lifetimes live
                tau1 = estimate_lifetime(time_bins_ns, hist_data1)
                tau2 = estimate_lifetime(time_bins_ns, hist_data2)
                
                # Rescale and label Plot 1
                axes[0].relim()
                axes[0].autoscale_view(True, True, True)
                axes[0].set_ylim(1, max(10, np.max(hist_data1) * 2))
                axes[0].set_title(f'Ch {det_ch1} TRPL | $\\tau \\approx$ {tau1:.2f} ns')
                
                # Rescale and label Plot 2
                axes[1].relim()
                axes[1].autoscale_view(True, True, True)
                axes[1].set_ylim(1, max(10, np.max(hist_data2) * 2))
                axes[1].set_title(f'Ch {det_ch2} TRPL | $\\tau \\approx$ {tau2:.2f} ns')
                
                # Update Main Title
                fig.suptitle(f'Live TRPL Measurement ({elapsed_t:.0f} / {mt} s)' if not finished else 'TRPL Measurement Completed', fontsize=14, fontweight='bold')
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                last_plot_time = time.time()
                
            if finished:
                succ = True
                break
                
        # Export the final raw text data side-by-side
        if succ:
            txt_filename = os.path.join(output_dir, f"trpldata_{mt:.0f}s_{dtnow}.txt")
            np.savetxt(txt_filename, np.column_stack((time_bins, hist_data1, hist_data2)), 
                       delimiter='\t', header=f"Time(ps)\tCh{det_ch1}_Counts\tCh{det_ch2}_Counts")
            print(f"Raw histogram data saved to: {os.path.basename(txt_filename)}")

        if save_figure:
            figpath = os.path.join(output_dir, f'trplplot_{mt}s_{dtnow}.png')
            try: fig.savefig(figpath)
            except Exception: pass
                
    except Exception as e:
        print(f"\nA critical error occurred: {e}")
    finally:
        if sn_local and sn:
            try: close_device_all(sn=sn)
            except Exception: pass
        plt.ioff()
        plt.show()