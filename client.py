import socket
import random
import json
import sys

HOST = ""
INITIAL_PORT = 8000
TRANSMISSION_PORT = 8001
TIMEOUT = 5
DATA_ENCODING = "utf-8"

CLI_UUID = hex(random.getrandbits(20))

BLOCK_SIZE = 512


def init_host():
    try:
        f = open('client_params.json', )
        global HOST
        HOST = json.load(f)["host"]
        return
    except KeyError:
        print("Wrong client_params.json file format")
    except FileNotFoundError:
        print("File client_params.json not found")
    sys.exit(-1)


def handshake():
    try:
        initial_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        initial_socket.connect((HOST, INITIAL_PORT))

        print(f'Connected to {HOST}:{INITIAL_PORT}')
    except ConnectionRefusedError:
        print("Server is unreachable")
        return

    initial_socket.send(CLI_UUID.encode(DATA_ENCODING))
    server_code = initial_socket.recv(BLOCK_SIZE).decode(DATA_ENCODING)
    print(f'Received server code: {server_code}')
    return server_code


def transmit(server_code):
    try:
        transmission_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transmission_socket.connect((HOST, TRANSMISSION_PORT))
        transmission_socket.settimeout(TIMEOUT)

        print(f'Connected to {HOST}:{TRANSMISSION_PORT}')
    except ConnectionRefusedError:
        print("Server is unreachable")
        return

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
    init_host()
    server_code = handshake()
    transmit(server_code)
