from QFLv4 import *

# --- Additional Hardware-Specific Import for Thorlabs KDC ---
try: 
    from pylablib.devices import Thorlabs
except ImportError as e: 
    print(e)

# --- Thorlabs KDC Controller Functions ---

def start_kdc(SN="27257399", kdc=None, force=False):
    """
    Initializes and connects to a Thorlabs Kinesis Motor (rotation mount).
    
    Args:
        SN (str): Serial number of the motor. Defaults to "27257399".
        kdc (Thorlabs.KinesisMotor, optional): Existing KDC motor instance.
        force (bool): If True, forces the motor to home upon starting. Defaults to False.
        
    Returns:
        Thorlabs.KinesisMotor: The connected motor object.
    """
    if kdc is not None:
        return kdc
    else:
        try:
            kdc = Thorlabs.KinesisMotor(SN)
            kdc.open()
            print(f"Homing KDC motor SN: {SN}...")
            kdc.home(force=force)
            print(f"Connected to KDC motor SN: {SN}")
            return kdc
        except Exception as e:
            print(f"ERROR: Failed to connect to KDC motor: {e}")
            return None

def kdc_move_deg(deg, kdc):
    """
    Moves the Thorlabs KDC rotation mount to the specified angle in degrees 
    and waits until movement is complete.
    
    Args:
        deg (float): Target angle in degrees.
        kdc (Thorlabs.KinesisMotor, optional): Existing KDC motor instance.
    """
    kdc_local = False
    if kdc is None:
        kdc = start_kdc()
        kdc_local = True
        
    if kdc is None:
        print("ERROR: KDC motor is not initialized.")
        return

    # Conversion factor: 1 degree = 1919.6418... steps
    step = deg * 1919.6418578623391
    kdc.move_to(step)
    
    # Wait until the motor starts moving (if there's a slight hardware delay)
    time.sleep(0.05)
    
    # Wait until movement completes
    try:
        while kdc.is_moving():
            time.sleep(0.01)
    except Exception:
        # Fallback if is_moving is a property instead of a method depending on pylablib version
        while getattr(kdc, 'is_moving', False):
            time.sleep(0.01)

    if kdc_local and kdc:
        try:
            kdc.close()
        except Exception:
            pass

def kdc_position_deg(kdc):
    """
    Reads the current position of the Thorlabs KDC rotation mount in degrees.
    
    Args:
        kdc (Thorlabs.KinesisMotor, optional): Existing KDC motor instance.
        
    Returns:
        float: Current position in degrees.
    """
    kdc_local = False
    if kdc is None:
        kdc = start_kdc()
        kdc_local = True
        
    if kdc is None:
        print("ERROR: KDC motor is not initialized.")
        return 0.0

    current_steps = kdc.get_position()
    current_deg = current_steps / 1919.6418578623391
    
    if kdc_local and kdc:
        try:
            kdc.close()
        except Exception:
            pass

    return current_deg


# --- Integrated Polarization PL Measurement ---

