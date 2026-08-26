from snAPI.Main import *
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import os
import numpy as np

sn = snAPI()

input_dir = r'D:/Gaurang/ChBN12_noann/Data_Post_Irrad/g2_raw'
output_dir = r'D:/Gaurang/ChBN12_noann/Data_Post_Irrad/g2_convert'
os.makedirs(output_dir, exist_ok=True)


filesstring = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.ptu')]

binsize= 100  #in ps
windowsize=100000 
#binsize*100 #in ps

a,b =3,4

for filename in filesstring:
    sn.getFileDevice(filename)
    print(f"Data from {filename} loaded successfully")
    sn.correlation.setG2Parameters(a, b, windowsize, binsize)
    sn.correlation.measure(waitFinished=True)
    fig, ax = plt.subplots()
    #plt.clf
    g2, lagtimes = sn.correlation.getG2Data()
    #df = pd.DataFrame({"lagtime": list(lagtimes), "g2": list(g2)})


    ax.plot(lagtimes, g2, label=f'{os.path.basename(filename)}', linewidth=0.5)
    plt.xlabel('Delay (s)')

    plt.ylabel('g(2)')
    plt.title(f'g(2) correlation (Bin = {binsize} ps & Window = {windowsize} ps)')
    plt.legend(loc='upper right')

    # Save the figure to the output folder
    sv=True
    if sv:
        figpath = os.path.join(output_dir, 'g2plot_' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.png')
        try:
            fig.savefig(figpath)
            print(f"Figure saved as {figpath}")
        except Exception as e:
            print(f"Error saving figure: {e}")
#sn.closeDevice
plt.show()

