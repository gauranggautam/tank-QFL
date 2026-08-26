import serial
import time
import struct

class FilterWheel:
    """
    Controls an Applied Motion ST5-S drive using software position tracking.
    """
    def __init__(self, port='COM4'):
        self.port = port
        self.baudrate = 9600
        self.timeout = 2
        self.ser = serial.Serial()
        self._current_position = -1 # Use -1 to indicate position is unknown

    def connect(self):
        """Opens the serial port connection."""
        if self.ser.is_open:
            return
        self.ser.port = self.port
        self.ser.baudrate = self.baudrate
        self.ser.timeout = self.timeout
        try:
            self.ser.open()
            print(f"Successfully connected to filter wheel on {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            raise

    def close(self):
        """Closes the serial port connection."""
        if self.ser.is_open:
            self.ser.close()
            print("Connection closed.")

    def _send_command(self, command_str: str):
        """Private method to send a command."""
        if not self.ser.is_open:
            raise ConnectionError("Not connected.")
        full_command = (command_str + '\r').encode('ascii')
        self.ser.write(full_command)
        # We don't read responses as they are not reliable
        time.sleep(0.1) # Small delay to allow command processing

    def get_status(self) -> int:
        """Gets the device status code as an integer."""
        self.ser.reset_input_buffer()
        self._send_command('RS')
        response_bytes = self.ser.read(2)
        if len(response_bytes) == 2:
            return struct.unpack('<H', response_bytes)[0]
        return 0

    def is_moving(self) -> bool:
        """Checks the status to see if the motor is currently moving."""
        status_code = self.get_status()
        return (status_code & 1) == 1

    def wait_for_move_to_finish(self, timeout_seconds=30):
        """Polls the status until the 'Motor Moving' flag is off."""
        print("  Waiting for move to complete...")
        start_time = time.time()
        time.sleep(0.2) # Wait for move to start
        while self.is_moving():
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError("Device did not stop moving.")
            time.sleep(0.2)
        print("  Move complete.")

    def home(self):
        """Sends the 'Home' command, waits for completion, and sets position to 0."""
        print("Homing device... This may take several seconds.")
        self._send_command('HO')
        self.wait_for_move_to_finish()
        self._current_position = 0 # After homing, we know the position is 0
        print("Homing finished.")

    def move_to_position(self, position: int):
        """Moves the wheel and updates the software position tracker."""
        print(f"Moving to position {position}...")
        self._send_command(f'FP{position}')
        self._send_command('ST')
        self.wait_for_move_to_finish()
        self._current_position = position # After moving, update our known position
        print("Move finished.")

    def get_position(self) -> int:
        """
        Returns the last commanded position from the software tracker.
        NOTE: This does not query the hardware.
        """
        return self._current_position

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

