import socket # Red 
import threading # Concurrencia
import database
import requests

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
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

# Comandos a utilizar por el cliente
def procesar_comando(mensaje):

    partes = mensaje.split() # Separa el mensaje del comando
    comando = partes[0] # Primer parte del mensaje

    # /repos usuario
    if comando == "/repos":

        if len(partes) < 2:
            return "Debe indicar un usuario de GitHub (Ej: /repos daira-dev)."
        
        usuario_github = partes[1]

        # Traigo los repositorios de github del usuario
        url = f"https://api.github.com/users/{usuario_github}/repos"
        respuesta = requests.get(url)

        if respuesta.status_code != 200:
            return "Error consultando GitHub o usuario inexistente."

        datos = respuesta.json()

        # Traigo los repositorios de la base
        repos_db = database.obtener_repositorios(usuario_github)
        repos_db_set = {r[0] for r in repos_db}  # Solo traigo los nombres + link

        lista = []

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
                    url_repo
                )

        return (f"[REPOSITORIOS] {usuario_github}:\n" + "\n".join(lista))
    
    if comando == "/info":
        return (
            "\nComandos disponibles:"
            "/repos usuario — Obtiene repositorios de GitHub y los guarda en la base de datos\n"
        )


    return "Comando no reconocido."

# Comunicación con el cliente
def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr}.")

    # Recibo datos del cliente
    usuario = conn.recv(1024).decode("utf-8")
    clave = conn.recv(1024).decode("utf-8")

    print(f"Intento de ingreso: {usuario}")

    # Verifico usuario y contraseña
    if database.validar_usuario(usuario, clave):
        conn.send("LOGUEADO".encode("utf-8"))
        print(f"[INGRESO DE USUARIO] El usuario '{usuario}' ingresó al sistema.")
    
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
                respuesta = procesar_comando(mensaje)
                conn.send(respuesta.encode("utf-8"))
                continue
            conn.send(mensaje.encode("utf-8"))

    except ConnectionResetError:
        print(f"[DESCONECTADO] {usuario} se ha desconectado abruptamente.")

    finally:
        conn.close()

iniciar_servidor()