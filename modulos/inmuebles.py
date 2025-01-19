import customtkinter as ctk
from .menubar import menubar
from functions.functions import * 
from tkinter import ttk
from functions.rectangle import rectangle
from tkinter import messagebox

def inmuebles(window, last_window):
    global busquedabtn, busquedainm, refrescartabla
    
    for widget in window.winfo_children():
        widget.destroy()
        
        #e

    
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
    
    #Contenido del top frame.
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Gestión de Inmuebles", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    crearinm = ctk.CTkButton(top_frame2, text="Asignar", command=lambda: ifasignar(bottom_frame, top_frame2, window, last_window), font=poppins14bold)
    crearinm.pack(padx=5, pady=5, side="left")

    gestionarinm = ctk.CTkButton(top_frame2, text="Gestionar", command=lambda: ifgestionar(window, bottom_frame, top_frame2, last_window), font=poppins14bold)
    gestionarinm.pack(padx=5, pady=5, side="left")

    refrescartabla = ctk.CTkButton(top_frame2, text="Refrescar Tabla", font=poppins14bold, width=80, command=lambda: loaddata())
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

    my_tree['columns'] = ('CI', 'Contribuyente', 'Inmueble', 'Codigo Catastral', 'Uso', 'Sector')

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
                SELECT c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, s.nom_sector AS sector
                FROM inmuebles i
                JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
                JOIN sectores s ON i.id_sector = s.id_sector
                """
                cursor.execute(sql)
                results = cursor.fetchall()

                # Ensure data fits Treeview structure
                for row in results:
                    my_tree.insert("", "end", values=row)

        except Exception as e:

            print(f"Error during database operation: {e}")
    loaddata()
    return window

def ifasignar(bottom_frame, top_frame2, window, last_window):
    global busquedainm, busquedabtn, refrescartabla

    if busquedabtn:
        busquedabtn.pack_forget()
    if busquedainm:
        busquedainm.pack_forget()
    if refrescartabla:
        refrescartabla.pack_forget()    
    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()
        
    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=400)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")
    
    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    # Contenido del frame left #########################################################################

    contribuyenteci_frame = ctk.CTkFrame(frame_left)
    contribuyenteci_frame.pack(padx=10, pady=5, fill="x")

    contribuyentenombre_frame = ctk.CTkFrame(frame_left)
    contribuyentenombre_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, anchor="w")

    inmueblecod_frame = ctk.CTkFrame(frame_left)
    inmueblecod_frame.pack(padx=10, pady=5, fill="x")

    uso_frame = ctk.CTkFrame(frame_left)
    uso_frame.pack(padx=10, pady=5, fill="x")

    sector_frame = ctk.CTkFrame(frame_left)
    sector_frame.pack(padx=10, pady=5, fill="x")
    
    cont_frame = ctk.CTkFrame(frame_left)
    cont_frame.pack(padx=10, pady=5, fill="x")
    
    text_label=ctk.CTkLabel(cont_frame, text="Contribuyente", font=poppins14bold)
    text_label.pack(pady=5)
    
    
    frame2 = ctk.CTkFrame(cont_frame, corner_radius=10, width=240, height=40)
    frame2.pack(pady=8, padx=10)
    frame2.pack_propagate(False)
    
    text_label2=ctk.CTkLabel(frame2, text="", font=poppins14bold)
    text_label2.pack(pady=5)
    
    #############################################

    refrescartabla = ctk.CTkButton(top_frame2, text="Refrescar tabla", font=poppins14bold, width=80, command=lambda: loaddata())
    refrescartabla.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    #############################################

    # Entrys del frame contribuyente
    contribuyenteci = ctk.CTkEntry(contribuyenteci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold, width=250)
    contribuyenteci.pack(pady=5, padx=5, side="left")

    contribuyentenombre = ctk.CTkEntry(contribuyentenombre_frame, placeholder_text="Contribuyente", font=poppins14bold, width=250)
    contribuyentenombre.pack(pady=5, padx=5, side="left")

    ########################################################
    def autofill_nombre_apellido(event):
        ci = contribuyenteci.get().strip()
        if not ci:
            return

        try:
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT nombres, apellidos FROM contribuyentes WHERE ci_contribuyente = ?",
                    (ci,)
                )
                result = cursor.fetchone()
                if result:
                    # Concatenate nombre and apellido
                    full_name = f"{result[0]} {result[1]}"
                    contribuyentenombre.delete(0, 'end')
                    contribuyentenombre.insert(0, full_name)  # Set full name
                else:
                    # Clear field if no match
                    contribuyentenombre.delete(0, 'end')
        except Exception as e:
            print(f"Error fetching contribuyente data: {e}")
        # Bind the function to contribuyenteci
    contribuyenteci.bind("<FocusOut>", autofill_nombre_apellido) 
    ########################################################

    inmueble = ctk.CTkEntry(inmueble_frame,placeholder_text="Inmueble", font=poppins14bold, width=250)
    inmueble.pack(padx=5, pady=5, side="left")

    inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
    inmueblecod.pack(pady=5, padx=5, side="left")

    usovalues = ["Comercial", "Residencial"]
    uso = ctk.CTkOptionMenu(uso_frame, values=usovalues, font=poppins14bold, width=250)
    uso.pack(pady=5, padx=5, side="left")

    sector_names = []
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nom_sector FROM sectores")
            sector_results = cursor.fetchall()
            sector_names = [row[0] for row in sector_results]
    except Exception as e:
        print(f"Error loading sectors: {e}")

    sector = ctk.CTkOptionMenu(sector_frame, values=sector_names, font=poppins14bold, width=250)
    sector.pack(pady=5, padx=5, side="left")

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: asignar_inmueble(contribuyenteci, contribuyentenombre, inmueble, inmueblecod, uso, sector), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    btnvolver = ctk.CTkButton(frame_left, text="Volver", command=lambda: inmuebles(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")

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
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ( 'CI', 'Contribuyente', 'Inmueble', 'Codigo Catastral', 'Uso', 'Sector')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    def loaddata():    
        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = """
                SELECT c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, s.nom_sector AS sector
                FROM inmuebles i
                JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
                JOIN sectores s ON i.id_sector = s.id_sector
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    my_tree.insert("", "end", values=row)

        except Exception as e:
            print(f"Error fetching data: {e}")
    loaddata()


