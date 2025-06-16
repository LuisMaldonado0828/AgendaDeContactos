# logica/clases.py

import sqlite3
import uuid # Necesario para generar IDs únicos si id_contacto es None
from logica.conexion import conectar # Importa la función conectar de tu módulo de conexión

class Contacto:
    """Representa un contacto con sus datos y un ID de base de datos."""
    def __init__(self, nombre, telefono, email, id_contacto=None):
        # Si el ID no viene, generamos uno con UUID para que sea TEXT PRIMARY KEY
        # Esto es robusto para evitar colisiones y es compatible con TEXT en SQLite.
        self.id_contacto = id_contacto if id_contacto is not None else str(uuid.uuid4())
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
        return f"ID: {self.id_contacto}, Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}"

    def __repr__(self):
        return f"Contacto(id_contacto='{self.id_contacto}', nombre='{self.nombre}', telefono='{self.telefono}', email='{self.email}')"


class Agenda:
    """Gestiona las operaciones CRUD (Crear, Leer, Actualizar, Borrar) de contactos en la base de datos."""
    def __init__(self):
        self.db = None
        self.cursor = None
        self._conectar_db()
        self._crear_tabla() # Aseguramos que la tabla exista al inicializar la Agenda

    def _conectar_db(self):
        """Intenta establecer la conexión a la base de datos."""
        self.db = conectar() # Llama a la función conectar de logica.conexion
        if self.db:
            self.cursor = self.db.cursor()
        else:
            print("ERROR: No se pudo establecer conexión a la base de datos.")

    def _asegurar_conexion(self):
        """Verifica si la conexión a la DB está activa y la reconecta si es necesario."""
        if not self.db:
            self._conectar_db()
        return self.db is not None

    def _crear_tabla(self):
        """
        Crea la tabla 'contactos' si no existe.
        Este método se llama una vez al inicializar la Agenda.
        Se ha corregido el 'unrecognized token: "#"' quitando el comentario de la línea SQL.
        Se ha añadido COLLATE NOCASE a telefono y email para unicidad insensible a mayúsculas/minúsculas.
        """
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para crear la tabla.")
            return

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS contactos (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    telefono TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    email TEXT NOT NULL COLLATE NOCASE UNIQUE
                )
            ''')
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tabla: {e}")


    def agregar_contacto(self, contacto):
        """Agrega un nuevo contacto a la base de datos. Retorna True si tiene éxito, False en caso contrario."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para agregar.")
            return False

        try:
            # Los placeholders de SQLite son '?'
            # Asegúrate de que Contacto.id_contacto tiene un valor (ej. UUID)
            self.cursor.execute("INSERT INTO contactos (id, name, telefono, email) VALUES (?, ?, ?, ?)",
                                (contacto.id_contacto, contacto.get_nombre(), contacto.get_telefono(), contacto.get_email()))
            self.db.commit()
            return True
        except sqlite3.IntegrityError as e: # Captura errores de unicidad (UNIQUE constraints)
            print(f"Error de integridad al agregar contacto (posible duplicado de email/teléfono): {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al agregar contacto: {e}")
            return False

    def obtener_contactos(self):
        """Obtiene todos los contactos de la base de datos como una lista de objetos Contacto."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para obtener contactos.")
            return []

        try:
            # COLLATE NOCASE para ordenamiento insensible a mayúsculas/minúsculas en SQLite
            self.cursor.execute("SELECT id, name, telefono, email FROM contactos ORDER BY name COLLATE NOCASE")
            resultados = self.cursor.fetchall()
            # Se construye una lista de objetos Contacto
            return [Contacto(fila[1], fila[2], fila[3], fila[0]) for fila in resultados]
        except sqlite3.Error as e:
            print(f"Error al obtener contactos: {e}")
            return []

    def eliminar_contacto(self, id_contacto):
        """Elimina un contacto de la base de datos por su ID. Retorna True si tiene éxito, False en caso contrario."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para eliminar.")
            return False
            
        try:
            self.cursor.execute("DELETE FROM contactos WHERE id = ?", (id_contacto,))
            self.db.commit()
            return self.cursor.rowcount > 0 # Retorna True si se eliminó una fila
        except sqlite3.Error as e:
            print(f"Error al eliminar contacto: {e}")
            return False

    def editar_contacto(self, id_contacto, nuevo_nombre, nuevo_telefono, nuevo_email):
        """Actualiza los datos de un contacto en la base de datos. Retorna True si tiene éxito, False en caso contrario."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para editar.")
            return False

        try:
            # La validación de duplicados (por teléfono/email) se manejará a nivel de interfaz (validar_datos_contacto)
            # o por las UNIQUE constraints de la DB.
            # No es necesario hacer una búsqueda explícita aquí antes del UPDATE si las constraints están bien.

            self.cursor.execute(
                "UPDATE contactos SET name = ?, telefono = ?, email = ? WHERE id = ?",
                (nuevo_nombre, nuevo_telefono, nuevo_email, id_contacto)
            )
            self.db.commit()
            return self.cursor.rowcount > 0 # Retorna True si se actualizó una fila
        except sqlite3.IntegrityError as e: # Captura si el nuevo teléfono/email ya existe en otro contacto
            print(f"Error de integridad al editar contacto (posible duplicado de teléfono/email): {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al editar contacto: {e}")
            return False

    def buscar_contacto(self, nombre=None, telefono=None, email=None, contacto_a_excluir=None):
        """
        Busca un contacto en la base de datos por nombre, teléfono o email.
        Este método es más para validación (duplicados) que para la búsqueda general en UI.
        """
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para buscar.")
            return None

        query = "SELECT id, name, telefono, email FROM contactos WHERE 1=1"
        params = []

        # Usamos LOWER() para hacer la búsqueda de nombre e email insensible a mayúsculas/minúsculas.
        # También se aplica a teléfono por si COLLATE NOCASE no fue suficiente o la validación lo requiere.
        if nombre:
            query += " AND LOWER(name) = LOWER(?)"
            params.append(nombre)
        if telefono:
            query += " AND LOWER(telefono) = LOWER(?)" # Modificado para que teléfono también sea insensible a mayúsculas/minúsculas en la búsqueda
            params.append(telefono)
        if email:
            query += " AND LOWER(email) = LOWER(?)"
            params.append(email)
        
        # Excluir un contacto específico (útil para la edición, para no considerarse a sí mismo un duplicado)
        if contacto_a_excluir and contacto_a_excluir.id_contacto:
            query += " AND id != ?"
            params.append(contacto_a_excluir.id_contacto)

        try:
            self.cursor.execute(query, tuple(params))
            fila = self.cursor.fetchone()
            if fila:
                # Retornar un objeto Contacto si se encuentra
                return Contacto(fila[1], fila[2], fila[3], fila[0])
            return None
        except sqlite3.Error as e:
            print(f"Error al buscar contacto: {e}")
            return None

    def buscar_contactos_por_cadena(self, cadena_busqueda):
        """
        Busca contactos cuyos nombres contengan la cadena de búsqueda.
        Realiza una búsqueda insensible a mayúsculas/minúsculas.
        """
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para buscar contactos por cadena.")
            return []

        try:
            # LOWER(name) LIKE ? para búsqueda de subcadenas insensible a mayúsculas/minúsculas
            self.cursor.execute("SELECT id, name, telefono, email FROM contactos WHERE LOWER(name) LIKE ? ORDER BY name COLLATE NOCASE ASC",
                           ('%' + cadena_busqueda.lower() + '%',))
            
            contactos_db = self.cursor.fetchall()
            return [Contacto(nombre, telefono, email, id_contacto) for id_contacto, nombre, telefono, email in contactos_db]
        except sqlite3.Error as e:
            print(f"Error al buscar contactos por cadena: {e}")
            return []