from snAPI.Main import *
import matplotlib.pyplot as plt
import datetime
import os


from QFLv3 import *
sn = snAPI()

def plot_g2(fpath, detector_config=2, bin=100, window=100000, sn=None, normalization=True, d1=None, d2=None):
    #if sn or d1 or d2 is None:
        #sn, d1, d2 = start_apds(detector_config=detector_config)
    output_dir = r'C:/Users/iq-qfl/Documents/Gaurang/GitHub/git_codes/PlotBasic/Output/g2data_m/input/plots'
    if fpath.endswith('.ptu'):
        try:
            sn.getFileDevice(fpath)
            print(f"Data from {fpath} loaded successfully")
            sn.correlation.setG2Parameters(d1, d2, window, bin, normalization=normalization)
            sn.correlation.measure(waitFinished=True)
            fig, ax = plt.subplots()
            g2, lagtimes = sn.correlation.getG2Data()

            ax.plot(lagtimes, g2, label=f'{os.path.basename(fpath)}', linewidth=0.5)
            plt.xlabel('Delay (s)')

            plt.ylabel('g(2)')
            plt.title(f'g(2) correlation (Bin = {bin} ps & Window = {window} ps)')
            plt.legend(loc='upper right')
            plt.show()
        except:
            print(f"Data from {fpath} could not be loaded.")
    else:
        print(f"File not PTU")
