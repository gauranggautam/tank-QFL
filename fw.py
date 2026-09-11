import serial
import time
def send_cmd(drive, command):
   """Helper function to send commands and read the response."""
   drive.write(f"{command}\r".encode('ascii'))
   return drive.read_until(b'\r').decode('ascii').strip()
def Power_apds(drive, state):
   """
   Controls the APDS (Gaba) device via Output 1.
   state = False (Closed/OFF, sends IH1)
   state = True  (Running/ON, sends IL1)
   """
   if state:
       send_cmd(drive, "IL1")
       print("APDS is now ON / Running (IL1).")
   else:
       send_cmd(drive, "IH1")
       print("APDS is now OFF / Closed (IH1).")
def seek_home_precise(drive):
   """Performs the two-stage edge-finding homing routine."""
   print("--- Starting Precise Homing Sequence ---")
   print("Stage 1: Fast seek to find sensor...")
   while True:
       bits = send_cmd(drive, "IS").replace("IS=", "")
       if len(bits) >= 4 and bits[3] == '0':
           print("Sensor hit! (Overshot slightly)")
           break
       send_cmd(drive, "FL100")
       time.sleep(0.05)
   print("Stage 2: Slow reverse to find exact edge...")
   while True:
       bits = send_cmd(drive, "IS").replace("IS=", "")
       if len(bits) >= 4 and bits[3] == '1':
           print("Exact edge found!")
           break
       send_cmd(drive, "FL-5")
       time.sleep(0.05)
   print("Setting origin (SP0)...")
   send_cmd(drive, "SP0")
   time.sleep(0.1)
   pr_response = send_cmd(drive, "PR")
   print(f"Homing Complete. Current Position: {pr_response}")
def filterwheel(slot, offset=13.43, home_first=True, apd_final_state=False):
   """
   0 = No Filter, 1 = LP420, 6 = BP450 ...
   Moves the filter wheel to a specific slot (0 to 14).
   apd_final_state controls whether the APDS is left ON (True) or OFF (False) after moving.
   """
   if slot < 0 or slot > 14:
       print(f"Error: Slot must be between 0 and 14. You entered {slot}.")
       return
   steps_per_slot = 1400
   target_steps = int(-(slot + offset) * steps_per_slot)
   print(f"--- Moving to Filter {slot} ---")
   try:
       with serial.Serial(port='COM4', baudrate=38400, timeout=1) as drive:
           # 1. Close APDS before moving (False = Closed)
           Power_apds(drive, False)
           # 2. Home the wheel if requested
           if home_first:
               seek_home_precise(drive)
           # 3. Execute the move
           print(f"Calculated target: {target_steps} steps...")
           ack_move = send_cmd(drive, f"FP{target_steps}")
           if ack_move == "%":
               print("Move accepted. Motor is turning...")
           else:
               print(f"Warning: Drive responded with '{ack_move}'")
           time.sleep(2)
           final_status = send_cmd(drive, "SC")
           print(f"Final Drive Status: {final_status}")
           # 4. Set APDS to the requested final state
           Power_apds(drive, apd_final_state)
       print("Done.\n")
   except serial.SerialException as e:
       print(f"Port Error: {e} \n(Make sure LabVIEW is closed!)")
if __name__ == "__main__":
   # Example: Home the wheel, move to slot 1, and leave the APDS OFF (False)
   filterwheel(1, offset=13.43, home_first=True, apd_final_state=False)