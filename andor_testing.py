
from pylablib import *
from pylablib.devices import Andor
import matplotlib.pyplot as plt


try:
    cam = Andor.AndorSDK2Camera(temperature=-80,fan_mode="on")
    cam.set_cooler(True)
    print("All good")
    fig, ax = plt.subplots()
    #cam.set_acquisition_mode()
    print(cam.get_temperature_setpoint())
    print(cam.get_temperature())
    cam.set_acquisition_mode("accum")
    print(cam.get_acquisition_mode())
    cam.setup_accum_mode(2,500)
    print(cam.get_accum_mode_parameters())
    x,y = cam.start_acquisition()
    ax.plot(x,y)
    print(cam.get_acquisition_progress())
    cam.close()
except:
    print("No good")