def guardar_inmueble(inmueble, inmueblecod, uso, sector, id_contr):
    # Verificar que todos los campos estén rellenados
    if not inmueble.get() or not inmueblecod.get() or not uso.get() or not sector.get():
        messagebox.showwarning("Advertencia", "Todos los campos deben estar rellenados")
        return

    # Verificar que se haya seleccionado un contribuyente
    if not id_contr:
        messagebox.showwarning("Advertencia", "Debe seleccionar un contribuyente")
        return

    try:
        with connection() as conn:
            cursor = conn.cursor()
            id_contribuyente = id_contr
            cursor.execute('''
                INSERT INTO inmuebles (nom_inmueble, cod_catastral, uso, id_contribuyente, id_sector)
                VALUES (?, ?, ?, ?, (SELECT id_sector FROM sectores WHERE nom_sector = ?))
            ''', (inmueble.get(), inmueblecod.get(), uso.get(), id_contribuyente, sector.get()))
            conn.commit()
            messagebox.showinfo("Información", "Inmueble registrado correctamente")
            print("Inmueble guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el inmueble: {e}")
        messagebox.showerror("Error", f"Error al guardar el inmueble: {e}")
        
        
        

def ifgestionar(window, bottom_frame, top_frame2, last_window):
    global busquedainm, busquedabtn, refrescartabla

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

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, anchor="w")

    inmueblecod_frame = ctk.CTkFrame(frame_left)
    inmueblecod_frame.pack(padx=10, pady=5, fill="x")

    uso_frame = ctk.CTkFrame(frame_left)
    uso_frame.pack(padx=10, pady=5, fill="x")

    sector_frame = ctk.CTkFrame(frame_left)
    sector_frame.pack(padx=10, pady=5, fill="x")

    infodelcontribuyente = ctk.CTkFrame(frame_left)
    infodelcontribuyente.pack(padx=10, pady=5, fill="x")

    ###############################
    

    
    ################################
    refrescartabla = ctk.CTkButton(top_frame2, text="Refrescar Tabla", font=poppins14bold, width=80, command=lambda: reload_treeview(my_tree))
    refrescartabla.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")
    ################################

    # Entrys del frame contribuyente

    inmueble = ctk.CTkEntry(inmueble_frame, placeholder_text="Inmueble", font=poppins14bold, width=250)
    inmueble.pack(padx=5, pady=5, side="left")

    inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
    inmueblecod.pack(pady=5, padx=5, side="left")

    usovalues = ["Comercial", "Residencial"]
    uso = ctk.CTkOptionMenu(uso_frame, values=usovalues, font=poppins14bold, width=250)
    uso.pack(pady=5, padx=5, side="left")

    sector_names = []
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nom_sector FROM sectores")
            sector_results = cursor.fetchall()
            sector_names = [row[0] for row in sector_results]
    except Exception as e:
        print(f"Error loading sectors: {e}")

    sector = ctk.CTkOptionMenu(sector_frame, values=sector_names, font=poppins14bold, width=250)
    sector.pack(pady=5, padx=5, side="left")

    selected_item = None  # Initialize selected_item

    
    # Label para el contribuyente seleccionado

    frame2 = ctk.CTkFrame(infodelcontribuyente, corner_radius=10, width=240, height=40)
    frame2.pack(pady=8, padx=10)
    frame2.pack_propagate(False)
    
    text_label=ctk.CTkLabel(frame2, text="Contribuyente", font=poppins14bold)
    text_label.pack(pady=5)
    
    text_label2=ctk.CTkLabel(infodelcontribuyente, text="", font=poppins14bold)
    text_label2.pack(pady=5)
    

    def on_tree_select(event):
        nonlocal selected_item  # Use nonlocal to modify the outer variable
        selected_item = my_tree.selection()[0]
        values = my_tree.item(selected_item, "values")

        inmueble.delete(0, ctk.END)
        inmueble.insert(0, values[2])

        inmueblecod.delete(0, ctk.END)
        inmueblecod.insert(0, values[3])

        uso.set(values[4])
        sector.set(values[5])

        text_label2.configure(text="{} {}".format(values[0], values[1]))

        my_tree.unbind("<ButtonRelease-1>")
        my_tree.bind("<<TreeviewSelect>>", on_tree_select)
        return values[0], values[1]

    def save_changes(selected_item, inmueble, inmueblecod, uso, sector):    
        cedula, nombre = on_tree_select(selected_item)
        _inmueble = inmueble.get()
        codcatastral = inmueblecod.get()
        usovalue = uso.get()
        sectorvalue = sector.get()
        

        try:
            with connection() as conn:
                cursor = conn.cursor()

                # Get id_contribuyente from contribuyentes table
                cursor.execute("SELECT id_contribuyente FROM contribuyentes WHERE ci_contribuyente = ?", (cedula,))
                id_contribuyente = cursor.fetchone()[0]

                # Get id_sector from sectores table
                cursor.execute("SELECT id_sector FROM sectores WHERE nom_sector = ?", (sectorvalue,))
                id_sector = cursor.fetchone()[0]

                sql = '''
                UPDATE inmuebles
                SET nom_inmueble = ?, cod_catastral = ?, uso = ?, id_contribuyente = ?, id_sector = ?
                WHERE id_inmueble = ?
                '''
                cursor.execute(sql, (_inmueble, codcatastral, usovalue, id_contribuyente, id_sector, selected_item))
                conn.commit()
                print("Changes saved successfully!")
                reload_treeview(my_tree)
                my_tree.bind("<ButtonRelease-1>", on_tree_select)

        except Exception as e:
            print(f"Error saving changes: {e}")

    def delete_record(selected_item):
        try:
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inmuebles WHERE id_inmueble = ?", (selected_item,))
                conn.commit()
                print("Record deleted successfully!")
                reload_treeview(my_tree)
                reset_selection()
        except Exception as e:
            print(f"Error deleting record: {e}")

    def confirm_delete(selected_item):
        if selected_item:
            confirm = ctk.CTkToplevel(window)
            confirm.title("Confirm Delete")
            confirm.geometry("300x150")

            label = ctk.CTkLabel(confirm, text="Are you sure you want to delete this record?", font=poppins14bold)
            label.pack(pady=20)

            btn_yes = ctk.CTkButton(confirm, text="Yes", command=lambda: [delete_record(selected_item), confirm.destroy()], font=poppins14bold)
            btn_yes.pack(side="left", padx=20, pady=20)

            btn_no = ctk.CTkButton(confirm, text="No", command=confirm.destroy, font=poppins14bold)
            btn_no.pack(side="right", padx=20, pady=20)

    def reset_selection():
        nonlocal selected_item
        selected_item = None
        my_tree.bind("<ButtonRelease-1>", on_tree_select)

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: save_changes(selected_item, inmueble, inmueblecod, uso, sector), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    btndelete = ctk.CTkButton(frame_left, text="Eliminar", command=lambda: confirm_delete(selected_item), font=poppins14bold)
    btndelete.pack(padx=10, pady=10, anchor="e", side="bottom")

    btnvolver = ctk.CTkButton(frame_left, text="Atrás", command=lambda: inmuebles(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")

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


    my_tree["columns"] = ("CI", "Contribuyente", "Inmueble", "Codigo Catastral", "Uso", "Sector")
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
            SELECT i.id_inmueble, c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, s.nom_sector AS sector
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
    ci = ci.get()
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' 
            SELECT c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, s.nom_sector AS sector
            FROM inmuebles i
            JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
            JOIN sectores s ON i.id_sector = s.id_sector
            WHERE c.ci_contribuyente = ?
            '''
            cursor.execute(sql,(ci,))
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")
