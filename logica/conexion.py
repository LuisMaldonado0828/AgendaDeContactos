# logica/conexion.py

import mysql.connector

def conectar():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # ¡IMPORTANTE! Ajusta si tu contraseña de MySQL es diferente
            database="agenda_db"
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None