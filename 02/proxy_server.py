import socket
import sys
from multiprocessing import Process


PROXY_SERVER_HOST = ""
PORT = 8001
BUFFER_SIZE = 4096

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # reuse address 
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((PROXY_SERVER_HOST, PORT))
        server_socket.listen(2)

        while True:
            conn_socket, addr = server_socket.accept()
            print("Connected by", addr)

            p = Process(target=serve, args=[conn_socket])
            p.daemon = True     # run in backround
            p.start()

            conn_socket.close()
            print("Parent process client socket closed")


def forward_payload(proxy_socket, payload):
    try:
        proxy_socket.sendall(payload)       # payload is already in bytes
    except socket.error:
        print("Error: forwarding payload failed")
        sys.exit()


def get_remote_ip(host):
    try:
        remoteIP = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved. Existing...", file=sys.stderr)
        sys.exit()

    return remoteIP


def serve(conn_socket):
    '''
    Child process function.
    Receives the encoded payload from the client and forwards it to destination server.
    After receiving data back from the destination server, forwards the data back to the
    client.
    '''
    client_payload = conn_socket.recv(BUFFER_SIZE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:

        dest_host = "www.google.com"
        remote_ip = get_remote_ip(dest_host)
        tcp_port = 80

        proxy_socket.connect((remote_ip, tcp_port))
        print(f"Proxy socket connected to {dest_host} on ip {remote_ip}")

        forward_payload(proxy_socket, client_payload)
        proxy_socket.shutdown(socket.SHUT_WR)

        # receive data from server
        received_data = b""
        while True:
            data = proxy_socket.recv(BUFFER_SIZE)
            if not data:
                break
            received_data += data

        # print(received_data)

    # send back the data to the client
    conn_socket.sendall(received_data)
    conn_socket.close()
    print("Child process client socket closed")
    

if __name__ == "__main__":
    main()
