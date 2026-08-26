import pyvisa
from pyvisa.constants import Parity, StopBits
import time

class ST5:
    def __init__(self, resource="ASRL4::INSTR", baud=9600):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(resource)

        # Serial settings (same as LabVIEW / NI MAX)
        self.inst.baud_rate = baud
        self.inst.data_bits = 8
        self.inst.parity = Parity.none
        self.inst.stop_bits = StopBits.one
        self.inst.timeout = 1000  # ms

        # ST5 SCL termination
        self.inst.write_termination = "\r"
        self.inst.read_termination = "\r"

        print("Connected to ST5 on", resource)

    # -------------------------------
    # Low-level functions
    # -------------------------------
    def send(self, cmd):
        """Send SCL command (no reply expected)."""
        print(">>", cmd)
        self.inst.write(cmd)

    def query(self, cmd):
        """Send SCL command and read one line, timeout safe."""
        print(">>", cmd)
        try:
            reply = self.inst.query(cmd)
            print("<<", reply)
            return reply
        except Exception:
            print("<< (no response)")
            return None

    # -------------------------------
    # BASIC FUNCTIONS
    # -------------------------------
    def enable(self):
        self.send("ME")   # Motor Enable

    def disable(self):
        self.send("MD")   # Motor Disable

    def stop(self):
        self.send("ST")   # Stop motion

    # -------------------------------
    # POSITION COMMANDS
    # -------------------------------
    def home(self):
        """Execute homing routine."""
        self.send("HM")   # Home command

    def move_abs(self, pos_steps):
        """Absolute move to position in steps."""
        self.send(f"PA{pos_steps}")
        self.send("G")    # Go

    def move_rel(self, delta_steps):
        """Relative move (positive or negative)."""
        self.send(f"PR{delta_steps}")
        self.send("G")

    def get_position(self):
        """Read actual position (in steps)."""
        reply = self.query("PR")   # position request
        try:
            return int(reply.strip())
        except:
            return None

    # -------------------------------
    # MOTION SETUP PARAMETERS
    # -------------------------------
    def set_velocity(self, vel_rev_per_sec):
        self.send(f"VE{vel_rev_per_sec}")

    def set_accel(self, accel):
        self.send(f"AC{accel}")

    def set_decel(self, decel):
        self.send(f"DE{decel}")

    # -------------------------------
    # DIGITAL OUTPUT CONTROL
    # -------------------------------
    def digital_out(self, channel, state):
        """
        Control digital output.
        channel = 1 or 2
        state = True/False
        """
        val = 1 if state else 0
        self.send(f"SO{channel}={val}")  # Set Output

    def close(self):
        self.inst.close()
        self.rm.close()
        print("Connection closed.")
