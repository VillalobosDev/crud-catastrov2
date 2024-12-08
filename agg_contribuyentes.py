import customtkinter as ctk
import tkinter as tk
from menubar import menubar
from tkcalendar import Calendar

def agg_contribuyentes(window, menu, last_window):

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)


    for widget in window.winfo_children():
        widget.destroy()


    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)
    
    left_frame = ctk.CTkFrame(window, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    
    right_frame = ctk.CTkFrame(window, corner_radius=15)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    #Contenido del frame top

    
    contribuyentes = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: contribuyentes(window, menu), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestion Contribuyentes", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    ################################################################ Contenido del left frame
    # Frames entrys    
    nombre_frame = ctk.CTkFrame(left_frame)
    nombre_frame.pack(padx=10, pady=5, fill="x")
    
    apellido_frame = ctk.CTkFrame(left_frame)
    apellido_frame.pack(padx=10, pady=5, fill="x")

    cedula_frame = ctk.CTkFrame(left_frame)
    cedula_frame.pack(padx=10, pady=5, fill="x")
    
    rif_frame = ctk.CTkFrame(left_frame)
    rif_frame.pack(padx=10, pady=5, fill="x")
    
    telefono_frame = ctk.CTkFrame(left_frame)
    telefono_frame.pack(padx=10, pady=5,fill="x")
    
    correo_frame = ctk.CTkFrame(left_frame)
    correo_frame.pack(padx=10, pady=5,fill="x")
    
    # Entrys del frame contribuyente

    nombre = ctk.CTkEntry(nombre_frame, placeholder_text="Nombre", font=poppins14bold, width=380)
    nombre.pack(pady=5, padx=5, side="left")

    apellido = ctk.CTkEntry(apellido_frame, placeholder_text="Apellido", font=poppins14bold, width=380)
    apellido.pack(pady=5, padx=5, side="left")

    cedula_values = ["V","E"]    
    cedula_indicator = ctk.CTkOptionMenu(cedula_frame, values=cedula_values, width=56, font=poppins14bold)
    cedula_indicator.pack(padx=5, pady=5, side="left")

    cedula = ctk.CTkEntry(cedula_frame, placeholder_text="Cedula de Identidad", font=poppins14bold, width=380)
    cedula.pack(pady=5, padx=5, side="left")

    
    rif_values = ["J","C","G"]    
    rif_indicator = ctk.CTkOptionMenu(rif_frame, values=rif_values, width=56, font=poppins14bold)
    rif_indicator.pack(padx=5, pady=5, side="left")

    rif = ctk.CTkEntry(rif_frame, placeholder_text="RIF", font=poppins14bold, width=380)
    rif.pack(pady=5, padx=5, side="left")

    telefono_values = ["0424", "0416", "0412", "0426", "0414"]    
    telefono_indicator = ctk.CTkOptionMenu(telefono_frame, values=telefono_values, width=56, font=poppins14bold)
    telefono_indicator.pack(padx=5, pady=5, side="left")

    telefono = ctk.CTkEntry(telefono_frame, placeholder_text="Telefono", font=poppins14bold, width=380)
    telefono.pack(pady=5, padx=5, side="left")
    
    correo = ctk.CTkEntry(correo_frame, placeholder_text="ejemplo@gmail.com", font=poppins14bold, width=380)
    correo.pack(pady=5, padx=5, side="left")

    ################################################################ Contenido del left frame
