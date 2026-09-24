from QFLv4 import *
amc = start_attocube()
# === CONFIG ===
wobble_speed = 2
delay=0.001# 
wobble_size = 6          # ± range from current focus
# === AMC Init ===

f_now = amc.move.getPosition(1) / 1000
print(f_now)
wobble_range= np.arange(f_now-wobble_size,f_now+wobble_size,wobble_speed)
rev_wobble_range= np.arange(f_now+wobble_size,f_now-wobble_size,-wobble_speed)

try:
    while True:
        for f in wobble_range:
            amc.move.setControlTargetPosition(1, int(f * 1000))
            wait_until_stable(amc_dev=amc, axis=1)
            #time.sleep(delay)
        #f_now = amc.move.getPosition(1) / 1000
        #print(f_now)
        for f in rev_wobble_range:
            amc.move.setControlTargetPosition(1, int(f * 1000))
            wait_until_stable(amc_dev=amc, axis=1)
            #time.sleep(delay)
        #f_now = amc.move.getPosition(1) / 1000
        #print(f_now)
except KeyboardInterrupt:
    close_device_all(amc=amc)