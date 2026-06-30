import pymysql # Conexión y ejecución de consultas en MySQL

# ——————————————————————————————————

# Establece y devuelve una conexión a la base de datos
def conexion_db():
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="daira",
            password="8277",
            database="tp_redes"
        )
        return conexion
    
    except Exception as e:
        print("Error de conexión:", e)
        return None

# ——————————————————————————————————

# Valida si existe un usuario con esa contraseña en la base de datos
def validar_usuario(usuario, clave):

    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return False # Conexión fallida

    cursor = conexion.cursor() # Cursor para ejecutar consultas SQL

    # Consulta para verificar si el usuario y contraseña existen
    sql = """
    SELECT * FROM usuarios
    WHERE usuario = %s AND clave = %s
    """

    cursor.execute(sql, (usuario, clave))
    resultado = cursor.fetchone() # Devuelve una fila si existe, None si no existe

    conexion.close()

    return resultado is not None # Si encuentra coincidencias retorna True

# ——————————————————————————————————

# Obtiene los repositorios de un usuario
def obtener_repositorios(usuario):

    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return [] # Devuelve el mismo tipo de dato
        
    cursor = conexion.cursor()

    sql = """
    SELECT nombre_repo, url_repo
    FROM repositorios
    WHERE usuario = %s
    """

    cursor.execute(sql, (usuario,))
    datos = cursor.fetchall()

    conexion.close()

    return datos

# ——————————————————————————————————

# Guarda un repositorio en la base de datos
def guardar_repositorio(usuario, nombre_repo, url_repo):
    
    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return # No devuelve nada
    
    cursor = conexion.cursor()

    sql = """
    INSERT INTO repositorios (usuario, nombre_repo, url_repo)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (usuario, nombre_repo, url_repo))
        conexion.commit() # Confirma los cambios realizados en la bd
        
        print(f"[REPOSITORIO AGREGADO] {usuario} -> {nombre_repo}.")

    except Exception as e:
        # Si el repositorio ya está en la tabla (evita duplicados)
        print(f"[IGNORADO] {usuario} -> {nombre_repo}. Error: {e}")
    
    finally:
        conexion.close()

# ——————————————————————————————————

# Obtiene los seguidores almacenados en la base de datos
def obtener_followers(usuario):

    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return []
        
    cursor = conexion.cursor()

    sql = """
    SELECT seguidor, url_follower
    FROM followers
    WHERE usuario = %s
    """

    cursor.execute(sql, (usuario,))
    datos = cursor.fetchall()

    conexion.close()

    return datos

# ——————————————————————————————————

# Guarda un follower en la base de datos si no existe
def guardar_follower(usuario, seguidor, tipo, url_follower):
    
    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return
    
    cursor = conexion.cursor()

    sql = """
    INSERT INTO followers (usuario, seguidor, tipo, url_follower)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (usuario, seguidor, tipo, url_follower))
        conexion.commit()
        
        print(f"[AGREGADO] {usuario} -> {seguidor}.")

    except Exception as e:
        # Si el seguidor ya esta en la tabla (evita duplicados)
        print(f"[IGNORADO] {usuario} -> {seguidor}. Error: {e}")

    finally:
        conexion.close()
