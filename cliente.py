import socket # Red de comunicación cliente-servidor (TPC)
import threading # Ejecutar tareas en paralelo

# ——————————————————————————————————

# Inicia el cliente y gestiona la conexión con el servidor
def iniciar_cliente():

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket
    cliente.connect(("localhost", 5050)) # IP + Puerto para conectar con el servidor
    
    print("[CONECTADO] Inicia sesión para continuar.\n")

    # Login
    # Solicita credenciales hasta autenticarse correctamente
    while True:
        usuario = input("Usuario: ")
        clave = input("Contraseña: ")
        
        # Envía credenciales al servidor
        cliente.send(usuario.encode("utf-8"))
        cliente.send(clave.encode("utf-8"))

        respuesta = cliente.recv(1024).decode("utf-8") # Espera la respuesta del servidor       

        # Login normal — Acceso autorizado
        if respuesta == "LOGUEADO": 
            print("\n[ACCESO CONCEDIDO] Bienvenido al sistema.")
            print("Para ver comandos puedes usar '/info'.\n")
            break

        # Error en el login — Acceso denegado
        print("\n[ACCESO DENEGADO] Usuario o contraseña incorrectos.\n")
    
    # ——————

    # Recepción de mensajes
    # Hilo que escucha mensajes del servidor sin bloquear el input
    hilo_receptor = threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True)
    hilo_receptor.start() # Inicio del hilo

    # Loop principal del chat
    # Chat del cliente
    while True:
        try:
            mensaje = input("> ") # Entrada del usuario
            cliente.send(mensaje.encode("utf-8"))

            # Comando de salida del sistema
            if mensaje.lower() == "/adios":
                print("\n[CERRANDO SESIÓN...]")
                print("[ADIOS] Gracias por utilizar el sistema.")
                break

        except ConnectionResetError:
            print("\n[CONEXIÓN CERRADA POR EL SERVIDOR]")
            break

        except BrokenPipeError:
            print("\n[CONEXIÓN PERDIDA]")
            break

    cliente.close()

# ——————————————————————————————————

# Función que se queda escuchando mensajes del servidor
def recibir_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024).decode("utf-8") # Espera mensaje del servidor
            
            # Si el servidor cierra la conexión
            if not mensaje:
                print("[DESCONECTADO DEL SERVIDOR]\n")
                break

            print(f"{mensaje}") # Muestra el mensaje recibido
            print("> ", end="", flush=True) # Para finjir el input
        
        except Exception:
            print("\n[CONEXIÓN CERRADA]")
            break # Desconexiones o errores

# ——————————————————————————————————

if __name__ == "__main__":
    iniciar_cliente() # Punto de entrada del programa cliente
