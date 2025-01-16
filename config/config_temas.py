import customtkinter as ctk
import tkinter as tk
from modulos.transitions import transition_to_next_ui
from config.config import centrar_ventana
import json


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
    
    fg = "#202020"
    poppins12bold = ("Poppins", 12, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins20bold = ("Poppins", 20, "bold")

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

    left_frame = ctk.CTkFrame(config_window, corner_radius=15)
    left_frame.pack(fill="y", side="left", pady=5, padx=5)

    Tema_button = ctk.CTkButton(left_frame, text="Apariencia", font=poppins12bold)
    Tema_button.pack(padx=20, pady=10, side="top")

    pass_button = ctk.CTkButton(left_frame, text="Contraseñas", font=poppins12bold)
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
