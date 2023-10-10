import base64
import json
import os
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


def send_file_to_server(file_path, file_name):
    with open(file_path, "rb") as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')

    upload_file_message = {
        "message_type": "upload",
        "payload": {
            "file_name": file_name,
            "file_content": file_content,
        }
    }

    client_socket.send(json.dumps(upload_file_message).encode('utf-8'))


def download_file(payload):
    file_name = payload.get("file_name")
    file_content = payload.get("file_content")

    if not os.path.exists(f"files_{username}"):
        os.makedirs(f"files_{username}")

    time.sleep(1)

    with open(os.path.join(f"files_{username}", file_name), "wb") as file:
        file.write(base64.b64decode(file_content))

    print(f"Received file: {file_name}")


def list_files_in_folder(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            files.append(filename)
    return files


def request_server_files_list():
    files_list_request = {
        "message_type": "server_files_list",
        "payload": {}
    }

    client_socket.send(json.dumps(files_list_request).encode('utf-8'))


def download_server_file(file_name):
    download_file_request = {
        "message_type": "download_file",
        "payload": {
            "file_name": file_name
        }
    }

    client_socket.send(json.dumps(download_file_request).encode('utf-8'))


def server_list(payload):
    server_files = payload.get("files", [])

    if server_files:
        print("\nAvailable server files:")
        for index, file_name in enumerate(server_files, start=1):
            print(f"{index}. {file_name}")
    else:
        print("\nNo files available on the server.")


def receive_messages():
    while True:
        message = client_socket.recv(262144).decode('utf-8')

        if not message:
            break

        try:
            message_dict = json.loads(message)
            message_type = message_dict.get("message_type")
            payload = message_dict.get("payload")

            if message_type == "file":
                download_file(payload)

            elif message_type == "server_files_list":
                server_list(payload)

        except json.JSONDecodeError:
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

client_socket.send(json.dumps(connect_message).encode('utf-8'))

while True:
    text = input("Enter a message ('exit' to quit, 'upload' or 'u', 'list' or 'l', 'download' or 'd'): ")

    if not text:
        continue

    if text.lower() == 'exit':
        break

    elif text.lower() == 'upload' or text.lower() == 'u':

        if not os.path.exists(f"files_{username}"):
            os.makedirs(f"files_{username}")

        file_list = list_files_in_folder(f"files_{username}")

        if not file_list:
            print("No files found in the 'files' directory.")
        else:
            print("Available files for upload:")
            for index, file_name in enumerate(file_list, start=1):
                print(f"{index}. {file_name}")

            try:
                file_choice = int(input("Enter the number of the file to upload: ")) - 1

                if 0 <= file_choice < len(file_list):
                    selected_file = file_list[file_choice]
                    file_path = os.path.join(f"files_{username}", selected_file)

                    send_file_to_server(file_path, selected_file)
                    continue
                else:
                    print("Invalid file choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    elif text.lower() == 'list' or text.lower() == 'l':
        request_server_files_list()

    elif text.lower() == 'download' or text.lower() == 'd':
        file_name = input("Enter the name of the file to download: ")

        if not file_name:
            print("Invalid file name.")
            continue

        download_server_file(file_name)

    else:
        message = {
            "message_type": "message",
            "payload": {
                "text": text
            }
        }
        client_socket.send(json.dumps(message).encode('utf-8'))

client_socket.close()
