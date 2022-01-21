#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process


# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # reuse addr
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind socket to address
        s.bind((HOST, PORT))
        # set to listening mode
        s.listen(2)

        # continuously listen for connections
        while True:
            conn_socket, addr = s.accept()
            print("Connected by", addr)

            p = Process(target=serve, args=[conn_socket])
            p.daemon = True     # run in background
            p.start()

            conn_socket.close()
            print("Parent process client socket closed")
            

def serve(conn_socket):
    '''
    Child process function.
    '''
    # recieve data, wait a bit, then send it back
    full_data = conn_socket.recv(BUFFER_SIZE)
    print(full_data)
    time.sleep(0.5)
    conn_socket.sendall(full_data)
    conn_socket.close()
    print("Child process client socket closed")


if __name__ == "__main__":
    main()
