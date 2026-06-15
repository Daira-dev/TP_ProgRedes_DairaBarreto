import pymysql # Base de datos

def conexion_db():
    # Conexión a la base de datos
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

def validar_usuario(usuario, clave):

    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return "Error de conexión."

    cursor = conexion.cursor() # Canal de consulta

    # Consulta para verificar si el usuario y contraseña existen
    sql = """
    SELECT * FROM usuarios
    WHERE usuario = %s AND clave = %s
    """

    cursor.execute(sql, (usuario, clave))
    resultado = cursor.fetchone()

    conexion.close()

    return resultado is not None # Si encuentra coincidencias retorna True

def obtener_repositorios(usuario):

    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return "Error de conexión."
        
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

def guardar_repositorio(usuario, nombre_repo, url_repo):
    
    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return "Error de conexión."
    
    cursor = conexion.cursor()

    sql = """
    INSERT INTO repositorios (usuario, nombre_repo, url_repo)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (usuario, nombre_repo, url_repo))
        conexion.commit()
        
        print(f"[REPOSITORIO AGREGADO] {usuario} -> {nombre_repo}.")

    except Exception as e:
        # Si el seguidor ya esta en la tabla
        print(f"[IGNORADO] {usuario} -> {nombre_repo}. Error: {e}")
    
    finally:
        conexion.close()

def obtener_followers(usuario):

    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return "Error de conexión."
        
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

def guardar_follower(usuario, seguidor, tipo, url_follower):
    
    conexion = conexion_db() # Conexión a la base de datos
    if conexion is None:
        return "Error de conexión."
    
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
        # Si el seguidor ya esta en la tabla
        print(f"[IGNORADO] {usuario} -> {seguidor}. Error: {e}")

    finally:
        conexion.close()
