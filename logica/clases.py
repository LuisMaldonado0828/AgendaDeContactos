''' Se crea la clase Contacto'''

class Contacto:

    '''Creo el constructor con atributos:  nombre , telefono y email.'''

    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    '''Se crea el  método Getter: Este sirve para acceder a los valores de los atributos.'''

    def get_nombre(self):
            return self.nombre
    def get_telefono (self):
            return self.telefono
    def get_email (self):
            return self.email
    
    '''Se crea el método Setter : Este modifica los valores de los atributos, utlizando  parametros como "nuevo_nombre", "nuevo_telefono" y "nuevo_email" permitiendo
    que pueda reemplazar el contenido original por estos nuevos valores que se pasaran como argumentos. '''

    def set_nombre(self, nuevo_nombre):  
            self.nombre = nuevo_nombre    
    def set_telefono (self, nuevo_telefono):
            self.telefono = nuevo_telefono   
    def set_email (self, nuevo_email):
            self.email = nuevo_email
