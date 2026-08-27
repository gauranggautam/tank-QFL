from pylablib.devices import Thorlabs
kdc = Thorlabs.KinesisMotor("27257399")
kdc.open()
kdc.home(force=True)

def start_kdc(SN="27257399",kdc=None):
    if kdc is not None:
        kdc = kdc
        return kdc
    else:
        kdc = Thorlabs.KinesisMotor("27257399")
        kdc.open()
        kdc.home(force=True)
        return kdc
def kdc_move_deg(deg,kdc=None):
    if kdc is None:
        kdc = start_kdc()
    step=deg*1919.6418578623391
    kdc.move_to(step)
    while true:
        if kdc.is_moving()==False

