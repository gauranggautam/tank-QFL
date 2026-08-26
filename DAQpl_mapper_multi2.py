import matplotlib.pyplot as plt
from QFLv4 import *

def main():
    scan_jobs = [
        {
            'center_x': 710, 'center_y': -1009, 'center_f': -10.74,
            'x_size': 20, 'y_size': 20, 'step': 0.2,
            'comment': 'Flake P12'
        },
        {
            'center_x': 1257, 'center_y': -1576, 'center_f': -16.44,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake R14'
        },
        {
            'center_x': 1066, 'center_y': -1539, 'center_f': -13.07,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake R13'
        },
        {
            'center_x': -2585, 'center_y': -1873, 'center_f': 30.86,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake S1'
        },
        {
            'center_x': 1832, 'center_y': -1944, 'center_f': -25.94,
            'x_size': 30, 'y_size': 30, 'step': 0.2,
            'comment': 'Flake S16'
        },
        {
            'center_x': -2417, 'center_y': -2013, 'center_f': 28.66,
            'x_size': 30, 'y_size': 30, 'step': 0.2,
            'comment': 'Flake T2THIN'
        },
        {
            'center_x': -2414, 'center_y': -2108, 'center_f': 27.66,
            'x_size': 20, 'y_size': 20, 'step': 0.2,
            'comment': 'Flake T2THICK'
        }
    ]
    amc = None
    daq, ch1, ch2 = None, None, None

    try:
        print("Initializing devices for the batch run...")
        amc = start_attocube()
        daq, ch1, ch2 = start_daq()

        # Abort if devices fail to start
        if amc is None or daq is None:
            raise ConnectionError("Failed to initialize hardware. Aborting batch.")

        print(f"Starting batch of {len(scan_jobs)} PL scans...")
        for i, params in enumerate(scan_jobs):
            print(f"\n--- Running Scan Job {i+1}/{len(scan_jobs)} ({params.get('comment', 'No comment')}) ---")
            print(f"Parameters: {params}")
            
            try:
                # --- FIX #2: Pass the existing handles into the scan function ---
                run_pl_scan_daq(
                    center_x=params['center_x'],
                    center_y=params['center_y'],
                    center_f=params['center_f'],
                    x_size=params['x_size'],
                    y_size=params['y_size'],
                    step=params['step'],
                    show_plot=False,
                    logz=False,
                    focus_sweep=False,
                    amc=amc,
                    daq=daq,
                    ch1=ch1,
                    ch2=ch2
                )
                time.sleep(10)
            except Exception as e:
                print(f"!!! An error occurred during scan job {i+1}: {e} !!!")
                print("Continuing with the next job.")

        print("\nAll scan jobs are complete.")

    finally:
 
        print("\n--- Cleaning up and closing all devices. ---")
        if amc:
            close_device_all(amc=amc)
        if daq:
            close_device_all(daq=daq, t_ch1=ch1, t_ch2=ch2)
        print("Cleanup complete.")


if __name__ == '__main__':
    main()