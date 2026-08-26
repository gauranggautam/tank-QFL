import os
import time
import re
import traceback
from datetime import datetime
from io import StringIO
# Third-Party Imports
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
import pyvisa
# Hardware-Specific Imports
try:
    from attocube import AMC
except ImportError as e:
    print(f"Warning: A hardware library could not be imported: {e}")
try:
    from snAPI.Main import *
except ImportError as e:
    print(f"Warning: A hardware library could not be imported: {e}")
try:
    from taiko_driver import TaikoLaser, PicoQuantException
except ImportError as e:
    print(f"Warning: A hardware library could not be imported: {e}")
try:
    import nidaqmx
    from nidaqmx.constants import Edge
except ImportError as e:
    print(f"Warning: A hardware library could not be imported: {e}")
try: 
    import labview_buttons_v2 as lv
except ImportError as e:
    print(f"Warning: A software library could not be imported: {e}")
uhd_plots = False
# LabView control imports
#         "btn0",  # scroll
#         "btn1",   #scollup
#         "btn2",   #apdswitch
#         "btn3",   #filterwheel
#         "btn4",   #FW450to420
#         "btn5",   #Detector
#         "btn6",   #D:APDtoSpectro
#         "btn7",   #AcquireAndor(set_settings)
#         "btn8",   #D:SpectrotoAPD
#         "btn9",   #FW420to450
    #     "btn10",  

def close_device_all(sn=None, amc=None,showcmd=True, daq=None, t_ch1=None, t_ch2=None):
    try:
        if amc:
            amc.close()
            if showcmd:
                print("AMC closed.")
        if sn:
            sn.closeDevice(allDevices=True)
            sn.exitAPI()
            if showcmd:
                print("MH150 closed.")
        if daq:
            if t_ch1:
                t_ch1.stop()
            if t_ch2:
                t_ch2.stop()
            if showcmd:
                print("DAQ closed.")
    except:
        print("Nothing to close.")
        return None
    
    
def run_g2_from_file(input_file, detector_config=2, output_dir=r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/fildevice', save_data=True, bin=100, window=100000):
    """
    Processes a .ptu file to generate, plot, and save a g2 correlation curve and its data.
    Args:
        input_file (str): Path to the .ptu file.
        detector_config (int): Detector configuration (1 for Exciletas or 2 for MPDs).
        output_dir (str): Directory to save output files. (Default : r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2/acquired')
        save_data (bool): If True, saves the plot and data to files.
        bin (int): Time bin size in picoseconds
    """
    sn = snAPI()
    try:
        if detector_config==1:
            a,b = 1,2
        else:
            a, b = 3, 4
        # Process the single file
        sn.getFileDevice(input_file)
        print(f"Data from {os.path.basename(input_file)} loaded successfully")
        sn.correlation.setG2Parameters(a, b, window, bin)
        sn.correlation.measure(waitFinished=True)

        # Plotting
        fig, ax = plt.subplots()
        g2, lagtimes = sn.correlation.getG2Data()

        ax.plot(lagtimes, g2, label=f'{os.path.basename(input_file)}', linewidth=0.5)
        ax.set_xlabel('Delay (s)')
        ax.set_ylabel('g(2)')
        ax.set_title(f'g(2) Correlation (Bin = {bin} ps & Window = {window} ps)')
        ax.legend(loc='upper right')
        #ax.grid(True)

        # Save the plot and data if save_data is True
        if save_data:
            base_name = os.path.basename(input_file).replace('.ptu', '')
            dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # --- Save Plot ---
            plot_filename = f'g2_filedevice_plot_{base_name}_{dt_now}.png'
            plot_path = os.path.join(output_dir, plot_filename)
            try:
                fig.savefig(plot_path, dpi=150)
                print(f"Plot saved as {plot_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")

            # --- Save Data ---
            data_filename = f'g2_filedevice_data_{base_name}_{dt_now}.txt'
            data_path = os.path.join(output_dir, data_filename)
            try:
                # Stack lagtimes and g2 as two columns
                data_to_save = np.column_stack((lagtimes, g2))
                # Save to a tab-delimited text file with a header
                np.savetxt(data_path, data_to_save, delimiter='\t', header='Lag Time (ps)\tg2(tau)', comments='# ')
                print(f"Data saved as {data_path}")
            except Exception as e:
                print(f"Error saving data: {e}")

        #plt.show()

    finally:
        # === Final Cleanup ===
        if sn:
            close_device_all(sn=sn)
            
            
            

input_dir = r'D:\Gaurang\ChBN12_noann\Data_Post_Irrad\g2_raw'
output_dir = r'D:\Gaurang\ChBN12_noann\Data_Post_Irrad\g2_convert'
filesstring = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.ptu')]

for filename in filesstring:
    run_g2_from_file(filename, detector_config=2, output_dir=output_dir, save_data=True, bin=100, window=100000)