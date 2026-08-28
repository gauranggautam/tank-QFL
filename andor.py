# %% Spectro Full
from pyHegel import *
import os
import matplotlib.pyplot as plt
# %% init spectro and camera  
spectro = instruments.andor_kymera()
camera = instruments.andor_iDus(spectro_instr=spectro,cooler_temp=-80)
camera.wait_for_cooler_stable(-80)
set(spectro.wavelength_nm, 484)
camera.conf(read_mode='full_vertical_binning',exposure_time=5,acq_mode="accumulate", acc_N=3)
set(camera.cosmic_filter_en, False)
minw = int(get(spectro.sensor_wavelengths_nm)[0])
maxw = int(get(spectro.sensor_wavelengths_nm)[-1])
print(f"Current wavelength range : {minw}nm to {maxw}nm")

# %% Single acq 5sX2 ~ cosmic not working
camera.conf(read_mode='full_vertical_binning',exposure_time=5,acq_mode="accumulate", acc_N=2)
set(camera.cosmic_filter_en, False)
#shutter: to open = 1 ; close =2
camera._sdk.SetShutter(1, 1, 100, 100)
#data

#def conf_shuter(enable):
#    if enable:
#        s = 1
#    else:
#        s = 2
#    camera._sdk.SetShutter(1, s, 100, 100)


v = get(camera.readval)
#plot
_, ax = plt.subplots()
ax.plot(v[0], v[1]) #label=f'{}')
ax.set_xlim(np.min(v[0]), np.max(v[0]))
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Counts (Arb.)')
ax.grid(True)
ax.set_title('PL Spectrum')
plt.show()
#ax.legend(loc='upper right')

# %% Continious mode:
camera.conf(read_mode='full_vertical_binning',exposure_time=1,acq_mode="single_scan")
set(camera.exposure_time, 1)
scope(camera.readval)


# %% Remove
unload(camera)
unload(spectro)