import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from menubar import menubar
from tkcalendar import Calendar
from rectangle import rectangle
from functions import *

def contribuyentes_gestion(window, menu, last_window):

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
    left_frame.pack(side="left", padx=10, pady=10, fill="y")
    
    right_frame = ctk.CTkFrame(window, corner_radius=15)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    #Contenido del frame top

    
    contribuyentes = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: contribuyentes(window, menu), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestion Contribuyentes", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")




    

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 
    
    
    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(right_frame, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ( 'nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    
    with connection() as conn:
        cursor = conn.cursor()
        sql = '''
        SELECT * FROM contribuyentes  
        '''
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            results[0] = results[0][1:]
        print(results)
        refreshTable(my_tree, results)




