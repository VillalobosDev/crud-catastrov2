import customtkinter as ctk
import tkinter as tk
from menubar import menubar
from functions import * 
from tkinter import ttk
from rectangle import rectangle





def ifagregar(bottom_frame):
    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")
    
    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    # Contenido del frame left
    nombre_frame = ctk.CTkFrame(frame_left)
    nombre_frame.pack(padx=10, pady=5, fill="x")

    apellido_frame = ctk.CTkFrame(frame_left)
    apellido_frame.pack(padx=10, pady=5, fill="x")

    cedula_frame = ctk.CTkFrame(frame_left)
    cedula_frame.pack(padx=10, pady=5, fill="x")
    
    rif_frame = ctk.CTkFrame(frame_left)
    rif_frame.pack(padx=10, pady=5, fill="x")
    
    telefono_frame = ctk.CTkFrame(frame_left)
    telefono_frame.pack(padx=10, pady=5, fill="x")
    
    correo_frame = ctk.CTkFrame(frame_left)
    correo_frame.pack(padx=10, pady=5, fill="x")
    
    # Entrys del frame contribuyente
    nombre = ctk.CTkEntry(nombre_frame, placeholder_text="Nombre", font=poppins14bold, width=250)
    nombre.pack(pady=5, padx=5, side="left")

    apellido = ctk.CTkEntry(apellido_frame, placeholder_text="Apellido", font=poppins14bold, width=250)
    apellido.pack(pady=5, padx=5, side="left")

    cedula_values = ["V", "E"]    
    cedula_indicator = ctk.CTkOptionMenu(cedula_frame, values=cedula_values, width=50, font=poppins14bold)
    cedula_indicator.pack(padx=5, pady=5, side="left")

    cedula = ctk.CTkEntry(cedula_frame, placeholder_text="Cédula de Identidad", font=poppins14bold, width=190)
    cedula.pack(pady=5, padx=5, side="left")

    rif_values = ["J", "C", "G"]    
    rif_indicator = ctk.CTkOptionMenu(rif_frame, values=rif_values, width=50, font=poppins14bold)
    rif_indicator.pack(padx=5, pady=5, side="left")

    rif = ctk.CTkEntry(rif_frame, placeholder_text="RIF", font=poppins14bold, width=190)
    rif.pack(pady=5, padx=5, side="left")

    telefono = ctk.CTkEntry(telefono_frame, placeholder_text="Teléfono", font=poppins14bold, width=250)
    telefono.pack(pady=5, padx=5, side="left")

    correo = ctk.CTkEntry(correo_frame, placeholder_text="ejemplo@gmail.com", font=poppins14bold, width=250)
    correo.pack(pady=5, padx=5, side="left")
    

    
    

    def cargar_datos():
        for item in my_tree.get_children():
            my_tree.delete(item)
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = 'SELECT nombres, apellidos, ci_contribuyente, rif, telefono, correo FROM contribuyentes'
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    my_tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Error during database operation: {e}")

    def guardar_datos():
        
        

        try:
            with connection() as conn:
                cursor = conn.cursor()
                cedula_completa = f"{cedula_indicator.get()}-{cedula.get()}"
                
                # Verificar si la cédula ya existe
                cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE ci_contribuyente = ?", (cedula_completa,))
                if cursor.fetchone()[0] > 0:
                    text = ctk.CTkLabel(frame_left, text="La cédula de identidad ya existe", text_color="red", font=poppins14bold)
                    text.place(x=20, y=430)
                    return
                
                sql = """INSERT INTO contribuyentes (nombres, apellidos, ci_contribuyente, rif, telefono, correo)
                        VALUES (?, ?, ?, ?, ?, ?)"""
                datos = (
                    nombre.get(),
                    apellido.get(),
                    cedula_completa,
                    f"{rif_indicator.get()}-{rif.get()}",
                    telefono.get(),
                    correo.get()
                )
                cursor.execute(sql, datos)
                conn.commit()                        
                text = ctk.CTkLabel(frame_left, text="Contribuyente agregado", text_color="green", font=poppins14bold,width=250)
                text.place(x=10, y=430)
                cargar_datos()  # Llamar a la función para actualizar el Treeview
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=guardar_datos, font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")
    

    # Contenido del RIGHT FRAME

    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(frame_right, fg_color='white')
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

    cargar_datos()  # Llamar a la función para cargar los datos inicialmente





        

   
    
