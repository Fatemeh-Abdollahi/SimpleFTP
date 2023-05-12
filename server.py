from socket import *
import os
import random

server="127.0.0.1"
portNumber=2121
mysocket = socket(AF_INET,SOCK_STREAM)
mysocket.bind((server,portNumber))
print("***  WEICOME  ***")
mysocket.listen()
connection , address = mysocket.accept()
print("Client connected !")

def HELP():
    msg="""Commands List:\n
    HELP : Show help\n
    LIST : Show files and their sizes\n
    DWLD file_name : Download file\n
    PWD : Show current directory\n
    CD dir_name : Change directory\n
    QUIT : Exit\n"""
    print("Help sent successfully !")
    return msg

def LIST():
    msg=''
    total_size=0
    for file_name in os.listdir():
        if os.path.isdir(file_name):
            msg+= ">   "+file_name+"\t"+str(os.path.getsize(file_name))+" bytes \n"
            total_size+= os.path.getsize(file_name)
        else:
            msg+= "    "+file_name+"\t"+str(os.path.getsize(file_name))+" bytes \n"
            total_size+= os.path.getsize(file_name)
    msg+="Total Size : "+ str(total_size)+"bytes\n"
    print("List sent successfully !")
    return msg

def DWLD(command):
    file_path=command.split(" ")
    if os.path.exists(file_path[1]):
        random_server_port=random.randint(3000,50000)
        my_server_socket=socket(AF_INET, SOCK_STREAM)
        my_server_socket.bind((server, random_server_port))
        my_server_socket.listen()
        print("Starting download...")
        connection.send(str(random_server_port).encode())
        download_connection, download_address = my_server_socket.accept()
        sending_file=open(file_path[1],"rb")
        download_connection.send(sending_file.read())
        sending_file.close()
        my_server_socket.close()
        print("File sent successfully !")
        msg="File sent successfully !"
        return msg
    else:
        print("File not found !")
        msg="File not found !"
        return msg

def PWD():
    msg= os.getcwd()
    print("Current directory sent successfully !")
    return msg

def CD(command):
    file_path=command.split(" ")
    
    if not file_path[1].startswith(os.getcwd()):
        msg="Access denied !"
        print("Access denied !")
        return msg

    elif os.path.exists(file_path[1]):
        os.chdir(file_path[1])
        print("Directory changed successfully !")
        msg="Directory changed successfully ! you are in "+ os.getcwd()
        return msg

    else:
        msg="Directory not found !"
        print("Directory not found !")
        return msg


while True:
    print("Waiting for request")
    recieved_msg=connection.recv(1024).decode()

    if recieved_msg.startswith("HELP"):
        ans=HELP()
        connection.send(ans.encode())
    elif recieved_msg.startswith("LIST"):
        ans=LIST()
        connection.send(ans.encode())
    elif recieved_msg.startswith("DWLD"):
        ans=DWLD(recieved_msg)
        connection.send(ans.encode())
    elif recieved_msg.startswith("PWD"):
        ans=PWD()
        connection.send(ans.encode())
    elif recieved_msg.startswith("CD"):
        ans=CD(recieved_msg)
        connection.send(ans.encode())
    elif recieved_msg.startswith("QUIT"):
        connection.close()
        print("Bye!")
        break
