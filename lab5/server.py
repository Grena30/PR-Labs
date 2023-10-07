import json
import os
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

clients = {}
rooms = {}
users = {}


def handle_file_upload(payload, client_socket):
    file_name = payload.get("file_name")
    is_image = payload.get("is_image")
    file_content = payload.get("file_content")

    room_name = clients.get(client_socket)

    if room_name:
        for client in rooms[room_name]:
            if client != client_socket:
                send_file_to_client(file_name, file_content, client)


def send_file_to_client(file_name, file_content, client_socket):
    file_message = {
        "message_type": "file",
        "payload": {
            "file_name": file_name,
            "file_content": file_content,
        }
    }
    client_socket.send(json.dumps(file_message).encode('utf-8'))


def send_room_message(payload, client_socket):
    text = payload.get("text")
    room = clients.get(client_socket)
    sender = users[client_socket]

    message = {
        "message_type": "message",
        "payload": {
            "sender": sender,
            "room": room,
            "text": text
        }
    }
    message_user = f"{sender}: {text}"
    if room in rooms:
        for client in rooms[room]:
            if client != client_socket:
                client.send(message_user.encode('utf-8'))


def send_room_connection(payload, client_socket):
    client_name = payload.get("name")
    room_name = payload.get("room")

    if room_name not in rooms:
        rooms[room_name] = []

    rooms[room_name].append(client_socket)
    clients[client_socket] = room_name
    users[client_socket] = client_name

    notification_message = f"{client_name} has joined the room."
    for client in rooms[room_name]:
        if client != client_socket:
            send_notification(client, notification_message)

    message = "Connected to the room."
    connect_ack_message = {
        "message_type": "connect_ack",
        "payload": {
            "message": message
        }
    }

    client_socket.send(message.encode('utf-8'))


def send_notification(client_socket, notification_message):
    notification = {
        "message_type": "notification",
        "payload": {
            "message": notification_message
        }
    }
    client_socket.send(notification_message.encode('utf-8'))


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            print(f"Received from {client_address}: {message}")

            try:
                message_dict = json.loads(message)
                message_type = message_dict.get("message_type")
                payload = message_dict.get("payload")

                if message_type == "connect":
                    send_room_connection(payload, client_socket)
                elif message_type == "message":
                    send_room_message(payload, client_socket)
                elif message_type == "upload":
                    if payload.get("is_image"):
                        pass
                    else:
                        handle_file_upload(payload, client_socket)
            except json.JSONDecodeError:
                pass

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")

    finally:
        room_name = clients.get(client_socket)

        if room_name:
            rooms[room_name].remove(client_socket)

            username = users[client_socket]
            notification_message = f"{username} has left the room."

            del clients[client_socket]
            del users[client_socket]

            for client in rooms[room_name]:
                send_notification(client, notification_message)

        client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    clients[client_socket] = None
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
