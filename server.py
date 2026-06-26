import socket # Red de comunicación cliente-servidor (TPC) 
import threading # Concurrencia — múltiples clientes 
import database # Funciones de acceso y consulta a la bd
import requests # Consumo de la API de Github
import datetime # Fecha y hora del sistema
import os # Variables de entorno (token de GitHub)

# ——————————————————————————————————

usuarios_conectados = [] # Lista de usuarios que están conectados al sistema
conexiones = {} # Diccionario para el usuario y su conexión (socket)

# ——————————————————————————————————

# Inicio del servidor — TCP 
# Inicializa el servidor TCP y crea un hilo independiente para cada cliente
def iniciar_servidor():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket
    puerto = 5050
    server.bind(("localhost", puerto)) # Asocia el servidor a la IP local + Puerto definido
    server.listen() # Servidor en escucha (para recibir conexiones)
    
    print("[INICIO] Servidor en escucha.")

    while True:
        conn, addr = server.accept() # Espera la conexión de un cliente
        
        # Crea un hilo (independiente) para el nuevo cliente  
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo_cliente.start()

# ——————————————————————————————————

# Comandos a utilizar por el cliente
# Procesa los comandos enviados por el cliente y devuelve la respuesta al servidor
def procesar_comando(mensaje, usuario):

    partes = mensaje.split() # Separa el mensaje del comando por palabras
    comando = partes[0].lower() # Obtiene el comando solicitado

    # ——————

    # /repos usuario
    if comando == "/repos":

        # Valida que se haya ingresado bien los parámetros del comando
        error = validar_usuario_github(partes, "/repos")
        if error:
            return error

        usuario_github = partes[1] 

        # Trae los repositorios de la API de GitHub (del usuario)
        url = f"https://api.github.com/users/{usuario_github}/repos"
        respuesta = requests.get(url, headers=obtener_headers_github()) # Realiza la consulta a la API de GitHub

        if respuesta.status_code != 200:
            return "Error consultando GitHub o usuario inexistente."

        datos = respuesta.json()

        # Trae los repositorios de la base de datos
        repos_db = database.obtener_repositorios(usuario_github)
        repos_db_set = {r[0] for r in repos_db}  # Solo traigo los nombres + link

        lista = [] # Para el msj a devolver al cliente

        # Recorre los repositorios obtenidos desde Github
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

    # ——————

    # /followers usuario
    if comando == "/followers":

        # Valida que se haya ingresado bien los parámetros del comando
        error = validar_usuario_github(partes, "/followers")
        if error:
            return error

        usuario_github = partes[1]

        # Traigo los seguidores de GitHub
        url = f"https://api.github.com/users/{usuario_github}/followers"
        respuesta = requests.get(url, headers=obtener_headers_github()) # Realiza la consulta a la API de GitHub

        if respuesta.status_code != 200:
            return "Error consultando GitHub o usuario inexistente."

        datos = respuesta.json()

        # Trae los seguidores (del usuario indicado) de la base de datos
        followers_db = database.obtener_followers(usuario_github)
        followers_db_set = {f[0] for f in followers_db}

        lista = [] # Para el msj a devolver al cliente

        # Recorre los seguidores obtenidos desde GitHub
        for follower in datos:
            seguidor = follower["login"]
            tipo = follower["type"]
            url_follower = follower["html_url"]

            lista.append(f"- {seguidor} ({tipo})\t{url_follower}")

            # Si el seguidor no existe en la base se agrega
            if seguidor not in followers_db_set:
                database.guardar_follower(
                    usuario_github, 
                    seguidor, 
                    tipo, 
                    url_follower)
                
        return ( f"[FOLLOWERS] {usuario_github}:\n" + "\n".join(lista) )
    
    # ——————

    # /hora
    if comando == "/hora":

        error = validar_parametros(partes, "/hora")
        if error:
            return error
        
        # Obtiene la hora actual del servidor
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        return f"[HORA] {hora}"

    # ——————

    # /usuarios
    if comando == "/usuarios":

        error = validar_parametros(partes, "/usuarios")
        if error:
            return error

        # Muestra los usuarios conectados (actualizado)
        return "[USUARIOS CONECTADOS]\n" + formatear_usuarios_conectados()
    
    # ——————

    # /info
    if comando == "/info":

        error = validar_parametros(partes, "/info")
        if error:
            return error

        return (
            "\nComandos disponibles:\n"
            "/info — Muestra los comandos disponibles.\n"
            "/repos usuario — Obtiene repositorios de GitHub.\n"
            "/followers usuario - Obtiene followers de GitHub.\n"
            "/hora - Muestra la hora actual del servidor.\n"
            "/usuarios - Muestra los usuarios conectados.\n"
            "/todos mensaje - Envía un mensaje a todos los usuarios conectados.\n"
            "/mensaje usuario mensaje - Envía un mensaje privado a un usuario en específico.\n"
            "/adios - Desconectarse del sistema.\n"
        )

    # ——————

    # /adios
    if comando == "/adios":

        error = validar_parametros(partes, "/adios")
        if error:
            return error

        return "[ADIOS] Gracias por utilizar el sistema."
    
    # ——————

    # /todos mensaje    
    if comando == "/todos":

        mensaje_todos = " ".join(partes[1:]).strip()

        # Evitar mensajes vacíos
        if not mensaje_todos:
            return "Debe escribir un mensaje. Ej: /todos Hola a todos."

        # Recorre todas las conexiones activas y envía el mensaje a cada cliente
        for conexion in conexiones.values():
            try:
                conexion.send(f"[CHAT GLOBAL] {usuario}: {mensaje_todos}".encode("utf-8"))
            except Exception:
                pass # Si un cliente falla, no detiene el envío global

        return "☑ Enviado."

    # ——————

    # /mensaje usuario mensaje
    if comando == "/mensaje":

        # Evitar mensajes vacíos
        if len(partes) < 3:
            return "Debe escribir un destino y un mensaje. Ej:/mensaje daira Hola Dai."

        destino = partes[1] # Usuario destino
        mensaje_privado = " ".join(partes[2:]).strip() # Mensaje a enviar

        if destino not in conexiones:
            return "El usuario no existe o no se encuentra conectado."
        
        try:
            conexiones[destino].send(f"[MENSAJE PV] {usuario}: {mensaje_privado}".encode("utf-8"))
        except:
            return "No se pudo enviar el mensaje."

        return f"☑ Enviado a {destino}."
    
    # ——————

    # Si no coincide con ningún comando conocido
    return "Comando no reconocido."

