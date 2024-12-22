import customtkinter as ctk
from menubar import menubar
from functions import * 
from tkinter import ttk
from rectangle import rectangle

def ifasignar(bottom_frame):
        
        poppins14bold = ("Poppins", 14, "bold")


        for widget in bottom_frame.winfo_children():
            widget.destroy()

        frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
        frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

        frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
        frame_left.pack(padx=5, pady=5, side="left", fill="y")

        #Contenido del frame left #########################################################################

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


        try:
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nom_sector FROM sectores")
                sector_results = cursor.fetchall()
                sector_names = [row[0] for row in sector_results]
                sector.configure(values=sector_names)  # Update dropdown options
        except Exception as e:
            print(f"Error loading sectors: {e}")

        sector = ctk.CTkOptionMenu(sector_frame, values=sector_names, font=poppins14bold, width=250)
        sector.pack(pady=5, padx=5, side="left")

        btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: asginarinmueble(contribuyenteci, contribuyentenombre, inmueble, inmueblecod, uso, sector), font=poppins14bold)
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
        
        horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    
        my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    
        horizontal_scrollbar.pack(side="bottom", fill="x")
    
        my_tree['columns'] = ( 'CI', 'Contribuyente', 'Inmueble', 'Codigo Catastral', 'Monto 1', 'Monto 2', 'Fecha Liquidacion')
    
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
                sql = 'SELECT * FROM inmuebles'
                cursor.execute(sql)
                results = cursor.fetchall()
                print(f"Query executed successfully, fetched results: {results}")

                # Ensure data fits Treeview structure
                for row in results:
                    my_tree.insert("", "end", values=row)

        except Exception as e:
            print(f"Error during database operation: {e}")


        def asginarinmueble(contribuyenteci, contribuyentenombre, inmueble, inmueblecod, uso, sector):
    # Get values from entry fields
            contribuyenteci = contribuyenteci.get()
            contribuyentenombre = contribuyentenombre.get()
            inmueble = inmueble.get()
            inmueblecod = inmueblecod.get()
            uso = uso.get()
            sector = sector.get()

            if not (contribuyenteci and contribuyentenombre and inmueble and inmueblecod and uso and sector):
                print("Please fill in all fields.")
                return

            try:
                with connection() as conn:
                    cursor = conn.cursor()

                    # Step 1: Get `id_contribuyente` from `contribuyentes` table
                    cursor.execute(
                        "SELECT id_contribuyente FROM contribuyentes WHERE ci_contribuyente = ? AND nombres = ?",
                        (contribuyenteci, contribuyentenombre)
                    )
                    contribuyente_result = cursor.fetchone()
                    if contribuyente_result:
                        id_contribuyente = contribuyente_result[0]
                    else:
                        print("Contribuyente not found.")
                        return

                    # Step 2: Get `id_sector` from `sectores` table
                    cursor.execute(
                        "SELECT id_sector FROM sectores WHERE nom_sector = ?",
                        (sector,)
                    )
                    sector_result = cursor.fetchone()
                    if sector_result:
                        id_sector = sector_result[0]
                    else:
                        print("Sector not found.")
                        return

                    # Step 3: Insert into `inmuebles` table
                    sql = '''
                    INSERT INTO inmuebles (nom_inmueble, cod_catastral, uso, id_contribuyente, id_sector)
                    VALUES (?, ?, ?, ?, ?)
                    '''
                    cursor.execute(sql, (inmueble, inmueblecod, uso, id_contribuyente, id_sector))
                    conn.commit()
                    print("Inmueble successfully assigned!")
                    # Inside asignarinmueble
                    reload_treeview(my_tree)

                    

            except Exception as e:
                print(f"Error: {e}")
