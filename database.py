import pymysql # Base de datos

def validar_usuario(usuario, clave):

    # Conexión a la base de datos
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="daira",
            password="8277",
            database="tp_redes"
        )
        print("Conexión exitosa")
        
    except Exception as e:
        print("Error:", e)

    cursor = conexion.cursor() # Canal de consulta

    # Consulta para verificar si el usuario y contraseña existen
    sql = """
    SELECT *
    FROM usuarios
    WHERE usuario = %s
    AND clave = %s
    """

    cursor.execute(sql, (usuario, clave))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None # Si encuentra coincidencias retorna True

