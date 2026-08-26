# %%
import time
from pylablib.devices import Thorlabs
#Thorlabs.list_kinesis_devices()
def start_kdc():
    kdc = Thorlabs.KinesisMotor("27257399")
    kdc.open()
    kdc.get_device_info()
    kdc.home(force=True)
    return kdc
def close_kdc():
    kdc.close()
def kdc_move_deg(x):
    x_deg=x*1919.6418578623391
    kdc.move_to(x_deg)
    while True:
        if kdc.is_moving() == False:
            break
        time.sleep(0.01)
def kdc_position_deg():
    posdeg =kdc.get_position()/1919.6418578623391
    print(f"{posdeg:.2f}")
# %%
FULLY WORKING