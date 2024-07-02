from socket import *
import socket
import threading
import logging
import time
import sys
import pytz
from datetime import datetime

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                data = self.connection.recv(32)
                if data:
                    logging.warning(f"[SERVER] received {data} from {self.address}")
                    if data.startswith(b'TIME') and data.endswith(b'\r\n'):
                        timez = "JAM " + datetime.strftime(datetime.now(), "%H:%M:%S") + "\r\n"
                        logging.warning(f"[SERVER] sending {timez} to {self.address}")
                        self.connection.sendall(timez.encode('UTF-8'))
                    # elif data == "QUIT":
                    #     logging.warning(f"{self.address}QUIT")
                    #     self.connection.close()
                    #     break
                    else:
                        logging.warning(f"[SERVER] QUIT")
                        self.connection.close()
                        break
                else:
                    self.connection.close()
                    break
        finally:
            self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
            
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
