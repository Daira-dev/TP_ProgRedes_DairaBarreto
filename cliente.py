import socket # Red

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creo el socket
    cliente.connect(('localhost', 5050)) # IP + Puerto para conectar con el servidor
    
    print("[CONECTADO] Escribe mensajes (di 'salir' para terminar)")

    while True:
        mensaje = input("> ") # Pido el mensaje del usuario
        if mensaje.lower() == 'salir':
            break
            
        cliente.send(mensaje.encode('utf-8'))  # Envio mensaje al servidor
        respuesta = cliente.recv(1024).decode('utf-8') # Recibo respuesta del servidor       
        print(f"Servidor: {respuesta}")

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
