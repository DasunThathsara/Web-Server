# Web Server using Python

## Introduction
This is a simple web server to serve the PHP and HTML files. It runs on `localhost:2728`, and it can identify the `index.php` files automatically. Also, it has a dashboard, and you can see the server details, developer contact, and server controlling switches in the dashboard. The dashboard runs on `localhost:2728/index.php`, or you can simply search `localhost:2728` and the server will automatically navigate to the dashboard.

## Libraries I used
- ### socket
  - It helps to create the socket and bind it with our server, it returns the web browser request to our server, and helps to send the server request to the web browser. 
- ### subprocess
  - THis library helps to pass the requested php file to `php.exe` in the php folder and get the compiled result to the server. You can donload the php file using [this link](https://windows.php.net/download#php-8.2)
- ### os & sys
  - Handle the system functions

## How to run

Run the `start.py` file to start the server. After that, go to your browser and browse to `localhost:2728` and go to your location. If you want to create a PHP file and run it, save your files first in the `htdocs` folder, or create a folder in the `htdocs` and put your files in that folder.

## Technical Overview

First, create web socket and bind it with our server file
```python
PORT = 2728
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
```

After that, we start the server and server start listening the requests
```python
server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)
```

Then the server can get the browser requests and respond to them using various logics. The request can be `GET` or `POST`. The server can identify it and send the request according to that method.

<br>

If the user requests a PHP page, the browser or server can't read it and convert it to HTML. Therefore, the server uses the subprocess` library and `php.exe` to handle it.

```python
php_output = subprocess.check_output(["./php/php.exe", "htdocs/" + split_url[0]], stderr=subprocess.STDOUT, cwd="./")
response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{php_output.decode('utf-8')}"""
```

This method can pass the requested PHP file to get the executed value of that file. After that, we decode that response to `utf-8`. Also, the server concatenates that value with the HTTP header and sends it to the web browser as the response to the request.


____

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<a href="https://hits.sh/github.com/DasunThathsara/Web-Server/">
    <img alt="Hits" src="https://hits.sh/github.com/DasunThathsara/Web-Server.svg?label=Views"/>
</a>
<a href="https://github.com/DasunThathsara/Web-Server/actions">
    <img alt="Tests Passing" src="https://github.com/anuraghazra/github-readme-stats/workflows/Test/badge.svg" />
</a>

