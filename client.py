from socket import *

server="127.0.0.1"
portNumber=2121
connection = socket(AF_INET,SOCK_STREAM)
connection.connect((server, portNumber))

while True:
    entered_command = input("Enter command: ")

    if entered_command=="HELP":
        connection.send(entered_command.encode())
        response=connection.recv(1024).decode()
        print(response)
    elif entered_command=="LIST":
        connection.send(entered_command.encode())
        response=connection.recv(1024).decode()
        print(response)
    elif entered_command.startswith("DWLD"):
        connection.send(entered_command.encode())
        response=connection.recv(1024).decode()
        if(response.isnumeric()):
            dwld_client = socket(AF_INET, SOCK_STREAM)
            dwld_client.connect((server, int(response)))
            filename = entered_command[5:]
            dwld_file = open(filename, 'wb')
            data = b""
            while True:
                binary_dwld = dwld_client.recv(1024)
                data += binary_dwld
                if not binary_dwld:
                    break
            dwld_file.write(data)
            dwld_file.close()
            dwld_client.close()
            print('Downloaded Successfully')
        else:
            print(response)
    elif entered_command=="PWD":
        connection.send(entered_command.encode())
        response=connection.recv(1024).decode()
        print(response)
    elif entered_command.startswith("CD"):
        connection.send(entered_command.encode())
        response=connection.recv(1024).decode()
        print(response)
    elif entered_command=="QUIT":
        connection.send(entered_command.encode())
        connection.close()
        print("Disconnected")
        break
    else:
        print("Command not found !")
