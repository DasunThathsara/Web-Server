import socket
import subprocess

HEADER = 64
PORT = 2728
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

request_type = "$_GET"


def serve_to_client(split_url, flag):
    if len(split_url) > 1 and flag:
        elements = """array("""
        value_array = split_url[1].split('&')
        for index in range(len(value_array)):
            elements += f"\"{value_array[index].split('=')[0]}\""
            elements += "=>"
            elements += f"\"{value_array[index].split('=')[1]}\""
            if index != len(value_array) - 1:
                elements += ", "
        elements += ")"

        try:
            print(split_url)

            f = open("temp.php", 'w')
            f.writelines(f"""
<?php
    {request_type}={elements};

    include_once './{split_url[0]}';
?>
""")
            f.close()
            php_output = subprocess.check_output(["./php/php.exe", "temp.php"], stderr=subprocess.STDOUT, cwd="./")
            return f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode('utf-8')
            return f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""

    else:
        try:
            php_output = subprocess.check_output(["./php/php.exe", "htdocs/" + split_url[0]], stderr=subprocess.STDOUT,
                                                 cwd="./")
            return f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode('utf-8')
            return f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""


def handle_client_request(conn, addr):
    global request_type
    print(f"[NEW CONNECTION] {addr} connected.")

    msg = conn.recv(4096).decode(FORMAT)

    lines = msg.split("\r\n")
    print("[REQUEST WITH DETAILS]", lines)

    requested_path = lines[0].split()[1][1:]
    if ".php" in requested_path:
        flag = 1
        split_url = []
        if lines[0].startswith("GET /"):
            split_url = requested_path.split("?")

        elif lines[0].startswith("POST /"):
            request_type = "$_POST"
            split_url = [requested_path, lines[-1]]

        else:
            flag = 0
            print(f"[{addr}] {msg}")

        response = serve_to_client(split_url, flag)

    elif requested_path == "favicon.ico":
        response = "./favicon.ico"

    elif requested_path == "":
        try:
            serve_to_client("index.php", 1)
        except:
            serve_to_client("index.html", 1)

    else:
        f = open(requested_path, 'r')
        msg = " ".join([i for i in f])
        response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{msg}"""

    conn.send(response.encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client_request(conn, addr)


print("[STARTING] server is starting...")
start()
