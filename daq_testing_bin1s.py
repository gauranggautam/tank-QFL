import nidaqmx
import time
from nidaqmx.constants import Edge

DEVICE = "Dev1"
COUNTER = f"{DEVICE}/ctr0"
SOURCE = f"/{DEVICE}/PFI10"     # MPD TTL input

BIN_TIME = 1   # === 10 ms bin size ===

with nidaqmx.Task() as task:
    task.ci_channels.add_ci_count_edges_chan(
        counter=COUNTER,
        edge=Edge.FALLING,
        initial_count=0
    )
    task.ci_channels.all.ci_count_edges_term = SOURCE

    task.start()
    prev = task.read()

    print(f"Counting photons in {BIN_TIME*1000:.1f} ms bins...")

    while True:
        time.sleep(BIN_TIME)

        now = task.read()
        diff = now - prev
        prev = now

        print(diff)
