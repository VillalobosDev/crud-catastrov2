import customtkinter as ctk
import tkinter as tk
from menubar import menubar
from inmuebles_agg import inmuebles_agg
from inmuebles_gestion import inmuebles_gestion

def inmuebles(window, last_window):
    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)
    
    menubar(window)
    
    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)
    
    left_frame = ctk.CTkFrame(window, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    
    right_frame = ctk.CTkFrame(window, corner_radius=15)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    #Contenido del frame top
    
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: last_window(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestion Inmuebles", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")
    
    #Contenido del left frame
    menu = last_window

    #                                                                                                       (window, last window, last_window2) 
    l_inmuebles_btn = ctk.CTkButton(left_frame, text="Agregar Inmuebles", command=lambda: inmuebles_agg(window, menu, inmuebles), width=190, font=poppins20bold)
    l_inmuebles_btn.pack(pady=105, padx=50, anchor="center", expand=True)
    
    #Contenido del right frame
    
    r_inmuebles_btn = ctk.CTkButton(right_frame, text="Gestionar Inmuebles", command=lambda: inmuebles_gestion(window, menu, inmuebles), width=190, font=poppins20bold)
    r_inmuebles_btn.pack(pady=105, padx=50, anchor="center", expand=True)
    
