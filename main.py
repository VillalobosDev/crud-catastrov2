import customtkinter as ctk
# Funciones personales
from menu import menu

# Set appearance and theme
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

poppins30bold = ("Poppins", 30, "bold")
poppins20bold = ("Poppins", 20, "bold")
poppins14bold = ("Poppins", 14, "bold")
poppins12 = ("Poppins", 12)

window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")

menu(window)

# Run the application
window.mainloop()   