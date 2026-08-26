   
from taiko_driver import TaikoLaser, PicoQuantException
import time

# --- User-configurable settings ---
TARGET_TEMP = 15.0      # Target temperature in Celsius
TARGET_POWER = 500      # Target power in permille (0-1000)
TEMP_TOLERANCE = 0.1    # How close the temp needs to be (in degrees C) to be "stable"
ACTIVE_WAIT_TIME = 5    # How many seconds the laser stays active

try:
    # The 'with' statement automatically connects and ensures the device is closed
    with TaikoLaser() as laser:
        print(f"Connected to: {laser.get_identity()}")

        # 1. Disable laser emission for safe configuration (softlock ON)
        print("\nDisabling laser emission for safe configuration (softlock ON)...")
        laser.softlock = True
        
        # 2. Set non-power parameters while the laser is disabled
        print("\nSetting non-power parameters...")
        laser.laser_mode = 'cw'
        laser.target_temperature_celsius = TARGET_TEMP
        print(f"Laser mode set to: {laser.laser_mode}")
        print(f"Target temperature set to: {laser.target_temperature_celsius:.2f} C")

        # 3. Wait for the laser's temperature to stabilize
        print("\nWaiting for temperature to stabilize...")
        while abs(laser.current_temperature_celsius - TARGET_TEMP) > TEMP_TOLERANCE:
            print(f"  Current temperature: {laser.current_temperature_celsius:.2f} C...")
            time.sleep(2) # Wait 2 seconds between checks
        print(f"Temperature stabilized at {laser.current_temperature_celsius:.2f} C.")
        
        # 4. Enable the laser emission (softlock OFF)
        print("\nEnabling laser emission (softlock OFF)...")
        laser.softlock = False
        print(f"Softlock is now: {laser.softlock} (Laser ENABLED)")
        time.sleep(0.5) # Give the device a moment to stabilize

        # 5. Now that the laser is stable and enabled, set the power level
        print(f"\nSetting CW power to {TARGET_POWER}/1000...")
        laser.cw_power_permille = TARGET_POWER
        print(f"CW power is now: {laser.cw_power_permille} / 1000")
        
        print(f"\nLaser is now active. Waiting {ACTIVE_WAIT_TIME} seconds...")
        time.sleep(ACTIVE_WAIT_TIME)
        
        # 6. Set power to zero before disabling
        print("\nSetting power to 0...")
        laser.cw_power_permille = 0
        
        # 7. Disable the laser emission as a final safety step
        print("\nDisabling laser emission before disconnect (softlock ON)...")
        laser.softlock = True
        laser.close
        
    print("\nScript finished and device closed.")

except PicoQuantException as e:
    print(f"A hardware or DLL error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    
    
    
    
    
print("\nSetting power to 0...")
laser.cw_power_permille = 0
# 7. Disable the laser emission as a final safety step
print("\nDisabling laser emission before disconnect (softlock ON)...")
laser.softlock = True
laser.close 