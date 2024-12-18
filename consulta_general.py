import customtkinter as ctk
from menubar import menubar
from functions import * 
from calendario import open_calendar_popup
from calendario import create_date_range_selector
from rectangle import rectangle
from tkinter import ttk

# Global flags
search_filter_shown = False
column_switch_shown = False
search_filter_created = False
column_switches_created = False

def display_column_switches(top_frame4, treeview, original_data):
    global column_switches_created
    if column_switches_created:
        return  # Skip if already created

    # Frame to hold switches
    switches_frame = ctk.CTkFrame(top_frame4, corner_radius=15)
    switches_frame.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    # Dictionary to store the switch states
    column_switches = {}

    # Treeview columns
    columns = [
        'Inmueble', 'Codigo Catastral', 'Uso', 'Contribuyente', 'CI', 'RIF', 
        'Telefono', 'Correo', 'Sector', 'Ubicacion Sector', 
        'Liquidacion ID', 'Monto 1', 'Monto 2', 'Fecha Liquidacion 1', 'Fecha Liquidacion 2'
    ]

    # Create switches in a grid
    max_columns_per_row = 10  # Number of switches per row
    row = 0
    col = 0

    for col_name in columns:
        switch = ctk.CTkSwitch(
            switches_frame,
            text=col_name,
            command=lambda c=col_name: toggle_column(column_switches, c)
        )
        switch.grid(row=row, column=col, padx=5, pady=5)  # Use grid layout for multi-row arrangement
        column_switches[col_name] = switch
        switch.select()  # Enable all columns by default

        col += 1
        if col >= max_columns_per_row:  # Move to the next row
            col = 0
            row += 1

    # Refresh button (place this next to the switches)
    refresh_button = ctk.CTkButton(
        switches_frame, 
        text="Refresh Treeview", 
        command=lambda: refresh_treeview(treeview, column_switches)
    )
    refresh_button.grid(row=row + 1, column=0, columnspan=max_columns_per_row, pady=10)  # Place the button below the switches

    column_switches_created = True  # Mark column switches as created

def toggle_column(column_switches, column):
    # Toggle the visibility of the column
    column_switches[column] = not column_switches[column]
    print(f"Column {column} visibility is now {column_switches[column]}")

def refresh_treeview(treeview, column_switches):
    # Clear the Treeview before updating with new data
    for item in treeview.get_children():
        treeview.delete(item)

    # Select columns that are marked as visible in the column_switches
    selected_columns = [col for col, is_visible in column_switches.items() if is_visible]
    
    # If no columns are selected, show an error and stop the function
    if not selected_columns:
        print("No columns selected. Please select at least one column.")
        return

    # Map the user-friendly column names to actual database fields
    db_columns = {
        'Inmueble': 'inmuebles.nom_inmueble',
        'Codigo Catastral': 'inmuebles.cod_catastral',
        'Uso': 'inmuebles.uso',
        'Contribuyente': "contribuyentes.nombres || ' ' || contribuyentes.apellidos",
        'CI': 'contribuyentes.ci_contribuyente',
        'RIF': 'contribuyentes.rif',
        'Telefono': 'contribuyentes.telefono',
        'Correo': 'contribuyentes.correo',
        'Sector': 'sectores.nom_sector',
        'Ubicacion Sector': 'sectores.ubic_sector',
        'Liquidacion ID': 'liquidaciones.id_liquidacion',
        'Monto 1': 'liquidaciones.monto_1',
        'Monto 2': 'liquidaciones.monto_2',
        'Fecha Liquidacion 1': 'liquidaciones.fecha_liquidacion_1',
        'Fecha Liquidacion 2': 'liquidaciones.fecha_liquidacion_2'
    }

    # Map the selected columns to the actual database fields for the SQL query
    selected_db_columns = [db_columns[col] for col in selected_columns]

    # Construct the SQL query dynamically based on selected columns
    query = f"SELECT {', '.join(selected_db_columns)} FROM inmuebles " \
            f"JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente " \
            f"JOIN sectores ON inmuebles.id_sector = sectores.id_sector " \
            f"JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble"

    print(f"Executing Query: {query}")  # Debugging: Show the query being executed

    # Try to fetch the data from the database
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filtered_data = cursor.fetchall()

            # Update the Treeview columns and insert the new data into the Treeview
            treeview["columns"] = selected_columns
            for col in selected_columns:
                treeview.heading(col, text=col)
                treeview.column(col, anchor="center", width=100)

            # Insert the rows fetched from the query into the Treeview
            for row in filtered_data:
                treeview.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during query execution: {e}")

