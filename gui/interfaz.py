import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from logica.clases import Contacto, Agenda
import re

class Interfaz:
    def __init__(self, root):
        self.agenda = Agenda()
        self.root = root
        self.root.title("Contactos Dark side of devs")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f6fa")

        self.crear_encabezado()
        self.crear_area_contactos()

    def crear_encabezado(self):
        header = tk.Frame(self.root, bg="white", height=60)
        header.pack(fill=tk.X)

        logo = tk.Label(header, text="📇", font=("Arial", 20), bg="white")
        logo.pack(side=tk.LEFT, padx=10)

        titulo = tk.Label(header, text="Dark Side Of Devs ", font=("Arial", 16, "bold"), bg="white")
        titulo.pack(side=tk.LEFT)

        self.contactos_btn = tk.Button(header, text="👥 Contactos", bg="#3b82f6", fg="white", command=self.mostrar_contactos)
        self.contactos_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        self.agregar_btn = tk.Button(header, text="＋ Agregar", bg="white", command=self.ventana_agregar)
        self.agregar_btn.pack(side=tk.RIGHT, padx=10)

        self.buscar_btn = tk.Button(header, text="🔍 Buscar", bg="white", command=self.ventana_buscar)
        self.buscar_btn.pack(side=tk.RIGHT, padx=10)

        self.acerca_btn = tk.Button(header, text="ℹ️ Acerca de", bg="white", command=self.ventana_acerca)
        self.acerca_btn.pack(side=tk.RIGHT, padx=10)

    def crear_area_contactos(self):
        self.area_contactos = tk.Frame(self.root, bg="#f5f6fa")
        self.area_contactos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.mostrar_contactos()

    def mostrar_contactos(self):
        for widget in self.area_contactos.winfo_children():
            widget.destroy()

        self.area_contactos.grid_columnconfigure((0, 1, 2), weight=1)
        contactos = self.agenda.cursor
        contactos.execute("SELECT * FROM contactos")
        resultados = contactos.fetchall()

        if not resultados:
            tk.Label(self.area_contactos, text="No hay contactos registrados.", bg="#f5f6fa", font=("Arial", 14)).pack()
            return

        for idx, fila in enumerate(resultados):
            card = tk.Frame(self.area_contactos, bg="white", bd=1, relief="raised")
            card.grid(row=idx//3, column=idx%3, padx=10, pady=10, sticky="nsew")

            nombre_contacto = fila[1] if fila[1] else "?"
            inicial = nombre_contacto[0].upper()
            icono = tk.Label(card, text=inicial, bg="#8e44ad", fg="white", width=2, font=("Arial", 14, "bold"))
            icono.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            nombre = tk.Label(card, text=nombre_contacto, bg="white", font=("Arial", 12, "bold"))
            nombre.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

            telefono = tk.Label(card, text=f"📞 {fila[2]}", bg="white", font=("Arial", 10))
            telefono.grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

            email = tk.Label(card, text=f"✉️ {fila[3]}", bg="white", font=("Arial", 10))
            email.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

            editar_btn = tk.Button(card, text="✏️", bg="white", command=lambda n=fila[1]: self.ventana_editar(n))
            editar_btn.grid(row=0, column=1, sticky="e", padx=5)

            eliminar_btn = tk.Button(card, text="🗑️", bg="white", command=lambda n=fila[1]: self.eliminar_contacto(n))
            eliminar_btn.grid(row=0, column=2, sticky="e", padx=5)

    def ventana_agregar(self):
        self.ventana_formulario("Agregar Contacto", self.agregar_contacto)

    def ventana_buscar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar Contacto")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Nombre del contacto").pack(pady=5)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.pack(pady=5)

        def buscar():
            nombre = nombre_entry.get()
            contacto = self.agenda.buscar_contacto(nombre)
            if contacto:
                messagebox.showinfo("Resultado", f"📇 Nombre: {contacto.get_nombre()}\n📞 Teléfono: {contacto.get_telefono()}\n✉️ Email: {contacto.get_email()}")
            else:
                messagebox.showinfo("Resultado", "Contacto no encontrado")

        tk.Button(ventana, text="Buscar", bg="#3b82f6", fg="white", command=buscar).pack(pady=10)

    def ventana_acerca(self):
        messagebox.showinfo("Acerca de", "ContactHub Pro\nDesarrollado con Tkinter + MySQL")

    def ventana_editar(self, nombre):
        contacto = self.agenda.buscar_contacto(nombre)
        if contacto:
            self.ventana_formulario("Actualizar Contacto", lambda: self.actualizar_contacto(contacto.get_nombre()), contacto)

    def ventana_formulario(self, titulo, comando, contacto=None):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("400x300")

        tk.Label(ventana, text="Nombre").pack(pady=5)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.pack(pady=5)
        if contacto:
            nombre_entry.insert(0, contacto.get_nombre())
            nombre_entry.config(state="disabled")

        tk.Label(ventana, text="Teléfono").pack(pady=5)
        telefono_entry = tk.Entry(ventana)
        telefono_entry.pack(pady=5)
        if contacto:
            telefono_entry.insert(0, contacto.get_telefono())

        tk.Label(ventana, text="Email").pack(pady=5)
        email_entry = tk.Entry(ventana)
        email_entry.pack(pady=5)
        if contacto:
            email_entry.insert(0, contacto.get_email())

        def ejecutar():
            nombre_val = nombre_entry.get().strip()
            telefono_val = telefono_entry.get().strip()
            email_val = email_entry.get().strip()

            if not nombre_val or not telefono_val or not email_val:
                messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
                return

            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email_val):
                messagebox.showwarning("Email inválido", "Por favor ingresa un correo electrónico válido.")
                return

            if not re.match(r"^\d{7,15}$", telefono_val):
                messagebox.showwarning("Teléfono inválido", "Ingresa un número de teléfono válido (7 a 15 dígitos).")
                return

            if contacto:
                self.agenda.actualizar_contacto(contacto.get_nombre(), telefono_val, email_val)
                messagebox.showinfo("Actualizado", "Contacto actualizado correctamente")
                ventana.destroy()
            else:
                nuevo = Contacto(nombre_val, telefono_val, email_val)
                exito = self.agenda.agregar_contacto(nuevo)
                if exito:
                    messagebox.showinfo("Agregado", "Contacto agregado correctamente")
                else:
                    messagebox.showwarning("Error", "No se pudo agregar el contacto")
                ventana.destroy()
            self.mostrar_contactos()

        tk.Button(ventana, text="Guardar", bg="#3b82f6", fg="white", command=ejecutar).pack(pady=20)

    def agregar_contacto(self):
        messagebox.showinfo("Info", "Funcionalidad de agregar contacto aún no implementada.")

    def buscar_contacto(self):
        messagebox.showinfo("Info", "Funcionalidad de buscar contacto aún no implementada.")

    def actualizar_contacto(self, nombre):
        messagebox.showinfo("Info", "Funcionalidad de actualizar contacto aún no implementada.")

    def eliminar_contacto(self, nombre):
        confirmacion = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este contacto?")
        if confirmacion:
            self.agenda.eliminar_contacto(nombre)
            self.mostrar_contactos()
            messagebox.showinfo("Eliminado", "Contacto eliminado correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
