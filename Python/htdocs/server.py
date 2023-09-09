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


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    msg = conn.recv(4096).decode(FORMAT)

    lines = msg.split("\r\n")
    print("[REQUEST WITH DETAILS]", lines)
    if lines[0].startswith("GET /"):
        requested_path = lines[0].split()[1][1:]

        if ".php" in requested_path:
            split_url = requested_path.split("?")

            if len(split_url) > 1:
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
                    $_GET={elements};

                    include_once './{split_url[0]}';
                ?>
                                """)
                    f.close()
                    php_output = subprocess.check_output(["./php/php.exe", "temp.php"], stderr=subprocess.STDOUT,
                                                         cwd="./")
                    response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
                except subprocess.CalledProcessError as e:
                    error_message = e.output.decode('utf-8')
                    response = f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""

            else:
                    try:
                        php_output = subprocess.check_output(["./php/php.exe", split_url[0]], stderr=subprocess.STDOUT, cwd="./")
                        response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
                    except subprocess.CalledProcessError as e:
                        error_message = e.output.decode('utf-8')
                        response = f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""

        elif requested_path == "favicon.ico":
            response = "./favicon.ico"

        else:
            f = open(requested_path, 'r')
            msg = " ".join([i for i in f])
            response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{msg}"""
        conn.send(response.encode(FORMAT))

    elif lines[0].startswith("POST /"):
        requested_path = lines[0].split()[1][1:]

        if ".php" in requested_path:
            split_url = [requested_path, lines[-1]]

            if len(split_url) > 1:
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
                            $_POST={elements};

                            include_once './{split_url[0]}';
                        ?>
                                        """)
                    f.close()
                    php_output = subprocess.check_output(["./php/php.exe", "temp.php"], stderr=subprocess.STDOUT,
                                                         cwd="./")
                    response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
                except subprocess.CalledProcessError as e:
                    error_message = e.output.decode('utf-8')
                    response = f"""HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\nInternal Server Error:<br>{error_message}"""
        else:
            f = open(requested_path, 'r')
            msg = " ".join([i for i in f])
            response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{msg}"""
        conn.send(response.encode(FORMAT))

    else:
        print(f"[{addr}] {msg}")

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


print("[STARTING] server is starting...")
start()
