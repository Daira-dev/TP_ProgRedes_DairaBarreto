import socket # Red 
import threading # Concurrencia
import database

# Inicio del servidor
def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creo socket
    puerto = 5050
    server.bind(("localhost", puerto)) # Defino IP + Puerto
    server.listen() # Servidor en escucha
    
    print("[INICIO] Servidor en escucha.")

    while True:
        conn, addr = server.accept() # Espero la conexión de un cliente
        
        # Creo hulo para el nuevo cliente  
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

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

    # Envío de mensajes
    try:
        while True:
            mensaje = conn.recv(1024).decode("utf-8")

            if not mensaje:
                break

            print(f"{usuario}: {mensaje}")

            conn.send(f"{mensaje}".encode("utf-8")) # Respondo al cliente
     
    except ConnectionResetError:
        print(f"[DESCONECTADO] {usuario} se ha desconectado.")

    finally:
        conn.close()

iniciar_servidor()