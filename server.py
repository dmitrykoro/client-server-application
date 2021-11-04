import socket
import random
import json
import threading
import sys
from threading import Thread, Lock

HOST = ""
INITIAL_PORT = 8000
TRANSMISSION_PORT = 8001
BLOCK_SIZE = 512
DATA_ENCODING = "utf-8"

authorized_users_dict = {}

lock = Lock()


def init_host():
    try:
        f = open('server_params.json', )
        global HOST
        HOST = json.load(f)["host"]
        return
    except KeyError:
        print("Wrong server_params.json file format")
    except FileNotFoundError:
        print("File server_params.json not found")
    sys.exit(-1)


def listen_for_handshake():
    initial_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    initial_socket.bind((HOST, INITIAL_PORT))
    initial_socket.listen(5)
    print(f'Listening for handshake connection in thread: {threading.get_native_id()}')

    while True:
        handshake_conn, address = initial_socket.accept()
        print('Connected for handshake:', address)

        Thread(target=handshake, args=(handshake_conn,)).start()


def handshake(handshake_conn):
    client_code = handshake_conn.recv(BLOCK_SIZE).decode(DATA_ENCODING)
    print(f'Handshaking with {client_code} in thread: {threading.get_native_id()}')

    curr_server_code = hex(random.getrandbits(20))
    handshake_conn.send(f'{curr_server_code}'.encode(DATA_ENCODING))

    handshake_conn.close()

    lock.acquire()
    authorized_users_dict[curr_server_code] = client_code
    lock.release()

    return


def listen_for_transmission():
    transmission_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transmission_socket.bind((HOST, TRANSMISSION_PORT))
    transmission_socket.listen(5)

    print(f'Listening for transmission connection in thread: {threading.get_native_id()}')
    while True:
        transmission_conn, address = transmission_socket.accept()
        print('Connected for transmission:', address)

        Thread(target=transmit, args=(transmission_conn,)).start()


def transmit(transmission_conn):
    message = transmission_conn.recv(BLOCK_SIZE).decode(DATA_ENCODING)
    server_code = json.loads(message).get("server_code")

    if server_code in authorized_users_dict.keys():
        text = json.loads(message).get("msg")
        print(f'Message: {text}')
        del authorized_users_dict[server_code]
    else:
        error_message = f'Received invalid server code {server_code}'
        transmission_conn.send(error_message.encode(DATA_ENCODING))

    transmission_conn.close()
    return


if __name__ == '__main__':
    init_host()
    Thread(target=listen_for_handshake).start()
    Thread(target=listen_for_transmission).start()
