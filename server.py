import socket # Red
import threading # Concurrencia

# Inicio del servidor
def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creo socket
    puerto = 5050
    server.bind(('localhost', puerto)) # Defino IP + Puerto
    server.listen() # Servidor en escucha
    
    print("[INICIO] Servidor escuchando en el puerto {puerto}...")

    clientes_activos = []
    print("[INICIO] Servidor escuchando en el puerto 5050...")

    while True:
        conn, addr = server.accept() # Espero la conexión de un cliente
        clientes_activos.append(conn)
        
        # Crear hilo para el nuevo cliente
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, clientes_activos))
        hilo.start()
        
        print(f"[CLIENTES ACTIVOS] {len(clientes_activos)}")


# Comunicación con el cliente
def manejar_cliente(conn, addr, clientes_activos):
    print(f"\n[NUEVA CONEXIÓN] {addr} conectado.")

    # Solicito usuario
    conn.send("USUARIO".encode('utf-8'))
    usuario = conn.recv(1024).decode('utf-8')

    # Solicito contraseña
    conn.send("CONTRASEÑA".encode('utf-8'))
    passw = conn.recv(1024).decode('utf-8')

    if validar_usuario(usuario, passw):
        conn.send("LOGUEADO".encode('utf-8'))
        conectado = True
        print(f'[USUARIO LOGUEADO] {usuario}')
    else:
        conn.send("ERROR DE LOGUEO".encode('utf-8'))
        conectado = False
        print(f'[ERROR AL INGRESAR] {usuario}')
        conn.close()
        return

    while conectado:
        mensaje = conn.recv(1024).decode('utf-8') #  Recibo el mensaje del cliente 

        if not mensaje:
            print("Cliente desconectado.")
            break

        print(f'{usuario}: {mensaje}')

        conn.send(f'{mensaje}'.encode('utf-8')) # Respondo al cliente
     
    conn.close()

def validar_usuario(usuario, password):
    # Verifica si el usuario y contraseña existen
    return usuario == 'Daira' and password == "1234"

iniciar_servidor()