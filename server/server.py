from typing import TYPE_CHECKING 
if TYPE_CHECKING: 
    from _typeshed import Self
import socket
import os 
import sys
import time 
import struct
from  dataclasses import dataclass

@dataclass
class ServerFTP(object):
    
    def __init__(self, ip,port,buffer=1024):
        #el guión bajo sirve para hacer la variables privadas
        self.__ip=ip
        self.__port=port
        self.__buffer=buffer
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.conn=None
        self.addr=None
        self.data_address=None
        self.datasock=None
        self.mode='I'
    
    def freeze(self):
        self.socket.bind((self.__ip,self.__port) ) #Mantiene la conexión abierta en esa dirección
        self.socket.listen(1)#escucha la conexión
        self.conn, self.data_address = self.socket.accept() #Se ha abierto una nueva conexión lo cual implica una nueva dirección(ip, puerto) y esta función regresa un socket que permite el envio de datos a está nueva dirección  
    #Se va a encargar de los mensajes que le lleguen al socket 
    def receive(self):
        return self.conn.recv(self.__buffer )
    
    def upload(self,data):
        menu_opt = data[0]
        if(menu_opt == "EXIT"):
            pass # Se creara la opción de salida 
        filename = data[1]
        #
        dirS = "../dataS/"
        #Se crea un nuevo directorio para almacenar los archivos subidos
        try:
            if(not (os.path.exists(dirS)) ):
                os.mkdir(dirS) 
            serveFile = dirS+filename
            print("[RECV] Filename received.")
            file = open(serveFile,"w") #Se creara un nuevo documento con ese nombre y dirección
            self.conn.send("Filename received".encode("utf-8"))
            body = self.receive().decode("utf-8")
            print(f"[RECV] File data received.")
            file.write(body)
            self.conn.send("File data received".encode("utf-8"))
            file.close()
        except OSError as e:
            print(str(e))
            print("Hubo un problema al crear el direcrtorio dataS")
        
             
        """print(f"[LOADING FILE]: {filename}")
        self.conn.send("OPEN CONNECTION".encode())
        self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        readmode = "wb" if self.mode == "I" else  "w"
        try:
            with open(filename,readmode) as file:
                while True:
                    byte_recived = self.datasock.recv(self._buffer)
                    if not byte_recived: break
                    file.write(byte_recived)
            self.conn.send("[Sucessful Transfer]")    
        except Exception as e:
            self.conn.send("[Error access file]")
            print(str(e))
        finally:
            self.datasock.close()
            print("Succesful onload")   """  

    def exit(self):
        #Mandar mensaje de que se el servidor se va a cerrar
        print("[CLIENT POWEROFF]")
        self.conn.send("[Succesful poweroff]".encode("utf-8"))       
        
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname()) #Obtiene la dirección ip a traves del nombre del host (esto ya que el valor de IP puede variar dependiendo de SO)
    PORT = 2350
    print(f"[LISTENING] Server is listening on {IP} : {PORT}")
    server = ServerFTP(IP,PORT)
    server.freeze() 
    print("[Waiting query...]")
    #Se genera un paso de escucha
    while True:
        data = server.receive()
        print('Query: {0}'.format(data)) 
        data = data.decode('utf-8').split(',')
        if "UP"in data:
            server.upload(data)
        
        elif "EXIT" in data:
            server.exit()
            break    
            
        
               