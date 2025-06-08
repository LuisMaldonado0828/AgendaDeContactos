# 📒 AgendaDeContactos

> “La organización no es solo una herramienta, es un hábito de quienes transforman el caos en soluciones.”

---

## 🧠 Descripción del Proyecto

**AgendaDeContactos** es una aplicación de consola desarrollada en **Python** por el equipo **Dark Side Of Devs**. Su propósito es ofrecer una herramienta funcional, sencilla y práctica para gestionar contactos personales o profesionales.

Con esta agenda digital puedes **agregar**, **buscar**, **actualizar** y **eliminar** contactos, todo desde una interfaz de línea de comandos clara y amigable. Está pensada como un ejercicio de programación orientada a objetos y modularidad, ideal para aprender y aplicar fundamentos sólidos en desarrollo de software.

---

## 🎯 Objetivos del Proyecto

- Aplicar programación orientada a objetos: clases, atributos y métodos.
- Manejar listas de objetos (`List[Contacto]`) como estructura de almacenamiento.
- Modularizar el código utilizando funciones y clases.
- Implementar validaciones como detección de duplicados y correos mal formateados.

---

## 📋 Funcionalidades Principales

- ➕ Agregar contacto (nombre, teléfono, correo electrónico).
- 🔍 Buscar contacto por nombre.
- ✏️ Actualizar información de contacto.
- ❌ Eliminar contacto.
- 🧾 Ver información del equipo en la opción “Acerca de”.
- ✅ Validaciones para evitar contactos duplicados y verificar formato de correos.

---

## 🧩 Estructura del Proyecto

### Clase `Contacto`

- **Atributos**: `nombre`, `telefono`, `email`
- **Métodos**: constructor, getters y setters

### Clase `Agenda`

- **Atributo**: `contactos` (lista de objetos `Contacto`)
- **Métodos**:
  - `agregar_contacto()`
  - `buscar_contacto()`
  - `actualizar_contacto()`
  - `eliminar_contacto()`

---

## ▶️ ¿Cómo ejecutar el programa?

1. Asegúrate de tener **Python 3.10 o superior** instalado.
2. Clona este repositorio o descarga los archivos `.py`.
3. Ejecuta el archivo principal desde consola:
   ```bash
   python agenda_contactos.py




