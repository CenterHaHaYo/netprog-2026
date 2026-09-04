# connect_demo.py
import socket, time

client_sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

s = socket.create_connection(("10.255.255.1", 59999))
print("Connected:", s.getpeername())
time.sleep(5) # keep it open so you can inspect it
s.close()
