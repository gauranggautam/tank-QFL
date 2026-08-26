import socket
import time
HOST="127.0.0.1"
PORT=5444

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    msg="HEllo"
    s.sendall(msg.encode("utf-8"))
    time.sleep(1)
