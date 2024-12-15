import customtkinter as ctk
from menubar import menubar
from functions import * 
from calendario import open_calendar_popup
from calendario import create_date_range_selector
from rectangle import rectangle
from tkinter import ttk

def consulta(window, last_window):
    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    # Fonts
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12, "bold")

    menubar(window)

    # Frames
    top_frame = ctk.CTkFrame(window, height=80, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=5)

    global top_frame2
    top_frame2 = ctk.CTkFrame(window, height=150, corner_radius=15)
    top_frame2.pack(fill="x", padx=10, pady=5)

    top_frame3 = ctk.CTkFrame(window, height=60, corner_radius=15)
    top_frame3.pack_forget()

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=5, fill="both", expand=True)

    bottom_frame2 = ctk.CTkFrame(window, corner_radius=15, height=60)
    bottom_frame2.pack(padx=10, pady=5, fill="x")

    # Top Frame Content
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")

    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestión Liquidación", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Top Frame 2 Content

    busqueda = ctk.CTkButton(top_frame2, text="Buscar", width=80, font=poppins14bold, command=lambda:  display_search_filter(top_frame3))
    busqueda.pack(padx=10, pady=5, side="left")

    #Bottom Frame Content

    bottom_treeview(bottom_frame)

def display_search_filter(frame):
    
    poppins12 = ("Poppins", 12, "bold")


    top_frame3 = frame
    top_frame3.pack(fill="x", padx=10, pady=5, after=top_frame2)
    
    current_widgets = {"frame": None}

    global searchbtn  # Make it globally accessible
    searchbtn = ctk.CTkButton(top_frame3, text="Buscar", font=poppins12, width=70)
    searchbtn.pack_forget()  # Initially hide the button

    def toggle_entry(switch_name, placeholder_text):
        """Replace the current entry with a new one based on the selected switch."""
        # Deactivate all switches except the current one
        for other_switch_name, other_switch in switches.items():
            if other_switch_name != switch_name:
                other_switch.deselect()

        # Remove current widgets if they exist
        if current_widgets["frame"]:
            current_widgets["frame"].destroy()
            current_widgets["frame"] = None

        # Create new widgets if the switch is activated
        if switches[switch_name].get() == 1:
            
            searchbtn.pack(side="right", pady=10, padx=5)
            
            if switch_name == "Rango Fecha":
                # Create date range selector
                current_widgets["frame"] = ctk.CTkFrame(top_frame3)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")
                create_date_range_selector(current_widgets["frame"])
            else:
                # Create a single entry
                current_widgets["frame"] = ctk.CTkFrame(top_frame3)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")

                new_entry = ctk.CTkEntry(current_widgets["frame"], placeholder_text=placeholder_text, font=poppins12, width=200)
                new_entry.pack(side="left")
        else:
            searchbtn.pack_forget()

    # Switches
    switches = {}
    switch_labels = ["Cedula", "Nombre", "Sector", "Inmueble", "Rango Fecha"]
    placeholders = ["Ingrese Cédula", "Ingrese Nombre", "Ingrese Sector", "Ingrese Inmueble", "Rango Fecha"]

    for label, placeholder in zip(switch_labels, placeholders):
        switch = ctk.CTkSwitch(
            top_frame3,
            text=label,
            font=poppins12,
            command=lambda l=label, p=placeholder: toggle_entry(l, p),
        )
        switch.pack(padx=10, pady=10, side="left")
        switches[label] = switch

def bottom_treeview(frame):
    # BOTTOM FRAME CONTENT  
    treeframe = ctk.CTkFrame(frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)

    # Creating the Treeview frame
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

    # Define the columns
    my_tree['columns'] = (
        'Inmueble', 'Codigo Catastral', 'Uso', 'Contribuyente', 'CI', 'RIF', 'Telefono', 'Correo', 
        'Sector', 'Ubicacion Sector', 'Liquidacion ID', 'Monto 1', 'Monto 2', 'Fecha Liquidacion 1', 'Fecha Liquidacion 2'
    )

    # Set column headers
    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Position the canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')

    try:
        # Database connection and query
        with connection() as conn:
            print("Database connection established.")
            cursor = conn.cursor()

            # SQL query to join the tables and fetch the required data
            sql = '''
                SELECT 
                    inmuebles.id_inmueble,
                    inmuebles.nom_inmueble,
                    inmuebles.cod_catastral,
                    inmuebles.uso,
                    contribuyentes.nombres || ' ' || contribuyentes.apellidos AS contribuyente,
                    contribuyentes.ci_contribuyente,
                    contribuyentes.rif,
                    contribuyentes.telefono,
                    contribuyentes.correo,
                    sectores.nom_sector,
                    sectores.ubic_sector,
                    liquidaciones.id_liquidacion,
                    liquidaciones.monto_1,
                    liquidaciones.monto_2,
                    liquidaciones.fecha_Liquidacion_1,
                    liquidaciones.fecha_Liquidacion_2
                FROM
                    inmuebles
                JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente
                JOIN sectores ON inmuebles.id_sector = sectores.id_sector
                JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble;
            '''
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Query executed successfully, fetched results: {results}")

            # Insert data into Treeview
            for row in results:
                for value in row:
                    print(value) 
                my_tree.insert("", "end", values=(
                    row[1],  # Inmueble name
                    row[2],  # Codigo Catastral
                    row[3],  # Uso
                    row[4],  # Contribuyente
                    row[5],  # CI
                    row[6],  # RIF
                    row[7],  # Telefono
                    row[8],  # Correo
                    row[9],  # Sector
                    row[10], # Ubicacion Sector
                    row[11], # Liquidacion ID
                    row[12], # Monto 1
                    row[13], # Monto 2
                    row[14], # Fecha Liquidacion 1
                    row[15]  # Fecha Liquidacion
                ))

    except Exception as e:
        print(f"Error during database operation: {e}")

