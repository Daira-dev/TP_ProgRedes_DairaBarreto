import socket # Red 
import threading # Concurrencia
import database
import requests
import datetime

usuarios_conectados = [] # Lista de usuarios que están conectados al sistema
conexiones = {}

# Inicio del servidor
def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creo socket
    puerto = 5050
    server.bind(("localhost", puerto)) # Defino IP + Puerto
    server.listen() # Servidor en escucha
    
    print("[INICIO] Servidor en escucha.")

    while True:
        conn, addr = server.accept() # Espero la conexión de un cliente
        
        # Creo hilo para el nuevo cliente  
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo_cliente.start()

# Comandos a utilizar por el cliente
def procesar_comando(mensaje, usuario):

    partes = mensaje.split() # Separa el mensaje del comando
    comando = partes[0] # Primer parte del mensaje

    # /repos usuario
    if comando == "/repos":

        if len(partes) < 2:
            return "Debe indicar un usuario de GitHub (Ej: /repos daira-dev)."
        
        usuario_github = partes[1] 

        # Traigo los repositorios de github del usuario
        url = f"https://api.github.com/users/{usuario_github}/repos"
        respuesta = requests.get(url) # texto en formato JSON

        if respuesta.status_code != 200:
            return "Error consultando GitHub o usuario inexistente."

        datos = respuesta.json() # convertir en estructuras Python

        # Traigo los repositorios de la base
        repos_db = database.obtener_repositorios(usuario_github)
        repos_db_set = {r[0] for r in repos_db}  # Solo traigo los nombres + link

        lista = [] # Para contruir el msj a devolver al cliente

        # Proceso los repositorios
        for repo in datos:
            nombre = repo["name"]
            url_repo = repo["html_url"]

            lista.append(f"- {nombre}\t{url_repo}")

            # Si el repositorio no existe en la base se agrega
            if nombre not in repos_db_set:
                database.guardar_repositorio(
                    usuario_github,
                    nombre,
                    url_repo)
                
        return (f"[REPOSITORIOS] {usuario_github}:\n" + "\n".join(lista))
    
    if comando == "/followers":

        if len(partes) < 2:
            return "Debe indicar un usuario de GitHub (Ej: /followers daira-dev)."
        
        usuario_github = partes[1]

        # Traigo los followers de GitHub
        url = f"https://api.github.com/users/{usuario_github}/followers"
        respuesta = requests.get(url) # texto en formato JSON

        if respuesta.status_code != 200:
            return "Error consultando GitHub o usuario inexistente."

        datos = respuesta.json() # convertir en estructuras Python

        # Traigo los followers de la base
        followers_db = database.obtener_followers(usuario_github)
        followers_db_set = {f[0] for f in followers_db}

        lista = [] # Para contruir el msj a devolver al cliente

        # Proceso los seguidores
        for follower in datos:
            seguidor = follower["login"]
            tipo = follower["type"]
            url_follower = follower["html_url"]

            lista.append(f"- {seguidor} ({tipo})\t{url_follower}")

            if seguidor not in followers_db_set:
                database.guardar_follower(
                    usuario_github, 
                    seguidor, 
                    tipo, 
                    url_follower)
                
        return ( f"[FOLLOWERS] {usuario_github}:\n" + "\n".join(lista) )
    
    if comando == "/hora":
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        return f"[HORA] {hora}"

    if comando == "/usuarios":

        lista_usuarios = []

        for usuario in usuarios_conectados:
            lista_usuarios.append(f"- {usuario}")

        return "[USUARIOS CONECTADOS]\n" + "\n".join(lista_usuarios)

    if comando == "/info":
        return (
            "\nComandos disponibles:\n"
            "/repos usuario — Obtiene repositorios de GitHub\n"
            "/followers usuario - Obtiene followers de GitHub\n"
            "/hora - Muestra la hora actual del servidor\n"
            "/usuarios - Muestra los usuarios conectados\n"
            "/todos - Envía un mensaje a todos los usuarios conectados\n"
            "/adios - Desconectarse del sistema\n"
        )

    if comando == "/adios":
        return "[ADIOS] Gracias por utilizar el sistema."
    
    if comando == "/todos":
        
        if len(partes) < 2:
            return "Debe escribir un mensaje. Ej: /todos Hola a todos."

        mensaje_todos = " ".join(partes[1:])
        
        for conexion in conexiones.items():
            try:
                conexion.send(f"[CHAT GLOBAL] {usuario}: {mensaje_todos}".encode("utf-8"))
            except:
                pass
    
    return "Comando no reconocido."

# Comunicación con el cliente
def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr}.")

    # Recibo datos del cliente
    while True:
        usuario = conn.recv(1024).decode("utf-8")
        clave = conn.recv(1024).decode("utf-8")

        print(f"Intento de ingreso: {usuario}")

        # Verifico usuario y contraseña
        if database.validar_usuario(usuario, clave):
            conn.send("LOGUEADO".encode("utf-8"))

            usuarios_conectados.append(usuario) # Agrega usuario
            conexiones[usuario] = conn # Conexión

            print(f"[INGRESO DE USUARIO] El usuario '{usuario}' ingresó al sistema.")
            break

        # Si la contraseña o usuario no coinciden / no existen
        else:
            conn.send("NO_LOGUEADO".encode("utf-8"))
            print(f"Error de ingreso: {usuario}")

    # Recibo y envío de mensajes
    try:
        while True:
            mensaje = conn.recv(1024).decode("utf-8")

            # Si no hay mensajes
            if not mensaje:
                print(f"[DESCONECTADO] {usuario} se ha desconectado.")
                break
            
            # Servidor recibe el mensaje del usuario
            print(f"[MENSAJE] {usuario}: {mensaje}")

            # Si el mensaje es un comando
            if mensaje.startswith("/"):
                respuesta = procesar_comando(mensaje, usuario)
                conn.send(respuesta.encode("utf-8"))

                if mensaje.lower() == "/adios":
                    if usuario in usuarios_conectados:
                        usuarios_conectados.remove(usuario)

                    if usuario in conexiones:
                        del conexiones[usuario]
                        
                    print(f"[DESCONECTADO] {usuario} cerró sesión.")
                    break
                continue

            # Mensaje normal
            conn.send(mensaje.encode("utf-8"))
                        
    except ConnectionResetError:
        print(f"[DESCONECTADO] {usuario} se ha desconectado.")
    
    finally:
        if usuario in usuarios_conectados:
            usuarios_conectados.remove(usuario)

        if usuario in conexiones:
            del conexiones[usuario]

        conn.close()

iniciar_servidor()