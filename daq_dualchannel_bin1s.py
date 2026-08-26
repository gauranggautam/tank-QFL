import nidaqmx
import time
from nidaqmx.constants import Edge
from QFLv4 import *


daq,t_ch1,t_ch2=start_daq()
# Start both counters
t_ch1.start()
t_ch2.start()
BIN_TIME = 1
# Initial readings
prev1 = t_ch1.read()
prev2 = t_ch2.read()

print(f"Counts per {BIN_TIME*1000:.1f} ms   (ch1 = PFI8, ch2 = PFI9)")
print("ch1\tch2\tch_sum")

try:
    while True:
        time.sleep(BIN_TIME)

        now1 = t_ch1.read()
        now2 = t_ch2.read()

        ch1 = now1 - prev1
        ch2 = now2 - prev2

        prev1, prev2 = now1, now2

        ch_sum = ch1 + ch2

        print(f"{ch1}\t{ch2}\t{ch_sum}")

except KeyboardInterrupt:
    print("Stopped by user.")

t_ch1.stop()
t_ch2.stop()
