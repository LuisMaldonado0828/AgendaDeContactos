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

    

''' Se crea la clase Agenda'''

class Agenda: 
       
       ''' Creo un Constructor '''

       def __init__(self):
              
              ''' Creo una lista vacia para guardar los contactos '''

              self.contactos = []

       def agregar_contacto(self, contacto):
              
              '''Recorre cada uno de los contactos existentes en la agenda para saber si hay uno igual y si lo hay no dejara seguir '''

              for i in self.contactos: 
                     if i.get_gmail() == Contacto.get_email():
                            print("Ya existe un contacto con este correo")
                            return
                     self.contactos.append(Contacto)
                     print("Contacto agregado conrrectamente")

       '''Se crea un metodo para buscar un contacto por el nombre '''
       
       def buscar_contacto(self, nombre):
              for i in self.contactos: 
                      
                      '''Compara el nombre ignorando las mayusculas'''

                      if i.get_nombre().lower() == nombre.lower():
                              
                              ''' Si lo encuetra este lo devielve: '''

                              return i 
                      
              ''' Si no lo encuentra devuelve None'''
              
              return None
       
       ''' Se crea un metodo para actualizar el nombre del contacto: '''
        
       def actualizar_contacto(self, nombre):
              
              ''' Aqui se busca el contacto con ese nombre'''

              Contacto = self.buscar_contacto(nombre)

              ''' Si lo encuentra se pide el nuevo telefono y email por consola'''

              if Contacto:
                     nuevo_telefono = input("Nuevo telefono: ")
                     nuevo_email = input("Nuevo email: ")

                     '''Aqui se guardan los cambios: '''

                     Contacto.set_telefono(nuevo_telefono)
                     Contacto.set_email(nuevo_email)
                     print("Contacto actualizado.")
              else: 
                print("El contacto no se encontro.") 

       '''Se crea un metodo para eliminar un contacto por el nombre'''

       def eliminar_contacto(self, nombre):
             
             '''Recorre la lista de contactos ignorando mayusculas y si lo encuntra se elimina si no se muestra un mensaje de contacto no encontrado'''

             for i in self.contactos:
                   if i.get_nombre().lower() == nombre.lower():
                         self.contactos.remove(i)
                         print("Se elimino correctamente el contacto")
                         return
             print("Contacto no encontrado")

       '''Se crea un metodo para poder ver todos los contactos de la agenda '''
       
       def mostrar_todos(self):
             
             ''' Aqui se revisa si la lista esta vacia y si lo esta mostrara que es la agenda esta vacia '''

             if not self.contactos:
                   print("Agenda vacia")
             else: 
                   for i in self.contactos:
                         print("--------")
                         i.mostrar_contacto()      
