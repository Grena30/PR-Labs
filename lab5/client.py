import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"\nReceived: {message}")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

username = input("Enter your username: ")
room = input("Enter the room name: ")

connect_message = {
    "message_type": "connect",
    "payload": {
        "name": username,
        "room": room
    }
}

# Send the "connect" request to the server
client_socket.send(json.dumps(connect_message).encode('utf-8'))

while True:
    text = input("Enter a message ('exit' to quit, 'upload' or 'u' to add a file): ")

    if not text:
        continue

    if text.lower() == 'exit':
        break

    elif text.lower() == 'upload' or text.lower == 'u':
        upload_file = open("upload.txt", "r")

        data = upload_file.read()

        upload_file = {
            "message_type": "upload",
            "payload": {
                "name": username,
                "room": room,
                "file_content": data
            }
        }

        client_socket.send(json.dumps(upload_file).encode('utf-8'))
        continue

    else:
        message = {
            "message_type": "message",
            "payload": {
                "text": text
            }
        }
        client_socket.send(json.dumps(message).encode('utf-8'))

client_socket.close()
