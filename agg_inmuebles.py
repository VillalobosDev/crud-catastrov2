import customtkinter as ctk
import tkinter as tk
from menubar import menubar
from tkcalendar import Calendar

def agg_inmuebles(window, menu, last_window):

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

    
    inmuebles = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: inmuebles(window, menu), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Sección de Agregar Inmuebles", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    ################################################################ Contenido del left frame
    # Frames entrys    
    nombreinm_frame = ctk.CTkFrame(left_frame)
    nombreinm_frame.pack(padx=10, pady=5, fill="x")
    
    codcatastral_frame = ctk.CTkFrame(left_frame)
    codcatastral_frame.pack(padx=10, pady=5, fill="x")

    cedula_frame = ctk.CTkFrame(left_frame)
    cedula_frame.pack(padx=10, pady=5, fill="x")
    
    sector_frame = ctk.CTkFrame(left_frame)
    sector_frame.pack(padx=10, pady=5, fill="x")
    
    uso_frame = ctk.CTkFrame(left_frame)
    uso_frame.pack(padx=10, pady=5,fill="x")
        
    # Entrys del frame contribuyente

    nombreinm = ctk.CTkEntry(nombreinm_frame, placeholder_text="Nombre", font=poppins14bold, width=380)
    nombreinm.pack(pady=5, padx=5, side="left")

    codcatastral = ctk.CTkEntry(codcatastral_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=380)
    codcatastral.pack(pady=5, padx=5, side="left")

    cedulacont = ctk.CTkEntry(cedula_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold, width=380)
    cedulacont.pack(pady=5, padx=5, side="left")

    sector_values = ["SectorValues"] #Dinamic values
    sector = ctk.CTkOptionMenu(sector_frame, values=sector_values, width=200, font=poppins14bold)
    sector.pack(padx=5, pady=5, side="left")

    uso_values = ["Residencial", "Comercial"]
    uso = ctk.CTkOptionMenu(uso_frame, values=uso_values, font=poppins14bold, width=200)
    uso.pack(padx=5, pady=5, side="left")

    ################################################################ Contenido del left frame
