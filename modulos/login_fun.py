import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from modulos.menu import menu
from modulos2.menu import menu2
from config.config import centrar_ventana
import json






def login(window):
    
    poppins14bold = ("Poppins", 12, "bold")
    poppins18bold = ("Poppins", 14, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins10 = ("Poppins", 10, "bold")
    
    for widget in window.winfo_children():
        widget.destroy()
        
    window.geometry("1000x600")
    window.resizable(False, False)
    centrar_ventana(window, 1000, 600)

    try:
        # Cargar la imagen desde la carpeta assets
        imagen = Image.open("assets/login_claro.png")
        imagendark = Image.open("assets/login_oscuro.png")

        imagen_ctk = ctk.CTkImage(light_image=imagen, dark_image=imagendark, size=(1000,600))
        
        # Crear un Label para mostrar la imagen
        label_imagen = ctk.CTkLabel(window, image=imagen_ctk, text="")
        label_imagen.image = imagen_ctk 
        label_imagen.pack(fill="both", expand=True)

        overlay_frame = ctk.CTkFrame(window, width=400, height=600)
        overlay_frame.place(x=0, y=0, anchor="nw")
        overlay_frame.pack_propagate(False)

        frame_login = ctk.CTkFrame(overlay_frame, corner_radius=15, width=380, height=580)
        frame_login.pack(pady=10, padx=10)
        frame_login.pack_propagate(False)
    
    

        text_inicio = ctk.CTkLabel(frame_login, text="Axio", font=poppins20bold)
        text_inicio.pack(pady=10, anchor="center", expand=True)
        

        frame_contenedor = ctk.CTkFrame(frame_login, corner_radius=15)
        frame_contenedor.pack(padx=5, pady=5, expand=True, anchor="n")

        login_frame(frame_contenedor, window)
        
        
        btn_cerrar=ctk.CTkButton(frame_login, text="Salir", font=poppins14bold, command=window.destroy)
        btn_cerrar.pack(pady=5, padx=5, side="left", anchor="s")
        
        btn_soporte=ctk.CTkButton(frame_login, text="Soporte", font=poppins14bold)
        btn_soporte.pack(pady=5, padx=5, side="right", anchor="s")
 

    except Exception as e:
        print(f"Error al cargar la imagen: {e}")


def login_frame(frame_contenedor, window):
    poppins14bold = ("Poppins", 12, "bold")
    poppins18bold = ("Poppins", 14, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins10 = ("Poppins", 10, "bold")

        
    for widget in frame_contenedor.winfo_children():
        widget.destroy()
        
    text = ctk.CTkLabel(frame_contenedor, text="Iniciar sesión como:", font=poppins18bold)
    text.pack(pady=20, padx=10, side="top")

    btn_admin = ctk.CTkButton(frame_contenedor, text="Administrador", font=poppins14bold, width=250, command=lambda: loginadmin(frame_contenedor, window))
    btn_admin.pack(pady=10, padx=10)

    btn_usuario = ctk.CTkButton(frame_contenedor, text="Usuario", width=250, font=poppins14bold, command=lambda: loginuser(frame_contenedor, window))
    btn_usuario.pack(pady=10, padx=10)


def loginadmin(left_frame, window):
    poppins14bold = ("Poppins", 14, "bold")
    poppins12bold = ("Poppins", 12, "bold")
    poppins16bold = ("Poppins", 16, "bold")
    poppins10 = ("Poppins", 10, "bold")

    for widget in left_frame.winfo_children():
        widget.destroy()
        
    text = ctk.CTkLabel(left_frame, text="Administrador", font=poppins16bold)
    text.pack(pady=20, padx=10, side="top")

    entry_password = ctk.CTkEntry(left_frame, placeholder_text="Ingresar Contraseña", font=poppins12bold, width=250, show="*")
    entry_password.pack(pady=20, padx=10, side="top")

    btn_iniciar = ctk.CTkButton(left_frame, text="Ingresar", font=poppins12bold, width=250, command=lambda: check(entry_password, window, left_frame))
    btn_iniciar.pack(pady=10, padx=10)

    btn_volver = ctk.CTkButton(left_frame, text="Volver", font=poppins12bold, width=250,command=lambda: volver_a_login_frame(left_frame, window))
    btn_volver.pack(pady=10, padx=10)
    
    
    
    
    
    
def loginuser(left_frame, window):
    poppins14bold = ("Poppins", 14, "bold")
    poppins12bold = ("Poppins", 12, "bold")
    poppins16bold = ("Poppins", 16, "bold")
    poppins10 = ("Poppins", 10, "bold")

    for widget in left_frame.winfo_children():
        widget.destroy()
        
    text = ctk.CTkLabel(left_frame, text="Usuario", font=poppins16bold)
    text.pack(pady=20, padx=10, side="top")

    entry_password = ctk.CTkEntry(left_frame, placeholder_text="Ingresar Contraseña", font=poppins12bold, width=250, show="*")
    entry_password.pack(pady=20, padx=10, side="top")

    btn_iniciar = ctk.CTkButton(left_frame, text="Ingresar", font=poppins12bold, width=250, command=lambda: check2(entry_password, window, left_frame))
    btn_iniciar.pack(pady=10, padx=10)

    btn_volver = ctk.CTkButton(left_frame, text="Volver", font=poppins12bold, width=250,command=lambda: volver_a_login_frame(left_frame, window))
    btn_volver.pack(pady=10, padx=10)


def volver_a_login_frame(left_frame, window):
    for widget in left_frame.winfo_children():
        widget.destroy()
    login_frame(left_frame, window)




def leer_contrasena():
    with open("modulos/c.json", "r") as archivo:
        datos = json.load(archivo)
    return datos.get("contrasena_admin")


def leer_contrasena2():
    with open("modulos/c.json", "r") as archivo:
        datos = json.load(archivo)
    return datos.get("contrasena_usuario")

def check(entry, window, left_frame):
    """Validación de contraseña"""
    contr = leer_contrasena()
    if entry.get() == contr:
        def logout(current_window):
            from modulos.login_fun import login
            from config.config import centrar_ventana
            for widget in current_window.winfo_children():
                widget.after_cancel(widget)
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
        
        
        
def check2(entry, window, left_frame):
    """Validación de contraseña"""
    contr = leer_contrasena2()
    if entry.get() == contr:
        def logout(current_window):
            from modulos.login_fun import login
            from config.config import centrar_ventana
            for widget in current_window.winfo_children():
                widget.after_cancel(widget)
            current_window.destroy()
            new_window = ctk.CTk()
            new_window.title("Axio")
            new_window.geometry("1080x720")
            centrar_ventana(new_window, 1080, 720)

            menu2(new_window)
            new_window.mainloop()
        logout(window)
    else:
        print("Contraseña incorrecta")
        
        
        
