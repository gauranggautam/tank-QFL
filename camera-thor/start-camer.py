# %%
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
pathe = r"D:\Gaurang\GitHub-QFL\tank-QFL\camera-thor\SDK\Python Toolkit\examples"
if pathe not in sys.path:
    sys.path.append(pathe)
    
import windows_setup
windows_setup.configure_path()

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK

with TLCameraSDK() as sdk:
    cameras = sdk.discover_available_cameras()
    print("Device found: ", cameras)
    camera =  sdk.open_camera("11484")
    print("success")
    current = camera.exposure_time_us
    print("current exposure", current)
    camera.exposure_time_us = 200000
    camera.gain = 10
    gain = camera.gain
    new = camera.exposure_time_us
    print("current exposure", new, gain)
    
    camera.frames_per_trigger_zero_for_unlimited = 1
    camera.arm(frames_to_buffer=1)
    camera.issue_software_trigger()
    frame = camera.get_pending_frame_or_null(timeout_ms=2000)
    imagem = np.asarray (frame.image_buffer)
    plt.imshow(imagem, cmap='gray')
    
    camera.dispose()
    sdk.dispose()

# %%
