import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from modulos.menu import menu
from modulos.login_fun import login
from modulos.consulta_general import consulta
from modulos.inmuebles import inmuebles
from modulos.liquidacion import liquidacion
from modulos.contribuyentes import contribuyentes
from modulos.sectores import sectores
from modulos2.menu import menu2
# from modulos2.consulta_general import consulta
# from modulos2.liquidacion import liquidacion
# from modulos2.contribuyentes import contribuyentes
from modulos2.sectores import sectores
from modulos.transitions import transition_to_next_ui
from config.config_temas import load_config, apply_theme, apply_color
from config.config import centrar_ventana

# Cargar configuración
config = load_config()
theme = config.get("theme", "Dark")  # Default to "Dark" if no theme is set
color = config.get("color", "blue")  # Default to "blue" if no color is set

# Configuración de CustomTkinter
apply_theme(theme)
apply_color(color)

window = ctk.CTk()
window.title("Axio")
window.geometry("1080x720")

# window.configure(fg_color="black")



centrar_ventana(window, 1080, 720)

def close_after_timeout(root, timeout):
    """Close the window after a specified timeout (in milliseconds)."""
    root.after(timeout, root.destroy)



#Este es para usuarios4

# menu(window)

#inmuebles(window, menu)

#Para iniciar desde el login, la contraseña es 1234
login(window)

# liquidacion(window, menu)
# consulta(window, menu)


window.mainloop()

