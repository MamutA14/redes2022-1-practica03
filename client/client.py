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
            rootfile = clientFile.split("/")[-1] #Me devolvera el nombre del documento y no toda la dirección
            try:
                file = open(clientFile,"r")
                data = file.read()
                message = "UP"+","+rootfile
                self.socket.send(message.encode("utf-8"))
                msg = self.socket.recv(1024).decode("utf-8")
                print(f"[SERVER] {msg}")
                self.socket.send(data.encode("utf-8"))
                msg = self.socket.recv(1024).decode("utf-8")
                print(f"[SERVER]:{msg}")
            except FileNotFoundError as e :
                print(str(e))
                print("File doesn't exist please try again: ")
                
                 
                
    def delete(self,filename):
        try:
             msg = "DELETE"+","+filename
             self.socket.send(msg.encode("utf-8"))
             msg = self.socket.recv(1024).decode("utf-8")
             if(msg == "s"):
                 print(f"[SERVER STATUS] SUCCESFULL DELETE OF "+filename)
             elif(msg == "er"):
                print(f"[SERVER STATUS] ERROR NO FILE NAME IT "+filename)       
             elif(msg == "em"):
                  print("[SERVER STATUS] ERROR THERE IS NO FILE IN SERVER")  
        except Exception as e :
            print(str(e))  

            
             
            
    
    def exit(self):
        try:
            self.socket.send("EXIT".encode("utf-8"))
            msg = self.socket.recv(1024).decode("utf-8")
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
        
        elif command.upper() == "DEL":
            filename = input("Insert name file: ")
            client.delete(filename)
        
        elif command.upper() == "EXIT":
            client.exit()
            break    
        else:
            client.socket.send(command.encode())