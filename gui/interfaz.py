import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from logica.clases import Contacto, Agenda

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

        logo = tk.Label(header, text="[Logo]", font=("Arial", 20), bg="white")
        logo.pack(side=tk.LEFT, padx=10)

        titulo = tk.Label(header, text="Dark Side Of Devs", font=("Arial", 16, "bold"), bg="white")
        titulo.pack(side=tk.LEFT)

        self.contactos_btn = tk.Button(header, text="Contactos", bg="#3b82f6", fg="white", command=self.mostrar_contactos)
        self.contactos_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        self.agregar_btn = tk.Button(header, text="Agregar", bg="white", command=self.ventana_agregar)
        self.agregar_btn.pack(side=tk.RIGHT, padx=10)

        self.buscar_btn = tk.Button(header, text="Buscar", bg="white", command=self.ventana_buscar)
        self.buscar_btn.pack(side=tk.RIGHT, padx=10)

        self.acerca_btn = tk.Button(header, text="Acerca de", bg="white", command=self.ventana_acerca)
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

            inicial = fila[1][0].upper()
            icono = tk.Label(card, text=inicial, bg="#8e44ad", fg="white", width=2, font=("Arial", 14, "bold"))
            icono.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            nombre = tk.Label(card, text=fila[1], bg="white", font=("Arial", 12, "bold"))
            nombre.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

            telefono = tk.Label(card, text=f"Teléfono: {fila[2]}", bg="white", font=("Arial", 10))
            telefono.grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

            email = tk.Label(card, text=f"Email: {fila[3]}", bg="white", font=("Arial", 10))
            email.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

            editar_btn = tk.Button(card, text="Editar", bg="white", command=lambda n=fila[1]: self.ventana_editar(n))
            editar_btn.grid(row=0, column=1, sticky="e", padx=5)

            eliminar_btn = tk.Button(card, text="Eliminar", bg="white", command=lambda n=fila[1]: self.eliminar_contacto(n))
            eliminar_btn.grid(row=0, column=2, sticky="e", padx=5)

    def ventana_buscar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar Contacto")
        ventana.geometry("400x300")
        ventana.configure(bg="white")

        tk.Label(ventana, text="Nombre del contacto:", bg="white", font=("Arial", 12)).pack(pady=10)
        nombre_entry = tk.Entry(ventana, font=("Arial", 12))
        nombre_entry.pack(pady=5)

        resultado_box = tk.Text(ventana, height=10, width=45, font=("Arial", 10))
        resultado_box.pack(pady=10)

        def buscar():
            resultado_box.delete("1.0", tk.END)
            nombre = nombre_entry.get().strip()
            if not nombre:
                messagebox.showwarning("Campo vacío", "Por favor, ingresa un nombre para buscar.")
                return
            try:
                consulta = "SELECT * FROM contactos WHERE LOWER(name) LIKE %s"
                self.agenda.cursor.execute(consulta, (f"%{nombre.lower()}%",))
                resultados = self.agenda.cursor.fetchall()
                if resultados:
                    for fila in resultados:
                        resultado_box.insert(tk.END, f"Nombre: {fila[1]}\nTeléfono: {fila[2]}\nEmail: {fila[3]}\n\n")
                else:
                    resultado_box.insert(tk.END, "No se encontraron contactos.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al buscar: {e}")

        tk.Button(ventana, text="Buscar", command=buscar, bg="#3b82f6", fg="white", font=("Arial", 11)).pack(pady=10)

    def ventana_agregar(self):
        self.ventana_formulario("Agregar Contacto", self.agregar_contacto)

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
            if contacto:
                self.agenda.actualizar_contacto(contacto.get_nombre(), telefono_entry.get(), email_entry.get())
                messagebox.showinfo("Actualizado", "Contacto actualizado correctamente")
                ventana.destroy()
            else:
                nuevo = Contacto(nombre_entry.get(), telefono_entry.get(), email_entry.get())
                exito = self.agregar_contacto(nuevo)
                if exito:
                    messagebox.showinfo("Agregado", "Contacto agregado correctamente")
                else:
                    messagebox.showwarning("Error", "No se pudo agregar el contacto")
                ventana.destroy()
            self.mostrar_contactos()

        tk.Button(ventana, text="Guardar", bg="#3b82f6", fg="white", command=ejecutar).pack(pady=20)

    def agregar_contacto(self, contacto):
        try:
            exito = self.agenda.agregar_contacto(contacto)
            return exito
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el contacto: {e}")
            return False

    def buscar_contacto(self):
        pass

    def actualizar_contacto(self, nombre):
        pass

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