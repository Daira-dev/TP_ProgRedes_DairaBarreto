# Trabajo Práctico Integrador Programación sobre Redes

`Carrera:` Tecnicatura Superior en Desarrollo de Software
`Alumna:` Daira Tamara Barreto

"Implementación de un sistema cliente-servidor utilizando sockets en Python, base de datos en MySQL e integración con la API de GitHub."

# Tecnologías usadas
- Python
- Sockets
- Threads
- MySQL
- GitHub API

# Instalaciones
Instalar, si es necesario, las dependencias del proyecto:
```pip install -r requirements.txt```

# Base de datos
Ejecutar el script SQL en MySQL o MariaDB para crear la base de datos `tp_redes`:

```bash
mysql -u root -p < script.sql

```└── tp_redes
    ├── Tables
    │   ├── followers
    │   ├── repositorios
    │   └── usuarios
    ├── Views
    ├── Stored Procedures
    └── Functions
```

# Ejecución
Iniciar primero el servidor:
```python server.py```

Luego iniciar uno o más clientes:
```python cliente.py```
- 'daira', '1234'
- 'profe', '1234'

# Estructura del proyecto
```
└── TPINTEGRADOR_PROGREDES
    ├── cliente.py
    ├── server.py
    ├── database.py
    ├── script.sql
    ├── requirements.txt
    └── README.md
```

# Funciones principales
- Login de usuarios mediante base de datos en MySQL
- Comunicación cliente-servidor en tiempo real
- Manejo de múltiples clientes con threads
- Sistema de comandos por prefijo "/"
- Comandos:
    - /repos usuario: guarda repositorios en base de datos y muestra los repositorios del usuario.
    - /followers usuario: guarda los datos de los seguidores del usuario ingresado en la base de datos y los muestra.
    /hora: El servidor debe devolver la hora del momento al cliente.
    - /usuarios El servidor debe devolver la lista de todos los usuarios conectados.
    - /todos mensaje : enviar mensaje a todos los clientes que estén conectados. 
    -/adios Se envía un mensaje de despedida y se desconecta.

# Commits
- Commit_01 | Estructura Inicial
- Commit_02 | Conexión con BD
- Commit_03 | Comando /repos
- Commit_04 | Comando /followers
- Commit_05 | Comando /hora + /usuarios
- Commit_06 | Comando /todos y chat concurrente
- Commit_07 | Agregado de documentación y comentarios
- Commit 08 | Correcciones README y requirements
- Commit 09 | Arreglos y Token para GitHub API
- Commit 10 | Revisiones y correcciones