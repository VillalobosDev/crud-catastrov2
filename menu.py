import customtkinter as ctk
import tkinter as tk
from menubar import menubar
from contribuyentes import contribuyentes


def menu(window):

    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)
    
    for widget in window.winfo_children():
        widget.destroy()

    menubar(window) 

    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)

    left_frame = ctk.CTkFrame(window, corner_radius=15, width=600, height=700)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    right_frame = ctk.CTkFrame(window, corner_radius=15)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)


    #Contenido del frame top

    salir_btn = ctk.CTkButton(top_frame, text="Salir", command=window.quit, font=poppins20bold)
    salir_btn.pack(padx=10, pady=10, side="left")

    window_title = ctk.CTkLabel(top_frame, text="Sistema de Gestion Catastral", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")


    #Contenido del frame left

    contribuyente_btn = ctk.CTkButton(left_frame, text="Contribuyentes", command=lambda: contribuyentes(window, menu), width=190, font=poppins20bold)
    contribuyente_btn.pack(pady=50, padx=50, anchor="center", expand=True)

    inmuebles_btn = ctk.CTkButton(left_frame, text="Inmuebles", command=lambda: print("Aca va la funcion de la ventana inmuebles"), width=190, font=poppins20bold)
    inmuebles_btn.pack( padx=50, anchor="center", expand=True)

    sector_btn = ctk.CTkButton(left_frame, text="Sectores", command=lambda: print("Aca va la funcion de la ventana sectores"), width=190, font=poppins20bold)
    sector_btn.pack(pady=50, padx=50, anchor="center", expand=True)
 # Define main window

