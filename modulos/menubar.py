import customtkinter as ctk
import tkinter as tk
from PIL import Image
from modulos.transitions import transition_to_next_ui
from config.config_temas import open_config_window
from config.config import centrar_ventana
import json




def cargar_imagen_uni(frame):
    try:
        # Cargar la imagen desde la carpeta assets
        imagen = Image.open("assets/uni_claro.png")
        imagendark = Image.open("assets/uni_oscuro.png")

        imagen_tk = ctk.CTkImage(light_image=imagen, dark_image=imagendark, size=(300,300))

        # Crear un Label para mostrar la imagen
        label_imagen = ctk.CTkLabel(frame, image=imagen_tk, text="")
        label_imagen.image = imagen_tk  # Guardar una referencia de la imagen para evitar que sea recolectada por el garbage collector
        label_imagen.pack(pady=30, padx=45, side="right")

    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

def set_menu_bar_color(menubar_frame, mode, menu_button, config_button, support_button, exit_button, window):
    if mode == "light":
        
        menubar_frame.configure(fg_color="#f3f3f3")  # Color blanco para modo claro
        menu_button.configure(fg_color="#f3f3f3", text_color="black")
        config_button.configure(fg_color="#f3f3f3", text_color="black")
        support_button.configure(fg_color="#f3f3f3", text_color="black")
        exit_button.configure(fg_color="#f3f3f3", text_color="black")
    else:
        menubar_frame.configure(fg_color="#202020")  # Color oscuro para otros modos
        menu_button.configure(fg_color="#202020", text_color="white")
        config_button.configure(fg_color="#202020", text_color="white")
        support_button.configure(fg_color="#202020", text_color="white")
        exit_button.configure(fg_color="#202020", text_color="white")

def get_mode_from_config():
    with open('config/config.json', 'r') as file:
        config = json.load(file)
        theme = config.get("theme", "Dark")
        if theme.lower() == "light":
            return "light"
        else:
            return "dark"

# Function to create the toolbar menu
def menubar(window):
    poppins12bold = ("Poppins", 12, "bold")
    fg = "#202020"
    fg2 = "#d10000"

    # Obtener el modo del archivo de configuración
    mode = get_mode_from_config()

    # Crear el marco superior que simula el menubar
    menubar_frame = ctk.CTkFrame(window, height=30, corner_radius=0, fg_color=fg)
    menubar_frame.pack(fill="x", side="top")

    # Botón "Menu"
    menu_button = ctk.CTkButton(menubar_frame, text="Creditos", font=poppins12bold, width=100, hover_color="gray", command=lambda: creditos(window))
    menu_button.pack(side="left", padx=5, pady=5)

    # Botón "Configuracion"
    config_button = ctk.CTkButton(menubar_frame, text="Configuracion", font=poppins12bold, width=120, hover_color="gray",  command=lambda: open_config_window(window))
    config_button.pack(side="left", padx=5, pady=5)

    # Botón "Soporte"
    support_button = ctk.CTkButton(menubar_frame, text="Soporte", font=poppins12bold, width=100, hover_color="gray", command=lambda: soporte(window))
    support_button.pack(side="left", padx=5, pady=5)

    # Botón "Salir"
    exit_button = ctk.CTkButton(menubar_frame, text="Cerrar sesión", font=poppins12bold, width=100, hover_color="darkred", command=lambda: logout_and_login(window))
    exit_button.pack(side="right", padx=5, pady=5)



    def logout_and_login(current_window):
        from modulos.login_fun import login

        # Cerrar la ventana actual
        current_window.destroy()

        # Crear una nueva ventana
        window = ctk.CTk()
        window.title("Axio")
        window.geometry("1000x600")
        window.resizable(False, False)
        window.iconbitmap(r"C:/Github/crud-catastrov2/assets/axiow.ico")
        centrar_ventana(window, 1000, 600)

        # Llamar a la función login con la nueva ventana
        login(window)
        window.mainloop()

    set_menu_bar_color(menubar_frame, mode, menu_button, config_button, support_button, exit_button, window)
  
