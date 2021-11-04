import socket
import random
import json

HOST = '127.0.0.1'
INITIAL_PORT = 8000
TRANSMISSION_PORT = 8001
TIMEOUT = 5
DATA_ENCODING = "utf-8"

CLI_UUID = hex(random.getrandbits(20))

BLOCK_SIZE = 512


def transmit():
    try:
        transmission_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transmission_socket.connect((HOST, TRANSMISSION_PORT))
        transmission_socket.settimeout(TIMEOUT)

        print(f'Connected to {HOST}:{TRANSMISSION_PORT}')
    except ConnectionRefusedError:
        print("Server is unreachable")
        return

    server_code = hex(random.getrandbits(20))

    message = input(f'Hello, {CLI_UUID}. Input your message: ')
    data = {"cli_uuid": CLI_UUID, "server_code": server_code, "msg": message}
    transmission_socket.send(bytes(json.dumps(data), encoding=DATA_ENCODING))

    try:
        response = transmission_socket.recv(BLOCK_SIZE).decode(DATA_ENCODING)
        if response:
            print(f'Server says: {response}')
    except socket.timeout:
        print("OK")
    return


if __name__ == '__main__':
    transmit()