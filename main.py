import atexit
import base64
import json
import os
import socket
import sys
import time
import uuid
from _thread import *
from multiprocessing import *

manager = Manager()

ServerSideSocket = None
__server_host = "localhost"
__server_ports = [x for x in range(1023, 1223)]
__server_port = None

process = None
session_id = uuid.uuid1()
modules_list = []
default_response = "Sorry, I don't understand."


def init_server():
    global __server_port
    global ServerSideSocket
    ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = False
    for port in __server_ports:
        print(f"Trying to initialize Cortana server on  port {port}...")
        try:
            ServerSideSocket.bind((__server_host, port))
            status = True
            __server_port = port
            break
        except Exception as e:
            print(str(e))
    ServerSideSocket.listen(5)
    return status


def import_modules():
    global modules_list
    files = os.listdir("modules")
    for filename in files:
        if filename.endswith(".py"):
            exec(f"global {filename[0:-3]};from modules import {filename[0:-3]}")
            print(f"Imported module [{filename[0:-3]}]")
            modules_list.append(filename[0:-3])


def process_header(input: str):
    a1 = input.find("::")
    header_len = int(input[0:a1])
    header = input[a1 + 2:header_len + 2]
    a2 = header.split("::")
    session_id, machine_name, remote_time, response_len = a2[0], base64.b64decode(a2[1]).decode('utf-8'), a2[2], a2[3]
    return session_id, machine_name, int(remote_time), int(response_len)


def create_header(input):
    global session_id
    machine_name = base64.b64encode("computer_1".encode()).decode()
    timestamp = round(time.time())
    content_len = len(input)
    tmp = f"::{session_id}::{machine_name}::{timestamp}::{content_len}"
    output = str(len(tmp)) + tmp
    output = output.ljust(85, '#')
    return output


def process_response(response):
    output = json.loads(response)
    return output


def check_scores(data):
    scores = []
    for module in modules_list:
        result = eval(f'{module}.check_input(data)')
        scores.append((module, result))
    max_value = -1
    module = ''
    for _index, e in enumerate(scores):
        if e[1] > max_value and e[1] != 0:
            max_value = e[1]
            module = e[0]
    return max_value, module


class CommandExecutionResult:
    def __init__(self, data: object, result: object):
        # May add more fields later as needed
        self.data = data
        self.exe_time = round(time.time())
        if result is not None:
            self.result = result
        else:
            self.result = None


def handle_request(connection: socket, data, client_command_memory: list):
    # Find module to use
    score, module = check_scores(data)
    if score == -1:
        header = create_header(default_response)
        connection.send((header + default_response).encode())
        return client_command_memory
    result = eval(f'{module}.eval(data, client_command_memory)')

    if result is None:
        header = create_header(default_response)
        connection.send((header + default_response).encode())
    header = create_header(result)
    connection.send((header + result).encode())
    client_command_memory.append(CommandExecutionResult(data, result))
    return client_command_memory


def threaded_client(connection: socket):
    session_active = True
    session_id, machine_name, remote_time, response_len = None, None, None, None
    client_command_memory = []

    while session_active:
        try:
            response1 = connection.recv(85).decode('utf-8')
            session_id, machine_name, remote_time, response_len = process_header(response1)
            response2 = connection.recv(response_len)
            new_data = process_response(response2)
            client_command_memory = handle_request(connection, new_data, client_command_memory)
        except Exception as ex:
            print(ex)


def handle_connections(ServerSideSocket: socket):
    while True:
        try:
            Client, address = ServerSideSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(threaded_client, (Client,))
        except Exception as ex:
            print(str(ex))


def exit_cleanup(*args):
    try:
        if process is not None:
            process.terminate()
            process.join()
        if ServerSideSocket is not None:
            ServerSideSocket.shutdown(1)
    except Exception as ex:
        print()
    finally:
        print("Exiting...")


def run_cortana():
    global process
    status = init_server()
    import_modules()
    if not status:
        print(f"Error initializing Cortana server on port {__server_port}.")
        quit(-1)
    else:
        print(f"Server initializing on port {__server_port}")
    process = Process(target=handle_connections, args=(ServerSideSocket,))
    process.start()
    while True:
        inp = input()
        if inp == "exit":
            exit_cleanup()
            sys.exit(0)


if __name__ == "__main__":
    try:
        run_cortana()
    except KeyboardInterrupt as ex:
        atexit.register(exit_cleanup)
