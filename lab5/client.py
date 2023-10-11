import base64
import json
import os
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


def send_connect_message():
    client_name = input("Enter your username: ")
    room_name = input("Enter the room name: ")

    connect_message = {
        "message_type": "connect",
        "payload": {
            "name": client_name,
            "room": room_name
        }
    }

    client_socket.send(json.dumps(connect_message).encode('utf-8'))

    return client_name, room_name


def send_message():
    message = {
        "message_type": "message",
        "payload": {
            "text": text
        }
    }
    client_socket.send(json.dumps(message).encode('utf-8'))


def send_file(path, name):
    with open(path, "rb") as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    upload_file_message = {
        "message_type": "upload",
        "payload": {
            "file_name": name,
            "file_content": content,
        }
    }

    client_socket.send(json.dumps(upload_file_message).encode('utf-8'))


def download_file(payload, client_name):
    name = payload.get("file_name")
    content = payload.get("file_content")

    if not os.path.exists(f"files_{client_name}"):
        os.makedirs(f"files_{client_name}")

    with open(os.path.join(f"files_{client_name}", name), "wb") as file:
        file.write(base64.b64decode(content))

    print(f"\nReceived file: {name}")


def list_client_files(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            files.append(filename)
    return files


def list_server_files(payload):
    server_files = payload.get("files", [])

    if server_files:
        print("\nAvailable server files:")
        for i, name in enumerate(server_files, start=1):
            print(f"{i}. {name}")
    else:
        print("\nNo files available on the server.")


def request_server_list():
    files_list_request = {
        "message_type": "server_files_list",
        "payload": {}
    }

    client_socket.send(json.dumps(files_list_request).encode('utf-8'))


def request_server_file(name):
    download_file_request = {
        "message_type": "download_file",
        "payload": {
            "file_name": name
        }
    }
    client_socket.send(json.dumps(download_file_request).encode('utf-8'))


def get_server_message(payload):
    message = payload.get("message")
    print(f"\n{message}")


def get_room_message(payload):
    message = payload.get("message")
    sender = payload.get("sender")
    print(f"\n{sender}: {message}")


def get_file_path():
    file_path = input("Enter the path to the file: ")
    if not file_path:
        print("Invalid file path.")
        return

    if not os.path.exists(file_path):
        print("File not found.")
        return

    return file_path


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
                download_file(payload, username)

            elif message_type == "server_files_list":
                list_server_files(payload)

            elif message_type == "connect_ack":
                get_server_message(payload)

            elif message_type == "notification":
                get_server_message(payload)

            elif message_type == "message":
                get_room_message(payload)

        except json.JSONDecodeError:
            print(f"\nReceived: {message}")


def create_upload(client_name):
    print("1. File choice from 'files' directory ")
    print("2. File path")
    choice = input("Enter the number of the file upload method: ")

    if choice == "1":
        if not os.path.exists(f"files_{client_name}"):
            os.makedirs(f"files_{client_name}")

        file_list = list_client_files(f"files_{client_name}")

        if not file_list:
            print("No files found in the 'files' directory.")
        else:
            print("Available files for upload:")
            for i, name in enumerate(file_list, start=1):
                print(f"{i}. {name}")

            try:
                file_choice = int(input("Enter the number of the file to upload: ")) - 1

                if 0 <= file_choice < len(file_list):
                    selected_file = file_list[file_choice]
                    file_path = os.path.join(f"files_{client_name}", selected_file)

                    send_file(file_path, selected_file)
                    return
                else:
                    print("Invalid file choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    elif choice == "2":
        file_path = get_file_path()

        if not file_path:
            return

        file_name = os.path.basename(file_path)
        send_file(file_path, file_name)

    else:
        print("Invalid choice.")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

username, room = send_connect_message()

while True:
    text = input("Enter a message ('exit', 'upload' or 'u', 'list' or 'l', 'download' or 'd'): ")

    if not text:
        continue

    if text.lower() == 'exit':
        break

    elif text.lower() == 'upload' or text.lower() == 'u':
        create_upload(username)

    elif text.lower() == 'list' or text.lower() == 'l':
        request_server_list()

    elif text.lower() == 'download' or text.lower() == 'd':
        file_name = input("Enter the name of the file to download: ")
        if not file_name:
            print("Invalid file name.")
            continue

        request_server_file(file_name)

    else:
        send_message()

client_socket.close()
