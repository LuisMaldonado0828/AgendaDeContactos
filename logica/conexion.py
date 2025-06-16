# logica/conexion.py

import sqlite3
import os

def conectar():
    """
    Establece y devuelve una conexión a la base de datos SQLite.
    Crea la base de datos si no existe.
    """
    db_file = 'agenda.db'
    # db_path apunta al archivo 'agenda.db' en el directorio raíz del proyecto
    # os.path.abspath(__file__) obtiene la ruta absoluta del archivo actual (conexion.py)
    # os.path.dirname(...) obtiene el directorio de conexion.py (logica)
    # '..' sube un nivel al directorio del proyecto
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', db_file)

    try:
        # Abre la conexión a la base de datos SQLite
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos SQLite: {e}")
        return None