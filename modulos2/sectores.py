import customtkinter as ctk
from modulos2.menubar import menubar
from functions.functions import * 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from functions.rectangle import rectangle
from PIL import ImageTk, Image
import sys
import os
import shutil
from tkinter import filedialog


def sectores(window, last_window):
    for widget in window.winfo_children():
        widget.destroy()

    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)
    
    menubar(window)
    
    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)

    top_frame2 = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame2.pack(fill="x", padx=10)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    # Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Gestión de Sectores", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    # Contenido del top frame 2

    
    
    recargarbusqueda = ctk.CTkButton(top_frame2, text="🔁", font=poppins14bold, width=30, command=lambda: loaddata(my_tree))
    recargarbusqueda.pack(padx=5, pady=5, side="right")
    
    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busqueda))
    busquedabtn.pack(padx=5, pady=5, side="right")
    
    busqueda = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por codigo", font=poppins14bold, width=200)
    busqueda.pack(padx=5, pady=5, side="right")

    # Contenido del bottom frame
    right_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
    right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    # Frame para la imagen
    image_frame = ctk.CTkFrame(right_frame, width=330, height=330, corner_radius=15)
    image_frame.pack(pady=60)
    image_frame.pack_propagate(False)  # Evita que el frame cambie de tamaño

    image_label = ctk.CTkLabel(image_frame, text="Selecciona un sector para continuar", font=poppins14bold)
    image_label.pack(expand=True, padx=10, pady=10)
    
    left_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)    
    
    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(left_frame, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    

    my_tree['columns'] = ('ID', 'Nombre sector', 'Codigo del sector')
    
    # Ocultar la columna ID
    my_tree.column('ID', width=0, stretch=tk.NO)
    my_tree.heading('ID', text='', anchor='center')
    
    for col in my_tree['columns'][1:]:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    def on_tree_select(event):
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            sector_id = item['values'][0]
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT image_path FROM sectores WHERE id_sector = ?", (sector_id,))
                    image_path = cursor.fetchone()[0]
                    if image_path and os.path.exists(image_path):
                        image = Image.open(image_path)
                    else:
                        print(f"Image not found: {image_path}")
                        image = Image.open("assets/default.jpg")
                        
                    image = image.resize((300, 300), Image.LANCZOS)
                    photo =  ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300))
                    image_label.configure(image=photo, text="")
                    image_label.image = photo
                    
            except Exception as e:
                print(f"Error loading image: {e}")

    my_tree.bind("<<TreeviewSelect>>", on_tree_select)

    loaddata(my_tree)



    def confirmar():
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            sector_id = item['values'][0]
            for widget in left_frame.winfo_children():
                widget.destroy()
            crear_arbol_inmuebles(left_frame, sector_id)
            confirmar_btn.destroy()
            volver_btn = ctk.CTkButton(right_frame, text="Volver", font=poppins14bold, command=lambda: sectores(window, last_window))
            volver_btn.pack(pady=0)

    confirmar_btn = ctk.CTkButton(right_frame, text="Confirmar", font=poppins14bold, command=confirmar)
    confirmar_btn.pack(pady=0)
    
def crear_arbol_inmuebles(parent_frame, sector_id):
    frame_tree = ctk.CTkFrame(parent_frame, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    inmuebles_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    inmuebles_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=inmuebles_tree.xview)
    inmuebles_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    inmuebles_tree['columns'] = ('Ubicación', 'Codigo catastral', 'Uso')
    for col in inmuebles_tree['columns']:
        inmuebles_tree.heading(col, text=col.capitalize(), anchor='center')
        inmuebles_tree.column(col, anchor='center')

    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ubicacion, cod_catastral, uso 
                FROM inmuebles 
                WHERE id_sector = ?
            """, (sector_id,))
            results = cursor.fetchall()
            for row in results:
                inmuebles_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error loading inmuebles: {e}")
        
        
        
def reload_treeviewsearch(my_tree, busqueda):
    busqueda = busqueda.get()
    if not busqueda:
        messagebox.showwarning("Advertencia", "Por favor ingrese un codigo de sector para buscar.")
        loaddata(my_tree)
        return
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = 'SELECT id_sector, nom_sector, cod_sector FROM sectores WHERE cod_sector = ?'
            cursor.execute(sql, (busqueda,))
            results = cursor.fetchall()

            # Clear existing rows
            for row in my_tree.get_children():
                my_tree.delete(row)

            if not results:
                messagebox.showerror("Error", "No se ha encontrado el código del sector.")
                loaddata(my_tree)
                return

            # Insert updated rows
            for row in results:
                my_tree.insert("", "end", iid=row[0], values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")

def loaddata(my_tree):
    try:
        with connection() as conn:
            print("Database connection established.")
            cursor = conn.cursor()
            sql = 'SELECT id_sector, nom_sector, cod_sector FROM sectores'
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Query executed successfully, fetched results: {results}")

            # Clear existing rows
            for row in my_tree.get_children():
                my_tree.delete(row)

            # Ensure data fits Treeview structure
            for row in results:
                my_tree.insert("", "end", values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")