def toggle_top_frame_visibility(frame_to_show, frame_to_hide):
    """Toggle visibility of the frames."""
    if frame_to_show.winfo_ismapped():
        frame_to_show.pack_forget()  # Hide it
    else:
        frame_to_show.pack(fill="x", padx=10, pady=5, after=top_frame2)  # Show it
        frame_to_hide.pack_forget()  # Hide the other frame

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

    global top_frame3
    top_frame3 = ctk.CTkFrame(window, height=150, corner_radius=15)
    top_frame4 = ctk.CTkFrame(window, height=150, corner_radius=15)

    top_frame3.pack_forget()  # Hide by default
    top_frame4.pack_forget()  # Hide by default

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

    # Bottom Frame Content
    my_tree, original_data = bottom_treeview(bottom_frame)

    # Top Frame 2 Content
    busqueda = ctk.CTkButton(top_frame2, text="Buscar", width=80, font=poppins14bold, command=lambda: toggle_top_frame_visibility(top_frame3, top_frame4))
    busqueda.pack(padx=10, pady=5, side="left")
    
    show_filter_btn = ctk.CTkButton(top_frame2, text="Show Filter", width=100, font=poppins14bold, command=lambda: toggle_top_frame_visibility(top_frame4, top_frame3))
    show_filter_btn.pack(padx=10, pady=5, side="left")

    # Add search filter UI to top_frame3
    display_search_filter(top_frame3, my_tree, original_data)

    # Add column switch UI to top_frame4
    display_column_switches(top_frame4, my_tree, original_data)

# Add a global variable to track if the filter has been created
def display_search_filter(frame, treeview, original_data):
    global search_filter_created
    if search_filter_created:
        return  # Avoid creating widgets multiple times

    poppins12 = ("Poppins", 12, "bold")
    
    top_frame3 = frame
    top_frame3.pack(fill="x", padx=10, pady=5, after=top_frame2)

    current_widgets = {"frame": None}

    global searchbtn
    searchbtn = ctk.CTkButton(top_frame3, text="Buscar", font=poppins12, width=70)
    searchbtn.pack_forget()

    def toggle_entry(switch_name, placeholder_text):
        for other_switch_name, other_switch in switches.items():
            if other_switch_name != switch_name:
                other_switch.deselect()

        if current_widgets["frame"]:
            current_widgets["frame"].destroy()
            current_widgets["frame"] = None

        if switches[switch_name].get() == 1:
            searchbtn.pack(side="right", pady=10, padx=5)
            
            if switch_name == "Rango Fecha":
                current_widgets["frame"] = ctk.CTkFrame(top_frame3)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")
                create_date_range_selector(current_widgets["frame"])
            else:
                current_widgets["frame"] = ctk.CTkFrame(top_frame3)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")

                new_entry = ctk.CTkEntry(current_widgets["frame"], placeholder_text=placeholder_text, font=poppins12, width=200)
                new_entry.pack(side="left")
        else:
            searchbtn.pack_forget()

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

    search_filter_created = True

def bottom_treeview(frame):
    # Treeview frame
    treeframe = ctk.CTkFrame(frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)

    # Treeview container
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
    columns = [
        'Inmueble', 'Codigo Catastral', 'Uso', 'Contribuyente', 'CI', 'RIF', 
        'Telefono', 'Correo', 'Sector', 'Ubicacion Sector', 
        'Liquidacion ID', 'Monto 1', 'Monto 2', 'Fecha Liquidacion 1', 'Fecha Liquidacion 2'
    ]
    my_tree["columns"] = columns

    # Set column headers
    for col in columns:
        my_tree.heading(col, text=col)
        my_tree.column(col, anchor="center", width=100)

    # Fetch data
    original_data = []
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' SELECT 
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
        JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble '''
            cursor.execute(sql)
            original_data = cursor.fetchall()

            print(f"Fetched {len(original_data)} rows from the database.")
            for row in original_data:
                print(row) 

            # Insert all data into Treeview initially
            for row in original_data:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during database operation: {e}")

    return my_tree, original_data  # Return both my_tree and original_data