def run_pl_polarization(start_deg=0, end_deg=360, step_deg=10, 
                        detector_config=2, out_dir_base=r'D:\Data_Python_PL\Polarization',
                        show_plot=True, force_home_kdc=False, kdc=None, amc=None, sn=None, d1=None, d2=None):
    """
    Performs a polarization-dependent PL measurement by sweeping a Thorlabs rotation mount 
    and recording APD count rates at each angle.
    
    Args:
        start_deg (float): Starting angle in degrees.
        end_deg (float): Ending angle in degrees.
        step_deg (float): Angle increment step in degrees.
        detector_config (int): Detector configuration (1 or 2).
        out_dir_base (str): Base directory to save output data and plots.
        show_plot (bool): If True, displays the plot after completion.
        force_home_kdc (bool): If True, passes force=True to start_kdc.
        kdc, amc, sn, d1, d2: Externally managed device handles (optional).
        
    Returns:
        tuple: (angles_deg, counts_total) arrays.
    """
    kdc_local = False
    amc_local = False
    sn_local = False
    data_file_handle = None

    try:
        # === Initialize Devices ===
        if kdc is None:
            kdc = start_kdc(force=force_home_kdc)
            if kdc is None: raise ConnectionError("Failed to start Thorlabs KDC motor.")
            kdc_local = True

        if amc is None:
            amc = start_attocube()
            if amc is None: raise ConnectionError("Failed to start Attocube.")
            amc_local = True

        if sn is None or d1 is None or d2 is None:
            sn, d1, d2 = start_apds(detector_config=detector_config)
            if sn is None: raise ConnectionError("Failed to start APDs.")
            sn_local = True

        # === Setup Output Directory and Files ===
        out_dir = output_dir_folder(base_dir=out_dir_base)
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        data_file = os.path.join(out_dir, f'polarization_data_{timestamp}.txt')
        plot_file = os.path.join(out_dir, f'polarization_plot_{timestamp}.png')

        print(f'Saving polarization data to: {data_file}')
        data_file_handle = open(data_file, 'w')
        data_file_handle.write(f'# Polarization PL Measurement - {timestamp}\n')
        data_file_handle.write('# Req_Angle(deg)\tAct_Angle(deg)\tCount1\tCount2\tTotal\n')

        angles = np.arange(start_deg, end_deg + step_deg, step_deg)
        actual_angles = []
        ch1_counts = []
        ch2_counts = []
        totals = []

        print("\nStarting polarization sweep...")
        for angle in angles:
            # Move polarization stage (passing persistent kdc handle if available)
            kdc_move_deg(angle, kdc=kdc)
            time.sleep(0.2)  # Allow stage to settle
            
            # Read back actual position and counts
            act_angle = kdc_position_deg(kdc=kdc)
            cnt = sn.getCountRates()
            c1, c2 = cnt[d1], cnt[d2]
            total = c1 + c2

            actual_angles.append(act_angle)
            ch1_counts.append(c1)
            ch2_counts.append(c2)
            totals.append(total)

            data_file_handle.write(f'{angle:.2f}\t{act_angle:.2f}\t{c1}\t{c2}\t{total}\n')
            print(f'Angle: {act_angle:.1f}° | Total Counts: {total}', end='\r')

        print("\nPolarization sweep complete.")

        # === Plot Results ===
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(actual_angles, totals, 'bo-', lw=2, label='Total Counts')
        ax.set_xlabel('Polarizer Angle (deg)')
        ax.set_ylabel('Counts (cps)')
        ax.set_title(f'Polarization Dependence | {timestamp}')
        ax.grid(True)
        ax.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")
        
        if show_plot:
            plt.show()
        else:
            plt.close(fig)

        return np.array(actual_angles), np.array(totals)

    except Exception as e:
        print(f"\nA critical error occurred during polarization scan: {e}")
        return None, None
    finally:
        print("\n--- Cleaning up polarization scan resources ---")
        if data_file_handle:
            data_file_handle.close()
        if kdc_local and kdc:
            try:
                kdc.close()
                print("KDC motor closed.")
            except Exception:
                pass
        if sn_local and sn: close_device_all(sn=sn)
        if amc_local and amc: close_device_all(amc=amc)
        
        
        
        
import os
import time
import numpy as np
import matplotlib.pyplot as plt