# ——————————————————————————————————

# Comunicación con el cliente
# Maneja la comunicación de cada cliente conectado al servidor
def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr}.") # Muestra IP y puerto del cliente como registro al servidor

    # Validación
    # Recibe usuario y contraseña hasta que sean válidos
    while True: 
        usuario = conn.recv(1024).decode("utf-8")
        clave = conn.recv(1024).decode("utf-8")

        print(f"Intento de ingreso: {usuario}")

        # Verifico usuario y contraseña contra la base de datos
        if database.validar_usuario(usuario, clave):
            conn.send("LOGUEADO".encode("utf-8"))

            usuarios_conectados.append(usuario) # Agrega usuario
            conexiones[usuario] = conn # Diccionario de conexión

            print(f"[INGRESO DE USUARIO] El usuario '{usuario}' ingresó al sistema.")
            break

        # Si la contraseña o usuario no coinciden / no existen
        else:
            conn.send("NO_LOGUEADO".encode("utf-8"))
            print(f"Error de ingreso: {usuario}") # Esto es para el sistema
    
    # ——————

    # Mensajes
    # Recibo y envío de mensajes
    try:
        while True:
            mensaje = conn.recv(1024).decode("utf-8")

            # Si el socket se cierra o no hay datos
            if not mensaje:
                print(f"[DESCONECTADO] {usuario} se ha desconectado.")
                break
            
            print(f"[MENSAJE] {usuario}: {mensaje}") # Log del servidor

            # Si el mensaje es un comando (empieza con "/")
            if mensaje.startswith("/"):
                respuesta = procesar_comando(mensaje, usuario)
                conn.send(respuesta.encode("utf-8"))

                # Manejo especial de desconexión
                if mensaje.lower() == "/adios":
                    usuarios_conectados.remove(usuario)
                    del conexiones[usuario]
                    break

                continue  # no es un mensaje normal

            # Mensaje normal / respuesta simple
            conn.send(mensaje.encode("utf-8"))
                        
    # Maneja si hay un problema / desconexión inesperada
    except ConnectionResetError:
        print(f"[DESCONECTADO] {usuario} se ha desconectado.")
    
    # Limpieza en la lista de usuario_conectados y conexiones
    finally:
        if usuario in usuarios_conectados:
            usuarios_conectados.remove(usuario)

        conexiones.pop(usuario, None)

        conn.close()

# ——————————————————————————————————

# Valida comandos con usuario de GitHub (/repos, /followers)
def validar_usuario_github(partes, comando):
    
    if len(partes) < 2:
        return f"Debe indicar un usuario de GitHub (Ej: {comando} daira-dev)."

    if len(partes) != 2:
        return f"Uso correcto: {comando} usuario"

    return None

# Valida comandos que no deben recibir parámetros (/hora, /usuarios, etc..)
def validar_parametros(partes, comando):
    if len(partes) != 1:
        return f"El comando {comando} no recibe parámetros."
    return None

# Formatea la lista de usuarios conectados para mostrar al cliente actualizada
def formatear_usuarios_conectados():
    return "\n".join(f"- {u}" for u in usuarios_conectados)

# Token de Github
def obtener_headers_github():
    token = os.getenv("GITHUB_TOKEN") # Para autenticar la API de GitHub

    if token:
        return {"Authorization": f"token {token}"}

    return {}

# ——————————————————————————————————

if __name__ == "__main__":
    iniciar_servidor() # Iniciación del servidor
