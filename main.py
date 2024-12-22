import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from login_fun import login
from menu import menu
from consulta_general import consulta
from inmuebles import inmuebles

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def close_after_timeout(root, timeout):
    """Close the window after a specified timeout (in milliseconds)."""
    root.after(timeout, root.destroy)

window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")

inmuebles(window, menu)

window.mainloop()
