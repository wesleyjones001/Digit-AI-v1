import atexit
import base64
import os
import socket
import sys
import time
import uuid
import hashlib
import ssl
from _thread import *
from glob import glob
from multiprocessing import *

manager = Manager()

ServerSideSocket = None
cert_file_location = "ssl/cert.pem"  # For basic auth: use the same as the client.
private_key_location = "ssl/key.pem"  # server private key
__server_host = "localhost"
__server_ports = [x for x in range(1023, 1050)]  # For rapid testing purposes.
__server_port = None

process = None
session_id = uuid.uuid1()
modules_list = []
default_response = "Sorry, I don't understand."


def init_server():
    global __server_port
    global ServerSideSocket
    status = False
    for port in __server_ports:
        print(f"Trying to initialize Digit server on  port {port}...")
        try:
            ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ServerSideSocket.bind((__server_host, port))

            ServerSideSocket.listen(5)
            __server_port = port
            print("Server listening:")
            status = True
            break
        except Exception as e:
            print(str(e))
    return status


def sha1_for_file(filename, block_size=1024):
    sha1 = hashlib.sha1()
    file = open(filename, "r")
    while True:
        data = file.read(block_size).encode()
        if not data:
            break
        sha1.update(data)
    return sha1.hexdigest()


# This function is used to compute this unique version of the software and module hash. This can be used to
# distinguish between different configurations of modules. It uses sha1 hash function.
def compute_unique_version_id():
    # Find modules recursively. Allows for organization of components.
    files = [y for x in os.walk("modules/") for y in glob(os.path.join(x[0], '*.py'))]  # Only get python files.
    tmp1 = ""
    for file in files:
        if file.endswith(".py"):
            tmp1 += sha1_for_file(file)
    files = os.listdir("./common")
    tmp2 = ""
    for file in files:
        if file.endswith(".py"):
            tmp2 += sha1_for_file(f"common/{file}")
    hash_of_modules = hashlib.sha1(tmp1.encode()).hexdigest()[0:16]
    hash_of_common = hashlib.sha1(tmp2.encode()).hexdigest()
    main = hashlib.sha1((sha1_for_file("main.py") + hash_of_common).encode()).hexdigest()

    version_id = "SERVER_VERSION{" + main[0:8] + "}, MODULES_HASH{" + hash_of_modules + "}"
    # Version format example:
    # SERVER_VERSION{hash}, MODULES_HASH{hash}
    return version_id


def import_modules():
    global modules_list
    files = [y for x in os.walk("modules/") for y in glob(os.path.join(x[0], '*.py'))]
    for filename in files:
        if filename.endswith(".py"):
            global_name = filename.split("/")[-1]
            import_name = ''.join(filename.split("/")[-1]).replace("/", ".")
            import_dir = '/'.join(filename.split("/")[0:-1]).replace("/", ".")
            # print(f"global {global_name[0:-3]};from {import_dir} import {import_name[0:-3]}")
            module_name = import_name[0:-3]
            exec(f"global {global_name[0:-3]};from {import_dir} import {module_name}")
            module_version = ""
            try:
                module_version = eval(f"{module_name}.module_version")
            except AttributeError as ex:
                pass
            print(f"Imported module [{filename[0:-3]}] {module_version}")
            modules_list.append(import_name[0:-3])


def process_header(input: str):
    a1 = input.find("::")
    header_len = int(input[0:a1])
    header = input[a1 + 2:header_len + 2]
    a2 = header.split("::")
    session_id, machine_name, remote_time, new_var, response_len = a2[0], base64.b64decode(a2[1]).decode('utf-8'), a2[
        2], a2[3], a2[4]
    return session_id, machine_name, int(remote_time), new_var, int(response_len)


def create_header(input):
    global session_id
    machine_name = base64.b64encode("DIGIT_SERVER_1".encode()).decode()
    timestamp = round(time.time())
    content_len = len(input)
    tmp = f"::{session_id}::{machine_name}::{timestamp}::test::{content_len}"
    output = str(len(tmp)) + tmp
    output = output.ljust(150, '#')
    return output


def process_response(response):
    output = response.decode()
    return output


def check_scores(data, memory):
    scores = []
    for module in modules_list:
        result = eval(f'{module}.check_input(data, memory)')
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
    score, module = check_scores(data, client_command_memory)
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
    # session_id, machine_name, remote_time, new_var, response_len = None, None, None, None, None
    client_command_memory = []
    i = 0
    session_id = uuid.uuid1()  # use later

    while session_active:
        try:
            response1 = connection.recv(150).decode('utf-8')
            if len(response1) > 0:
                start = time.time()
                _, machine_name, remote_time, new_var, response_len = process_header(response1)
                response2 = connection.recv(response_len)
                new_data = process_response(response2)
                client_command_memory = handle_request(connection, new_data, client_command_memory)
                end = time.time()
                print(end - start, "S")
            time.sleep(0.2)
        except Exception as ex:
            print(str(ex))


def handle_connections(ServerSideSocket: socket):
    while True:
        try:
            Client, address = ServerSideSocket.accept()
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.check_hostname = False
            context.verify_mode = ssl.VerifyMode.CERT_OPTIONAL
            context.load_cert_chain(certfile=cert_file_location, keyfile=private_key_location)

            secureClientSocket = context.wrap_socket(Client, server_side=True)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(threaded_client, (secureClientSocket,))
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


def run_digit():
    global process
    status = init_server()
    import_modules()
    if not status:
        print(f"Error initializing Digit server on port {__server_port}.")
        quit(-1)
    else:
        print(f"Server initializing on port {__server_port}")
    print("This is Digit version is:", compute_unique_version_id())
    process = Process(target=handle_connections, args=(ServerSideSocket,))
    process.start()
    while True:
        inp = input()
        if inp == "exit":
            exit_cleanup()
            sys.exit(0)


if __name__ == "__main__":
    try:
        run_digit()
    except KeyboardInterrupt as ex:
        atexit.register(exit_cleanup)