def creditos(parent):
    poppins16 = ("Poppins", 16, "bold")
    poppins12bold = ("Poppins", 12, "bold")
    poppins10bold = ("Poppins", 10, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    
    config_window = ctk.CTkToplevel(parent)
    config_window.title("Creditos")
    config_window.geometry("700x400")
    config_window.grab_set()
    config_window.resizable(False, False)
    centrar_ventana(config_window, 700, 400)

    left_frame = ctk.CTkFrame(config_window, corner_radius=15)
    left_frame.pack(fill="y", side="left", pady=5, padx=5)
    
    atras_button = ctk.CTkButton(config_window, text="Atrás", command=config_window.destroy, font=poppins12bold)
    atras_button.pack(padx=10, pady=10, side="bottom", anchor="e") 
    
    cargar_imagen_uni(config_window)   
    
    
    top = ctk.CTkLabel(left_frame, text="Desarrolladadores:", font=poppins16)
    top.pack(pady=30, padx=70, side="top", anchor="w")

    # Dimensiones uniformes para los frames
    frame_width = 300
    frame_height = 60

    frame = ctk.CTkFrame(left_frame, corner_radius=15, width=frame_width, height=frame_height)
    frame.pack(pady=5, padx=5, side="top", anchor="w", fill="y")
    frame.pack_propagate(False)

    frame2 = ctk.CTkFrame(left_frame, corner_radius=15, width=frame_width, height=frame_height)
    frame2.pack(pady=5, padx=5, side="top", anchor="w")
    frame2.pack_propagate(False)

    frame3 = ctk.CTkFrame(left_frame, corner_radius=15, width=frame_width, height=frame_height)
    frame3.pack(pady=5, padx=5, side="top", anchor="w")
    frame3.pack_propagate(False)

    nombre1 = ctk.CTkLabel(frame, text="Nelson Villalobos CI:31.675.830", font=poppins14bold)
    nombre1.pack(pady=10, padx=10)

    nombre2 = ctk.CTkLabel(frame2, text="Cristhian Bracho  CI:31.625.272", font=poppins14bold)
    nombre2.pack(pady=10, padx=10)

    nombre3 = ctk.CTkLabel(frame3, text="José Lanz CI:31.760.396", font=poppins14bold)
    nombre3.pack(pady=10, padx=10)
    
    nombre4 = ctk.CTkLabel(left_frame, text="Hecho en Python y CustomTkinter :)", font=poppins10bold)
    nombre4.pack(pady=5, padx=20, side="left", anchor="s")



def soporte(parent):
    poppins16 = ("Poppins", 16, "bold")
    poppins12bold = ("Poppins", 12, "bold")
    poppins10bold = ("Poppins", 10, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    
    sopor_window = ctk.CTkToplevel(parent)
    sopor_window.title("Soporte")
    sopor_window.geometry("700x400")
    sopor_window.grab_set()
    sopor_window.resizable(False, False)
    centrar_ventana(sopor_window, 700, 400)
    

    
    
    left_frame = ctk.CTkFrame(sopor_window, corner_radius=15, width=300, height=400)
    left_frame.pack(side="left", pady=5, padx=5)
    left_frame.pack_propagate(False)
    
    botonatras=ctk.CTkButton(sopor_window, text="Atrás", font=poppins12bold, command=sopor_window.destroy)
    botonatras.pack(pady=10, padx=10, side="bottom", anchor="e")  
    
      
    text_top=ctk.CTkLabel(left_frame, text="Contactos", font=poppins16)
    text_top.pack(pady=10, padx=10)
    
    text_con=ctk.CTkLabel(left_frame, text="• Correo: Axio@gmail.com", font=poppins14bold)
    text_con.pack(pady=10, padx=10, anchor="w")
    
    text_con2=ctk.CTkLabel(left_frame, text="• Número: 0424-9691-737", font=poppins14bold)
    text_con2.pack(pady=10, padx=10, anchor="w")
    
    
    right_frame=ctk.CTkFrame(sopor_window, corner_radius=15, width=400, height=165)
    right_frame.pack(anchor="ne", pady=5, padx=5)
    right_frame.pack_propagate(False)
    
    manual_user=ctk.CTkButton(right_frame, text="Manual de Usuario", font=poppins12bold, command=abrir_manual_usuario)
    manual_user.pack(anchor="center", pady=65)
    
    right_frame2=ctk.CTkFrame(sopor_window, corner_radius=15, width=400, height=165)
    right_frame2.pack(anchor="se", pady=5, padx=5)
    right_frame2.pack_propagate(False)
    
    manual_user2=ctk.CTkButton(right_frame2, text="Manual de Sistema", font=poppins12bold)
    manual_user2.pack(anchor="center", pady=65)
    
import os
import webbrowser

def abrir_manual_usuario():
    # Obtener la ruta absoluta del archivo PDF basado en la ubicación del script actual
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_pdf = os.path.join(ruta_base, "../assets/manual_usuario.pdf")
    ruta_pdf = os.path.abspath(ruta_pdf)  # Convertir a ruta absoluta

    # Abrir el archivo PDF en el navegador
    webbrowser.open(f"file:///{ruta_pdf}")
    









