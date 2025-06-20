# logica/conexion.py

import sqlite3
import os
import sys

def conectar():
    """
    Establece y devuelve una conexión a la base de datos SQLite.
    La base de datos se ubicará junto al ejecutable final (.exe)
    o en la raíz del proyecto durante el desarrollo.
    """
    db_file = 'agenda.db'
    
    if getattr(sys, 'frozen', False):
        # Si la aplicación se ejecuta como un ejecutable (PyInstaller)
        # La DB se guardará en el mismo directorio que el ejecutable.
        base_path = os.path.dirname(sys.executable) # <--- CAMBIO CRUCIAL AQUÍ
    else:
        # Si la aplicación se ejecuta desde un script Python (desarrollo)
        # La DB se guardará en el directorio principal del proyecto (donde está main.py).
        # Subimos dos niveles desde 'conexion.py' (logica/conexion.py -> logica -> proyecto_raiz)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    db_path = os.path.join(base_path, db_file)
    
    print(f"Ruta de la base de datos: {db_path}") # Útil para depuración

    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos SQLite: {e}")
        return None