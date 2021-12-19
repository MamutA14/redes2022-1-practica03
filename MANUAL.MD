# Manual de uso de socket cliente-servidor (ALAM ACOSTA MEZA num.d.cuenta:315124569)
## Inicialización
Primero se tiene que ejecutar el servidor o el cliente.(Realmente no importa el orden).Para ello hay que ubicarse en las carpetas client y server de manera correspondiente.
### Cliente
`>python3 client.py
------[Client ftp]
-----------MENU(Teclee su opción)--------
             *)CONN(Conexión a servidor..siempre ejecutar al principio)
             *)UP(actualizar archivo del servidor)
             *)SHOW(Muestra archivos del servidor)
             *)DOWN(Descarga archivos de servidor)
             *)DEL(Elimina un archivo del programa)
             *)EXIT(Salir del programa)      
[Insert command]: _
### Servidor
`>python3 server.py
[LISTENING] Server is listening on 127.0.1.1 : 2350

[Waiting query...]
Query: b'[SUCCESSFUL CONECTION]'`
`

### CONEXIÓN
Luego de ello se debe de ejecutar el comando conn. El cual permitara la conexión entre el cliente y el servidor .Si se ejecuta otro comando mandara mensaje de que se debe de ejecutar primero ese.
`>python3 client.py

------[Client ftp]
-----------MENU(Teclee su opción)--------
             *)CONN(Conexión a servidor..siempre ejecutar al principio)
             *)UP(actualizar archivo del servidor)
             *)SHOW(Muestra archivos del servidor)
             *)DOWN(Descarga archivos de servidor)
             *)DEL(Elimina un archivo del programa)
             *)EXIT(Salir del programa)      
[Insert command]: conn
Sending Query Connection
[SUCCESSFUL CONECTION]
`
A partir de aquí se pueden efectuar todas las operaciones. A excepción de conn ya que la conexión se estableció si se pide entonces mandara un mensaje de que la conexión ya se ha realizado y es inncesario volverla a hacer. 
## Operaciones
### UPLOAD(UP)
Bien lo que se va a hacer es simple por parte del cliente se va a declarar la opción "up". Up se encargara de actualizar un archivo en el servidor el cual tenga el mismo nombre tanto del 
lado del cliente como del servidor. Si no hay ningún documento que posea el nombre del archivo por parte del cliente entonces se generara un nuevo archivo.
En caso dado que se este ejecutando por 1era vez el programa la carpeta (que corresponderia al almacenamiento por parte del servidor) dataS se generara junto con el documento.(Sin embargo en el repositorio ya hay un ejemplar de este directorio)

Anotaciones:
Como esto es una simulación la carpeta dataC representara el almacenamiento por parte del cliente por lo que luego de haber puesto la opcion "UP" inmediatamente se le pedira el nombre del archivo a subir y este nombre sera buscado en esa misma carpeta.


Tambien en dado caso que el archivo no se encuentre en dataC (o no se encuentre en subdirectorios de este) entonces desplegara un mensaje de error y que por favor lo vuelva a intentar.
### SHOW
Este método tiene como función desplegar los archivos o directorios de una ruta en especifico del servidor.
Para usarla hay que declarar en la terminal el comando "SHOW" luego de ello pedira una ruta en especial. Si en caso dado se requiere ver el directorio raíz se da enter sin haber declarado nada. En otro caso se tendra que insertar la ruta. En caso de que se busque un archivo mandara un mensaje de que es un archivo y no se puede desplegar. Tambien maneja errores  tanto de no encontrar la ruta o mostrar al cliente que esa ruta está vacia. Al igual que con update se simulara la busqueda a partir del directorio dataS.
### DELETE
El método delete empezara cuando el usuario teclee la opción "del" de esa manera se le pedira la ruta del archivo  a eliminar. Si se encuentra en el directorio raíz solo es necesario poner el nombre. En otro caso hay que poner toda la ruta por ejemplo si se encuentra en el directorio dir0 que se encuentra en el directorio raíz entonces hay que declarar dir0/[nombre de archivo]nombre.
Aquí pueden ocurrir tres posibles escenarios:
1. Se encuentra el archivo y se elimina de manera exitosa por parte del servidor(dataS) se manda mensaje de exito al cliente.
2. No se encuentra el archivo entonces se manda mensaje de error.
3.Como no hay ningún archivo por parte del servidor entonces la carpeta("almacenamiento") del servidor no se ha creado aun  por lo tanto manda mensaje de error.

### DOWN(DOWNLOAD)
La opcion de download se aplicara cuando el cliente tecle el comando "down" ó "DOWN" (su función sera  similar al upload) luego se  le pedira la ruta completa del archivo a descargar. Si no  se encuentra disponible o esta mal escrito se le anunciara al cliente, que tal archivo no existe, por ello, es recomendable utilizar la función show antes de este comando en caso de dudas de la ubicación del archivo. Si el archivo existe en el servidor no debería haber ningún problema y se debera resguardar en el almacenamiento del cliente(es decir la carpeta dataC).
### EXIT
La opción exit pondra fin a la comunicación entre cliente y servidor.Se aplicara cuando el cliente tecle el comando "exit".Poniendo un fin a la  ejeccución de ambos. Pero antes que eso suceda al cliente le debe de llegar un mensaje de  que la sesión se cerro de manera exitosa.

## Notas finales
Se hace la simulación de que se está ejecutando en dos equipos distintos el cliente y el servidor. Para ello se utilizan dos directorios distintos dataC y dataS lo que correspondera al storage del cliente y el servidor respectivamente.
Finalmente las opciones del menu no son case sensitive por lo que no hay problema si se escriben todas en mayusculas o en minusculas. Seguira siendo lo mismo. Tambíen si una opción no se encuentra  disponible en el menu mandara un mensaje sobre ello. Y volvera a mostrarlo y seguir con su ejecucción habitual.
