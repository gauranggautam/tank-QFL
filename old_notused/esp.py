import pyvisa
import time
# Initialize VISA resource manager
rm = pyvisa.ResourceManager()
# Open the ESP300 at GPIB1 address 7
esp = rm.open_resource("GPIB1::7::INSTR")
#esp.write("3PA10.5")
#print("Axis 1 moving to 10.5 mm")
#is_moving = esp.query("1MD?")
#if is_moving.strip() == '0':
#    print("Axis 1 motion complete.")
#else:
#    print("Axis 1 is still moving.")
#time.sleep(1)
## Query position of axis 1
posi = esp.query("3TP?")
print("Axis 3 Position:", posi.strip(), "mm")

#esp.write("3PA0")
#print("Detection axis moving to APDs")
#is_moving = esp.query("3MD?")
#time.sleep(5)
#if is_moving.strip() == '0':
#    print("Detection axis motion complete.")
#posf = esp.query("3TP?")
#print("Detection axis Position:", posf.strip(), "mm")




posi = esp.query("2TP?")
print("Axis 2 Position:", posi.strip(), "mm")