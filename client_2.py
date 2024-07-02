import socket
import logging

logging.basicConfig(level=logging.WARNING)

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 45000)
    logging.warning(f"Connecting to server at {server_address}")
    sock.connect(server_address)

    try:
        while True:
            # Send data
            message = input("Message: ")
            if message == "QUIT":
                print("QUIT")
                sock.sendall(message.encode('UTF-8') + b'\r\n')
                data = sock.recv(1024)
                print(data.decode('UTF-8'))
                sock.close()
                break
            elif message.startswith("TIME"):
                sock.sendall(message.encode('UTF-8') + b'\r\n')
                data = sock.recv(1024)
                print(data.decode('UTF-8'))
            else:
                print("Invalid message. Please start with 'TIME' or send 'QUIT' to exit.")
    finally:
        logging.warning("Closing connection")
        sock.close()

if __name__ == "__main__":
    kirim_data()