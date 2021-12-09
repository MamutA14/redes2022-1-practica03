import socket
import os 
import sys
import time 
import struct
import tqdm
import errno

class ClientFTP(object):
    
    def __init__(self, ip,port,buffer=1024):
        #el guión bajo sirve para hacer la variables privadas
        self.__ip=ip
        self.__port=port
        self.__buffer=buffer
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Se establecera la conexión aquí
    def connect(self):
        try:
            self.socket.connect((self.__ip,self.__port))
            print("[SUCCESSFUL CONECTION]")
            client.socket.send("[SUCCESSFUL CONECTION]".encode())
        except Exception as e:
            print(str(e))
            print("[ERROR CONECTION]")
            client.socket.send("[ERROR CONECTION]".encode())    
    
    
    def update(self,filename):
            clientFile = "../dataC/"+ filename
            try:
                file = open(clientFile,"r")
                data = file.read()
                message = "UP"+","+filename
                client.socket.send(message.encode("utf-8"))
                msg = client.socket.recv(1024).decode("utf-8")
                print(f"[SERVER] {msg}")
                client.socket.send(data.encode("utf-8"))
                msg = client.socket.recv(1024).decode("utf-8")
                print(f"[SERVER]:{msg}")
            except FileNotFoundError as e :
                print(str(e))
                print("File doesn't exist please try again: ")
                
                 
                
            

            
             
            """
            try:
                message = "UP"+","+filename
                self.socket.send(message.encode())
            except Exception as e:
                print(str(e))
            self.socket.send(struct.pack("i",len(filename.encode())))
            self.socket.send(filename.encode())
            filesize = os.path.getsize(filename)
            progress = tqdm.tqdm(range(filesize),f"Enciends {filename}",unit_scale=True,unit_divisor=1024)
            with open(filename,'rb') as file:
                self.socket.send(struct.pack("i",filesize))
                for x in progress:
                    bytes_read = file.read(self.__buffer)
                    if not bytes_read:
                        break
                    self.socket.sendall(bytes_read)
                    progress.update(len(bytes_read))   
                    """ 
    
    def exit(self):
        try:
            client.socket.send("EXIT".encode("utf-8"))
            msg = client.socket.recv(1024).decode("utf-8")
            print(f"[SERVER POWEROFF] {msg}")
        except Exception as e:
            print(str(e))
            print("[ERROR CONECTION]")
            #client.socket.send("[ERROR CONECTION]".encode())               
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname()) #Obtiene la dirección ip a traves del nombre del host (esto ya que el valor de IP puede variar dependiendo de SO)
    PORT = 2350
    client = ClientFTP(IP,PORT)
    print( "------[Client ftp]")
    while True:
        command = input ("[Insert command]: ")
        if command.upper() == "CONN":
            print("Sending Query Connection")
            client.connect()
        elif command.upper() == "UP":
            filename = input("Insert name file: ")
            client.update(filename)
        
        elif command.upper() == "EXIT":
            client.exit()
            break    
        else:
            client.socket.send(command.encode())