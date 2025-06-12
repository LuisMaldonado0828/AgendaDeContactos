import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Ajusta según tu configuración
        database="agenda_db"
    )