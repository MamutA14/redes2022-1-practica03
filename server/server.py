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
            self.conn.send("There was an intern problem uploading file please retry".encode("utf-8"))
            
    
    def delete(self, data):
        filename = data[1]
        msg_stat = ""
        dirS ="../dataS/"
        absfilename = dirS+filename
        if(not (os.path.exists(dirS)) ):
            msg_stat = "em"
            print("[ERROR] THERE IS NO FILE IN SERVER")
        elif(os.path.exists(absfilename)):
            os.remove(absfilename)     
            msg_stat = "s"
            print("[SUCCESS] DELETE OF "+filename)
        else:
            msg_stat = "er"
            print("[ERROR] NO FILE NAME IT "+filename) 
        #Mandar status
        self.conn.send(msg_stat.encode("utf-8"))    
    
    def show(self,data):
        directory = data[1]
        msg =""
        rootdir = "../dataS/"
        '''
            Funciones lambda que seran necesarias al aplicar mapeo 
        '''
        f1 = lambda s: rootdir+s
        f2 = lambda s: s.replace(rootdir,'')
        f3 = lambda s: rootdir+directory+s if (directory[-1] == '/') else rootdir+directory+'/'+s
        f4 = lambda s: s.replace(rootdir+directory,'')if (directory[-1] == '/') else s.replace(rootdir+directory+'/','')
        d1 = lambda s: s.replace(rootdir,'')+'/' 
        d2 = lambda s: s.replace(rootdir+directory,'')+'/' if (directory[-1] == '/') else s.replace(rootdir+directory+'/','')+'/'
        if (directory== "."):
            try:
                ls = os.listdir(rootdir)
                files = (list(map(f2, (list(filter(os.path.isfile, map(f1,ls)))))))
                dirs = (list(map(d1, (list(filter(os.path.isdir,map(f1,ls)))))))
                msg = "  ".join(files + dirs)
                print("[SUCCESS] SHOWING FILES AND DIRECTORIES TO CLIENT")
                
            except FileNotFoundError as e:
                msg = "THERE IS NOTHING IN SERVER"
                print("[ERROR] NOTHING IN THE SERVER")
                
            
            finally:
                self.conn.send(msg.encode("utf-8"))
        else:
            try:
                ls = os.listdir(rootdir+directory)
                files = (list(map(f4, (list(filter(os.path.isfile, map(f3,ls)))))))
                dirs = (list(map(d2, (list(filter(os.path.isdir,map(f3,ls)))))))
                msg = "  ".join(files + dirs)
                print("[SUCCESS] SHOWING FILES AND DIRECTORIES TO CLIENT")
                
            except FileNotFoundError as e:
                 
                if(os.path.exists(rootdir)):
                    print(str(e)) #Mando el mensaje de que no hay ningún elemento en el directorio raíz
                    msg = "THERE IS  NO THAT DIRECTORY IN THE SERVER"
                    print("[SUGGEST]RETRY WITH A REAL DIRECTORY")
                else:
                     msg = "THERE IS NOTHING IN SERVER"
                     print("[ERROR] NOTHING IN THE SERVER")   
            except NotADirectoryError as e:
                msg = "THAT IS NOT A DIRECTORY PLEASE TRY AGAIN"
                print("[ERROR] THIS IS A FILE")    
            finally:
                if(len(msg) == 0):
                    msg = "."
                self.conn.send(msg.encode("utf-8"))         
          
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
        
        if(len(data) == 0):
            print("[CLIENT DISCONNECT PROTOCOL]")
            break 
        print('Query: {0}'.format(data))
        data = data.decode('utf-8').split(',')
        if "UP"in data:
            server.upload(data)
        
        elif "DELETE" in data:
            server.delete(data)
            
        elif "SHOW" in data:
            server.show(data)    
        elif "EXIT" in data:
            server.exit()
            server.socket.close()
            break    
            
        
               