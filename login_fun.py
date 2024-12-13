import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from menu import menu

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def login(window):
    """Pantalla de inicio de sesión"""
    # Configuración de fuentes
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20)
    poppins16bold = ("Poppins", 16, "bold")

    # Fondo de pantalla
    background_image = Image.open("login.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Crear un Label para la imagen de fondo
    background_label = tk.Label(window, image=background_photo)
    background_label.image = background_photo  # Evita que se elimine la referencia
    background_label.place(relwidth=1, relheight=1)

    # Frame principal
    left_frame = ctk.CTkFrame(window, width=500)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Contenido del frame
    text = ctk.CTkLabel(left_frame, text="¡Bienvenido!", font=poppins30bold)
    text.place(x=155, y=150)

    text2 = ctk.CTkLabel(left_frame, text="¿Cómo desea ingresar?", font=poppins20bold)
    text2.place(x=130, y=250)

    text3 = ctk.CTkLabel(left_frame, text="o", font=poppins20bold)
    text3.place(x=250, y=370)

    admin = ctk.CTkButton(
        left_frame,
        text="Administrador",
        command=lambda: loginadmin(left_frame, window),
        width=200,
        font=poppins16bold,
    )
    admin.place(x=150, y=320)

    usuario = ctk.CTkButton(
        left_frame,
        text="Usuario",
        command=lambda: print(":v"),
        width=200,
        font=poppins16bold,
    )
    usuario.place(x=150, y=420)

def loginadmin(left_frame, window):
    """Pantalla de inicio de sesión del administrador"""
    # Limpiar el frame actual
    for widget in left_frame.winfo_children():
        widget.destroy()

    # Configuración de fuentes
    poppins30bold = ("Poppins", 30, "bold")
    poppins16bold = ("Poppins", 16, "bold")

    # Contenido del frame
    text = ctk.CTkLabel(left_frame, text="¡Bienvenido administrador!", font=poppins30bold)
    text.place(x=40, y=150)

    contrasena = ctk.CTkEntry(
        left_frame, placeholder_text="Ingrese Contraseña", show="*", font=poppins16bold, width=250
    )
    contrasena.place(x=125, y=300)

    inicio = ctk.CTkButton(
        left_frame,
        text="Iniciar Sesión",
        command=lambda: check(contrasena, window),
        width=200,
        font=poppins16bold,
    )
    inicio.place(x=150, y=370)

def check(entry, window):
    """Validación de contraseña"""
    contr = "1234"
    if entry.get() == contr:
       
        for widget in window.winfo_children():
            widget.destroy()
        menu(window)
    else:
        print("Contraseña incorrecta")
