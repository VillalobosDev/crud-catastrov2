import customtkinter as ctk
from tkinter import Menu

# Function to create the toolbar menu
def menubar(window):
    
    # Create a Menu Bar with black background
    menu_bar = Menu(window, bg="black", fg="white")

    # Menu Menu (replaces File)
    menu_menu = Menu(menu_bar, tearoff=0, bg="black", fg="white")
    menu_menu.add_separator()
    menu_menu.add_command(label="Salir del programa", command=window.quit)

    # Config Menu (replaces Edit)
    config_menu = Menu(menu_bar, tearoff=0, bg="black", fg="white")
    config_menu.add_separator()
    config_menu.add_command(label="Preferencias", command=lambda: print("Preferences"))

    # Soporte Menu (replaces Help)
    soporte_menu = Menu(menu_bar, tearoff=0, bg="black", fg="white")
    soporte_menu.add_command(label="Contactar Soporte", command=lambda: print("Contact Support"))
    soporte_menu.add_command(label="FAQ", command=lambda: print("FAQ"))

    # Add Menus to the Menu Bar
    menu_bar.add_cascade(label="Menu", menu=menu_menu)
    menu_bar.add_cascade(label="Configuracion", menu=config_menu)
    menu_bar.add_cascade(label="Soporte", menu=soporte_menu)

    # Attach the Menu Bar to the window
    window.config(menu=menu_bar)
