import tkinter as tk
import customtkinter as ctk
import tkinter as tk
from .menubar import menubar
from functions.functions import * 
from tkinter import ttk
from functions.rectangle import rectangle
from tkinter import messagebox


def inmuebles(window, last_window):
    global busquedabtn, busquedainm, refrescartabla
    
    for widget in window.winfo_children():
        widget.destroy()
        


    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12, "bold")
    
    menubar(window)
    
    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)

    top_frame2 = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame2.pack(fill="x", padx=10)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    #Contenido del top frame.
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Gestion Inmuebles", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    crearinm = ctk.CTkButton(top_frame2, text="Asignar", command=lambda: ifasignar(bottom_frame, top_frame2, window, last_window, window_title), font=poppins14bold)
    crearinm.pack(padx=5, pady=5, side="left")

    gestionarinm = ctk.CTkButton(top_frame2, text="Gestionar", command=lambda: ifgestionar(window, bottom_frame, top_frame2, last_window, window_title), font=poppins14bold)
    gestionarinm.pack(padx=5, pady=5, side="left")

    refrescartabla = ctk.CTkButton(top_frame2, text="🔁", font=poppins14bold, width=30, command=lambda: loaddata())
    refrescartabla.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

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

    my_tree['columns'] = ('CI', 'Contribuyente', 'Inmueble','Codigo Catastral', 'Uso', 'Ubicación','Sector')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    def loaddata():    
        try:
            with connection() as conn:
                print("Database connection established.")
                cursor = conn.cursor()
                sql = """
                SELECT c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, i.ubicacion, s.nom_sector AS sector
                FROM inmuebles i
                JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
                JOIN sectores s ON i.id_sector = s.id_sector
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
                # Clear existing rows
                for row in my_tree.get_children():
                    my_tree.delete(row)

                # Ensure data fits Treeview structure
                for row in results:
                    my_tree.insert("", "end", values=row)

        except Exception as e:

            print(f"Error during database operation: {e}")
    loaddata()
    return window

def ifasignar(bottom_frame, top_frame2, window, last_window, window_title):
    global busquedainm, busquedabtn, refrescartabla, id_contr

    if busquedabtn:
        busquedabtn.pack_forget()
    if busquedainm:
        busquedainm.pack_forget()
    if refrescartabla:
        refrescartabla.pack_forget()    
    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()
        
    window_title.configure(text="Gestion Inmuebles | Asignar")
        
    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=400)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")
    
    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)
    
    poppins18 = ("Poppins", 18, "bold")
    
    

    # Contenido del frame left #########################################################################

    
    frameinformacion = ctk.CTkFrame(frame_left)
    frameinformacion.pack(padx=10, pady=5, fill="x")

    frameinformacion2 = ctk.CTkFrame(frameinformacion)
    frameinformacion2.pack(padx=10, pady=8, fill="x", side="bottom")


    
    text_label=ctk.CTkLabel(frameinformacion, text="Información del Contribuyente", font=poppins14bold)
    text_label.pack(pady=5)
    
    text_label2=ctk.CTkLabel(frameinformacion2, text="", font=poppins14bold)
    text_label2.pack(pady=5)


    ##############################################



    inmueblecod_frame = ctk.CTkFrame(frame_left)
    inmueblecod_frame.pack(padx=10, pady=5, fill="x")
    
    ubic_frame = ctk.CTkFrame(frame_left)
    ubic_frame.pack(padx=10, pady=5, anchor="w")

    sector_frame = ctk.CTkFrame(frame_left)
    sector_frame.pack(padx=10, pady=5, fill="x")
    
    uso_frame = ctk.CTkFrame(frame_left)
    uso_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, anchor="w")
    
    
    
    #############################################
    
    refrescartabla = ctk.CTkButton(top_frame2, text="🔁", font=poppins14bold, width=30, command=lambda: loaddata())
    refrescartabla.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: busca(busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    #############################################
    

    # Entrys del frame contribuyente



    inmueble = ctk.CTkEntry(inmueble_frame,placeholder_text="Nombre del Inmueble", font=poppins14bold, width=250)
    inmueble.pack(padx=5, pady=5, side="left")

    inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
    inmueblecod.pack(pady=5, padx=5, side="left")
    
    inmuebleubic = ctk.CTkEntry(ubic_frame, placeholder_text="Ubicación del inmueble", font=poppins14bold, width=250)
    inmuebleubic.pack(pady=5, padx=5, side="left")
    
    usovalues = ["Comercial", "Recidencial"]
    uso = ctk.CTkOptionMenu(uso_frame, values=usovalues, font=poppins14bold, width=250)

    def on_uso_change(choice):
        if choice == "Comercial":
            inmueble_frame.pack(padx=10, pady=5, anchor="w")
        else:
            inmueble_frame.pack_forget()

    uso.set("Comercial")  # Establecer valor predeterminado
    uso.pack(pady=5, padx=5, side="left")
    uso.configure(command=on_uso_change)

    sector_names = ["Sector"]
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nom_sector FROM sectores")
            sector_results = cursor.fetchall()
            sector_names.extend([row[0] for row in sector_results])
    except Exception as e:
        print(f"Error loading sectors: {e}")

    sector = ctk.CTkOptionMenu(sector_frame, values=sector_names, font=poppins14bold, width=250)
    sector.set("Sector")
    sector.pack(pady=5, padx=5, side="left")
    
    id_contr=""
    
    
    btnvolver = ctk.CTkButton(frame_left, text="Atrás", command=lambda: inmuebles(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    btnsave = ctk.CTkButton(frame_left, text="Guardar", font=poppins14bold, command=lambda: guardar_inmueble(inmueble, inmueblecod, uso, sector, id_contr, inmuebleubic, text_label2))
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    # Fin del contenido del left frame #########################################################################

    # Contenido del RIGHT FRAME
    
    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(frame_right, fg_color='white')
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    

    my_tree['columns'] = ('ID', 'Nombre', 'Apellido', 'CI')
    
    my_tree.column('ID', width=0, stretch=tk.NO)
    my_tree.heading('ID', text='', anchor='center')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')

    def cargar_contribuyentes():
        original_data = []
        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = '''
                SELECT 
                    id_contribuyente,
                    nombres,
                    apellidos,
                    v_e || "-" || ci_contribuyente AS cedula_completa
                FROM contribuyentes
                ORDER BY ci_contribuyente ASC
                '''
                cursor.execute(sql)
                original_data = cursor.fetchall()
                
                print(f"Fetched {len(original_data)} rows from the database.")
        except Exception as e:
            print(f"Error during database operation: {e}")

        return original_data

    def loaddata():
        try:
            data = cargar_contribuyentes()
            
            # Clear existing rows
            for row in my_tree.get_children():
                my_tree.delete(row)
            
            # Insert new rows
            for row in data:
                my_tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Error fetching data: {e}")

    def on_tree_select(event):
        global id_contr
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            values = item['values']
            text_label2.configure(text=f"{values[1]} {values[2]}")
            id_contr=f"{values[0]}"

    my_tree.bind("<<TreeviewSelect>>", on_tree_select)

    loaddata()
    
    def busca(ci):
        ci_value = ci.get()
        if not ci_value:
            messagebox.showwarning("Advertencia", "Por favor ingrese una cedula para buscar")
            return

        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = ''' 
                SELECT 
                    id_contribuyente,
                    nombres,
                    apellidos,
                    v_e || "-" || ci_contribuyente AS cedula_completa
                FROM contribuyentes
                WHERE ci_contribuyente = ?
                ORDER BY ci_contribuyente ASC
                '''
                cursor.execute(sql, (ci_value,))
                results = cursor.fetchall()
                
                if not results:
                    messagebox.showerror("Error", "No se ha encontrado la cédula del contribuyente.")
                    loaddata()
                    return

                # Clear existing rows
                for row in my_tree.get_children():
                    my_tree.delete(row)

                # Insert updated rows
                for row in results:
                    my_tree.insert("", "end", values=row)
        except Exception as e:
            print(f"Error refreshing Treeview: {e}")

def guardar_inmueble(inmueble, inmueblecod, uso, sector, id_contr, inmuebleubic, label):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            id_contribuyente = id_contr
            cursor.execute('''
                INSERT INTO inmuebles (nom_inmueble, ubicacion, cod_catastral, uso, id_contribuyente, id_sector)
                VALUES (?, ?, ?, ?, ?, (SELECT id_sector FROM sectores WHERE nom_sector = ?))
            ''', (inmueble.get(),inmuebleubic.get(), inmueblecod.get(), uso.get(), id_contribuyente, sector.get()))
            conn.commit()
            messagebox.showinfo("Información","Se ha guardado el inmueble correctamente")

            label.configure(text="")

            inmueble.delete(0, ctk.END)
            inmueble.configure(placeholder_text="Inmueble")

            inmueblecod.delete(0, ctk.END)
            inmueblecod.configure(placeholder_text="Codigo Catastral")
            
            inmuebleubic.delete(0, ctk.END)
            inmuebleubic.configure(placeholder_text="Ubicación del inmueble")

            uso.set("Comercial") 
            sector.set("Sector")
    
            print("Inmueble guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el inmueble: {e}")

        messagebox.showerror("Error", f"Error al guardar el inmueble: {e}")
        
def ifgestionar(window, bottom_frame, top_frame2, last_window, window_title):
    global busquedainm, busquedabtn, refrescartabla, id_contr
    
    window_title.configure(text="Gestion Inmuebles | Gestionar")

    if busquedabtn:
        busquedabtn.pack_forget()
    if busquedainm:
        busquedainm.pack_forget()
    if refrescartabla:
        refrescartabla.pack_forget()

    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    frameinformacion = ctk.CTkFrame(frame_left)
    frameinformacion.pack(padx=10, pady=5, fill="x")

    frameinformacion2 = ctk.CTkFrame(frameinformacion)
    frameinformacion2.pack(padx=10, pady=8, fill="x", side="bottom")

    contribuyenteci_frame = ctk.CTkFrame(frame_left)
    contribuyenteci_frame.pack(padx=10, pady=5, fill="x")

    contribuyentenombre_frame = ctk.CTkFrame(frame_left)
    contribuyentenombre_frame.pack(padx=10, pady=5, fill="x")
    

    inmueblecod_frame = ctk.CTkFrame(frame_left)
    inmueblecod_frame.pack(padx=10, pady=5, fill="x")


    ubic_frame = ctk.CTkFrame(frame_left)
    ubic_frame.pack(padx=10, pady=5, anchor="w")
    
    sector_frame = ctk.CTkFrame(frame_left)
    sector_frame.pack(padx=10, pady=5, fill="x")
    
    uso_frame = ctk.CTkFrame(frame_left)
    uso_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, anchor="w")
    

    ################################
    refrescartabla = ctk.CTkButton(top_frame2, text="🔁", font=poppins14bold, width=30, command=lambda: reload_treeview())
    refrescartabla.pack(padx=5, pady=5, side="right")


    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")
    ################################

    # Entrys del frame contribuyente

    labelcontribuyente = ctk.CTkLabel(frameinformacion, text="Informacion del Contribuyente", font=poppins14bold)
    labelcontribuyente.pack(pady=5)

    labelcontri = ctk.CTkLabel(frameinformacion2, text="", font=poppins14bold)
    labelcontri.pack(pady=5, side="bottom")

    contribuyenteci = ctk.CTkEntry(contribuyenteci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold, width=250)
    contribuyenteci.pack(pady=5, padx=5, side="left")
    #hide the contribuyenteci
    contribuyenteci.pack_forget()
    contribuyenteci_frame.pack_forget()

    contribuyentenombre = ctk.CTkEntry(contribuyentenombre_frame, placeholder_text="Contribuyente", font=poppins14bold, width=250)
    contribuyentenombre.pack(pady=5, padx=5, side="left")
    #hide the contribuyentenombre
    contribuyentenombre.pack_forget()
    contribuyentenombre_frame.pack_forget()
    
    
    #######################################

    inmueble = ctk.CTkEntry(inmueble_frame, placeholder_text="Inmueble", font=poppins14bold, width=250)
    inmueble.pack(padx=5, pady=5, side="left")

    inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
    inmueblecod.pack(pady=5, padx=5, side="left")
    
    inmuebleubic = ctk.CTkEntry(ubic_frame, placeholder_text="Ubicación del inmueble", font=poppins14bold, width=250)
    inmuebleubic.pack(pady=5, padx=5, side="left")
    
    

    usovalues = ["Comercial", "Recidencial"]
    uso = ctk.CTkOptionMenu(uso_frame, values=usovalues, font=poppins14bold, width=250)

    def on_uso_change(choice):
        if choice == "Comercial":
            inmueble_frame.pack(padx=10, pady=5, anchor="w")
        else:
            inmueble_frame.pack_forget()

    uso.set("Comercial")  # Establecer valor predeterminado
    uso.pack(pady=5, padx=5, side="left")
    uso.configure(command=on_uso_change)



    sector_names = ["Sector"]
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nom_sector FROM sectores")
            sector_results = cursor.fetchall()
            sector_names = [row[0] for row in sector_results]
    except Exception as e:
        print(f"Error loading sectors: {e}")

    sector = ctk.CTkOptionMenu(sector_frame, values=sector_names, font=poppins14bold, width=250)
    sector.set("Sector")
    sector.pack(pady=5, padx=5, side="left")

    # Informacion del contribuyente ##################################################

    

    selected_item = None  # Initialize selected_item

    def clear():
        contribuyenteci.delete(0, ctk.END)
        contribuyenteci.configure(placeholder_text="")

        contribuyentenombre.delete(0, ctk.END)
        contribuyentenombre.configure(placeholder_text="")

        inmueble.delete(0, ctk.END)
        inmueble.configure(placeholder_text="Inmueble")

        inmueblecod.delete(0, ctk.END)
        inmueblecod.configure(placeholder_text="Codigo Catastral")
        
        inmuebleubic.delete(0, ctk.END)
        inmuebleubic.configure(placeholder_text="Ubicación del inmueble")

        uso.set("Comercial") 
        sector.set("Sector")

        
    def on_tree_select(event):
        nonlocal selected_item  # Use nonlocal to modify the outer variable
        selected_items = my_tree.selection()
        if not selected_items:
            return  # No hay ningún elemento seleccionado
        selected_item = selected_items[0]
        values = my_tree.item(selected_item, "values")

        contribuyenteci.delete(0, ctk.END)
        contribuyenteci.insert(0, values[0])

        contribuyentenombre.delete(0, ctk.END)
        contribuyentenombre.insert(0, values[1])

        inmueble.delete(0, ctk.END)
        inmueble.insert(0, values[2])
        
        inmuebleubic.delete(0, ctk.END)
        inmuebleubic.insert(0, values[5])

        inmueblecod.delete(0, ctk.END)
        inmueblecod.insert(0, values[3])

        uso.set(values[4])
        sector.set(values[6])

        labelcontri.configure(text=f"{values[1]}")

        # Mostrar u ocultar el frame de inmueble según el valor de uso
        if values[4] == "Comercial":
            inmueble_frame.pack(padx=10, pady=5, anchor="w")
        else:
            inmueble_frame.pack_forget()

        my_tree.unbind("<ButtonRelease-1>")
        my_tree.bind("<<TreeviewSelect>>", on_tree_select)
                     
    def save_changes(selected_item):
        new_values = (
            contribuyenteci.get(),
            contribuyentenombre.get(),
            inmueble.get(),
            inmueblecod.get(),
            inmuebleubic.get(),
            uso.get(),
            sector.get()
        )

        try:
            with connection() as conn:
                cursor = conn.cursor()

                # Get id_contribuyente from contribuyentes table
                cursor.execute("SELECT id_contribuyente FROM contribuyentes WHERE ci_contribuyente = ?", (new_values[0],))
                id_contribuyente = cursor.fetchone()[0]

                # Get id_sector from sectores table
                cursor.execute("SELECT id_sector FROM sectores WHERE nom_sector = ?", (new_values[6],))
                id_sector = cursor.fetchone()[0]

                sql = '''
                UPDATE inmuebles
                SET nom_inmueble = ?, cod_catastral = ?, ubicacion = ?, uso = ?, id_contribuyente = ?, id_sector = ?
                WHERE id_inmueble = ?
                '''
                cursor.execute(sql, (new_values[2], new_values[3], new_values[4], new_values[5], id_contribuyente, id_sector, selected_item))
                conn.commit()
                print("Changes saved successfully!")
                messagebox.showinfo("Información", "Se han Actualizado los datos correctamente")
                reload_treeview(my_tree)
                clear()
                labelcontri.configure(text='')
                my_tree.bind("<ButtonRelease-1>", on_tree_select)
        except Exception as e:
            print(f"Error saving changes: {e}")

    def delete_record(selected_item):
        if not selected_item:
            print("no se selecciono nah")
            return

        if messagebox.askyesno("Confirmar eliminación", "¿Estás seguro que deseas eliminar este inmueble?"):
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM inmuebles WHERE id_inmueble = ?", (selected_item,))
                    conn.commit()
                    print("Record deleted successfully!")
                    clear()
                    messagebox.showinfo("Información", "Se ha eliminado el inmueble correctamente")
                    reload_treeview(my_tree)
                    reset_selection()
            except Exception as e:
                print(f"Error deleting record: {e}")

    def reset_selection():
        nonlocal selected_item
        selected_item = None
        my_tree.bind("<ButtonRelease-1>", on_tree_select)

    btnvolver = ctk.CTkButton(frame_left, text="Atrás", command=lambda: inmuebles(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: save_changes(selected_item), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    btndelete = ctk.CTkButton(frame_left, text="Eliminar", command=lambda: delete_record(selected_item), font=poppins14bold)
    btndelete.pack(padx=10, pady=10, anchor="e", side="bottom")

    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")


    my_tree["columns"] = ("CI", "Contribuyente", "Inmueble", "Codigo Catastral", "Uso", "Ubicación","Sector")
    for col in my_tree["columns"]:
        my_tree.heading(col, text=col.capitalize(), anchor="center")
        my_tree.column(col, anchor="center")

    # Fetch data to populate Treeview
    reload_treeview(my_tree)

    my_tree.bind("<ButtonRelease-1>", on_tree_select)

def reload_treeview(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """
            SELECT i.id_inmueble, c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, i.ubicacion, s.nom_sector AS sector
            FROM inmuebles i
            JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
            JOIN sectores s ON i.id_sector = s.id_sector
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row[1:])

    except Exception as e:
        print(f"Error fetching data: {e}")

def reload_treeviewsearch(treeview, ci):
    ci_value = ci.get()
    if not ci_value:
        messagebox.showwarning("Advertencia", "Por favor ingrese una cedula para buscar")
        return

    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' 
            SELECT c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, i.ubicacion, s.nom_sector AS sector
            FROM inmuebles i
            JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
            JOIN sectores s ON i.id_sector = s.id_sector
            WHERE c.ci_contribuyente = ?
            '''
            cursor.execute(sql, (ci_value,))
            results = cursor.fetchall()
            
            if not results:
                messagebox.showerror("Error", "No se ha encontrado la cédula del contribuyente.")
                reload_treeview(treeview)
                return

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")