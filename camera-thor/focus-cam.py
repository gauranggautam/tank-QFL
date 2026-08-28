import sys
import os
import time

# === FIX FOR FORTRAN/MKL CTRL+C CRASH ===
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

import numpy as np
import matplotlib.pyplot as plt

# === Path Setup for QFLv4 ===
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
    
import windows_setup
windows_setup.configure_path()

from QFLv4 import *
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK

def get_peak_intensity(image_array):
    """
    Collapses 3D arrays to 2D grayscale and finds the absolute brightest pixel.
    """
    if image_array.ndim == 3:
        gray_img = np.mean(image_array, axis=2)
    else:
        gray_img = image_array
        
    max_val = float(np.max(gray_img))
    max_coords = np.unravel_index(np.argmax(gray_img), gray_img.shape)
    
    return max_val, max_coords, gray_img

def run_camera_focus_sweep(center_f=None, f_size=10.0, step=1.0,
                           camera_serial="11484", exposure_us=100000, 
                           out_dir_base=r'D:\Data_Python_PL\PLmaps',
                           move_to_best=True, post_sweep_live_feed=True,
                           amc=None):
    amc_local = False
    data_file_handle = None
    best_f = None
    aborted = False

    try:
        # === 1. Start AMC ===
        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        fnow = center_f if center_f is not None else amc.move.getPosition(1) / 1000
        center_f = fnow
        best_f = center_f  

        # Setup Output Directories
        out_dir = output_dir_folder(base_dir=out_dir_base)

        # Setup Real-time Plotting
        plt.ion()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        f_start, f_end = center_f - (f_size / 2), center_f + (f_size / 2)
        f_pos = np.arange(f_start, f_end + step, step)
        intensity_data = np.zeros(len(f_pos), dtype=float)
        
        line1, = ax1.plot(f_pos, intensity_data, 'b-o', markersize=4)
        ax1.set_xlabel('F / Z (µm)')
        ax1.set_ylabel('Max Single-Pixel Intensity')
        ax1.set_title('Focus Sweep Curve')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        img_display = None
        ax2.set_title('Live Camera Feed')
        ax2.axis('off')
        fig.tight_layout()

        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        plot_file = os.path.join(out_dir, f'cam_focus_plot_{timestamp}.png')
        data_file = os.path.join(out_dir, f'cam_focus_data_{timestamp}.txt')

        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# Camera Focus Sweep - {timestamp}\n# Center F: {center_f}\n')
        data_file_handle.write('# f_req\tf_act\tintensity\tmax_x\tmax_y\n')

        # === 2. Start Camera inside Context Managers ===
        with TLCameraSDK() as sdk:
            available_cameras = sdk.discover_available_cameras()
            if not available_cameras: raise ConnectionError("No Thorlabs cameras found!")
            
            target_serial = next((cam for cam in available_cameras if camera_serial in cam), available_cameras[0])
            
            with sdk.open_camera(target_serial) as camera:
                camera.exposure_time_us = exposure_us
                camera.frames_per_trigger_zero_for_unlimited = 1

                # === 3. THE DUMMY FRAME FIX ===
                print("\nClearing stale hardware buffers...")
                camera.arm(frames_to_buffer=1)
                camera.issue_software_trigger()
                time.sleep(0.2)
                _ = camera.get_pending_frame_or_null() # Throw away the bad first frame
                camera.disarm()
                time.sleep(0.1)

                max_int = -1
                total_points = len(f_pos)
                point_counter = 0

                print(f"--- Starting Sweep ({f_start:.2f} µm to {f_end:.2f} µm) ---")

                # === SWEEP LOOP ===
                for i, y in enumerate(f_pos):
                    amc.move.setControlTargetPosition(1, int(y * 1000))
                    wait_until_stable(amc, axis=1)
                    time.sleep(0.3) 

                    f_act = amc.move.getPosition(1) / 1000
                    
                    camera.arm(frames_to_buffer=1)
                    camera.issue_software_trigger()
                    
                    frame = None
                    attempts = 0
                    while frame is None and attempts < 15:
                        time.sleep(0.1) 
                        frame = camera.get_pending_frame_or_null()
                        attempts += 1
                    
                    if frame is None:
                        print(f"Warning: Frame missing at Z={f_act:.2f} µm")
                        intensity, coords, process_img = 0, (0, 0), np.zeros((10, 10))
                    else:
                        imagem = np.asarray(frame.image_buffer)
                        intensity, coords, process_img = get_peak_intensity(imagem)
                    
                    camera.disarm()

                    intensity_data[i] = intensity
                    if intensity > max_int:
                        max_int, best_f = intensity, f_act

                    max_y, max_x = coords
                    data_file_handle.write(f'{y:.3f}\t{f_act:.3f}\t{intensity:.2f}\t{max_x}\t{max_y}\n')
                    data_file_handle.flush()

                    point_counter += 1
                    print(f'Scan: {point_counter}/{total_points} | Z: {f_act:.2f} | Peak: {intensity:.0f} at X:{max_x}, Y:{max_y}', end='\r')

                    line1.set_ydata(intensity_data)
                    ax1.relim()
                    ax1.autoscale_view()
                    ax1.set_title(f'Focus Sweep – Max: {max_int:.0f} @({best_f:.2f} µm)')
                    
                    # VISIBILITY IMPROVEMENT
                    if img_display is None:
                        img_display = ax2.imshow(process_img, cmap='gray', vmin=0)
                    else:
                        img_display.set_data(process_img)
                        # dynamically track the peak without washing out dim lasers
                        vmax_val = max(10, process_img.max()) 
                        img_display.set_clim(vmin=0, vmax=vmax_val)
                        
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                print("\n\nScan complete.")
                
                # === MOVE TO BEST FOCUS ===
                target_f = best_f if move_to_best else center_f
                print(f"Moving to target focus position: {target_f:.2f} µm...")
                amc.move.setControlTargetPosition(1, int(target_f * 1000))
                wait_until_stable(amc, axis=1)
                time.sleep(0.3)

                # === LIVE FEED ===
                if post_sweep_live_feed:
                    print(f"\n[LIVE FEED ACTIVE] Stage parked at {target_f:.2f} µm.")
                    print(">>> PRESS 'CTRL+C' IN THE TERMINAL TO STOP AND CLOSE <<<")
                    
                    ax1.set_title(f'Sweep Finished – Parked at {target_f:.2f} µm')
                    
                    try:
                        while True:
                            camera.arm(frames_to_buffer=1)
                            camera.issue_software_trigger()
                            
                            frame = None
                            attempts = 0
                            while frame is None and attempts < 10:
                                time.sleep(0.05)
                                frame = camera.get_pending_frame_or_null()
                                attempts += 1
                            
                            if frame is not None:
                                imagem = np.asarray(frame.image_buffer)
                                intensity, coords, process_img = get_peak_intensity(imagem)
                                
                                img_display.set_data(process_img)
                                vmax_val = max(10, process_img.max())
                                img_display.set_clim(vmin=0, vmax=vmax_val)
                                ax2.set_title(f'Live Camera | Peak: {intensity:.0f}')
                                
                                fig.canvas.draw()
                                fig.canvas.flush_events()
                                
                            camera.disarm()
                    except KeyboardInterrupt:
                        print("\nKeyboard Interrupt received. Closing live feed...")
                        aborted = True

    except Exception as e:
        print(f"\nA critical error occurred: {e}")
        aborted = True
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt received during sweep.")
        aborted = True
    finally:
        print("\n--- Cleaning up resources ---")
        plt.ioff()
        if not aborted:
            plt.savefig(plot_file)
            print(f"Plot saved to: {plot_file}")
            
        plt.close('all') 
        if data_file_handle: data_file_handle.close()
        if amc_local and amc:
            try: amc.close() 
            except AttributeError: pass

    return best_f

if __name__ == "__main__":
    run_camera_focus_sweep(f_size=20.0, step=0.1)