# FIN del Contenido del RIGHT FRAME
def ifgestionar(bottom_frame):
    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

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

    # Entrys del frame contribuyente

    contribuyenteci = ctk.CTkEntry(contribuyenteci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold, width=250)
    contribuyenteci.pack(pady=5, padx=5, side="left")

    contribuyentenombre = ctk.CTkEntry(contribuyentenombre_frame, placeholder_text="Contribuyente", font=poppins14bold, width=250)
    contribuyentenombre.pack(pady=5, padx=5, side="left")

    inmueble = ctk.CTkEntry(inmueble_frame, placeholder_text="Inmueble", font=poppins14bold, width=250)
    inmueble.pack(padx=5, pady=5, side="left")

    inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
    inmueblecod.pack(pady=5, padx=5, side="left")

    usovalues = ["Comercial", "Residencial"]
    uso = ctk.CTkOptionMenu(uso_frame, values=usovalues, font=poppins14bold, width=250)
    uso.pack(pady=5, padx=5, side="left")

    valuesector = ["Sector"]
    sector = ctk.CTkOptionMenu(sector_frame, values=valuesector, font=poppins14bold, width=250)
    sector.pack(pady=5, padx=5, side="left")

    selected_item = None  # Initialize selected_item

    def cancel_action():
        contribuyenteci.delete(0, ctk.END)
        contribuyentenombre.delete(0, ctk.END)
        inmueble.delete(0, ctk.END)
        inmueblecod.delete(0, ctk.END)
        uso.set("")
        sector.set("")
        my_tree.bind("<ButtonRelease-1>", on_tree_select)

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: save_changes(selected_item), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    btncancel = ctk.CTkButton(frame_left, text="Cancelar", command=lambda: cancel_action(), font=poppins14bold)
    btncancel.pack(padx=10, pady=10, anchor="e", side="bottom")

    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    my_tree["columns"] = ("CI", "Contribuyente", "Inmueble", "Codigo Catastral", "Uso", "Sector")
    for col in my_tree["columns"]:
        my_tree.heading(col, text=col.capitalize(), anchor="center")
        my_tree.column(col, anchor="center")

    # Fetch data to populate Treeview
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT ci_contribuyente, contribuyente, nom_inmueble, cod_catastral, uso, sector FROM inmuebles"  # Modify table name as needed
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error fetching data: {e}")

    def on_tree_select(event):
        nonlocal selected_item  # Use nonlocal to modify the outer variable
        selected_item = my_tree.selection()[0]
        values = my_tree.item(selected_item, "values")

        contribuyenteci.delete(0, ctk.END)
        contribuyenteci.insert(0, values[0])

        contribuyentenombre.delete(0, ctk.END)
        contribuyentenombre.insert(0, values[1])

        inmueble.delete(0, ctk.END)
        inmueble.insert(0, values[2])

        inmueblecod.delete(0, ctk.END)
        inmueblecod.insert(0, values[3])

        uso.set(values[4])
        sector.set(values[5])

        my_tree.unbind("<ButtonRelease-1>")

    def save_changes(selected_item):
        new_values = (
            contribuyenteci.get(),
            contribuyentenombre.get(),
            inmueble.get(),
            inmueblecod.get(),
            uso.get(),
            sector.get()
        )

        try:
            with connection() as conn:
                cursor = conn.cursor()
                sql = '''
                UPDATE inmuebles
                SET ci_contribuyente = ?, contribuyente = ?, nom_inmueble = ?, cod_catastral = ?, uso = ?, sector = ?
                WHERE ci_contribuyente = ? AND cod_catastral = ?
                '''
                cursor.execute(sql, new_values + (my_tree.item(selected_item, "values")[0], my_tree.item(selected_item, "values")[3]))
                conn.commit()
                print("Changes saved successfully!")
                reload_treeview(my_tree)
                my_tree.bind("<ButtonRelease-1>", on_tree_select)

        except Exception as e:
            print(f"Error saving changes: {e}")

    my_tree.bind("<ButtonRelease-1>", on_tree_select)

def inmuebles(window, last_window):
    
    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
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
    
    #Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestion Liquidacion", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    crearliq = ctk.CTkButton(top_frame2, text="Asignar", command=lambda: ifasignar(bottom_frame), font=poppins14bold)
    crearliq.pack(padx=5, pady=5, side="left")

    gestionarliq = ctk.CTkButton(top_frame2, text="Gestionar", command=lambda:ifgestionar(bottom_frame), font=poppins14bold)
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

    my_tree['columns'] = ( 'CI', 'Contribuyete', 'Inmueble', 'Codigo Catastral', 'Monto 1', 'Monto 2', 'Fecha Liquidacion')

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
            sql = 'SELECT * FROM liquidaciones'
            cursor.execute(sql)
            results = cursor.fetchall()

            # Ensure data fits Treeview structure
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during database operation: {e}")

def reload_treeview(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inmuebles")
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")

