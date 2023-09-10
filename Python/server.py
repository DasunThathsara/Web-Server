import socket
import subprocess
import os
import sys


HEADER = 64
PORT = 2728
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

request_type = "$_GET"


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def handle_client(conn, addr):
    global request_type
    print(f"[NEW CONNECTION] {addr} connected.")

    msg = conn.recv(4096).decode(FORMAT)

    lines = msg.split("\r\n")
    print("[REQUEST WITH DETAILS]", lines)

    if lines == ['']:
        start()

    requested_path = lines[0].split()[1][1:]

    url_end_slash = True
    if requested_path == "":
        url_end_slash = False
        requested_path = "index.php"
    elif ".php" not in requested_path and ".html" not in requested_path:
        if requested_path[-1] == '/':
            requested_path += "index.php"
        else:
            url_end_slash = False
            requested_path += "/index.php"

    if ".php" in requested_path:
        flag = 1
        split_url = []
        if lines[0].startswith("GET /"):
            request_type = "$_GET"
            split_url = requested_path.split("?")

        elif lines[0].startswith("POST /"):
            request_type = "$_POST"
            split_url = [requested_path, lines[-1]]
            if lines[-1] == "shutdown=":
                exit(0)

        else:
            flag = 0
            print(f"[{addr}] {msg}")

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
                f = open("temp.php", 'w')
                f.writelines(f"""
<?php
    {request_type}={elements};

    include_once './htdocs/{split_url[0]}';
?>
""")
                f.close()
                php_output = subprocess.check_output(["./php/php.exe", "temp.php"], stderr=subprocess.STDOUT, cwd="./")
                response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
            except subprocess.CalledProcessError as e:
                error_message = e.output.decode('utf-8')
                response = f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""

        else:
            try:
                if url_end_slash:
                    php_output = subprocess.check_output(["./php/php.exe", "htdocs/" + split_url[0]], stderr=subprocess.STDOUT, cwd="./")
                    response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
                else:
                    php_output = subprocess.check_output(["./php/php.exe", "htdocs/" + requested_path],
                                                         stderr=subprocess.STDOUT, cwd="./")
                    response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}""" + """    <script>\n        window.history.pushState({}, "", "/""" + requested_path + """\");\n    </script>\n</body>\n</html>\n"""

            except subprocess.CalledProcessError as e:
                error_message = e.output.decode('utf-8')
                response = f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""

    elif requested_path == "favicon.ico":
        response = "./favicon.ico"

    else:
        f = open('./htdocs/' + requested_path, 'r')
        msg = " ".join([i for i in f])
        response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{msg}"""

    conn.send(response.encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


print("[STARTING] server is starting...")
start()
