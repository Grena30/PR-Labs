import json
import socket
import signal
import sys
import json2html


HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

with open("products.json", "r") as json_file:
    data = json.load(json_file)


product_pages = []
for i, product in enumerate(data):
    html = json2html.json2html.convert(json=product)
    product_pages.append(html)


def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    request_lines = request_data.split('\n')

    if len(request_lines) > 0:
        request_line = request_lines[0].strip().split()
    else:
        response = 'HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\nBad Request'
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        return

    if len(request_line) >= 2:
        method = request_line[0]
        path = request_line[1]
    else:
        response = 'HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\nBad Request'
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        return

    response_content = ''
    status_code = 200

    if path == '/':
        response_content = 'Hello, World!'
    elif path == '/about':
        response_content = 'This is the About page.'
    elif path == '/contact':
        response_content = 'This is the Contact page.'
    elif path == '/products':
        for i in range(len(data)):
            response_content += f"<a href='/product/{i}' target='_blank'>Product {i}</a> <br>"
    elif path.startswith('/product/'):
        id = path.split('/')[-1]
        try:
            response_content += product_pages[int(id)]
        except IndexError:
            response_content = '404 Not Found'
            status_code = 404
    else:
        response_content = '404 Not Found'
        status_code = 404

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    try:
        handle_request(client_socket)
    except KeyboardInterrupt:
        pass
