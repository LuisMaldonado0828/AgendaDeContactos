# main.py

import tkinter as tk
from gui.interfaz import Interfaz    # Importa la clase Interfaz desde tu carpeta gui
from logica.clases import Agenda     # Importa la clase Agenda desde tu carpeta logica

# --- PUNTO DE ENTRADA PRINCIPAL DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk() # Crea la ventana principal de Tkinter

    # 1. Crea una instancia de la Agenda. Esta Agenda es la que interactúa con tu base de datos.
    agenda = Agenda() 

    # 2. Crea una instancia de la Interfaz. Es fundamental pasarle 'root' (la ventana)
    #    Y la instancia de 'agenda' para que la interfaz pueda usar los métodos de la agenda (agregar, obtener, etc.)
    app = Interfaz(root, agenda) 
    
    # 3. Inicia el bucle principal de eventos de Tkinter. Esto mantiene la ventana abierta y responsiva.
    root.mainloop()