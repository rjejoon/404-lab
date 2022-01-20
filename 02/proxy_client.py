import socket
import sys


def main():
    try:
        proxy_server_host = "127.0.0.1"      # localhost
        proxy_port = 8001
        dest_host = "www.google.com"
        payload = f'GET / HTTP/1.0\r\nHost: {dest_host}\r\n\r\n'
        buffer_size = 4096

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((proxy_server_host, proxy_port))

        send_payload(s, payload)
        s.shutdown(socket.SHUT_WR)

        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
        print(full_data)

    except Exception as e:
        print(e, file=sys.stderr)

    finally:
        s.close()


def get_remote_ip(host):
    try:
        remoteIP = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved. Existing...", file=sys.stderr)
        sys.exit()

    return remoteIP


def send_payload(s, payload):
    try:
        s.sendall(payload.encode())
    except socket.error:
        print("Error: sending payload failed")
        sys.exit()



if __name__ == "__main__":
    main()
