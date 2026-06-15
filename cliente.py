import socket # Red

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creo el socket
    cliente.connect(("localhost", 5050)) # IP + Puerto para conectar con el servidor
    
    print("[CONECTADO] Inicia sesión para continuar.\n")

    # Loop de login
    while True:
        usuario = input("Usuario: ")
        clave = input("Contraseña: ")

        cliente.send(usuario.encode("utf-8")) # Envio al servidor
        cliente.send(clave.encode("utf-8")) # Envio al servidor

        respuesta = cliente.recv(1024).decode("utf-8") # Recibo respuesta del servidor       

        # Login normal
        if respuesta == "LOGUEADO": 
            print("\n[ACCESO CONCEDIDO] Bienvenido al sistema.")
            print("Para ver comandos puedes usar '/info'.\n")
            break

        print("\n[ACCESO DENEGADO] Usuario o contraseña incorrectos.\n")
        continue

    # Chat del cliente
    while True:
        mensaje = input("> ")

        cliente.send(mensaje.encode("utf-8"))
        respuesta = cliente.recv(1024).decode("utf-8")

        print(respuesta)
        if mensaje.lower() == "/adios":
            break

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()