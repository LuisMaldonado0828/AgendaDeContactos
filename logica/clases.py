class Contacto: 
    def __init__(self, nombre, telefono, email):
    
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
# comienzoc metedo getter y este sirve para leer los valores de un atributo 
        def get_nombre(self):
            return self.nombre
        def get_telefono (self):
            return self.telefono
        def get_email (self):
            return self.email
# aqui utilizo el metodo setter: este modifica los valores de un atributo
#utlizo el "nuevo_nombre" como para cuando se quiere colocar un nuevo valor o mejor dicho asignarle otro valor 
#un ejemplo seria que me van a dar un nuevo valor para remplazar el que ya estabaa y esto tambien sucede con "nuevo_telefono" y "nuevo_email"
        def set_nombre(self, nuevo_nombre):  
            self_nombre = nuevo_nombre    
        def set_telefono (self, nuevo_telefono):
            self_telefono = nuevo_telefono   
        def set_email (self, nuevo_email):
            self_email = nuevo_email
