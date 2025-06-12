# Archivo: interfaz.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from logica.clases import Contacto, Agenda

class Interfaz:
    def __init__(self, root):
        self.agenda = Agenda()
        self.root = root
        self.root.title("Agenda de Contactos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Fondo
        imagen_fondo = Image.open("resourses/fondo-de-pantalla-el-mundo-fondo-negro.jpg")
        fondo_tk = ImageTk.PhotoImage(imagen_fondo)
        fondo_label = tk.Label(self.root, image=fondo_tk)
        fondo_label.image = fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame contenedor
        frame = tk.Frame(self.root, bg="white", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Widgets
        self.nombre_label = tk.Label(frame, text="Nombre", bg="white", font=("Arial", 12))
        self.nombre_label.grid(row=0, column=0, padx=10, pady=5)
        self.nombre_entry = tk.Entry(frame, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        self.telefono_label = tk.Label(frame, text="Teléfono", bg="white", font=("Arial", 12))
        self.telefono_label.grid(row=1, column=0, padx=10, pady=5)
        self.telefono_entry = tk.Entry(frame, width=30)
        self.telefono_entry.grid(row=1, column=1, padx=10, pady=5)

        self.email_label = tk.Label(frame, text="Email", bg="white", font=("Arial", 12))
        self.email_label.grid(row=2, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones
        self.agregar_btn = tk.Button(frame, text="Agregar", command=self.agregar_contacto, width=20, bg="#4CAF50", fg="white")
        self.agregar_btn.grid(row=3, column=0, pady=10)

        self.buscar_btn = tk.Button(frame, text="Buscar", command=self.buscar_contacto, width=20, bg="#2196F3", fg="white")
        self.buscar_btn.grid(row=3, column=1, pady=10)

        self.actualizar_btn = tk.Button(frame, text="Actualizar", command=self.actualizar_contacto, width=20, bg="#FFC107", fg="black")
        self.actualizar_btn.grid(row=4, column=0, pady=10)

        self.eliminar_btn = tk.Button(frame, text="Eliminar", command=self.eliminar_contacto, width=20, bg="#F44336", fg="white")
        self.eliminar_btn.grid(row=4, column=1, pady=10)

        self.mostrar_btn = tk.Button(frame, text="Mostrar Todos", command=self.mostrar_todos, width=42, bg="#9C27B0", fg="white")
        self.mostrar_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def agregar_contacto(self):
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        email = self.email_entry.get()
        if nombre and telefono and email:
            contacto = Contacto(nombre, telefono, email)
            self.agenda.agregar_contacto(contacto)
            messagebox.showinfo("Éxito", "Contacto agregado")
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos")

    def buscar_contacto(self):
        nombre = self.nombre_entry.get()
        contacto = self.agenda.buscar_contacto(nombre)
        if contacto:
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, contacto.get_telefono())
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contacto.get_email())
        else:
            messagebox.showinfo("Buscar", "Contacto no encontrado.")

    def actualizar_contacto(self):
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        email = self.email_entry.get()
        self.agenda.actualizar_contacto(nombre, telefono, email)
        messagebox.showinfo("Actualizado", "Contacto actualizado correctamente")

    def eliminar_contacto(self):
        nombre = self.nombre_entry.get()
        self.agenda.eliminar_contacto(nombre)
        messagebox.showinfo("Eliminado", "Contacto eliminado")

    def mostrar_todos(self):
        self.agenda.mostrar_todos()

# Este archivo no se ejecuta directamente, se importa desde main.py
