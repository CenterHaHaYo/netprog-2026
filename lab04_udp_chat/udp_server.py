import socket
import threading

HOST = "0.0.0.0"
PORT = 6000

clients = set()
clients_lock = threading.Lock()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP chat server listening on {HOST}:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        with clients_lock:
            if addr not in clients:                           # TODO 1
                clients.add(addr)
                print(f"New client: {addr[0]}:{addr[1]}")
            recipients = list(clients)

        message = f"[{addr[0]}:{addr[1]}]: {data.decode('utf-8')}"
        print(message)                                       
        for client_addr in recipients:
            sock.sendto(message.encode("utf-8"), client_addr) # TODO 2


if __name__ == "__main__":
    main()
