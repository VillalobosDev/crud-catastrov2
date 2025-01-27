import customtkinter as ctk
from modulos2.menubar import menubar
from functions.functions import * 
from tkinter import ttk
from functions.rectangle import rectangle
from tkinter import messagebox

def inmuebles(window, last_window):
    global busquedabtn, busquedainm, refrescartabla
    
    for widget in window.winfo_children():
        widget.destroy()
        
    def toggle_columns():
        if comer_rec.get():
            my_tree["displaycolumns"] = ('Cédula', 'Contribuyente', 'Código Catastral', 'Uso', 'Ubicación', 'Sector')
            comer_rec.configure(text="Recidencial")
            loaddata("Recidencial")
        else:
            my_tree["displaycolumns"] = ('Cédula', 'Contribuyente', 'Inmueble', 'Código Catastral', 'Uso', 'Ubicación', 'Sector')
            comer_rec.configure(text="Comercial")
            loaddata("Comercial")
    
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


    
    comer_rec = ctk.CTkSwitch(top_frame2, text="Comerciales", font=poppins14bold, command=toggle_columns)
    comer_rec.pack(padx=5, pady=5, side="left")

    refrescartabla = ctk.CTkButton(top_frame2, text="🔁", font=poppins14bold, width=30, command=lambda: loaddata("Comercial"))
    refrescartabla.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cédula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    # Contenido del bottom frame

    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)

    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 12, "bold"))

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ('Cédula', 'Contribuyente', 'Inmueble', 'Código Catastral', 'Uso', 'Ubicación', 'Sector')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')

    def loaddata(uso="Comercial"):
        try:
            with connection() as conn:
                print("Database connection established.")
                cursor = conn.cursor()
                sql = """
                SELECT c.v_e || "-" || c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, i.ubicacion, s.nom_sector AS sector
                FROM inmuebles i
                JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
                JOIN sectores s ON i.id_sector = s.id_sector
                WHERE i.uso = ?
                ORDER BY c.ci_contribuyente ASC
                """
                cursor.execute(sql, (uso,))
                results = cursor.fetchall()

                # Clear existing rows
                for row in my_tree.get_children():
                    my_tree.delete(row)

                # Ensure data fits Treeview structure
                for row in results:
                    my_tree.insert("", "end", values=row)

        except Exception as e:
            print(f"Error during database operation: {e}")

    # Load initial data as "Comercial"
    loaddata("Comercial")
    return window



def reload_treeview(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """
            SELECT i.id_inmueble, c.v_e || "-" || c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, i.ubicacion, s.nom_sector AS sector
            FROM inmuebles i
            JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
            JOIN sectores s ON i.id_sector = s.id_sector
            ORDER BY c.ci_contribuyente ASC
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
            SELECT c.v_e || "-" || c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente, i.nom_inmueble, i.cod_catastral, i.uso, i.ubicacion, s.nom_sector AS sector
            FROM inmuebles i
            JOIN contribuyentes c ON i.id_contribuyente = c.id_contribuyente
            JOIN sectores s ON i.id_sector = s.id_sector
            WHERE c.ci_contribuyente = ?
            ORDER BY c.ci_contribuyente ASC
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