import customtkinter as ctk
from modulos.login_fun import login
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
window.iconbitmap(r"assets/axiow.ico")

centrar_ventana(window, 1080, 720)
login(window)

window.mainloop()

