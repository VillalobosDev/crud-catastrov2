import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from modulos.menu import menu
from modulos2.menu import menu2
from modulos.transitions import transition_to_next_ui

def set_initial_background(window, original_image, background_label):
    """Set the initial background image once window is initialized."""
    try:
        # Set the window size to fixed 1080x720
        window.geometry("1080x720")
        window.resizable(False, False)  # Disable resizing
        
        # Resize the image to fit the window dimensions
        resized_image = original_image.resize((1380, 920), Image.Resampling.LANCZOS)
        background_photo = ImageTk.PhotoImage(resized_image)
        background_label.configure(image=background_photo)
        background_label.image = background_photo
        print(f"Initial background set to 1080x720")
    except Exception as e:
        print(f"Error setting initial background: {e}")

def load_login_ui(window):
    """Load the login UI components after the background is set."""
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20)
    poppins16bold = ("Poppins", 16, "bold")

    left_frame = ctk.CTkFrame(window, width=500)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

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
        command=lambda: menu2(window),
        width=200,
        font=poppins16bold,
    )
    usuario.place(x=150, y=420)

def login(window):
    """Pantalla de inicio de sesión"""
    try:
        # Clear existing widgets
        for widget in window.winfo_children():
            widget.destroy()

        original_image = Image.open("assets/login.png")
        print("Original image loaded successfully.")

        background_label = tk.Label(window, bg="black")  # Set initial background color
        background_label.place(relwidth=1, relheight=1)

        # Set the initial background image
        set_initial_background(window, original_image, background_label)

        # Load the login UI components immediately
        window.after(1, load_login_ui, window)

    except Exception as e:
        print(f"Error during login setup: {e}")

def loginadmin(left_frame, window):
    """Pantalla de inicio de sesión del administrador"""
    for widget in left_frame.winfo_children():
        widget.destroy()

    poppins30bold = ("Poppins", 30, "bold")
    poppins16bold = ("Poppins", 16, "bold")

    text = ctk.CTkLabel(left_frame, text="¡Bienvenido administrador!", font=poppins30bold)
    text.place(x=40, y=150)

    contrasena = ctk.CTkEntry(
        left_frame, placeholder_text="Ingrese Contraseña", show="*", font=poppins16bold, width=250
    )
    contrasena.place(x=125, y=300)

    inicio = ctk.CTkButton(
        left_frame,
        text="Iniciar Sesión",
        command=lambda: check(contrasena, window, left_frame),
        width=200,
        font=poppins16bold,
    )
    inicio.place(x=150, y=370)

def check(entry, window, left_frame):
    """Validación de contraseña"""
    contr = "1234"
    if entry.get() == contr:
        def logout(current_window):
            from modulos.login_fun import login
            from config.config import centrar_ventana
            current_window.destroy()
            new_window = ctk.CTk()
            new_window.title("Axio")
            new_window.geometry("1080x720")
            centrar_ventana(new_window, 1080, 720)

            menu(new_window)
            new_window.mainloop()
        logout(window)
    else:
        print("Contraseña incorrecta")
