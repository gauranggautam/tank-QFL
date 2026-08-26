import serial
import time

st5 = serial.Serial(
    port='COM3',
    baudrate=9600
)
print(st5)


def send_command(cmd):
    st5.write(f"{cmd}\r".encode())
    time.sleep(0.1)
    #response = st5.read(100)
    #return response.decode()

send_command("ME")
print("ME")
time.sleep(1)
send_command("SP200")
print("SP100")
time.sleep(1)
send_command("MD")
print("MD")
st5.close()