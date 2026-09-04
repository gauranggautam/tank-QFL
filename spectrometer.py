import os 
import time
import matplotlib.pyplot as plt

def start_spectro(spectro_set_cw=484, shutter_init=True,waitfortemp=True,showrange=True):
    
    spectro = instruments.andor_kymera()
    set(spectro.wavelength_nm, spectro_set_cw)
    camera = instruments.andor_iDus(spectro_instr=spectro,cooler_temp=-80,shutter_init=shutter_init)
    camera.conf(read_mode='full_vertical_binning',exposure_time=5,acq_mode="accumulate", acc_N=2)
    set(camera.cosmic_filter_en, True)
    vbg=None
    if waitfortemp:
        camera.wait_for_cooler_stable(-80)
    minw = int(get(spectro.sensor_wavelengths_nm)[0])
    maxw = int(get(spectro.sensor_wavelengths_nm)[-1])
    if showrange:
        print(f"Current wavelength range : {minw}nm to {maxw}nm")
    return spectro, camera, minw, maxw
        
def close_spectro(spectro=None,camera=None):
    if camera is not None:
        unload(camera)
    if spectro is not None:
        unload(spectro)

def take_spectrum_bg(camera=None):
    set(camera.shutter, False)
    time.sleep(1)
    vbg = get(camera.readval)
    set(camera.shutter, True)
    return vbg

def take_spectrum(bg=True, vbg=None,
                  read_mode='full_vertical_binning',
                  exposure_time=5,
                  acq_mode="accumulate",
                  acc_N=2,
                  data_only=False,
                  show_plot=True,
                  camera=None,spectro=None):
    if camera is None:
        spectro, camera, minw, maxw = start_spectro()
    camera.conf(read_mode=read_mode,exposure_time=exposure_time,acq_mode=acq_mode, acc_N=acc_N)
    if bg:
        if vbg is None:
            set(camera.shutter, False)
            time.sleep(1)
            vbg = get(camera.readval)
            set(camera.shutter, True)
            time.sleep(1)
        v = get(camera.readval, bkg_rem=vbg[1])
    else:
        v = get(camera.readval)
    #plot
    if show_plot:
        _, ax = plt.subplots()
        ax.plot(v[0], v[1]) #label=f'{}')
        ax.set_xlim(np.min(v[0]), np.max(v[0]))
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Counts (Arb.)')
        ax.grid(True)
        ax.set_title('PL Spectrum')
        plt.show()
    if data_only:
        return v[1]
    else:
        return v