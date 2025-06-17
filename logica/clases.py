import sqlite3
import uuid
from logica.conexion import conectar

class Contacto:
    """Representa un contacto con sus datos y un ID de base de datos."""
    def __init__(self, nombre, telefono, email, foto_path=None, id_contacto=None):
        self.id_contacto = id_contacto if id_contacto is not None else str(uuid.uuid4())
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.foto_path = foto_path # Nuevo atributo para la ruta de la foto

    def get_nombre(self):
        return self.nombre

    def get_telefono(self):
        return self.telefono

    def get_email(self):
        return self.email

    def get_foto_path(self):
        return self.foto_path
    
    def __str__(self):
        return f"ID: {self.id_contacto}, Nombre: {self.nombre}, Teléfono: {self.telefono}, Email: {self.email}, Foto: {self.foto_path if self.foto_path else 'N/A'}"

    def __repr__(self):
        return f"Contacto(id_contacto='{self.id_contacto}', nombre='{self.nombre}', telefono='{self.telefono}', email='{self.email}', foto_path='{self.foto_path}')"


class Agenda:
    """Gestiona las operaciones CRUD (Crear, Leer, Actualizar, Borrar) de contactos en la base de datos."""
    def __init__(self):
        self.db = None
        self.cursor = None
        self._conectar_db()
        self._crear_tabla()

    def _conectar_db(self):
        """Intenta establecer la conexión a la base de datos."""
        self.db = conectar()
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
        Ahora incluye la columna 'foto_path'.
        """
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para crear la tabla.")
            return

        try:
            # Añadir la columna foto_path si no existe, o crear la tabla con ella
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS contactos (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    telefono TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    foto_path TEXT -- Nueva columna para la ruta de la foto
                )
            ''')
            self.db.commit()

            # Alterar la tabla si ya existía y no tenía la columna foto_path
            try:
                self.cursor.execute("SELECT foto_path FROM contactos LIMIT 1")
            except sqlite3.OperationalError:
                self.cursor.execute("ALTER TABLE contactos ADD COLUMN foto_path TEXT")
                self.db.commit()
                print("Columna 'foto_path' añadida a la tabla 'contactos'.")

        except sqlite3.Error as e:
            print(f"Error al crear o alterar tabla: {e}")

    def agregar_contacto(self, contacto):
        """Agrega un nuevo contacto a la base de datos, incluyendo la ruta de la foto."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para agregar.")
            return False

        try:
            self.cursor.execute("INSERT INTO contactos (id, name, telefono, email, foto_path) VALUES (?, ?, ?, ?, ?)",
                                (contacto.id_contacto, contacto.get_nombre(), contacto.get_telefono(), contacto.get_email(), contacto.get_foto_path()))
            self.db.commit()
            return True
        except sqlite3.IntegrityError as e:
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
            self.cursor.execute("SELECT id, name, telefono, email, foto_path FROM contactos ORDER BY name COLLATE NOCASE")
            resultados = self.cursor.fetchall()
            # Ahora pasamos el quinto elemento (foto_path) al constructor de Contacto
            return [Contacto(fila[1], fila[2], fila[3], fila[4], fila[0]) for fila in resultados]
        except sqlite3.Error as e:
            print(f"Error al obtener contactos: {e}")
            return []

    def eliminar_contacto(self, id_contacto):
        """Elimina un contacto de la base de datos por su ID."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para eliminar.")
            return False
            
        try:
            self.cursor.execute("DELETE FROM contactos WHERE id = ?", (id_contacto,))
            self.db.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar contacto: {e}")
            return False

    def editar_contacto(self, id_contacto, nuevo_nombre, nuevo_telefono, nuevo_email, nueva_foto_path=None):
        """Actualiza los datos de un contacto, incluyendo la ruta de la foto."""
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para editar.")
            return False

        try:
            self.cursor.execute(
                "UPDATE contactos SET name = ?, telefono = ?, email = ?, foto_path = ? WHERE id = ?",
                (nuevo_nombre, nuevo_telefono, nuevo_email, nueva_foto_path, id_contacto)
            )
            self.db.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al editar contacto (posible duplicado de teléfono/email): {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error al editar contacto: {e}")
            return False

    def buscar_contacto(self, nombre=None, telefono=None, email=None, contacto_a_excluir=None):
        """
        Busca un contacto en la base de datos por nombre, teléfono o email.
        Ahora también retorna la ruta de la foto.
        """
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para buscar.")
            return None

        query = "SELECT id, name, telefono, email, foto_path FROM contactos WHERE 1=1"
        params = []

        if nombre:
            query += " AND LOWER(name) = LOWER(?)"
            params.append(nombre)
        if telefono:
            query += " AND LOWER(telefono) = LOWER(?)"
            params.append(telefono)
        if email:
            query += " AND LOWER(email) = LOWER(?)"
            params.append(email)
        
        if contacto_a_excluir and contacto_a_excluir.id_contacto:
            query += " AND id != ?"
            params.append(contacto_a_excluir.id_contacto)

        try:
            self.cursor.execute(query, tuple(params))
            fila = self.cursor.fetchone()
            if fila:
                # Retornar un objeto Contacto incluyendo la ruta de la foto
                return Contacto(fila[1], fila[2], fila[3], fila[4], fila[0])
            return None
        except sqlite3.Error as e:
            print(f"Error al buscar contacto: {e}")
            return None

    def buscar_contactos_por_cadena(self, cadena_busqueda):
        """
        Busca contactos cuyos nombres contengan la cadena de búsqueda.
        Ahora también retorna la ruta de la foto.
        """
        if not self._asegurar_conexion():
            print("No hay conexión a la base de datos para buscar contactos por cadena.")
            return []

        try:
            self.cursor.execute("SELECT id, name, telefono, email, foto_path FROM contactos WHERE LOWER(name) LIKE ? ORDER BY name COLLATE NOCASE ASC",
                                ('%' + cadena_busqueda.lower() + '%',))
            
            contactos_db = self.cursor.fetchall()
            # Retornar lista de Contacto incluyendo la ruta de la foto
            return [Contacto(nombre, telefono, email, foto_path, id_contacto) for id_contacto, nombre, telefono, email, foto_path in contactos_db]
        except sqlite3.Error as e:
            print(f"Error al buscar contactos por cadena: {e}")
            return []