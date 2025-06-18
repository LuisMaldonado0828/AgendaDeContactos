# gui/interfaz.py
# --- CÓDIGO COMPLETO Y CORREGIDO ---

import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import shutil
import sys
import qrcode
import threading # Importar threading
import queue     # Importar queue

from logica.clases import Contacto, Agenda

# Directorio para guardar las fotos de los contactos
PHOTOS_DIR = "fotos_contactos"
QR_DIR = "qrs_temp" 

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
        self.canvas = None 

        self.search_entry = None
        self.search_results_frame = None 
        self._search_timer = None 

        self.selected_photo_path = None
        self.photo_preview_label = None 

        os.makedirs(PHOTOS_DIR, exist_ok=True)
        os.makedirs(QR_DIR, exist_ok=True)

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
        self.placeholder_bg = "#6C757D" 

        self.font_main = font.Font(family="Roboto", size=11)
        self.font_heading = font.Font(family="Roboto Medium", size=16, weight="bold")
        self.font_button = font.Font(family="Roboto", size=10, weight="bold")
        self.font_error = font.Font(family="Roboto", size=9, weight="bold")
        self.font_logo = font.Font(family="Poppins", size=12, weight="bold")
        self.font_about_title = font.Font(family="Poppins", size=18, weight="bold")
        self.font_about_text = font.Font(family="Roboto", size=10)
        self.font_initial = font.Font(family="Roboto Medium", size=40, weight="bold")


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
        self.style.configure('ContactCardButtonsFrame.TFrame', background=self.bg_card)

        self.style.configure('PhotoFrame.TFrame', background=self.bg_card, borderwidth=1, relief="solid", bordercolor=self.border_color)
        self.style.configure('PhotoPlaceholder.TLabel', background=self.placeholder_bg, foreground="white", font=self.font_initial, anchor="center")
        
        self.style.configure('QRFrame.TFrame', background=self.bg_card, borderwidth=1, relief="solid", bordercolor=self.border_color)

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
        
        self.image_queue = queue.Queue()
        self.contact_images = {} 

        self.mostrar_contactos() 

        self.root.after(100, self._process_image_queue)

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
        self.contact_images.clear()

    def limpiar_campos_formulario(self):
        """Limpia el contenido de los campos de entrada, el mensaje de error y la vista previa de la foto del formulario."""
        if hasattr(self, 'entry_nombre') and self.entry_nombre.winfo_exists():
            self.entry_nombre.delete(0, tk.END)
        if hasattr(self, 'entry_telefono') and self.entry_telefono.winfo_exists():
            self.entry_telefono.delete(0, tk.END)
        if hasattr(self, 'entry_email') and self.entry_email.winfo_exists():
            self.entry_email.delete(0, tk.END)
        if self.error_label_form and self.error_label_form.winfo_exists():
            self.error_label_form.config(text="")
        
        self.selected_photo_path = None
        if self.photo_preview_label and self.photo_preview_label.winfo_exists():
            self.photo_preview_label.config(image='')
            self.photo_preview_label.image = None 

    def mostrar_contactos(self):
        """
        Muestra la lista de contactos como tarjetas en un área desplazable, con barra de búsqueda.
        """
        self.limpiar_main_area()
        if self.formulario_actual_frame:
            self.formulario_actual_frame.destroy()
            self.formulario_actual_frame = None
        if self.current_confirmation_dialog:
            self.current_confirmation_dialog.destroy()
            self.current_confirmation_dialog = None
        
        top_bar_frame = ttk.Frame(self.main_area, style='TFrame')
        top_bar_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(top_bar_frame, text="📂 Mis Contactos", font=self.font_heading,
                    foreground=self.text_light, background=self.bg_main).pack(side="left", padx=(0, 20))

        search_frame = ttk.Frame(top_bar_frame, style='TFrame')
        search_frame.pack(side="right", fill="x", expand=True)

        self.search_entry = ttk.Entry(search_frame, width=30, style='TEntry')
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.search_entry.insert(0, "Buscar por nombre...")
        self.search_entry.bind("<FocusIn>", self._clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self._restore_search_placeholder)
        self.search_entry.bind("<KeyRelease>", self._perform_search_delayed)

        ttk.Button(search_frame, text="🔍", style='TButton', command=self._perform_search).pack(side="left")

        self.contact_list_frame = ttk.Frame(self.main_area, style='TFrame')
        self.contact_list_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.contact_list_frame, bg=self.bg_main, highlightthickness=0) 
        scrollbar = ttk.Scrollbar(self.contact_list_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_content_frame = ttk.Frame(self.canvas, style='TFrame')
        
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.scrollable_content_frame, anchor="nw") 
        
        self.scrollable_content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.canvas_window_id, width=e.width))

        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel_event) 
        self.canvas.bind("<Button-4>", self._on_mousewheel_event) 
        self.canvas.bind("<Button-5>", self._on_mousewheel_event) 

        self.contact_images = {} 

        self._perform_search() 

        self.root.update_idletasks() 
        
        self.scrollable_content_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_content_frame.grid_columnconfigure(1, weight=1)

        self.scrollable_content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel_event(self, event):
        """Maneja el evento de la rueda del ratón/touchpad para el desplazamiento."""
        if self.canvas:
            scroll_amount = 0
            scroll_speed_factor = 20 

            if sys.platform == "darwin":
                scroll_amount = -event.delta 
            elif sys.platform == "win32":
                scroll_amount = int(-1 * (event.delta / 120) * scroll_speed_factor)
            else: 
                if event.num == 4: 
                    scroll_amount = -1 * scroll_speed_factor
                elif event.num == 5: 
                    scroll_amount = 1 * scroll_speed_factor
            
            if scroll_amount != 0:
                self.canvas.yview_scroll(scroll_amount, "units")
            return "break" 

    def _display_contacts_in_grid(self, contactos_a_mostrar):
        """
        Limpia el frame de contactos y los muestra en una cuadrícula, incluyendo la imagen, inicial y código QR.
        Las imágenes y QR se cargarán de forma asíncrona.
        """
        for widget in self.scrollable_content_frame.winfo_children():
            widget.destroy()

        if not contactos_a_mostrar:
            no_contacts_label = ttk.Label(self.scrollable_content_frame, text="No se encontraron contactos que coincidan.",
                                            font=self.font_main, foreground=self.text_light, background=self.bg_main)
            no_contacts_label.grid(row=0, column=0, columnspan=3, pady=40, sticky="nsew") 
            self.scrollable_content_frame.grid_rowconfigure(0, weight=1) 
            self._bind_scroll_events_to_widget(no_contacts_label)
            return

        num_cols = 2 

        for index, contacto in enumerate(contactos_a_mostrar):
            frame_card = ttk.Frame(self.scrollable_content_frame, style='ContactCard.TFrame', padding=15, relief="solid", borderwidth=1)
            
            row = index // num_cols
            col = index % num_cols
            frame_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew") 
            
            frame_card.grid_columnconfigure(0, weight=0) 
            frame_card.grid_columnconfigure(1, weight=1) 
            frame_card.grid_columnconfigure(2, weight=0) 

            photo_frame = ttk.Frame(frame_card, style='PhotoFrame.TFrame', width=70, height=70)
            photo_frame.grid(row=0, column=0, rowspan=2, padx=(0, 10), pady=(0, 5), sticky="n") 
            photo_frame.pack_propagate(False) 

            initial_img = self._generate_initial_image(contacto.get_nombre(), (70, 70))
            photo_label = ttk.Label(photo_frame, image=initial_img, background=self.bg_card)
            photo_label.image = initial_img 
            photo_label.pack(expand=True)
            self.contact_images[(contacto.id_contacto, 'photo')] = photo_label 

            info_frame = ttk.Frame(frame_card, style='ContactCard.TFrame') 
            info_frame.grid(row=0, column=1, padx=(0, 5), pady=(0,2), sticky="ew") 

            ttk.Label(info_frame, text=contacto.nombre, foreground=self.text_light, background=self.bg_card, font=self.font_heading).pack(anchor="w", fill="x", expand=True)
            ttk.Label(info_frame, text=f"📞 {contacto.telefono}", foreground=self.text_light, background=self.bg_card, font=self.font_main).pack(anchor="w", fill="x", expand=True)
            ttk.Label(info_frame, text=f"📧 {contacto.email}", foreground=self.text_light, background=self.bg_card, font=self.font_main).pack(anchor="w", fill="x", expand=True)
            
            qr_frame = ttk.Frame(frame_card, style='QRFrame.TFrame', width=70, height=70) 
            qr_frame.grid(row=0, column=2, rowspan=2, padx=(5, 0), pady=(0, 5), sticky="n")
            qr_frame.pack_propagate(False)

            initial_qr_img = self._generate_initial_image("QR", (70,70), bg_color="lightgray")
            qr_label = ttk.Label(qr_frame, image=initial_qr_img, background=self.bg_card)
            qr_label.image = initial_qr_img 
            qr_label.pack(expand=True)
            self.contact_images[(contacto.id_contacto, 'qr')] = qr_label 
            
            self._bind_scroll_events_to_widget(qr_frame)

            btn_frame_card = ttk.Frame(frame_card, style='ContactCardButtonsFrame.TFrame') 
            btn_frame_card.grid(row=1, column=1, columnspan=2, pady=(10, 0), sticky="w") 

            ttk.Button(btn_frame_card, text="✏️ Editar", style='TButton', command=lambda c=contacto: self.mostrar_formulario_editar(c)).pack(side="left", padx=5)
            ttk.Button(btn_frame_card, text="🗑️ Eliminar", style='Danger.TButton', command=lambda c=contacto: self._show_delete_confirmation(c)).pack(side="left")
            
            self._bind_scroll_events_to_widget(frame_card)
            self._bind_scroll_events_to_widget(photo_frame)
            self._bind_scroll_events_to_widget(photo_label)
            self._bind_scroll_events_to_widget(info_frame)
            for child in info_frame.winfo_children():
                self._bind_scroll_events_to_widget(child)
            self._bind_scroll_events_to_widget(btn_frame_card)
            for child in btn_frame_card.winfo_children():
                self._bind_scroll_events_to_widget(child)

        threading.Thread(target=self._load_contact_images_async, args=(contactos_a_mostrar,)).start()

        self.scrollable_content_frame.update_idletasks()
        if self.canvas and self.contact_list_frame.winfo_children():
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _load_contact_images_async(self, contactos):
        """
        Carga las imágenes de los contactos y genera los QR en un hilo separado
        y coloca los resultados en la cola.
        """
        for contacto in contactos:
            photo_img = self._get_contact_image(contacto.get_foto_path(), contacto.get_nombre())
            if photo_img:
                self.image_queue.put((contacto.id_contacto, 'photo', photo_img))

            qr_img = self._generate_contact_qr(contacto)
            if qr_img:
                self.image_queue.put((contacto.id_contacto, 'qr', qr_img))

    def _process_image_queue(self):
        """
        Procesa los resultados de la cola de imágenes en el hilo principal de Tkinter.
        """
        try:
            while True:
                contact_id, img_type, photo_image = self.image_queue.get_nowait()
                if (contact_id, img_type) in self.contact_images:
                    label = self.contact_images[(contact_id, img_type)]
                    if label.winfo_exists():
                        label.config(image=photo_image)
                        label.image = photo_image
                        if img_type == 'photo' and photo_image != self._generate_initial_image(contact_id, (70,70)):
                             label.config(background=self.bg_card)
                        elif img_type == 'qr' and photo_image != self._generate_initial_image("QR", (70,70), bg_color="lightgray"):
                             label.config(background=self.bg_card)

        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._process_image_queue)


    def _bind_scroll_events_to_widget(self, widget):
        """
        Vincula los eventos de scroll (rueda del ratón/touchpad)
        a un widget dado, para que el scroll funcione cuando el puntero
        está sobre ese widget.
        """
        widget.bind("<MouseWheel>", self._on_mousewheel_event)
        widget.bind("<Button-4>", self._on_mousewheel_event)
        widget.bind("<Button-5>", self._on_mousewheel_event)

    def _generate_contact_qr(self, contacto):
        """
        Genera un código QR para el contacto utilizando el formato VCard.
        Retorna un objeto PhotoImage de Tkinter.
        """
        vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nN:{contacto.nombre}\nFN:{contacto.nombre}\nTEL:{contacto.telefono}\nEMAIL:{contacto.email}\nEND:VCARD"
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10, 
                border=2,    
            )
            qr.add_data(vcard_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            qr_size = (70, 70) 
            img = img.resize(qr_size, Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al generar QR para {contacto.nombre}: {e}")
            return None


    def _get_contact_image(self, photo_path, contact_name):
        """
        Carga la imagen del contacto si existe y es válida, de lo contrario genera una imagen con la inicial.
        """
        image_size = (70, 70) 

        if photo_path and os.path.exists(photo_path):
            try:
                img = Image.open(photo_path)
                img = img.resize(image_size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error al cargar imagen '{photo_path}': {e}")
        
        return self._generate_initial_image(contact_name, image_size)

    def _generate_initial_image(self, name, size, bg_color=None):
        """Genera una imagen con la inicial del nombre del contacto."""
        initial = name[0].upper() if name else "?"
        color = bg_color if bg_color else self.placeholder_bg
        img = Image.new('RGB', size, color = color) 
        d = ImageDraw.Draw(img)
        
        try:
            fnt = ImageFont.truetype("arial.ttf", 40) 
        except IOError:
            fnt = ImageFont.load_default() 

        bbox = d.textbbox((0,0), initial, font=fnt)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (size[0] - width) / 2 - bbox[0]
        y = (size[1] - height) / 2 - bbox[1]

        d.text((x, y), initial, font=fnt, fill="white")
        return ImageTk.PhotoImage(img)

    def _clear_search_placeholder(self, event):
        """Elimina el texto de marcador de posición cuando el usuario hace clic en la barra de búsqueda."""
        if self.search_entry.get() == "Buscar por nombre...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground=self.text_light) 

    def _restore_search_placeholder(self, event):
        """Restaura el texto de marcador de posición si la barra de búsqueda está vacía."""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar por nombre...")
            self.search_entry.config(foreground="#808080") 

    def _perform_search_delayed(self, event):
        """Realiza la búsqueda con un pequeño retraso para evitar ejecuciones excesivas."""
        if self._search_timer: 
            self.root.after_cancel(self._search_timer)
        self._search_timer = self.root.after(300, self._perform_search)

    def _perform_search(self):
        """Realiza la búsqueda de contactos según el texto de entrada."""
        search_query = self.search_entry.get().strip()
        if search_query == "Buscar por nombre...":
            search_query = "" 

        contactos_filtrados = self.agenda.buscar_contactos_por_cadena(search_query)
        
        self._display_contacts_in_grid(contactos_filtrados)

    def select_photo(self):
        """Abre un diálogo para seleccionar un archivo de imagen y lo muestra como vista previa."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar foto de contacto",
            filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.selected_photo_path = file_path
            try:
                img = Image.open(file_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS) 
                img_tk = ImageTk.PhotoImage(img)
                self.photo_preview_label.config(image=img_tk)
                self.photo_preview_label.image = img_tk 
                self.photo_preview_label.config(background=self.bg_form) 
            except Exception as e:
                self._show_internal_message(f"❌ Error al cargar la vista previa: {e}", is_error=True)
                self.selected_photo_path = None 

    def crear_formulario(self, title, save_command, initial_contact=None):
        """Crea y muestra un formulario genérico para agregar o editar contactos, ahora con selector de foto."""
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
                    background=self.bg_form, foreground=self.text_light).grid(row=0, column=0, columnspan=3, pady=15)

        self.error_label_form = ttk.Label(self.formulario_actual_frame, text="",
                                                 foreground=self.accent_red, font=self.font_error, background=self.bg_form)
        self.error_label_form.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        self.formulario_actual_frame.grid_columnconfigure(0, weight=0) 
        self.formulario_actual_frame.grid_columnconfigure(1, weight=1) 
        self.formulario_actual_frame.grid_columnconfigure(2, weight=0) 


        ttk.Label(self.formulario_actual_frame, text="Nombre:", style='Form.TLabel').grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.entry_nombre = ttk.Entry(self.formulario_actual_frame, width=35)
        self.entry_nombre.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        ttk.Label(self.formulario_actual_frame, text="Teléfono:", style='Form.TLabel').grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.entry_telefono = ttk.Entry(self.formulario_actual_frame, width=35)
        self.entry_telefono.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        ttk.Label(self.formulario_actual_frame, text="Email:", style='Form.TLabel').grid(row=4, column=0, sticky="e", pady=5, padx=5)
        self.entry_email = ttk.Entry(self.formulario_actual_frame, width=35)
        self.entry_email.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        ttk.Label(self.formulario_actual_frame, text="Foto:", style='Form.TLabel').grid(row=5, column=0, sticky="ne", pady=5, padx=5) 
        
        photo_input_frame = ttk.Frame(self.formulario_actual_frame, style='Form.TFrame')
        photo_input_frame.grid(row=5, column=1, pady=5, padx=5, sticky="nw") 

        ttk.Button(photo_input_frame, text="🖼️ Seleccionar Foto", command=self.select_photo, style='TButton').pack(side="left", padx=(0,5))
        ttk.Button(photo_input_frame, text="Limpiar", command=self._clear_photo_selection, style='Danger.TButton').pack(side="left")

        self.photo_preview_label = ttk.Label(self.formulario_actual_frame, background=self.bg_form)
        self.photo_preview_label.grid(row=2, column=2, rowspan=4, padx=10, pady=5, sticky="n") 


        if initial_contact:
            self.entry_nombre.insert(0, initial_contact.nombre)
            self.entry_telefono.insert(0, initial_contact.telefono)
            self.entry_email.insert(0, initial_contact.email)
            self.selected_photo_path = initial_contact.foto_path
            img_to_display = self._get_contact_image_for_form(initial_contact.foto_path, initial_contact.nombre)
            self.photo_preview_label.config(image=img_to_display)
            self.photo_preview_label.image = img_to_display
            self.photo_preview_label.config(background=self.bg_form if initial_contact.foto_path else self.placeholder_bg)
        else:
            img_to_display = self._generate_initial_image("?", (100, 100)) 
            self.photo_preview_label.config(image=img_to_display)
            self.photo_preview_label.image = img_to_display
            self.photo_preview_label.config(background=self.placeholder_bg)


        ttk.Button(self.formulario_actual_frame, text="💾 Guardar", style='TButton', command=save_command).grid(row=6, column=0, columnspan=3, pady=20)

    def _get_contact_image_for_form(self, photo_path, contact_name):
        """
        Similar a _get_contact_image, pero para el tamaño de vista previa del formulario.
        """
        image_size = (100, 100) 

        if photo_path and os.path.exists(photo_path):
            try:
                img = Image.open(photo_path)
                img = img.resize(image_size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error al cargar imagen para formulario '{photo_path}': {e}")
        
        return self._generate_initial_image(contact_name, image_size)

    def _clear_photo_selection(self):
        """Limpia la selección de foto en el formulario y muestra la inicial del nombre."""
        self.selected_photo_path = None
        current_name = self.entry_nombre.get().strip() if hasattr(self, 'entry_nombre') else ""
        img_to_display = self._generate_initial_image(current_name if current_name else "?", (100, 100))
        self.photo_preview_label.config(image=img_to_display)
        self.photo_preview_label.image = img_to_display
        self.photo_preview_label.config(background=self.placeholder_bg)


    def mostrar_formulario_agregar(self):
        """Muestra el formulario para agregar un nuevo contacto."""
        self.selected_photo_path = None 
        self.crear_formulario("➕ Agregar Contacto", self.guardar_nuevo_contacto)

    def mostrar_formulario_editar(self, contacto):
        """Muestra el formulario para editar un contacto existente."""
        self.selected_photo_path = contacto.foto_path 
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
        
        if not telefono.strip():
            self.error_label_form.config(text="⚠️ Error: El teléfono no puede estar vacío.")
            return False
        telefono_limpio = telefono.strip().replace(" ", "").replace("-", "")
        if not telefono_limpio.isdigit():
            self.error_label_form.config(text="⚠️ Error: El teléfono solo debe contener números (opcionalmente con espacios o guiones).")
            return False

        if not email.strip():
            self.error_label_form.config(text="⚠️ Error: El email no puede estar vacío.")
            return False
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
            self.error_label_form.config(text="⚠️ Error: Formato de email inválido (ej. usuario@dominio.com).")
            return False

        # --- INICIO DE LA CORRECCIÓN ---
        # Validación de nombre duplicado
        duplicado_nombre = self.agenda.buscar_contacto(nombre=nombre.strip(), contacto_a_excluir=contacto_a_excluir)
        if duplicado_nombre:
            self.error_label_form.config(text="⚠️ Error: Ya existe un contacto con ese nombre.")
            return False
        # --- FIN DE LA CORRECCIÓN ---

        duplicado_tel = self.agenda.buscar_contacto(telefono=telefono.strip(), contacto_a_excluir=contacto_a_excluir)
        if duplicado_tel:
            self.error_label_form.config(text="⚠️ Error: Ya existe un contacto con ese teléfono.")
            return False
        
        duplicado_email = self.agenda.buscar_contacto(email=email.strip(), contacto_a_excluir=contacto_a_excluir)
        if duplicado_email:
            self.error_label_form.config(text="⚠️ Error: Ya existe un contacto con ese email.")
            return False

        return True

    def _save_photo_and_get_path(self, contact_id):
        """
        Copia la foto seleccionada a la carpeta de fotos de la aplicación
        y retorna la ruta relativa para guardar en la DB.
        """
        if self.selected_photo_path:
            extension = os.path.splitext(self.selected_photo_path)[1]
            photo_filename = f"{contact_id}{extension}"
            destination_path = os.path.join(PHOTOS_DIR, photo_filename)
            try:
                shutil.copy2(self.selected_photo_path, destination_path)
                return destination_path
            except Exception as e:
                print(f"Error al copiar la imagen: {e}")
                return None
        return None

    def guardar_nuevo_contacto(self):
        """Intenta guardar un nuevo contacto después de la validación de los datos y la foto."""
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()

        if not self.validar_datos_contacto(nombre, telefono, email):
            return

        temp_contact = Contacto(nombre, telefono, email) 
        foto_path_to_save = self._save_photo_and_get_path(temp_contact.id_contacto)

        nuevo_contacto = Contacto(nombre, telefono, email, foto_path_to_save, temp_contact.id_contacto) 
        if self.agenda.agregar_contacto(nuevo_contacto):
            self._show_internal_message(" Contacto agregado correctamente.")
            self.cerrar_formulario_actual()
        else:
            if foto_path_to_save and os.path.exists(foto_path_to_save):
                os.remove(foto_path_to_save)
            self._show_internal_message(" Error: No se pudo agregar el contacto. Verifique que los datos no estén duplicados.", is_error=True)

    def guardar_edicion(self, contacto_original):
        """Intenta guardar los cambios de un contacto editado después de la validación y la foto."""
        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_telefono = self.entry_telefono.get().strip()
        nuevo_email = self.entry_email.get().strip()

        if not self.validar_datos_contacto(nuevo_nombre, nuevo_telefono, nuevo_email, contacto_a_excluir=contacto_original):
            return
        
        foto_path_to_save = None
        if self.selected_photo_path: 
            foto_path_to_save = self._save_photo_and_get_path(contacto_original.id_contacto)
        elif self.selected_photo_path is None and contacto_original.foto_path: 
            if os.path.exists(contacto_original.foto_path):
                os.remove(contacto_original.foto_path)
            foto_path_to_save = None 
        else: 
            foto_path_to_save = contacto_original.foto_path 

        if self.agenda.editar_contacto(contacto_original.id_contacto, nuevo_nombre, nuevo_telefono, nuevo_email, foto_path_to_save):
            self._show_internal_message(" Contacto editado correctamente.")
            self.cerrar_formulario_actual()
        else:
            self._show_internal_message(" Error: No se pudo editar el contacto. Verifique que los datos no estén duplicados.", is_error=True)

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
        """Ejecuta la eliminación del contacto y muestra un mensaje, además de eliminar la foto."""
        if contacto_a_eliminar.foto_path and os.path.exists(contacto_a_eliminar.foto_path):
            try:
                os.remove(contacto_a_eliminar.foto_path)
                print(f"Foto '{contacto_a_eliminar.foto_path}' eliminada.")
            except Exception as e:
                print(f"Error al eliminar el archivo de foto: {e}")

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

        ttk.Label(about_frame, text="   • Jesus Manuel Torres Bandera (Product Owner)",
                    font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        ttk.Label(about_frame, text="   • Diego Fernando Pinzon Quintero (Scrum Master)",
                    font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        ttk.Label(about_frame, text="   • Luis David Maldonado Suarez (Development Team)",
                    font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        ttk.Label(about_frame, text="   • Oscar Leonardo Macias Puentes (Development Team)",
                    font=self.font_about_text, foreground=self.text_light, background=self.bg_form).pack(anchor='center')
        
        ttk.Label(about_frame, text="\nEquipo: DARK SIDE OF DEVS",
                    font=self.font_button, foreground=self.text_light, background=self.bg_form).pack(pady=(15, 0))