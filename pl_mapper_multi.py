import matplotlib.pyplot as plt
from QFLv4 import *

def main():
    scan_jobs = [
        {
            'center_x': -2430, 
            'center_y': 10, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '11'
        },
        {
            'center_x': -2410, 
            'center_y': 10, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '21'
        },
        {
            'center_x': -2390, 
            'center_y': 10, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '31'
        },
        {
            'center_x': -2430, 
            'center_y': -10, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '11'
        },
        {
            'center_x': -2410, 
            'center_y': -10, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '21'
        },
        {
            'center_x': -2390, 
            'center_y': -10, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '31'
        },
        {
            'center_x': -2430, 
            'center_y': -30, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '11'
        },
        {
            'center_x': -2410, 
            'center_y': -30, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '21'
        },
        {
            'center_x': -2390, 
            'center_y': -30, 
            'center_f': 20,
            'x_size': 20, 'y_size':20, 'step': 0.3,
            'comment': '31'
        },
    ]
    amc = None
    sn, d1, d2 = None, None, None

    try:
        print("Initializing devices for the batch run...")
        amc = start_attocube()
        sn, d1, d2 = start_apds(detector_config=2)

        # Abort if devices fail to start
        if amc is None or sn is None:
            raise ConnectionError("Failed to initialize hardware. Aborting batch.")

        print(f"Starting batch of {len(scan_jobs)} PL scans...")
        for i, params in enumerate(scan_jobs):
            print(f"\n--- Running Scan Job {i+1}/{len(scan_jobs)} ({params.get('comment', 'No comment')}) ---")
            print(f"Parameters: {params}")
            
            try:
                # ---
                run_pl_scan(
                    center_x=params['center_x'],
                    center_y=params['center_y'],
                    center_f=params['center_f'],
                    x_size=params['x_size'],
                    y_size=params['y_size'],
                    step=params['step'],
                    detector_config=2,
                    show_plot=False,
                    logz=False,
                    focus_sweep=True,
                    f_size=50,
                    amc=amc,
                    sn=sn,
                    d1=d1,
                    d2=d2
                )
                time.sleep(10)
            except Exception as e:
                print(f"!!! An error occurred during scan job {i+1}: {e} !!!")
                print("Continuing with the next job.")

        print("\nAll scan jobs are complete.")

    finally:
 
        print("\n--- Cleaning up and closing all devices. ---")
        if amc or sn:
            close_device_all(amc=amc, sn=sn)
        print("Cleanup complete.")


if __name__ == '__main__':
    main()