def ifgestionar(bottom_frame):

    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    nombre_contribuyente_frame = ctk.CTkFrame(frame_left)
    nombre_contribuyente_frame.pack(padx=10, pady=5, fill="x")

    apellido_contribuyente_frame = ctk.CTkFrame(frame_left)
    apellido_contribuyente_frame.pack(padx=10, pady=5, fill="x")

    cedula_frame = ctk.CTkFrame(frame_left)
    cedula_frame.pack(padx=10, pady=5, fill="x")

    rif_frame = ctk.CTkFrame(frame_left)
    rif_frame.pack(padx=10, pady=5, fill="x")

    telefono_frame = ctk.CTkFrame(frame_left)
    telefono_frame.pack(padx=10, pady=5, fill="x")

    correo_frame = ctk.CTkFrame(frame_left)
    correo_frame.pack(padx=10, pady=5, anchor="w")

    nombre_contribuyente = ctk.CTkEntry(nombre_contribuyente_frame, placeholder_text="Nombre", font=poppins14bold, width=250)
    nombre_contribuyente.pack(pady=5, padx=5, side="left")

    apellido_contribuyente = ctk.CTkEntry(apellido_contribuyente_frame, placeholder_text="Apellido", font=poppins14bold, width=250)
    apellido_contribuyente.pack(pady=5, padx=5, side="left")

    correo = ctk.CTkEntry(correo_frame, placeholder_text="Correo", font=poppins14bold, width=250)
    correo.pack(pady=5, padx=5, side="left")

    cedula_values = ["V", "E"]
    cedula_indicator = ctk.CTkOptionMenu(cedula_frame, values=cedula_values, width=50, font=poppins14bold)
    cedula_indicator.pack(padx=5, pady=5, side="left")

    cedula = ctk.CTkEntry(cedula_frame, placeholder_text="Cédula de Identidad", font=poppins14bold, width=190)
    cedula.pack(pady=5, padx=5, side="left")

    rif_values = ["J", "C", "G"]
    rif_indicator = ctk.CTkOptionMenu(rif_frame, values=rif_values, width=50, font=poppins14bold)
    rif_indicator.pack(padx=5, pady=5, side="left")

    rif = ctk.CTkEntry(rif_frame, placeholder_text="RIF", font=poppins14bold, width=190)
    rif.pack(pady=5, padx=5, side="left")

    telefono = ctk.CTkEntry(telefono_frame, placeholder_text="Telefono", font=poppins14bold, width=250)
    telefono.pack(pady=5, padx=5, side="left")
    
    
    def cargar_datos():
        for item in my_tree.get_children():
            my_tree.delete(item)
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = 'SELECT nombres, apellidos, ci_contribuyente, rif, telefono, correo FROM contribuyentes'
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    my_tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Error during database operation: {e}")

    def save_changes():
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            values = item['values']
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    sql = '''UPDATE contribuyentes SET nombres=?, apellidos=?, ci_contribuyente=?, rif=?, telefono=?, correo=?
                             WHERE ci_contribuyente=?'''
                    cursor.execute(sql, (nombre_contribuyente.get(), apellido_contribuyente.get(), cedula.get(), rif.get(), telefono.get(), correo.get(), values[2]))
                    conn.commit()
                    text = ctk.CTkLabel(frame_left, text="Datos actualizados correctamente", text_color="green", font=poppins14bold,width=250)
                    text.place(x=10, y=430)
                    cargar_datos()
            except Exception as e:
                print(f"Error al actualizar datos: {e}")

    btnsave = ctk.CTkButton(frame_left, text="Actualizar", command=save_changes, font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    my_tree["columns"] = ('nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')
    for col in my_tree["columns"]:
        my_tree.heading(col, text=col.capitalize(), anchor="center")
        my_tree.column(col, anchor="center")
        
        
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")

    def on_tree_select(event):
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            values = item['values']
            nombre_contribuyente.delete(0, tk.END)
            nombre_contribuyente.insert(0, values[0])
            apellido_contribuyente.delete(0, tk.END)
            apellido_contribuyente.insert(0, values[1])
            cedula.delete(0, tk.END)
            cedula.insert(0, values[2])
            rif.delete(0, tk.END)
            rif.insert(0, values[3])
            telefono.delete(0, tk.END)
            telefono.insert(0, values[4])
            correo.delete(0, tk.END)
            correo.insert(0, values[5])
            text = ctk.CTkLabel(frame_left, text="", text_color="green", font=poppins14bold,width=270)
            text.place(x=0, y=430)

    my_tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Fetch data to populate Treeview
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = 'SELECT nombres, apellidos, ci_contribuyente, rif, telefono, correo FROM contribuyentes'
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error fetching data: {e}")


def contribuyentes(window, last_window):
    
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

    top_frame2 = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame2.pack(fill="x", padx=10)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    #Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Contribuyentes Catastrales", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    crearliq = ctk.CTkButton(top_frame2, text="Agregar", command=lambda: ifagregar(bottom_frame), font=poppins14bold)
    crearliq.pack(padx=5, pady=5, side="left")

    gestionarliq = ctk.CTkButton(top_frame2, text="Modificar", command=lambda:ifgestionar(bottom_frame), font=poppins14bold)
    gestionarliq.pack(padx=5, pady=5, side="left")

    eliminarliq = ctk.CTkButton(top_frame2, text="Eliminar", command=lambda: print("Example"), font=poppins14bold)
    eliminarliq.pack(padx=5, pady=5, side="left")

    busquedaliq = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedaliq.pack(padx=5, pady=5, side="right")

    #Contenido del bottom frame

    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)
    
    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
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
    
    try:
        with connection() as conn:
            print("Database connection established.")
            cursor = conn.cursor()
            sql = 'SELECT nombres, apellidos, ci_contribuyente, rif, telefono, correo FROM contribuyentes'
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Query executed successfully, fetched results: {results}")

            # Ensure data fits Treeview structure
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during database operation: {e}")

    

