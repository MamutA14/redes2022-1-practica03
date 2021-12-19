import socket
import os 
import struct
import sys

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
            self.socket.send("[SUCCESSFUL CONECTION]".encode())
            return 1
        except  ConnectionRefusedError as e:
            print(str(e))      
            print("[ERROR CONECTION] THE SERVER ISN'T REPLY....CLOSING CONNECTION")
            print("[SUGGEST] RETRY CONNECTION")
            return 0
        except BrokenPipeError as e:
            print(str(e))
            print("[ERROR CONECTION]")      
            self.socket.send("[ERROR CONECTION]".encode())
            return 0
        except OSError as e:
            try:
                print(str(e))
                print("[SUGGEST] CONNECTION WAS ESTABLISHED...don't make it again") 
                self.socket.send("[CONNECTION STATUS]".encode("utf-8"))
                return 1
            except Exception as e:
                print(str(e))
                print("CONNECTION IS NO LONGER AVAILABLE..CLOSING")
                exit()
                               
    def update(self,filename):
            clientFile = "../dataC/"+ filename
            rootfile = clientFile.split("/")[-1] #Me devolvera el nombre del documento y no toda la dirección
            try:
                file = open(clientFile,"rb")
                
                message = "UP"+","+rootfile
                self.socket.send(message.encode("utf-8"))
                msg = self.socket.recv(self.__buffer).decode("utf-8")
                print(f"[SERVER] {msg}")
                
                self.socket.send(struct.pack("i", os.path.getsize(clientFile)))
                
                data = file.read(self.__buffer)
                while data:
                    self.socket.send(data)
                    data = file.read(self.__buffer)
                file.close()    
                msg = self.socket.recv(self.__buffer).decode("utf-8")
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
             msg = self.socket.recv(self.__buffer).decode("utf-8")
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
            msg = self.socket.recv(self.__buffer).decode("utf-8")
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
            
    def download(self,filename):
        msg = "DOWNLOAD"+","+filename
        self.socket.send(msg.encode("utf-8"))
        file_size = struct.unpack("i",self.socket.recv(self.__buffer))[0] 
        if(file_size == -1):
            print("[SERVER ERROR] FILE DOESN'T EXIST IN SERVER")
            return
        else:
            #get file size if(exists)
            fm = msg.split(",")[1]
            clientFile = "../dataC/"+fm
            #Como queremos descargarlo y no actualizarlo entonces verificamos que no exista
            if(os.path.exists(clientFile)):
                files_list = os.listdir("../dataC/") #El directorio para simular el storage del cliente  
                i = 0
                for f in files_list:
                    if(f.find(fm.split(".")[0])  != -1):
                        #En caso de que se encuentre un archivo con el mismo nombre en el storage del cliente entonces simplemente le agregamos al nombre número extra para diferenciarlo una descarga de otra
                        fst =  f.find('(')
                        snd = f.find(')')
                        if (fst != -1  and snd != -1):
                            num =  int (f[fst+1:snd])
                            if(i < num):
                                i = num  
                               
                clientfilename = fm.split(".")[0] #Asi se evita que se actualice el actual que se posee
                clientfileext =fm.split(".")[1]
                #Se encuentra la descarga n-esima +1 y al nombre de este archivo le sumamos un uno más 
                clientFile = '../dataC/'+clientfilename +'(' + str(i+1) + ').'+clientfileext
            file = open(clientFile,"wb") #Se creara un nuevo documento con ese nombre y dirección
            self.socket.send("Filename received".encode("utf-8"))
            b_recieved = 0
            while b_recieved < file_size:
                doc = self.socket.recv(self.__buffer)
                file.write(doc)
                b_recieved += self.__buffer
            msg2 =  "[CLIENT]File data received..DOWNLOAD SUCCESSFUL"    
            self.socket.send(msg2.encode("utf-8"))
            print(msg2)
            file.close()
            
                
    def exit(self):
        try:
            self.socket.send("EXIT".encode("utf-8"))
            msg = self.socket.recv(self.__buffer).decode("utf-8")
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
        print("-----------MENU(Teclee su opción)--------\n             *)CONN(Conexión a servidor..siempre ejecutar al principio)\n             *)UP(actualizar archivo del servidor)\n             *)SHOW(Muestra archivos del servidor)\n             *)DOWN(Descarga archivos de servidor)\n             *)DEL(Elimina un archivo del programa)\n             *)EXIT(Salir del programa)      ")
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
                filename=""
                while(len(filename) == 0):
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
   
        elif command.upper() == "DOWN":
            if(connected):
                filename=""
                while(len(filename) == 0):
                    filename = input("Insert path with filename or  only filename(if it's in root): ")
                client.download(filename)
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
            print("COMMAND NOT FOUND PLEASE TRY AGAIN")
            if(connected):
                client.socket.send(command.encode())