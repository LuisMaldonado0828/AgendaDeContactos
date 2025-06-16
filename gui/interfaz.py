# gui/interfaz.py

import tkinter as tk
from tkinter import ttk, messagebox, font
from logica.clases import Contacto, Agenda

class Interfaz:
    """Define la estructura y el comportamiento de la interfaz gráfica de usuario."""
    def __init__(self, root, agenda):
        self.root = root
        self.agenda = agenda
        self.formulario_actual_frame = None
        self.error_label_form = None
        self.message_label = None
        self.hide_message_timer = None
        self.current_confirmation_dialog = None

        self.root.title("Agenda de Contactos - Dark Side Of Devs")
        self.root.geometry("1000x600")
        self.root.config(bg="#18152b")
        self.root.minsize(800, 500)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.bg_main = "#18152b"
        self.bg_sidebar = "#0f0d1a"
        self.bg_card = "#1e1a30"
        self.bg_form = "#2a2735"
        self.text_light = "#E0E0E0"
        self.accent_blue = "#4c2ce9"
        self.accent_red = "#e63946"
        self.border_color = "#3A3A3A"
        self.success_green = "#28a745"

        self.font_main = font.Font(family="Roboto", size=11)
        self.font_heading = font.Font(family="Roboto Medium", size=16, weight="bold")
        self.font_button = font.Font(family="Roboto", size=10, weight="bold")
        self.font_error = font.Font(family="Roboto", size=9, weight="bold")
        self.font_logo = font.Font(family="Poppins", size=12, weight="bold")
        self.font_about_title = font.Font(family="Poppins", size=18, weight="bold")
        self.font_about_text = font.Font(family="Roboto", size=10)

        self.style.configure('.', font=self.font_main, background=self.bg_main, foreground=self.text_light)
        self.style.configure('TFrame', background=self.bg_main)
        self.style.configure('Sidebar.TFrame', background=self.bg_sidebar)
        self.style.configure('TLabel', background=self.bg_main, foreground=self.text_light, font=self.font_main)
        
        self.style.configure('TEntry',
                                fieldbackground="#3A3A3A", foreground=self.text_light,
                                insertbackground=self.text_light, borderwidth=1, relief="flat", padding=5)
        self.style.map('TEntry', bordercolor=[('focus', self.accent_blue)])

        self.style.configure('TButton',
                                background=self.accent_blue, foreground='white',
                                font=self.font_button, relief="flat", borderwidth=0, padding=[10, 5])
        self.style.map('TButton', background=[('active', self.accent_blue)], foreground=[('active', 'white')])

        self.style.configure('Danger.TButton',
                                background=self.accent_red, foreground='white',
                                font=self.font_button, relief="flat", borderwidth=0, padding=[10, 5])
        self.style.map('Danger.TButton', background=[('active', '#C02E39')])

        self.style.configure('Sidebar.TButton',
                                background=self.bg_sidebar, foreground=self.text_light,
                                font=self.font_button, relief="flat", borderwidth=0, padding=[20, 10])
        self.style.map('Sidebar.TButton', background=[('active', self.accent_blue), ('pressed', self.accent_blue)],
                        foreground=[('active', 'white'), ('pressed', 'white')])

        self.style.configure('Form.TFrame', background=self.bg_form, borderwidth=1, relief="solid", bordercolor=self.border_color)
        self.style.configure('Form.TLabel', background=self.bg_form, foreground=self.text_light, font=self.font_main)
        self.style.configure('FormTitle.TLabel', background=self.bg_form, foreground=self.text_light, font=self.font_heading)

        self.style.configure('Close.TButton',
                                background=self.accent_red, foreground='white',
                                font=("Arial", 9, "bold"), relief="flat", borderwidth=0, width=3, padding=[0, 0])
        self.style.map('Close.TButton', background=[('active', '#CC0000')])

        self.style.configure('ContactCard.TFrame',
                                background=self.bg_card,
                                borderwidth=1,
                                relief="solid",
                                bordercolor=self.border_color)
        self.style.configure('ContactCard.TLabel', background=self.bg_card, foreground=self.text_light)
        self.style.configure('ContactCardButtons.TFrame', background=self.bg_card)

        self.sidebar = ttk.Frame(root, width=150, style='Sidebar.TFrame')
        self.sidebar.pack(side="left", fill="y")

        self.logo = ttk.Label(self.sidebar, text="🧠\nDARK SIDE\nOF DEVS",
                                background=self.bg_sidebar, foreground='white', font=self.font_logo)
        self.logo.pack(pady=20)

        self.btn_contactos = ttk.Button(self.sidebar, text="📂 Contactos", style='Sidebar.TButton', command=self.mostrar_contactos)
        self.btn_contactos.pack(pady=5, ipadx=10, ipady=5, fill='x')

        self.btn_agregar = ttk.Button(self.sidebar, text="➕ Agregar", style='Sidebar.TButton', command=self.mostrar_formulario_agregar)
        self.btn_agregar.pack(pady=5, ipadx=10, ipady=5, fill='x')

        self.btn_about = ttk.Button(self.sidebar, text="ℹ️ Acerca de", style='Sidebar.TButton', command=self.mostrar_acerca_de)
        self.btn_about.pack(pady=5, ipadx=10, ipady=5, fill='x')

        self.main_area = ttk.Frame(root, style='TFrame')
        self.main_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.message_label = ttk.Label(self.main_area, text="", font=self.font_error, background=self.bg_main)
        self.message_label.pack(pady=5)

        self.contact_list_frame = None 
        self.mostrar_contactos()

    def _show_internal_message(self, message, is_error=False):
        """Muestra un mensaje temporal de éxito o error en la interfaz principal."""
        if self.hide_message_timer:
            self.root.after_cancel(self.hide_message_timer)
        self.message_label.config(text=message, foreground=self.accent_red if is_error else self.success_green)
        self.message_label.pack(pady=5)
        self.hide_message_timer = self.root.after(3000, self._hide_internal_message)

    def _hide_internal_message(self):
        """Oculta la etiqueta de mensaje temporal."""
        if self.message_label.winfo_exists():
            self.message_label.config(text="")
            self.message_label.pack_forget()

    def limpiar_main_area(self):
        """Elimina todos los widgets del área principal, excepto la etiqueta de mensaje."""
        for widget in self.main_area.winfo_children():
            if widget != self.message_label:
                widget.destroy()
        self._hide_internal_message()

    def limpiar_campos_formulario(self):
        """Limpia el contenido de los campos de entrada y el mensaje de error del formulario."""
        if hasattr(self, 'entry_nombre') and self.entry_nombre.winfo_exists():
            self.entry_nombre.delete(0, tk.END)
        if hasattr(self, 'entry_telefono') and self.entry_telefono.winfo_exists():
            self.entry_telefono.delete(0, tk.END)
        if hasattr(self, 'entry_email') and self.entry_email.winfo_exists():
            self.entry_email.delete(0, tk.END)
        if self.error_label_form and self.error_label_form.winfo_exists():
            self.error_label_form.config(text="")

    def mostrar_contactos(self):
        """Muestra la lista de contactos como tarjetas en un área desplazable."""
        self.limpiar_main_area()
        if self.formulario_actual_frame:
            self.formulario_actual_frame.destroy()
            self.formulario_actual_frame = None
        if self.current_confirmation_dialog:
            self.current_confirmation_dialog.destroy()
            self.current_confirmation_dialog = None

        self.contact_list_frame = ttk.Frame(self.main_area, style='TFrame')
        self.contact_list_frame.pack(fill="both", expand=True)

        contactos = self.agenda.obtener_contactos()
        if not contactos:
            ttk.Label(self.contact_list_frame, text="No hay contactos guardados. ¡Agrega uno!",
                      font=self.font_main, foreground=self.text_light, background=self.bg_main).pack(pady=40)
            return

        canvas = tk.Canvas(self.contact_list_frame, bg=self.bg_main, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.contact_list_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas, style='TFrame') 
        self.canvas_window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- AÑADIDOS PARA SCROLL CON RUEDA/TOUCHPAD ---
        # 1. Configurar el canvas para que el scrollregion se actualice cuando cambie el tamaño del frame interno
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # 2. Vincular el evento de la rueda del ratón al canvas (Windows/macOS)
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        
        # 3. Vincular los eventos de la rueda del ratón (Linux)
        canvas.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
        # --- FIN DE LOS AÑADIDOS ---

        self.root.update_idletasks() # Actualiza para calcular tamaños correctamente
        
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)

        for index, contacto in enumerate(contactos):
            frame_card = ttk.Frame(scrollable_frame, style='ContactCard.TFrame', padding=15, relief="solid", borderwidth=1)
            frame_card.grid(row=index // 2, column=index % 2, padx=15, pady=15, sticky="nsew")
            
            ttk.Label(frame_card, text=contacto.nombre, foreground=self.text_light, background=self.bg_card, font=self.font_heading).pack(anchor="w", pady=(0,5))
            ttk.Label(frame_card, text=f"📞 {contacto.telefono}", foreground=self.text_light, background=self.bg_card, font=self.font_main).pack(anchor="w")
            ttk.Label(frame_card, text=f"📧 {contacto.email}", foreground=self.text_light, background=self.bg_card, font=self.font_main).pack(anchor="w")

            btn_frame_card = ttk.Frame(frame_card, style='ContactCardButtons.TFrame')
            btn_frame_card.pack(anchor="w", pady=(10, 0))

            ttk.Button(btn_frame_card, text="✏️ Editar", style='TButton', command=lambda c=contacto: self.mostrar_formulario_editar(c)).pack(side="left", padx=5)
            ttk.Button(btn_frame_card, text="🗑️ Eliminar", style='Danger.TButton', command=lambda c=contacto: self._show_delete_confirmation(c)).pack(side="left")

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def crear_formulario(self, title, save_command, initial_contact=None):
        """Crea y muestra un formulario genérico para agregar o editar contactos."""
        self.limpiar_main_area()
        if self.formulario_actual_frame:
            self.formulario_actual_frame.destroy()

        self.formulario_actual_frame = ttk.Frame(self.main_area, style='Form.TFrame', padding=30)
        self.formulario_actual_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_cerrar = ttk.Button(self.formulario_actual_frame, text="❌",
                                command=self.cerrar_formulario_actual,
                                style='Close.TButton')
        btn_cerrar.place(relx=1.0, rely=0.0, anchor='ne', x=5, y=-5)

        ttk.Label(self.formulario_actual_frame, text=title, font=self.font_heading,
                  background=self.bg_form, foreground=self.text_light).grid(row=0, column=0, columnspan=2, pady=15)

        self.error_label_form = ttk.Label(self.formulario_actual_frame, text="",
                                          foreground=self.accent_red, font=self.font_error, background=self.bg_form)
        self.error_label_form.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(self.formulario_actual_frame, text="Nombre:", style='Form.TLabel').grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.entry_nombre = ttk.Entry(self.formulario_actual_frame, width=35)
        self.entry_nombre.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(self.formulario_actual_frame, text="Teléfono:", style='Form.TLabel').grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.entry_telefono = ttk.Entry(self.formulario_actual_frame, width=35)
        self.entry_telefono.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(self.formulario_actual_frame, text="Email:", style='Form.TLabel').grid(row=4, column=0, sticky="e", pady=5, padx=5)
        self.entry_email = ttk.Entry(self.formulario_actual_frame, width=35)
        self.entry_email.grid(row=4, column=1, pady=5, padx=5)

        if initial_contact:
            self.entry_nombre.insert(0, initial_contact.nombre)
            self.entry_telefono.insert(0, initial_contact.telefono)
            self.entry_email.insert(0, initial_contact.email)

        ttk.Button(self.formulario_actual_frame, text="💾 Guardar", style='TButton', command=save_command).grid(row=5, column=0, columnspan=2, pady=20)


    def mostrar_formulario_agregar(self):
        """Muestra el formulario para agregar un nuevo contacto."""
        self.crear_formulario("➕ Agregar Contacto", self.guardar_nuevo_contacto)

    def mostrar_formulario_editar(self, contacto):
        """Muestra el formulario para editar un contacto existente."""
        self.crear_formulario("✏️ Editar Contacto", lambda: self.guardar_edicion(contacto), initial_contact=contacto)

    def cerrar_formulario_actual(self):
        """Cierra el formulario actualmente visible y vuelve a la lista de contactos."""
        if self.formulario_actual_frame:
            self.formulario_actual_frame.place_forget()
            self.formulario_actual_frame.destroy()
            self.formulario_actual_frame = None
            self.limpiar_campos_formulario()
            self.mostrar_contactos()

    def validar_datos_contacto(self, nombre, telefono, email, contacto_a_excluir=None):
        """Valida los datos de entrada del formulario antes de guardar o editar."""
        self.error_label_form.config(text="")

        if not nombre.strip():
            self.error_label_form.config(text="⚠️ Error: El nombre no puede estar vacío.")
            return False
        if not all(char.isalpha() or char.isspace() for char in nombre.strip()):
            self.error_label_form.config(text="⚠️ Error: El nombre solo debe contener letras y espacios.")
            return False

        if not telefono.strip():
            self.error_label_form.config(text="⚠️ Error: El teléfono no puede estar vacío.")
            return False
        if not telefono.strip().isdigit():
            self.error_label_form.config(text="⚠️ Error: El teléfono solo debe contener números.")
            return False

        if not email.strip():
            self.error_label_form.config(text="⚠️ Error: El email no puede estar vacío.")
            return False
        if "@" not in email.strip() or "." not in email.strip().split("@")[-1] or \
           len(email.strip().split("@")[0]) == 0 or len(email.strip().split("@")[1]) < 3:
            self.error_label_form.config(text="⚠️ Error: Formato de email inválido (ej. usuario@dominio.com).")
            return False

        duplicado_por_nombre_tel = self.agenda.buscar_contacto(nombre=nombre.strip(), telefono=telefono.strip(), contacto_a_excluir=contacto_a_excluir)
        if duplicado_por_nombre_tel:
            self.error_label_form.config(text="⚠️ Error: Ya existe un contacto con ese nombre y teléfono.")
            return False
        
        duplicado_por_email = self.agenda.buscar_contacto(email=email.strip(), contacto_a_excluir=contacto_a_excluir)
        if duplicado_por_email:
            self.error_label_form.config(text="⚠️ Error: Ya existe un contacto con ese email.")
            return False

        return True

    def guardar_nuevo_contacto(self):
        """Intenta guardar un nuevo contacto después de la validación de los datos."""
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()

        if not self.validar_datos_contacto(nombre, telefono, email):
            return

        nuevo_contacto = Contacto(nombre, telefono, email)
        if self.agenda.agregar_contacto(nuevo_contacto):
            self._show_internal_message("✅ Contacto agregado correctamente.")
            self.cerrar_formulario_actual()
        else:
            self._show_internal_message("❌ Error: No se pudo agregar el contacto. Puede que ya exista un email igual.", is_error=True)

    def guardar_edicion(self, contacto_original):
        """Intenta guardar los cambios de un contacto editado después de la validación."""
        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_telefono = self.entry_telefono.get().strip()
        nuevo_email = self.entry_email.get().strip()

        if not self.validar_datos_contacto(nuevo_nombre, nuevo_telefono, nuevo_email, contacto_a_excluir=contacto_original):
            return
        
        if self.agenda.editar_contacto(contacto_original.id_contacto, nuevo_nombre, nuevo_telefono, nuevo_email):
            self._show_internal_message("✅ Contacto editado correctamente.")
            self.cerrar_formulario_actual()
        else:
            self._show_internal_message("❌ Error: No se pudo editar el contacto. Verifique datos.", is_error=True)

    def _show_delete_confirmation(self, contacto_a_eliminar):
        """Muestra un diálogo de confirmación interno para eliminar un contacto."""
        if self.formulario_actual_frame:
            self.formulario_actual_frame.place_forget()
        if self.contact_list_frame:
            self.contact_list_frame.pack_forget()

        self.current_confirmation_dialog = ttk.Frame(self.main_area, style='Form.TFrame', padding=30)
        self.current_confirmation_dialog.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.current_confirmation_dialog, text=f"¿Estás seguro de eliminar a {contacto_a_eliminar.nombre}?",
                  font=self.font_heading, foreground=self.text_light, background=self.bg_form).pack(pady=20)
        
        btn_frame = ttk.Frame(self.current_confirmation_dialog, style='Form.TFrame')
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✅ Sí, Eliminar", style='Danger.TButton', 
                   command=lambda: self._perform_deletion(contacto_a_eliminar)).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ No, Cancelar", style='TButton', 
                   command=self._cancel_deletion).pack(side="left", padx=10)

    def _perform_deletion(self, contacto_a_eliminar):
        """Ejecuta la eliminación del contacto y muestra un mensaje."""
        if self.agenda.eliminar_contacto(contacto_a_eliminar.id_contacto):
            self._show_internal_message("✅ Contacto eliminado correctamente.")
        else:
            self._show_internal_message("❌ Error: No se pudo eliminar el contacto.", is_error=True)
        self._cancel_deletion()
        self.mostrar_contactos()

    def _cancel_deletion(self):
        """Cancela la eliminación y cierra el diálogo de confirmación."""
        if self.current_confirmation_dialog:
            self.current_confirmation_dialog.destroy()
            self.current_confirmation_dialog = None
        self.mostrar_contactos()

    def mostrar_acerca_de(self):
        """Muestra la información 'Acerca de' en la interfaz principal."""
        self.limpiar_main_area()
        if self.formulario_actual_frame:
            self.formulario_actual_frame.destroy()
            self.formulario_actual_frame = None
        if self.current_confirmation_dialog:
            self.current_confirmation_dialog.destroy()
            self.current_confirmation_dialog = None

        about_frame = ttk.Frame(self.main_area, style='Form.TFrame', padding=30)
        about_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        btn_cerrar_about = ttk.Button(about_frame, text="❌",
                                      command=self.mostrar_contactos,
                                      style='Close.TButton')
        btn_cerrar_about.place(relx=1.0, rely=0.0, anchor='ne', x=5, y=-5)


        ttk.Label(about_frame, text="🚀 Agenda de Contactos",
                  font=self.font_about_title, foreground=self.accent_blue, background=self.bg_form).pack(pady=20)

        ttk.Label(about_frame, text="Proyecto desarrollado por:",
                  font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(pady=(10, 0))

        ttk.Label(about_frame, text="  • Jesus Manuel Torres Bandera (Product Owner)",
                  font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        ttk.Label(about_frame, text="  • Diego Fernando Pinzon Quintero (Scrum Master)",
                  font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        ttk.Label(about_frame, text="  • Luis David Maldonado Suarez (Development Team)",
                  font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        ttk.Label(about_frame, text="  • Oscar Leonardo Macias Puentes (Development Team)",
                  font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        
        ttk.Label(about_frame, text="\nEquipo: DARK SIDE OF DEVS",
                  font=self.font_button, foreground=self.text_light, background=self.bg_form).pack(pady=(15, 0))