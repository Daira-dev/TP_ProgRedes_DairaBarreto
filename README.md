# Trabajo Práctico Integrador Programación sobre Redes
Implementación de un sistema cliente-servidor utilizando sockets en Python, base de datos en MySQL e integración con la API de GitHub.

# Tecnologías usadas
- Python
- Sockets
- Threads
- MySQL
- GitHub API

# Funciones principales
- Login de usuarios mediante base de datos en MySQL
- Comunicación cliente-servidor en tiempo real
- Manejo de múltiples clientes con threads
- Sistema de comandos por prefijo "/"
- Comandos:
    - /repos usuarios: guarda repositorios en base de datos y muestra los repositorios del usuario.
    - /followers usuario: guardar los datos de los seguidores del usuario ingresado en la base de datos y los muestra.
    /hora: El servidor debe devolver la hora del momento al cliente.
    - /usuarios El servidor debe devolver la lista de todos los usuarios conectados.
    - /todos "mensaje" : enviar mensaje a todos los clientes que estén conectados. 
    
    -/adios Se envía un mensaje de despedida y se desconecta.

# Commits
Commit_01 | Estructura Inicial
Commit_02 | Conexión con BD
Commit_03 | Comando /repos
Commit_04 | Comando /followers
Commit_05 | Comando /hora + /usuarios
Commit_06 | Comando /todos y chat concurrente