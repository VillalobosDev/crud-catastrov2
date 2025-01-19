import customtkinter as ctk
from modulos.menubar import menubar
from functions.functions import * 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from functions.rectangle import rectangle
from PIL import ImageTk, Image
import sys
import os
import shutil
from tkinter import filedialog



def create_image_folder():
    image_folder = "images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    return image_folder

def cargar_imagen(frameimg, img_label1):
    global image_path  # Hacer la variable global para acceder a ella en guardar_datos
    file_path = filedialog.askopenfilename()
    if file_path:
        img_label1.destroy()
        image = Image.open(file_path)
        image = image.resize((260, 260), Image.LANCZOS)
        image_path = file_path  # Guardar la ruta original de la imagen
        
        image_tk = ctk.CTkImage(light_image=image, dark_image=image, size=(260, 260))
        
        img_label = ctk.CTkLabel(frameimg, image=image_tk, text="")
        img_label.pack(expand=True, padx=10, pady=10)
        img_label.image = image_tk  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
        
def ifasignar(bottom_frame, window, last_window, busqueda, busquedabtn):
    busqueda.destroy()
    busquedabtn.destroy()
    global center_frame, image_path  # Definir image_path como variable global
    image_path = ""  # Inicializar image_path

    poppins14bold = ("Poppins", 14, "bold")
    poppins18bold = ("Poppins", 18, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins12 = ("Poppins", 12)

    for widget in bottom_frame.winfo_children():
        widget.destroy()
      
    # Contenido del bottom frame
    left_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both")

    center_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    center_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)
    
    right_frame_bajo = ctk.CTkFrame(bottom_frame, corner_radius=15)
    right_frame_bajo.pack(side="right", padx=10, pady=10, fill="both")    

    text = ctk.CTkLabel(left_frame, text="Nuevo Sector", font=poppins18bold, width=250)
    text.pack(padx=10, pady=10)    
  
    nom_sectores_frame = ctk.CTkFrame(left_frame)
    nom_sectores_frame.pack(padx=10, pady=5, fill="x")    

    cod_sectores_frame = ctk.CTkFrame(left_frame)
    cod_sectores_frame.pack(padx=10, pady=5, fill="x")
    
    img_sectores_frame = ctk.CTkFrame(center_frame, width=260, height=260, corner_radius=15)
    img_sectores_frame.pack(pady=50)
    img_sectores_frame.pack_propagate(False)
    
    img_label1 = ctk.CTkLabel(img_sectores_frame, text="Insertar Imagen", font=poppins14bold, width=240, height=240)
    img_label1.place(x=10, y=10)    
    
    nom_sectores = ctk.CTkEntry(nom_sectores_frame, placeholder_text="Nombre del Sector", font=poppins14bold, width=250)
    nom_sectores.pack(pady=5, padx=5, side="left")
    
    cod_sectores = ctk.CTkEntry(cod_sectores_frame, placeholder_text="Codigo del Sector", font=poppins14bold, width=250)
    cod_sectores.pack(pady=5, padx=5, side="left")

    def cargar_imagen(img_frame, img_label):
        global image_path  # Usar la variable global image_path
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            img_label.destroy()
            image = Image.open(image_path)
            image = image.resize((260, 260), Image.LANCZOS)
            image_tk = ctk.CTkImage(light_image=image, dark_image=image, size=(260, 260))
            img_label = ctk.CTkLabel(img_frame, image=image_tk, text="")
            img_label.pack(expand=True, padx=10, pady=10)
            img_label.image = image_tk  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector

    btncargar = ctk.CTkButton(center_frame, text="Buscar", command=lambda: cargar_imagen(img_sectores_frame, img_label1), font=poppins14bold)
    btncargar.pack(padx=30, pady=10)
    
    def guardar_datos():
        global center_frame, image_path  # Usar la variable global image_path
        nombre = nom_sectores.get()
        codigo = cod_sectores.get()
        
        if not nombre or not codigo:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            return
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                # Verificar si el código ya existe
                cursor.execute('SELECT COUNT(*) FROM sectores WHERE cod_sector = ?', (codigo,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showwarning("Advertencia", "El código del sector ya existe.")
                else:
                    # Asignar ruta predeterminada si no se selecciona ninguna imagen
                    if not image_path:
                        image_path = "assets/default.png"
                    
                    # Guardar la ruta de la imagen directamente en la base de datos
                    sql = 'INSERT INTO sectores (nom_sector, cod_sector, image_path) VALUES (?, ?, ?)'
                    cursor.execute(sql, (nombre, codigo, image_path))
                    conn.commit()

                    print("Datos guardados exitosamente.")
                    messagebox.showinfo("Información", "Datos guardados exitosamente.")
                    
                    nom_sectores.delete(0, tk.END)
                    cod_sectores.delete(0, tk.END)
                    
                    # Recargar el frame de center_frame
                    center_frame.destroy()
                    center_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
                    center_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)
                    
                    img_sectores_frame = ctk.CTkFrame(center_frame, width=260, height=260, corner_radius=15)
                    img_sectores_frame.pack(pady=50)
                    img_sectores_frame.pack_propagate(False)
                    img_label1 = ctk.CTkLabel(img_sectores_frame, text="Insertar Imagen", font=poppins14bold, width=240, height=240)
                    img_label1.place(x=10, y=10)
                    
                    btncargar = ctk.CTkButton(center_frame, text="Cargar", command=lambda: cargar_imagen(img_sectores_frame, img_label1), font=poppins14bold)
                    btncargar.pack(padx=30, pady=10) 
                    
                    # Actualizar el Treeview
                    my_tree.insert("", "end", values=(nombre, codigo))
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    btnsave = ctk.CTkButton(left_frame, text="Guardar", command=guardar_datos, font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    btnvolver = ctk.CTkButton(left_frame, text="Atrás", command=lambda: sectores(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    # Creando el treeview para mostrar los registros
    
    frame_tree = ctk.CTkFrame(right_frame_bajo, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ('Nombre sector', 'Codigo del sector')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    
    loaddata(my_tree)

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
    crear = ctk.CTkButton(top_frame2, text="Agregar", command=lambda: ifasignar(bottom_frame, window, last_window, busqueda, busquedabtn), font=poppins14bold)
    crear.pack(padx=5, pady=5, side="left")

    gestionar = ctk.CTkButton(top_frame2, text="Modificar", command=lambda: ifgestionar(bottom_frame, window, last_window, busqueda, busquedabtn), font=poppins14bold)
    gestionar.pack(padx=5, pady=5, side="left")
    
    
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

    inmuebles_tree['columns'] = ('Nombre inmueble', 'Codigo catastral', 'Uso')
    for col in inmuebles_tree['columns']:
        inmuebles_tree.heading(col, text=col.capitalize(), anchor='center')
        inmuebles_tree.column(col, anchor='center')

    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nom_inmueble, cod_catastral, uso 
                FROM inmuebles 
                WHERE id_sector = ?
            """, (sector_id,))
            results = cursor.fetchall()
            for row in results:
                inmuebles_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error loading inmuebles: {e}")

def ifgestionar(bottom_frame, window, last_window, busqueda, busquedabtn):
    global image_save_path, id_sector, center_frame
    image_save_path = ""  # Inicializar image_save_path
    id_sector = None  # Inicializar id_sector
    busqueda.destroy()
    busquedabtn.destroy()
    
    

    poppins14bold = ("Poppins", 14, "bold")
    poppins18bold = ("Poppins", 18, "bold")
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins12 = ("Poppins", 12)

    for widget in bottom_frame.winfo_children():
        widget.destroy()
      
    # Contenido del bottom frame
    left_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both")

    center_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    center_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)
    
    right_frame_bajo = ctk.CTkFrame(bottom_frame, corner_radius=15)
    right_frame_bajo.pack(side="right", padx=10, pady=10, fill="both")    

    text = ctk.CTkLabel(left_frame, text="Modificar Sector", font=poppins18bold, width=250)
    text.pack(padx=10, pady=10)    
  
    nom_sectores_frame = ctk.CTkFrame(left_frame)
    nom_sectores_frame.pack(padx=10, pady=5, fill="x")    

    cod_sectores_frame = ctk.CTkFrame(left_frame)
    cod_sectores_frame.pack(padx=10, pady=5, fill="x")
    
    img_sectores_frame = ctk.CTkFrame(center_frame, width=260, height=260, corner_radius=15)
    img_sectores_frame.pack(pady=50)
    img_sectores_frame.pack_propagate(False)
    
    image_label = ctk.CTkLabel(img_sectores_frame, text="Cambiar Imagen", font=poppins14bold)
    image_label.pack(expand=True, padx=10, pady=10)   
    
    nom_sectores = ctk.CTkEntry(nom_sectores_frame, placeholder_text="Selecciona un Sector", font=poppins14bold, width=250)
    nom_sectores.pack(pady=5, padx=5, side="left")
    
    cod_sectores = ctk.CTkEntry(cod_sectores_frame, placeholder_text="-", font=poppins14bold, width=250)
    cod_sectores.pack(pady=5, padx=5, side="left")

    def cambiar_imagen():
        global image_save_path  # Usar la variable global image_save_path
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            sector_code = item['values'][1]
            new_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
            if new_image_path:
                try:
                    # Guardar la ruta de la nueva imagen seleccionada
                    image_save_path = new_image_path
                    
                    # Actualizar la imagen en la interfaz
                    image = Image.open(image_save_path)
                    image = image.resize((250, 250), Image.LANCZOS)
                    photo = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))
                    image_label.configure(image=photo, text="")
                    image_label.image = photo
                except Exception as e:
                    print(f"Error al cambiar la imagen: {e}")

    btncargar = ctk.CTkButton(center_frame, text="Buscar", command=cambiar_imagen, font=poppins14bold)
    btncargar.pack(padx=30, pady=10)

    def guardar_datos():
        global image_save_path, id_sector  # Usar las variables globales image_save_path y id_sector
        nombre = nom_sectores.get()
        codigo = cod_sectores.get()
        
        if not nombre or not codigo:
            return
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                # Obtener la ruta de la imagen anterior
                cursor.execute("SELECT image_path FROM sectores WHERE id_sector = ?", (id_sector,))
                old_image_path = cursor.fetchone()[0]
                
                # Si no se seleccionó una nueva imagen, mantener la ruta de la imagen anterior
                if not image_save_path:
                    image_save_path = old_image_path
                
                # Mover la nueva imagen a la carpeta "images"
                if image_save_path and image_save_path != old_image_path:
                    image_folder = "images"
                    if not os.path.exists(image_folder):
                        os.makedirs(image_folder)
                    new_image_name = os.path.basename(image_save_path)
                    new_image_path = os.path.join(image_folder, new_image_name)
                    shutil.copy(image_save_path, new_image_path)
                    image_save_path = new_image_path
                
                # Actualizar el sector existente
                sql = 'UPDATE sectores SET nom_sector = ?, cod_sector = ?, image_path = ? WHERE id_sector = ?'
                cursor.execute(sql, (nombre, codigo, image_save_path, id_sector))
                conn.commit()
                print("Datos actualizados exitosamente.")
                messagebox.showinfo("Información", "Datos actualizados exitosamente.")
                
                # Actualizar el Treeview
                selected_item = my_tree.selection()[0]
                my_tree.item(selected_item, values=(id_sector, nombre, codigo))
                
                # Eliminar la imagen anterior si es diferente de la nueva y no es default.png
                if old_image_path and old_image_path != image_save_path and os.path.exists(old_image_path) and "assets/default.png" not in old_image_path:
                    os.remove(old_image_path)
                    print("Imagen anterior eliminada exitosamente.")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def eliminar_datos():
        global id_sector, center_frame  # Usar las variables globales id_sector y center_frame
        selected_item = my_tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este sector?")
            if confirm:
                try:
                    with connection() as conn:
                        cursor = conn.cursor()
                        # Obtener la ruta de la imagen antes de eliminar el registro
                        cursor.execute("SELECT image_path FROM sectores WHERE id_sector = ?", (id_sector,))
                        image_path = cursor.fetchone()[0]
                        
                        # Eliminar el sector de la base de datos
                        sql = 'DELETE FROM sectores WHERE id_sector = ?'
                        cursor.execute(sql, (id_sector,))
                        conn.commit()
                        print("Datos eliminados exitosamente.")
                        
                        # Eliminar el sector del Treeview
                        my_tree.delete(selected_item)
                        
                        # Eliminar la imagen del sistema de archivos
                        if image_path and os.path.exists(image_path) and "assets/default.png" not in image_path:
                            os.remove(image_path)
                            print("Imagen eliminada exitosamente.")
                        
                        # Limpiar los campos de entrada y la imagen
                        nom_sectores.delete(0, tk.END)
                        cod_sectores.delete(0, tk.END)
                        
                        
                except Exception as e:
                    print(f"Error al eliminar los datos: {e}")
                    
                    
                    
    btnsave = ctk.CTkButton(left_frame, text="Guardar", command=guardar_datos, font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    btneliminar = ctk.CTkButton(left_frame, text="Eliminar", command=eliminar_datos, font=poppins14bold)
    btneliminar.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    btnvolver = ctk.CTkButton(left_frame, text="Atrás", command=lambda: sectores(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    # Creando el treeview para mostrar los registros
    
    frame_tree = ctk.CTkFrame(right_frame_bajo, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ('ID', 'Nombre sector', 'Codigo del sector')

    # Ocultar la columna ID
    my_tree.column('ID', width=0, stretch=tk.NO)
    my_tree.heading('ID', text='', anchor='center')
    
    for col in my_tree['columns'][1:]:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')
  

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    
    def on_tree_select(event):
        global id_sector  # Usar la variable global id_sector
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            id_sector = item['values'][0]
            sector_name = item['values'][1]
            sector_code = item['values'][2]
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT image_path FROM sectores WHERE id_sector = ?", (id_sector,))
                    image_path = cursor.fetchone()[0]
                    if image_path and os.path.exists(image_path):
                        image = Image.open(image_path)
                    else:
                        print(f"Image not found: {image_path}, loading default image.")
                        image = Image.open("images/default.jpg")
                    
                    image = image.resize((260, 260), Image.LANCZOS)
                    photo = ctk.CTkImage(light_image=image, dark_image=image, size=(260, 260))
                    image_label.configure(image=photo, text="")
                    image_label.image = photo
                    
                    # Actualizar los campos de entrada con los datos del sector
                    nom_sectores.delete(0, tk.END)
                    nom_sectores.insert(0, sector_name)
                    cod_sectores.delete(0, tk.END)
                    cod_sectores.insert(0, sector_code)

            except Exception as e:
                print(f"Error loading image: {e}")

    my_tree.bind("<<TreeviewSelect>>", on_tree_select)

    loaddata(my_tree)

        
        
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