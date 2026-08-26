import matplotlib.pyplot as plt
from datetime import datetime

#sweeps_filename = ['TG5_SweepX+Vgg_Vg1=0_Vg2=0_Vb=0_20250607-164406',
#'TG5_SweepX+Vgg_Vg1=-10_Vg2=10_Vb=0_20250607-213321',
#'TG5_SweepX+Vgg_Vg1=10_Vg2=-10_Vb=0_20250607-215416',
#'TG5_SweepX+Vgg_Vg1=-10_Vg2=-10_Vb=0_20250607-221330',
#'TG5_SweepX+Vgg_Vg1=10_Vg2=10_Vb=0_20250607-223417',
#'TG5_SweepX+Vgg_Vg1=-10_Vg2=-10_Vb=0_20250607-221330']
#prefix = "C:\Data\Emile/20250606"

sweeps_filename = ['TG5_SweepVg2+Y_Vg1=-10_Vgg=0_Vb=0_',
'TG5_SweepVg2+Y_Vg1=10_Vgg=0_Vb=0_',
'TG5_SweepVg1+Y_Vg2=-10_Vgg=0_Vb=0_',
'TG5_SweepVg1+Y_Vg2=10_Vgg=0_Vb=0_',
'TG5_SweepVb+Y_Vg2=-2.5_Vg1=10_Vgg=0_',
'TG5_SweepVb+Y_Vg2=-10_Vg1=10_Vgg=0_',
'TG5_SweepVb+Y_Vg1=-2.5_Vg2=10_Vgg=0_',
'TG5_SweepVb+Y_Vg1=-10_Vg2=10_Vgg=0_']
prefix = "C:\Data\Emile/20250608"

for file in sweeps_filename:
    full_file = f'{prefix}\{file}*' 
    print(full_file)
    m=readfile(full_file)
    z=util.xy2rt(m[2],m[3],dB=False)
    plt.figure()
    plt.pcolor(m[0], m[1],z[0])
    plt.colorbar()
    plt.title(file)
    plt.savefig(f'{full_file[:-1]}_.png')

#os.system('cls' if os.name == 'nt' else 'clear')
#rint(f'using file name: {data_file})