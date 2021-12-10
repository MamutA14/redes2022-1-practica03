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
            return 1
        except  ConnectionRefusedError as e:
            print(str(e))      
            print("[ERROR CONECTION] THE SERVER ISN'T REPLY....CLOSING CONNECTION")
            print("[SUGGEST] RETRY CONNECTION")
            return 0
        except BrokenPipeError as e:
            print(str(e))
            print("[ERROR CONECTION]")      
            client.socket.send("[ERROR CONECTION]".encode())
            return 0
        except OSError as e:
            try:
                print(str(e))
                print("[SUGGEST] CONNECTION WAS ESTABLISHED...don't make it again") 
                client.socket.send("[CONNECTION STATUS]".encode("utf-8"))
                return 1
            except Exception as e:
                print(str(e))
                print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
                exit()
                
                   
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
            except  BrokenPipeError as e:
                print(str(e))
                print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
                exit()   
            except IsADirectoryError as e:
                print(str(e))
                print("[SUGGEST] NOT PUT A DIRECTORY PLEASE TRY AGAIN")     
                
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
             elif(len(msg) == 0):
                print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
                exit()   
        except BrokenPipeError as e :
            print(str(e))
            print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
            exit() 

            
    def show(self,directory):
        try:
            msg = "SHOW"
            if(directory == ""):
                msg += ","+"." #Haciendo alución que es el directorio raíz
            else:
                msg +=","+directory #Se le pasa todo el directorio correspondiente
            self.socket.send(msg.encode("utf-8"))
            msg = self.socket.recv(1024).decode("utf-8")
            if(msg != "e" and msg != "." and len(msg)!=0):
                print("[SERVER STATUS] \n"+msg)
            elif(msg == '.'):
                print("[SERVER STATUS] \n"+"Empty")
            elif (len(msg) == 0):
                print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
                exit()
            else:
                print("[SERVER STATUS] THERE IS NO DIRECTORY CALL "+directory)            
            
        except BrokenPipeError as e:
            print(str(e))
            print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
            exit()
            
    
    def exit(self):
        try:
            self.socket.send("EXIT".encode("utf-8"))
            msg = self.socket.recv(1024).decode("utf-8")
            if(len(msg)==0):
                print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
                exit()
            else:    
                print(f"[SERVER POWEROFF] {msg}")
        except BrokenPipeError as e:
            print(str(e))
            print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
            exit()
            #client.socket.send("[ERROR CONECTION]".encode())               
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname()) #Obtiene la dirección ip a traves del nombre del host (esto ya que el valor de IP puede variar dependiendo de SO)
    PORT = 2350
    client = ClientFTP(IP,PORT)
    print( "------[Client ftp]")
    connected = False
    while True:
        command = input ("[Insert command]: ")
        if command.upper() == "CONN":
            print("Sending Query Connection")
            op = client.connect()
            connected = True if(op == 1) else False
        elif command.upper() == "UP":
            if(connected):
                filename=""
                while(len(filename) == 0):
                    filename = input("Insert name file: ")
                client.update(filename)
            else:
                print("[ERROR OPTION] PLEASE CONNECT TO SERVER: USE [CONN] OPTION IN THE LINE COMMAND")    
        
        elif command.upper() == "DEL":
            if(connected):
                filename = input("Insert name file: ")
                client.delete(filename)
            else:
                print("[ERROR OPTION] PLEASE CONNECT TO SERVER: USE [CONN] OPTION IN THE LINE COMMAND")  
    
        elif command.upper() == "SHOW":
            if(connected): 
                directory = input("Insert directory (or empty to see root):")
                client.show(directory)    
            else:
                print("[ERROR OPTION] PLEASE CONNECT TO SERVER: USE [CONN] OPTION IN THE LINE COMMAND")  
   
        
        elif command.upper() == "EXIT":
            if(connected):
                client.exit()
                client.socket.close()
                break
            else:
                print("[ERROR OPTION] PLEASE CONNECT TO SERVER: USE [CONN] OPTION IN THE LINE COMMAND")
                
        else:
            client.socket.send(command.encode())