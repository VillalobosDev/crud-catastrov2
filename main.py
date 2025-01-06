import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from modulos.login_fun import login
from modulos.menu import menu
from modulos.consulta_general import consulta
from modulos.inmuebles import inmuebles
from modulos.liquidacion import liquidacion
from modulos.contribuyentes import contribuyentes
from modulos.sectores import sectores

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def close_after_timeout(root, timeout):
    """Close the window after a specified timeout (in milliseconds)."""
    root.after(timeout, root.destroy)

window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")

sectores(window, menu)

window.mainloop()
