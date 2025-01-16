import customtkinter as ctk
import tkinter as tk
from modulos.menubar import menubar
from functions.functions import * 
from tkinter import ttk, messagebox
from functions.rectangle import rectangle
from config.config import centrar_ventana
import tkinter


def ifagregar(bottom_frame, top_frame2, window, last_window):
    global busquedainm, busquedabtn, refrescarbtn
    

    if busquedabtn:
        busquedabtn.pack_forget()
    if busquedainm:
        busquedainm.pack_forget()
    if refrescarbtn:
        refrescarbtn.pack_forget()

    poppins14bold = ("Poppins", 14, "bold")
    poppins10 = ("Poppins", 10)
    poppins18 = ("Poppins", 18, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")
    
    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    text = ctk.CTkLabel(frame_left, text="Nuevo Contribuyente", font=poppins18, width=250)
    text.pack(padx=10, pady=10)

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

    #############################################

    refrescarbtn = ctk.CTkButton(top_frame2, text="Refrescar Tabla", font=poppins14bold, width=80, command=lambda: cargar_datos())
    refrescarbtn.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    #############################################
    
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
    def clear():
        nombre.delete(0, tk.END)
        nombre.configure(placeholder_text="Nombre")

        apellido.delete(0, tk.END)
        apellido.configure(placeholder_text="Apellido")

        cedula.delete(0, tk.END)
        cedula.configure(placeholder_text="Cédula de Identidad")

        rif.delete(0, tk.END)
        rif.configure(placeholder_text="RIF")

        telefono.delete(0, tk.END)
        telefono.configure(placeholder_text="Teléfono")

        correo.delete(0, tk.END)
        correo.configure(placeholder_text="ejemplo@gmail.com")

    def volver():
        contribuyentes
        print("back")

    def cargar_datos():
        for item in my_tree.get_children():
            my_tree.delete(item)
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = 'SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo, telefono, correo FROM contribuyentes'
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    my_tree.insert("", "end", iid=row[0], values=row[1:])
        except Exception as e:
            print(f"Error during database operation: {e}")

    def guardar_datos():
        text = ctk.CTkLabel(frame_left, text="", text_color="red", font=poppins14bold)
        text.place(x=30, y=450)
        try:
            with connection() as conn:
                cursor = conn.cursor()
                
                # Verificar si la cédula ya existe
                cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE ci_contribuyente = ?", (cedula.get(),))
                if cursor.fetchone()[0] > 0:
                    text = ctk.CTkLabel(text="La cédula de identidad ya existe", text_color="red")
                    return
                
                if len(cedula.get()) == 0:
                    text.configure(text="Ingrese la cedula de identidad", text_color="red")
                    return
                    
                elif len(nombre.get()) == 0:
                    text.configure(text="Ingrese el nombre", text_color="red")
                    return
                elif len(apellido.get()) == 0:
                    text.configure(text="Ingrese el apellido", text_color="red")
                    return

                sql = """INSERT INTO contribuyentes (nombres, apellidos, v_e, ci_contribuyente, j_c_g, rif, telefono, correo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                
                datos = (
                    nombre.get(),
                    apellido.get(),
                    cedula_indicator.get(), 
                    cedula.get(),
                    rif_indicator.get(),
                    rif.get(),
                    telefono.get(),
                    correo.get()
                )
                
                cursor.execute(sql, datos)
                conn.commit()
                text.configure(text="Contribuyente agregado", text_color="green")
                cargar_datos()  # Llamar a la función para actualizar el Treeview
                clear()
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command = guardar_datos, font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    btncancelar = ctk.CTkButton(frame_left, text="Volver", command=lambda: contribuyentes(window, last_window), font=poppins14bold)
    btncancelar.pack(padx=10, pady=10, anchor="e", side="bottom")

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
    vertical_scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=my_tree.yview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")
    vertical_scrollbar.pack(side="right", fill="y")

    my_tree['columns'] = ('nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    cargar_datos()  # Llamar a la función para cargar los datos inicialmente

def ifgestionar(bottom_frame, top_frame2, window, last_window):
    global busquedainm, busquedabtn, refrescarbtn

    if busquedabtn:
        busquedabtn.pack_forget()
    if busquedainm:
        busquedainm.pack_forget()
    if refrescarbtn:
        refrescarbtn.pack_forget()

    poppins14bold = ("Poppins", 14, "bold")
    poppins18 = ("Poppins", 18, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)
    
    text = ctk.CTkLabel(frame_left, text="Modificar Contribuyentes", font=poppins18, width=250)
    text.pack(padx=10, pady=10)

    #Contenido del frame left

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
    correo_frame.pack(padx=10, pady=5, fill="x")

    ##############################################
    
    refrescarbtn = ctk.CTkButton(top_frame2, text="Refrescar Tabla", font=poppins14bold, width=80, command=lambda: cargar_datos())
    refrescarbtn.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    ##############################################

    nombre_contribuyente = ctk.CTkEntry(nombre_contribuyente_frame, placeholder_text="Selecciona un Contribuyente", font=poppins14bold, width=250)
    nombre_contribuyente.pack(pady=5, padx=5, side="left")

    apellido_contribuyente = ctk.CTkEntry(apellido_contribuyente_frame, placeholder_text="Apellido Contribuyente", font=poppins14bold, width=250)
    apellido_contribuyente.pack(pady=5, padx=5, side="left")

    correo = ctk.CTkEntry(correo_frame, placeholder_text="correo@gmail.com", font=poppins14bold, width=250)
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

    telefono = ctk.CTkEntry(telefono_frame, placeholder_text="Teléfono", font=poppins14bold, width=250)
    telefono.pack(pady=5, padx=5, side="left")

    def clear():
        nombre_contribuyente.delete(0, tk.END)
        nombre_contribuyente.configure(placeholder_text="Nombre")

        apellido_contribuyente.delete(0, tk.END)
        apellido_contribuyente.configure(placeholder_text="Apellido")

        cedula.delete(0, tk.END)
        cedula.configure(placeholder_text="Cédula de Identidad")

        rif.delete(0, tk.END)
        rif.configure(placeholder_text="RIF")

        telefono.delete(0, tk.END)
        telefono.configure(placeholder_text="Teléfono")

        correo.delete(0, tk.END)
        correo.configure(placeholder_text="ejemplo@gmail.com")

    def cargar_datos():
        for item in my_tree.get_children():
            my_tree.delete(item)
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = '''SELECT
                id_contribuyente, 
                nombres, 
                apellidos, v_e || "-" || ci_contribuyente AS cedula_completa,
                j_c_g || "-" || rif AS rif_completo,
                telefono, 
                correo 
                FROM contribuyentes
                '''
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    my_tree.insert("", "end", iid=row[0], values=row)
        except Exception as e:
            print(f"Error during database operation: {e}")

    def save_changes(cedula_entry, nombre_entry, apellido_entry, rif_entry, telefono_entry, correo_entry, cedula_indicator, rif_indicator):
        
        text = ctk.CTkLabel(frame_left, text="La cédula de identidad ya existe", text_color="red", font=poppins14bold, width=250)
        text.place(x=10, y=400)
        
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            values = item['values']
            print(f"Selected item values: {values}")  # Debug print statement
            
            if len(values) < 7:
                print("Error: Selected item does not have enough values.")
                return
                
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cedula = cedula_entry.get()
                    sql = '''
                    SELECT COUNT(*) FROM contribuyentes WHERE ci_contribuyente=?
                    '''
                    cursor.execute(sql, (cedula, ))
                    count = cursor.fetchone()[0]

                    if count > 1:
                        
                        
                        text.configure(text="La cédula de identidad ya existe", text_color="red")
                        tkinter.messagebox.showerror("Error", "La cédula de identidad ya existe")
                        print(f'error print: {cedula}')
                        return
                    
                    sql = '''UPDATE contribuyentes SET nombres=?, apellidos=?, v_e=?, ci_contribuyente=?, j_c_g=?, rif=?, telefono=?, correo=?
                             WHERE id_contribuyente=?'''
                    cursor.execute(sql, (nombre_entry.get(), apellido_entry.get(), cedula_indicator.get(), cedula, rif_indicator.get(), rif_entry.get(), telefono_entry.get(), correo_entry.get(), values[0]))
                    conn.commit()
                    text.configure(text="Datos actualizados correctamente", text_color="green")
                    text.place(x=10, y=400)
                    cargar_datos()
                    clear()
            except Exception as e:
                print(f"Error al actualizar datos: {e}")
        else:
            print("Error: No item selected in the Treeview.")

    def delete_record():
        text = ctk.CTkLabel(frame_left, text="", text_color="green", font=poppins14bold, width=250)
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            values = item['values']
            confirm = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este registro?")
            if confirm:
                try:
                    with connection() as conn:
                        cursor = conn.cursor()
                        sql = 'DELETE FROM contribuyentes WHERE id_contribuyente=?'
                        cursor.execute(sql, (values[0],))
                        conn.commit()    
                        text.configure(text="Registro eliminado correctamente", text_color="green")
                        text.place(x=10, y=400)
                        cargar_datos()
                        clear()
                    
                except Exception as e:
                    print(f"Error al eliminar datos: {e}")

    btnsave = ctk.CTkButton(frame_left, text="Actualizar", command=lambda: save_changes(cedula, nombre_contribuyente, apellido_contribuyente, rif, telefono, correo, cedula_indicator, rif_indicator), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    btndelete = ctk.CTkButton(frame_left, text="Eliminar", command=delete_record, font=poppins14bold)
    btndelete.pack(padx=10, pady=10, anchor="e", side="bottom")

    
    btncancelar = ctk.CTkButton(frame_left, text="Atrás", command=lambda: contribuyentes(window, last_window), font=poppins14bold)
    btncancelar.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    
    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    vertical_scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=my_tree.yview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")
    vertical_scrollbar.pack(side="right", fill="y")

    my_tree["columns"] = ('id_contribuyente', 'nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')
    for col in my_tree["columns"]:
        my_tree.heading(col, text=col.capitalize(), anchor="center")
        my_tree.column(col, anchor="center")
        
    my_tree.column('id_contribuyente', width=0, stretch=tk.NO)

    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    vertical_scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=my_tree.yview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")
    vertical_scrollbar.pack(side="right", fill="y")

    def on_tree_select(event):
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            values = item['values']
            nombre_contribuyente.delete(0, tk.END)
            nombre_contribuyente.insert(0, values[1])
            apellido_contribuyente.delete(0, tk.END)
            apellido_contribuyente.insert(0, values[2])
            print(f'Value is {values[3]} and type is {type(values[3])}')
            ced = values[3]

            if isinstance(ced, str):
                cedula_indicator.set(ced[0])
                ced = ced[2:]
                print(ced)
                cedula.delete(0, tk.END)
                cedula.insert(0, ced)
            else:
                cedula.delete(0, tk.END)
                cedula.insert(0, values[3])

            rif.delete(0, tk.END)
            rif.insert(0, values[4][2:])
            rif_indicator.set(values[4][0])
            telefono.delete(0, tk.END)
            telefono.insert(0, values[5])
            correo.delete(0, tk.END)
            correo.insert(0, values[6])
            text = ctk.CTkLabel(frame_left, text="", text_color="green", font=poppins14bold, width=270)
            text.place(x=0, y=400)

    my_tree.bind("<<TreeviewSelect>>", on_tree_select)
    cargar_datos()
    # def cargartreeview():
    #     try:
    #         # Establish a database connection
    #         with connection() as conn:
    #             cursor = conn.cursor()
    #             # SQL query to fetch data
    #             sql = '''
    #                 SELECT 
    #                     id_contribuyente, 
    #                     nombres, 
    #                     apellidos, 
    #                     v_e || "-" || ci_contribuyente AS cedula_completa, 
    #                     j_c_g || "-" || rif AS rif_completo, 
    #                     telefono, 
    #                     correo 
    #                 FROM contribuyentes
    #             '''
    #             cursor.execute(sql)
    #             results = cursor.fetchall()

    #             # Clear the Treeview before populating
    #             for item in my_tree.get_children():
    #                 my_tree.delete(item)

    #             # Populate the Treeview with fetched data
    #             for row in results:
    #                 my_tree.insert("", "end", iid=row[0], values=row)

    #     except Exception as e:
    #         print(f"Error fetching data: {e}")
    # cargartreeview()

def contribuyentes(window, last_window):
    global busquedainm, busquedabtn, refrescarbtn
    
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
    
    #Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Contribuyentes Catastrales", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    crearliq = ctk.CTkButton(top_frame2, text="Agregar", command=lambda: ifagregar(bottom_frame, top_frame2, window, last_window), font=poppins14bold)
    crearliq.pack(padx=5, pady=5, side="left")

    gestionarliq = ctk.CTkButton(top_frame2, text="Modificar", command=lambda:ifgestionar(bottom_frame, top_frame2, window, last_window), font=poppins14bold)
    gestionarliq.pack(padx=5, pady=5, side="left")

    refrescarbtn = ctk.CTkButton(top_frame2, text="Refrescar Tabla", font=poppins14bold, width=80, command=lambda: loaddata(my_tree))
    refrescarbtn.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    #Contenido del bottom frame

    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)
    
    # Creando el treeview para mostrar los registros


    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both", side="left")

    # Configuración del estilo del Treeview (usando ttk dentro de CustomTkinter)
    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    # Crear el Treeview
    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    # Crear el scrollbar vertical con CustomTkinter

    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")


    my_tree['columns'] = ('ID', 'nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')
    
    my_tree.column('ID', width=0, stretch=tk.NO)
    my_tree.heading('ID', text='', anchor='center')
    
    
    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    

    my_tree.bind("<<TreeviewSelect>>")  # Selección básica
    my_tree.bind("<Double-1>", lambda event: mostrar_modal_contribuyente(my_tree))  # Doble clic
    my_tree.bind("<Return>", lambda event: mostrar_modal_contribuyente(my_tree))  # Tecla Enter

    loaddata(my_tree)
    return window, last_window


def reload_treeviewsearch(treeview, ci):
    ci = ci.get()
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' 
            SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo,
            telefono, correo FROM contribuyentes where ci_contribuyente = ?
            '''
            cursor.execute(sql,(ci,))
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")
        
def loaddata(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = 'SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo, telefono, correo FROM contribuyentes'
            cursor.execute(sql)
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row)
            
    except Exception as e:
        print(f'Ocurrio un error: {e}')



def mostrar_modal_contribuyente(treeview):
    poppins14bold = ("Poppins", 14, "bold")
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 25, "bold")
    
    # Obtener el elemento seleccionado
    seleccion = treeview.selection()
    if seleccion:
        item = treeview.item(seleccion[0])  # Obtener datos del elemento
        datos = item['values']  # Recuperar los valores de las columnas
        if not datos:
            print("No hay datos seleccionados.")
            return
        
        id_contribuyente = datos[0]
        datos_contribuyente = cargar_datoss(id_contribuyente)
        
        if not datos_contribuyente:
            print("No se encontraron datos del contribuyente.")
            return







        # config
        modal = ctk.CTkToplevel()
        modal.title("Contribuyente")
        modal.geometry("600x500")  
        modal.grab_set()  
        modal.resizable(False, False)
        centrar_ventana(modal, 600, 500)
        
        
        cerrar_btn = ctk.CTkButton(modal, text="Cerrar", command=modal.destroy, font=poppins14bold)
        cerrar_btn.pack(pady=10, padx=10, side="bottom", anchor="e") 
        
        
        frame_left = ctk.CTkFrame(modal, corner_radius=15, width=250)
        frame_left.pack(padx=5, pady=5, side="left", fill="both", expand=True)
        

        # Mostrar datos en la ventana modal
        nombre = datos_contribuyente[0][0]
        cedula = datos_contribuyente[0][1]
        rif = datos_contribuyente[0][2]
        telefono = datos_contribuyente[0][3]
        correo = datos_contribuyente[0][4]
        
        text= ctk.CTkLabel(frame_left, text="Datos del Contribuyente", font=poppins20bold)
        text.pack(pady=5)
        
        frame_nombre= ctk.CTkFrame(frame_left, corner_radius=15)
        frame_nombre.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_cedula=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_cedula.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_rif=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_rif.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_telefono=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_telefono.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_correo=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_correo.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        
        
        ###############labels##########
        
        label_nombre = ctk.CTkLabel(frame_nombre, text=(f"Nombre: {nombre}"), font=poppins14bold)
        label_nombre.pack(pady=10, padx=10)
        
        label_cedula = ctk.CTkLabel(frame_cedula, text=(f"Cédula: {cedula}"), font=poppins14bold)
        label_cedula.pack(pady=10)
        
        label_rif = ctk.CTkLabel(frame_rif, text=(f"RIF: {rif}"), font=poppins14bold)
        label_rif.pack(pady=10)
        
        label_telefono = ctk.CTkLabel(frame_telefono, text=(f"Teléfono: {telefono}"), font=poppins14bold)
        label_telefono.pack(pady=10)
        
        label_correo = ctk.CTkLabel(frame_correo, text=(f"Correo: {correo}"), font=poppins14bold)
        label_correo.pack(pady=10)
        
        # Botón para cerrar la ventana modal

    else:
        print("No se ha seleccionado ningún elemento en el Treeview.")

def cargar_datoss(ID):
    original_data = []
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = '''
            SELECT 
                contribuyentes.nombres || ' ' || contribuyentes.apellidos AS contribuyente,
                v_e || "-" || ci_contribuyente AS cedula_completa,
                j_c_g || "-" || rif AS rif_completo,
                contribuyentes.telefono,
                contribuyentes.correo
            FROM contribuyentes
            WHERE id_contribuyente = ?
            ORDER BY contribuyentes.ci_contribuyente ASC
            '''
            cursor.execute(sql, (ID,))
            original_data = cursor.fetchall()
            
            print(f"Fetched {len(original_data)} rows from the database.")
    except Exception as e:
        print(f"Error during database operation: {e}")

    return original_data
1