from pylablib.devices import Andor
import matplotlib.pyplot as plt
cam = Andor.AndorSDK2Camera(temperature=-80,fan_mode="full")  # camera should be connected first
cam.set_cooler(True)
spec = Andor.ShamrockSpectrograph()
spec.set_wavelength(484E-9)  # set 600nm center wavelength
spec.setup_pixels_from_camera(cam)  # setup camera sensor parameters (number and size of pixels) for wavelength calibration
wavelengths = spec.get_calibration()
# return array of wavelength corresponding to each pixel
#cam.set_image_mode("fvb")
spectrum = cam.snap()[0]
fig, ax = plt.subplots()
ax.plot(wavelengths, spectrum)# 1D array of the corresponding spectrum intensities
cam.close()
spec.close()

