import customtkinter as ctk
from modulos.menu import menu
from modulos.login_fun import login
from modulos.consulta_general import consulta
from modulos.inmuebles import inmuebles
from modulos.liquidacion import liquidacion
from modulos.contribuyentes import contribuyentes
from modulos.sectores import sectores

from modulos2.menu import menu2
from modulos2.consulta_general import consulta
from modulos2.inmuebles import inmuebles
from modulos2.liquidacion import liquidacion
from modulos2.contribuyentes import contribuyentes
from modulos2.sectores import sectores
from modulos.transitions import transition_to_next_ui

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def close_after_timeout(root, timeout):
    """Close the window after a specified timeout (in milliseconds)."""
    root.after(timeout, root.destroy)

window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")
window.configure(bg="black")  # Set initial background color

#Este es para admin

# menu(window)

#Este es para usuarios

#menu2(window)

#Para iniciar desde el login, la contraseña es 1234

window.after(200, lambda: transition_to_next_ui(window, None, login, duration=500))  # Show loading transition before login

window.mainloop()
