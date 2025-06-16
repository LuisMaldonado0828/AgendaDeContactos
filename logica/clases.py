# logica/clases.py

import mysql.connector
from logica.conexion import conectar

class Contacto:
    """Representa un contacto con sus datos y un ID de base de datos."""
    def __init__(self, nombre, telefono, email, id_contacto=None):
        self.id_contacto = id_contacto
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def get_nombre(self):
        return self.nombre

    def get_telefono(self):
        return self.telefono

    def get_email(self):
        return self.email
    
    def __str__(self):
        return f"Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}"


class Agenda:
    """Gestiona las operaciones CRUD (Crear, Leer, Actualizar, Borrar) de contactos en la base de datos."""
    def __init__(self):
        self.db = None
        self.cursor = None
        self._conectar_db()

    def _conectar_db(self):
        """Intenta establecer la conexión a la base de datos."""
        self.db = conectar()
        if self.db:
            self.cursor = self.db.cursor()

    def _asegurar_conexion(self):
        """Verifica si la conexión a la DB está activa y la reconecta si es necesario."""
        if not self.db or not self.db.is_connected():
            self._conectar_db()
        return self.db is not None and self.db.is_connected()

    def agregar_contacto(self, contacto):
        """Agrega un nuevo contacto a la base de datos. Retorna True si tiene éxito, False en caso contrario."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para agregar.")
            return False

        try:
            self.cursor.execute("SELECT id FROM contactos WHERE email = %s", (contacto.get_email(),))
            if self.cursor.fetchone():
                return False
            
            self.cursor.execute(
                "INSERT INTO contactos (name, telefono, email) VALUES (%s, %s, %s)",
                (contacto.get_nombre(), contacto.get_telefono(), contacto.get_email())
            )
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error al agregar contacto: {e}")
            return False

    def obtener_contactos(self):
        """Obtiene todos los contactos de la base de datos como una lista de objetos Contacto."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para obtener contactos.")
            return []

        try:
            self.cursor.execute("SELECT id, name, telefono, email FROM contactos ORDER BY name")
            resultados = self.cursor.fetchall()
            return [Contacto(fila[1], fila[2], fila[3], fila[0]) for fila in resultados]
        except mysql.connector.Error as e:
            print(f"Error al obtener contactos: {e}")
            return []

    def eliminar_contacto(self, id_contacto):
        """Elimina un contacto de la base de datos por su ID. Retorna True si tiene éxito, False en caso contrario."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para eliminar.")
            return False
            
        try:
            self.cursor.execute("DELETE FROM contactos WHERE id = %s", (id_contacto,))
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error al eliminar contacto: {e}")
            return False

    def editar_contacto(self, id_contacto, nuevo_nombre, nuevo_telefono, nuevo_email):
        """Actualiza los datos de un contacto en la base de datos. Retorna True si tiene éxito, False en caso contrario."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para editar.")
            return False

        try:
            self.cursor.execute("SELECT id FROM contactos WHERE email = %s AND id != %s", (nuevo_email, id_contacto))
            if self.cursor.fetchone():
                return False
                
            self.cursor.execute(
                "UPDATE contactos SET name = %s, telefono = %s, email = %s WHERE id = %s",
                (nuevo_nombre, nuevo_telefono, nuevo_email, id_contacto)
            )
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error al editar contacto: {e}")
            return False

    def buscar_contacto(self, nombre=None, telefono=None, email=None, contacto_a_excluir=None):
        """Busca un contacto en la base de datos por nombre, teléfono o email."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para buscar.")
            return None

        query = "SELECT id, name, telefono, email FROM contactos WHERE 1=1"
        params = []

        if nombre:
            query += " AND LOWER(name) = LOWER(%s)"
            params.append(nombre)
        if telefono:
            query += " AND telefono = %s"
            params.append(telefono)
        if email:
            query += " AND LOWER(email) = LOWER(%s)"
            params.append(email)
        
        if contacto_a_excluir and contacto_a_excluir.id_contacto:
            query += " AND id != %s"
            params.append(contacto_a_excluir.id_contacto)

        try:
            self.cursor.execute(query, tuple(params))
            fila = self.cursor.fetchone()
            if fila:
                return Contacto(fila[1], fila[2], fila[3], fila[0])
            return None
        except mysql.connector.Error as e:
            print(f"Error al buscar contacto: {e}")
            return None