def run_pl_polarization_spectrum(start_deg=0, end_deg=360, step_deg=10, 
                        detector_config=2, out_dir_base=r'D:\Data_Python_PL\Polarization',
                        show_plot=True, force_home_kdc=False, kdc=None, amc=None, 
                        camera=None, bg=True, vbg=None, ide=None, idex=None):
    """
    Performs a polarization-dependent PL measurement by sweeping a Thorlabs rotation mount 
    and recording a full spectrum at each angle using the camera/spectrometer.
    
    Args:
        start_deg (float): Starting angle in degrees.
        end_deg (float): Ending angle in degrees.
        step_deg (float): Angle increment step in degrees.
        detector_config (int): Detector configuration.
        out_dir_base (str): Base directory to save output data and plots.
        show_plot (bool): If True, displays the plot after completion.
        force_home_kdc (bool): If True, passes force=True to start_kdc.
        kdc, amc, camera: Externally managed device handles (optional).
        bg (bool): If True, takes background subtraction before scanning.
        vbg (tuple): Pre-acquired background data.
        ide, idex: Optional identifiers used in folder and filenames.
        
    Returns:
        tuple: (actual_angles, all_spectra) arrays/lists.
    """
    kdc_local = False
    amc_local = False

    try:
        # === Initialize Devices ===
        if kdc is None:
            kdc = start_kdc(force=force_home_kdc)
            if kdc is None: raise ConnectionError("Failed to start Thorlabs KDC motor.")
            kdc_local = True

        if amc is None:
            try:
                amc = start_attocube()
                amc_local = True
            except NameError:
                pass

        if camera is None:
            print("No Camera provided.")
            return None, None

        # === Setup Output Directory and Subfolder with Timestamp and Identifiers ===
        timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
        folder_suffix = f"{f'_{ide}' if ide is not None else ''}{f'_{idex}' if idex is not None else ''}"
        sub_folder_name = f"{timestamp}{folder_suffix}"
        out_dir = os.path.join(out_dir_base, sub_folder_name)
        os.makedirs(out_dir, exist_ok=True)

        print(f'Saving polarization spectra to directory: {out_dir}')

        # === Optional Background Acquisition ===
        if bg and vbg is None:
            try:
                set(camera.shutter, False)
                time.sleep(1)
                data_file_bg = os.path.join(out_dir, f'spectrum_data_BG{folder_suffix}_{timestamp}.txt')
                print("Taking BG...")
                print(f"Using Filename : {data_file_bg}")
                vbg = get(camera.readval, filename=data_file_bg)
                set(camera.shutter, True)
                time.sleep(1)
            except Exception as e:
                print(f"Warning: Could not take background automatically: {e}")
                vbg = None

        angles = np.arange(start_deg, end_deg + step_deg, step_deg)
        actual_angles = []
        all_spectra = []

        print("\nStarting polarization spectrum sweep...")
        for angle in angles:
            # Move polarization stage
            kdc_move_deg(angle, kdc=kdc)
            time.sleep(0.2)  # Allow stage to settle
            
            # Read back actual position
            act_angle = kdc_position_deg(kdc=kdc)
            actual_angles.append(act_angle)

            # Construct filename including the KDC position degree
            deg_str = f"deg_{act_angle:.1f}".replace('.', '_')
            data_file = os.path.join(out_dir, f'spectrum_data{folder_suffix}_{deg_str}_{timestamp}.txt')

            # Take spectrum using camera logic
            if bg and vbg is not None and len(vbg) > 1:
                print(f"Taking Spectrum at {act_angle:.1f}°...")
                v = get(camera.readval, bkg_rem=vbg[1], filename=data_file)
            else:
                print(f"Taking Spectrum at {act_angle:.1f}°...")
                v = get(camera.readval, filename=data_file)

            all_spectra.append(v)

        print("\nPolarization spectrum sweep complete.")

        # === Plot Results ===
        if show_plot:
            fig, ax = plt.subplots(figsize=(8, 6))
            for i, (ang, v) in enumerate(zip(actual_angles, all_spectra)):
                ax.plot(v[0], v[1], label=f'{ang:.1f}°')
            
            ax.set_xlim(np.min(all_spectra[0][0]), np.max(all_spectra[0][0]))
            ax.set_xlabel('Wavelength (nm)')
            ax.set_ylabel('Counts (Arb.)')
            ax.grid(True)
            ax.set_title(f'PL Polarization Spectra | {timestamp}')
            
            if len(angles) <= 12:
                ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
                
            plt.tight_layout()
            plot_file = os.path.join(out_dir, f'polarization_summary_plot_{timestamp}.png')
            plt.savefig(plot_file)
            print(f"Summary plot saved to: {plot_file}")
            plt.show()
        else:
            plt.close('all')

        return np.array(actual_angles), all_spectra

    except Exception as e:
        print(f"\nA critical error occurred during polarization scan: {e}")
        return None, None
    finally:
        print("\n--- Cleaning up polarization scan resources ---")
        if kdc_local and kdc:
            try:
                kdc.close()
                print("KDC motor closed.")
            except Exception:
                pass
        if amc_local and amc:
            try:
                close_device_all(amc=amc)
            except Exception:
                pass