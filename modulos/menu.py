import customtkinter as ctk
import tkinter as tk
from modulos.menubar import menubar
from modulos.contribuyentes import contribuyentes
from modulos.inmuebles import inmuebles
from modulos.liquidacion import liquidacion
from modulos.consulta_general import consulta
from modulos.sectores import sectores
from PIL import Image, ImageTk



def cargar_imagen_alcaldia(frame):
    try:
        # Cargar la imagen desde la carpeta assets
        imagen = Image.open("assets/alcaldia_claro.png")
        imagendark = Image.open("assets/alcaldia_oscuro.png")

        imagen_tk = ctk.CTkImage(light_image=imagen, dark_image=imagendark, size=(400,400))

        # Crear un Label para mostrar la imagen
        label_imagen = ctk.CTkLabel(frame, image=imagen_tk, text="")
        label_imagen.image = imagen_tk  # Guardar una referencia de la imagen para evitar que sea recolectada por el garbage collector
        label_imagen.pack(pady=100, anchor="center")

    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

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

    left_frame = ctk.CTkFrame(window, corner_radius=15)
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
    contribuyente_btn.pack(pady=30, padx=50, anchor="center", expand=True)

    inmuebles_btn = ctk.CTkButton(left_frame, text="Inmuebles", command=lambda: inmuebles(window, menu), width=190, font=poppins20bold)
    inmuebles_btn.pack(pady=30, padx=50, anchor="center", expand=True)

    liquidacion_btn = ctk.CTkButton(left_frame, text="Liquidación", command=lambda: liquidacion(window, menu), width=190, font=poppins20bold)
    liquidacion_btn.pack(pady=30, padx=50, anchor="center", expand=True)
    
    sector_btn = ctk.CTkButton(left_frame, text="Sectores", command=lambda: sectores(window, menu), width=190, font=poppins20bold)
    sector_btn.pack(pady=30, padx=50, anchor="center", expand=True)    
    
    consulta_btn = ctk.CTkButton(left_frame, text="Consultar", command=lambda: consulta(window, menu), width=190, font=poppins20bold)
    consulta_btn.pack(pady=30, padx=50, anchor="center", expand=True)
    
    
    #frame right
    cargar_imagen_alcaldia(right_frame)
    

 # Define main window
