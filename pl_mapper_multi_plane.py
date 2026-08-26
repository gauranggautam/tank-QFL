import matplotlib.pyplot as plt
from QFLv3 import *

def main():
    a,b,c=-0.015608478000000014,-0.00199193599999998,48.425097528718325
    
    scan_jobs = [
        {
            'center_x': -1975, 'center_y': 1360, 'center_f': 82.5,
            'x_size': 20, 'y_size': 20, 'step': 0.2,
            'comment': 'Flake D3'
        },
        {
            'center_x': 302, 'center_y': 1065, 'center_f': 44.5,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake F10'
        },
        {
            'center_x': 1543, 'center_y': 761, 'center_f': 27.5,
            'x_size': 30, 'y_size': 30, 'step': 0.2,
            'comment': 'Flake H14'
        },
        {
            'center_x': 235, 'center_y': -410, 'center_f': 55.10,
            'x_size': 50, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake K10'
        },
        {
            'center_x': 1275, 'center_y': -255, 'center_f': 37.5,
            'x_size': 40, 'y_size': 40, 'step': 0.2,
            'comment': 'Flake K13L'
        },
        {
            'center_x': 1423, 'center_y': -183, 'center_f': 36,
            'x_size': 20, 'y_size': 20, 'step': 0.2,
            'comment': 'Flake K13R_Thin'
        },
        {
            'center_x': 2445, 'center_y': -338, 'center_f': 18.8,
            'x_size': 20, 'y_size': 20, 'step': 0.2,
            'comment': 'Flake K17'
        },
        {
            'center_x': 2781, 'center_y': -2181, 'center_f': 26.3,
            'x_size': 30, 'y_size': 30, 'step': 0.2,
            'comment': 'Flake R17'
        }
    ]
    print(f"Starting batch of {len(scan_jobs)} PL scans...")
    for i, params in enumerate(scan_jobs):
        print(f"\n--- Running Scan Job {i+1}/{len(scan_jobs)} ({params.get('comment', 'No comment')}) ---")
        print(f"Parameters: {params}")
        
        try:
            run_pl_scan_focusplanemodel(
                center_x=params['center_x'],
                center_y=params['center_y'],
                x_size=params['x_size'],
                y_size=params['y_size'],
                step=params['step'],
                detector_config=2, 
                logz=False,
                out_dir_base='C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/PLmaps_autofocus',
                show_plot=False,
                amc=None,
                sn=None,
                plane_coeffs=(a,b,c)
            )
        except Exception as e:
            print(f"!!! An error occurred during scan job {i+1}: {e} !!!")
            print("Continuing with the next job.")

    print("\nAll scan jobs are complete.")

if __name__ == '__main__':
    main()

