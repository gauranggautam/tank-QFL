# %%
from pyHegel import start_pyHegel
start_pyHegel()
%run QFLv5.py

# %%
em="E1"
amc_move(axis=0,d=-805.98)
amc_move(axis=2,d=190.13)

# %%
#set_detection("apd", apd_final_state=True)
#time.sleep(10)


em="E7"
amc_move(axis=0,d=-800.945)
amc_move(axis=2,d=186.094)

run_pl_position_optimizer(ide=em) # moveto best true
run_pl_polarization(step_deg=2,ide=em)
kdc_move_deg(0)
set_detection("spectro")
time.sleep(2)
spectro,camera=start_spectro(waitfortemp=False)
unload(camera)
unload(spectro)
time.sleep(5)
spectro,camera=start_spectro()
set_spectrum(camera=camera, spectro=spectro, acq_mode="accumulate", cosmic_filter=True, exposure_time=10,wl=461,acc_N=6,grating=2)
time.sleep(2)
take_spectrum(camera=camera, bg=False, ide=em) #no BG correction
unload(camera)
unload(spectro)
time.sleep(30)
set_detection("apd", apd_final_state=True)
time.sleep(20)
set_laser(33,pulsed=True,freq_khz=10000)
trpl_measure(time_m=600,ide=em)
time.sleep(5)
set_laser(33,pulsed=False)
g2_measure(time_m=600,ide=em,binsize_ps=200)
time.sleep(5)

em="E8"
amc_move(axis=0,d=-805.719)
amc_move(axis=2,d=183.850)

run_pl_position_optimizer(ide=em) # moveto best true
run_pl_polarization(step_deg=2,ide=em)
kdc_move_deg(0)
set_detection("spectro")
time.sleep(2)
spectro,camera=start_spectro(waitfortemp=False)
unload(camera)
unload(spectro)
time.sleep(5)
spectro,camera=start_spectro()
set_spectrum(camera=camera, spectro=spectro, acq_mode="accumulate", cosmic_filter=True, exposure_time=10,wl=461,acc_N=6,grating=2)
time.sleep(2)
take_spectrum(camera=camera, bg=False, ide=em) #no BG correction
unload(camera)
unload(spectro)
time.sleep(30)
set_detection("apd", apd_final_state=True)
time.sleep(20)
set_laser(33,pulsed=True,freq_khz=10000)
trpl_measure(time_m=600,ide=em)
time.sleep(5)
set_laser(33,pulsed=False)
g2_measure(time_m=600,ide=em,binsize_ps=200)
time.sleep(5)

em="E9"
amc_move(axis=0,d=-803.149)
amc_move(axis=2,d=184.086)

run_pl_position_optimizer(ide=em) # moveto best true
run_pl_polarization(step_deg=2,ide=em)
kdc_move_deg(0)
set_detection("spectro")
time.sleep(2)
spectro,camera=start_spectro(waitfortemp=False)
unload(camera)
unload(spectro)
time.sleep(5)
spectro,camera=start_spectro()
set_spectrum(camera=camera, spectro=spectro, acq_mode="accumulate", cosmic_filter=True, exposure_time=10,wl=461,acc_N=6,grating=2)
time.sleep(2)
take_spectrum(camera=camera, bg=False, ide=em) #no BG correction
unload(camera)
unload(spectro)
time.sleep(30)
set_detection("apd", apd_final_state=True)
time.sleep(20)
set_laser(33,pulsed=True,freq_khz=10000)
trpl_measure(time_m=600,ide=em)
time.sleep(5)
set_laser(33,pulsed=False)
g2_measure(time_m=600,ide=em,binsize_ps=200)
time.sleep(5)

em="E10"
amc_move(axis=0,d=-803.209)
amc_move(axis=2,d=182.255)

run_pl_position_optimizer(ide=em) # moveto best true
run_pl_polarization(step_deg=2,ide=em)
kdc_move_deg(0)
set_detection("spectro")
time.sleep(2)
spectro,camera=start_spectro(waitfortemp=False)
unload(camera)
unload(spectro)
time.sleep(5)
spectro,camera=start_spectro()
set_spectrum(camera=camera, spectro=spectro, acq_mode="accumulate", cosmic_filter=True, exposure_time=10,wl=461,acc_N=6,grating=2)
time.sleep(2)
take_spectrum(camera=camera, bg=False, ide=em) #no BG correction
unload(camera)
unload(spectro)
time.sleep(30)
set_detection("apd", apd_final_state=True)
time.sleep(20)
set_laser(33,pulsed=True,freq_khz=10000)
trpl_measure(time_m=600,ide=em)
time.sleep(5)
set_laser(33,pulsed=False)
g2_measure(time_m=600,ide=em,binsize_ps=200)
time.sleep(5)


# %%
