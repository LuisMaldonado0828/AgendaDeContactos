import mysql.connector
from logica.conexion import conectar

class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def get_nombre(self):
        return self.nombre

    def get_telefono(self):
        return self.telefono

    def get_email(self):
        return self.email

class Agenda:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="agenda_db"
        )
        self.cursor = self.db.cursor()

    def agregar_contacto(self, contacto):
        try:
            self.cursor.execute("SELECT * FROM contactos WHERE email = %s", (contacto.get_email(),))
            if self.cursor.fetchone():
                print(" Ya existe un contacto con este correo.")
                return False
            self.cursor.execute(
                "INSERT INTO contactos (name, telefono, email) VALUES (%s, %s, %s)",
                (contacto.get_nombre(), contacto.get_telefono(), contacto.get_email())
            )
            self.db.commit()
            print(" Contacto agregado correctamente.")
            return True
        except Exception as e:
            print(" Error al agregar contacto:", e)
            return False

    def buscar_contacto(self, nombre):
        try:
            consulta = "SELECT * FROM contactos WHERE LOWER(name) LIKE %s"
            self.cursor.execute(consulta, (f"%{nombre.lower()}%",))
            fila = self.cursor.fetchone()
            if fila:
                return Contacto(fila[1], fila[2], fila[3])
            return None
        except Exception as e:
            print(" Error al buscar contacto:", e)
            return None

    def actualizar_contacto(self, nombre, nuevo_telefono, nuevo_email):
        try:
            self.cursor.execute(
                "UPDATE contactos SET telefono = %s, email = %s WHERE name = %s",
                (nuevo_telefono, nuevo_email, nombre)
            )
            self.db.commit()
            print("Contacto actualizado.")
        except Exception as e:
            print(" Error al actualizar:", e)

    def eliminar_contacto(self, nombre):
        try:
            self.cursor.execute("DELETE FROM contactos WHERE name = %s", (nombre,))
            self.db.commit()
            print(" Contacto eliminado correctamente.")
        except Exception as e:
            print("Error al eliminar:", e)

    def mostrar_todos(self):
        try:
            self.cursor.execute("SELECT * FROM contactos")
            resultados = self.cursor.fetchall()
            if not resultados:
                print(" Agenda vacía.")
            else:
                for fila in resultados:
                    print("------")
                    print(f"Nombre: {fila[1]}")
                    print(f"Teléfono: {fila[2]}")
                    print(f"Email: {fila[3]}")
        except Exception as e:
            print(" Error al mostrar todos los contactos:", e)
