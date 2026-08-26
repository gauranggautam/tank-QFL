from QFLv4 import *

def main():
    scan_jobs = [
        {
            'center_x': -898, 'center_y': 2651, 'center_f': 118.9,
            'x_size': 35, 'y_size': 35, 'step': 0.2,
            'comment': 'Flake I18'
        },         
        {
            'center_x': -1200, 'center_y': 2258, 'center_f': 107.8,
            'x_size': 30, 'y_size': 30, 'step': 0.2,
            'comment': 'Flake K17'
        }, 
        {
            'center_x': -1491, 'center_y': 2291, 'center_f': 99.6,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake K16'
        },                
        {
            'center_x': -210 , 'center_y': 2541, 'center_f': 156.19,
            'x_size': 30, 'y_size': 25, 'step': 0.2,
            'comment': 'Flake J20'
        },
        {
            'center_x': -1641, 'center_y': 1651, 'center_f': 108.20,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake M15'
        },
        {
            'center_x': -2699, 'center_y': 1255, 'center_f':  76.2,
            'x_size': 25, 'y_size': 25, 'step': 0.2,
            'comment': 'Flake M12'
        },                   
        {
            'center_x': -3752, 'center_y': 305, 'center_f': 40.8,
            'x_size': 30, 'y_size': 30, 'step': 0.2,
            'comment': 'Flake N8'
        },
        {
            'center_x': -1478, 'center_y': 1390, 'center_f': 115.2,
            'x_size': 45, 'y_size': 45, 'step': 0.2,
            'comment': 'Flake N16'
        },     
        {
            'center_x': -2088, 'center_y': 997, 'center_f':  95.8,
            'x_size': 50, 'y_size': 50, 'step': 0.2,
            'comment': 'Flake O14'
        }             
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
                # --- FIX #2: Pass the existing handles into the scan function ---
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
                    f_size=100,
                    amc=amc,
                    sn=sn,
                    d1=d1,
                    d2=d2
                )
                time.sleep(5)
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