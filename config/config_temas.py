import customtkinter as ctk
import tkinter as tk
from modulos.transitions import transition_to_next_ui
from config.config import centrar_ventana
import json
from tkinter import messagebox


def save_config(config):
    with open("config/config.json", "w") as config_file:
        json.dump(config, config_file)


def load_config():
    try:
        with open("config/config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}


def apply_theme(temas):
    ctk.set_appearance_mode(temas)
    config = load_config()
    config["theme"] = temas
    save_config(config)


def apply_color(color):
    ctk.set_default_color_theme(color)
    config = load_config()
    config["color"] = color
    save_config(config)


def open_config_window(parent):
    

    config = load_config()
    current_tema = config.get("theme", "Dark")
    current_color = config.get("color", "blue")

    # Variables temporales para los valores seleccionados
    temp_tema = ctk.StringVar(value=current_tema)
    temp_color = ctk.StringVar(value=current_color)

    config_window = ctk.CTkToplevel(parent)
    config_window.title("Configuración")
    config_window.geometry("800x500")
    config_window.grab_set()
    config_window.resizable(False, False)

    centrar_ventana(config_window, 800, 500)
    temas(config_window, temp_tema, temp_color, parent)



def temas(config_window, temp_tema, temp_color, parent):
    
    for widget in config_window.winfo_children():
        widget.destroy()
    
    fg = "#202020"
    poppins12bold = ("Poppins", 12, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins20bold = ("Poppins", 20, "bold")

    left_frame = ctk.CTkFrame(config_window, corner_radius=15)
    left_frame.pack(fill="y", side="left", pady=5, padx=5)

    Tema_button = ctk.CTkButton(left_frame, text="Apariencia", font=poppins12bold)
    Tema_button.pack(padx=20, pady=10, side="top")

    pass_button = ctk.CTkButton(left_frame, text="Contraseñas", font=poppins12bold, command=lambda: contrasenas_cambiar(config_window, temp_tema, temp_color, parent))
    pass_button.pack(padx=20, pady=10, side="top")

    accept_button = ctk.CTkButton(left_frame, text="Atrás", command=config_window.destroy, font=poppins12bold)
    accept_button.pack(padx=20, pady=10, side="bottom")

    ########## Temas ########

    top_frame = ctk.CTkFrame(config_window, corner_radius=15)
    top_frame.pack(fill="x", anchor="n", pady=5, padx=5)

    text = ctk.CTkLabel(top_frame, text="Apariencia", font=poppins20bold)
    text.pack(padx=20, pady=10, side="top")

    right_frame = ctk.CTkFrame(config_window, corner_radius=15)
    right_frame.pack(fill="both", anchor="n", pady=5, padx=5, expand=True)

    right_frame2 = ctk.CTkFrame(config_window, corner_radius=15)
    right_frame2.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)

    text2 = ctk.CTkLabel(right_frame, text="Tema", font=poppins14bold)
    text2.pack(pady=10, side="top")

    tema_options = ["Dark", "Light", "System"]

    for tema in tema_options:
        radio_button = ctk.CTkRadioButton(
            right_frame,
            text=tema,
            variable=temp_tema,
            value=tema,
            font=poppins12bold
        )
        radio_button.pack(padx=50, pady=50, side="left")

    text3 = ctk.CTkLabel(right_frame2, text="Colores", font=poppins14bold)
    text3.pack(pady=10, side="top")

    color_options = ["blue", "green", "dark-blue"]

    for color in color_options:
        radio_button = ctk.CTkRadioButton(
            right_frame2,
            text=color.capitalize(),
            variable=temp_color,
            value=color,
            font=poppins12bold
        )
        radio_button.pack(padx=50, pady=50, side="left")

    def aplicar_cambios():
        from modulos.menu import menu
        # Aplica los cambios seleccionados
        
        apply_theme(temp_tema.get())
        apply_color(temp_color.get())
        config_window.destroy()
        menu(parent)

    aplicar_button = ctk.CTkButton(config_window, text="Aplicar", command=aplicar_cambios, font=poppins12bold)
    aplicar_button.pack(padx=10, pady=10, side="bottom", anchor="e")
    
    
def contrasenas_cambiar(config_window, temp_tema, temp_color, parent):
    # Limpiar la ventana
    for widget in config_window.winfo_children():
        widget.destroy()

    # Crear la interfaz de cambio de contraseñas
    poppins12bold = ("Poppins", 12, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    
    left_frame = ctk.CTkFrame(config_window, corner_radius=15)
    left_frame.pack(fill="y", side="left", pady=5, padx=5)

    Tema_button = ctk.CTkButton(left_frame, text="Apariencia", font=poppins12bold, command=lambda: temas(config_window, temp_tema, temp_color, parent))
    Tema_button.pack(padx=20, pady=10, side="top")

    pass_button = ctk.CTkButton(left_frame, text="Contraseñas", font=poppins12bold, command=lambda: contrasenas_cambiar(config_window))
    pass_button.pack(padx=20, pady=10, side="top")

    accept_button = ctk.CTkButton(left_frame, text="Atrás", command=config_window.destroy, font=poppins12bold)
    accept_button.pack(padx=20, pady=10, side="bottom")
    
    #############

    top_frame = ctk.CTkFrame(config_window, corner_radius=15)
    top_frame.pack(fill="x", anchor="n", pady=5, padx=5)

    text = ctk.CTkLabel(top_frame, text="Cambiar Contraseñas", font=poppins20bold)
    text.pack(padx=20, pady=10, side="top")

    right_frame = ctk.CTkFrame(config_window, corner_radius=15)
    right_frame.pack(fill="both", anchor="n", pady=5, padx=5, expand=True)
    
    right_frame2 = ctk.CTkFrame(config_window, corner_radius=15)
    right_frame2.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)

    text2 = ctk.CTkLabel(right_frame, text="Nueva Contraseña de Administrador", font=poppins14bold)
    text2.pack(pady=10, side="top")

    entry_admin_password = ctk.CTkEntry(right_frame, placeholder_text="Nueva Contraseña de Administrador", font=poppins12bold, width=250, show="*")
    entry_admin_password.pack(pady=10, padx=10, side="top")

    text3 = ctk.CTkLabel(right_frame2, text="Nueva Contraseña de Usuario", font=poppins14bold)
    text3.pack(pady=10, side="top")

    entry_user_password = ctk.CTkEntry(right_frame2, placeholder_text="Nueva Contraseña de Usuario", font=poppins12bold, width=250, show="*")
    entry_user_password.pack(pady=10, padx=10, side="top")


    def guardar_contraseñas():
        # Leer las contraseñas actuales del archivo JSON
        with open("modulos/c.json", "r") as archivo:
            contraseñas_actuales = json.load(archivo)

        # Obtener los valores de los campos de entrada
        nueva_contrasena_admin = entry_admin_password.get()
        nueva_contrasena_usuario = entry_user_password.get()

        # Verificar si ha habido algún cambio
        if (nueva_contrasena_admin and nueva_contrasena_admin != contraseñas_actuales.get("contrasena_admin")) or \
        (nueva_contrasena_usuario and nueva_contrasena_usuario != contraseñas_actuales.get("contrasena_usuario")):
            
            # Confirmar antes de guardar
            if messagebox.askyesno("Confirmar", "¿Desea guardar los cambios en las contraseñas?"):
                # Actualizar las contraseñas solo si ha habido cambios
                nuevas_contraseñas = {
                    "contrasena_admin": nueva_contrasena_admin if nueva_contrasena_admin else contraseñas_actuales.get("contrasena_admin"),
                    "contrasena_usuario": nueva_contrasena_usuario if nueva_contrasena_usuario else contraseñas_actuales.get("contrasena_usuario")
                }
                
                # Guardar las nuevas contraseñas en el archivo JSON
                with open("modulos/c.json", "w") as archivo:
                    json.dump(nuevas_contraseñas, archivo)
                
                messagebox.showinfo("Contraseñas guardadas", "Las contraseñas han sido guardadas exitosamente.")
            else:
                messagebox.showinfo("Cancelado", "Los cambios no han sido guardados.")
        else:
            messagebox.showinfo("Sin cambios", "No se han realizado cambios en las contraseñas.")
        


    guardar_button = ctk.CTkButton(config_window, text="Guardar", command=guardar_contraseñas, font=poppins12bold)
    guardar_button.pack(padx=10, pady=10, side="bottom", anchor="e")