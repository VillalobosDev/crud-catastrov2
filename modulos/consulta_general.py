import customtkinter as ctk
from modulos.menubar import menubar
from functions.functions import * 
from functions.calendario import create_date_range_selector
from config.config import centrar_ventana
from tkinter import ttk
from tkinter import filedialog
from functions.rango_fecha import *
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
from tkinter import messagebox
import tkinter

# Global flags
search_filter_shown = False
column_switch_shown = False
search_filter_created = False
column_switches_created = False

# Global variable to store the column order
COLUMN_ORDER = [
    'Contribuyente',
    'Cedula',
    'Sector',
    'Cod-Sector',
    'Cod-Catastral',
    'Monto Solicitud',
    'Pago Solicitud',
    'Monto Impuesto-Ocup',
    'Pago Impuesto-Ocup',
    'Monto Inm-Urbano',
    'Pago Inm-Urbano',
    'Inmueble',
    'Uso',
    'RIF',
    'Telefono',
    'Correo',
]
#######

# Global dictionary to store the switch states
column_switch_states = {
    'Contribuyente': True,
    'Cedula': True,
    'Sector': True,
    'Cod-Sector': True,
    'Cod-Catastral': True,
    'Monto Solicitud': True,
    'Pago Solicitud': True,
    'Monto Impuesto-Ocup': True,
    'Pago Impuesto-Ocup': True,
    'Monto Inm-Urbano': True,
    'Pago Inm-Urbano': True,
    'Inmueble': True,
    'Uso': True,
    'RIF': True,
    'Telefono': True,
    'Correo': True
}

def display_column_switches(top_frame4, treeview, original_data, window):
    poppins12 = ("Poppins", 12, "bold")
    poppins20 = ("Poppins", 20, "bold")  
    poppins16 = ("Poppins", 16, "bold")     

    global column_switches_created
    column_switches_created = False
    if column_switches_created:
        print("Already exist")
        return  # Skip if already created

    # Frame to hold switches
    toplevel = ctk.CTkToplevel(window)
    toplevel.title("Filtros")
    toplevel.geometry("800x400")
    toplevel.grab_set()
    toplevel.resizable(False, False)
    centrar_ventana(toplevel, 800, 500)

    switches_frame = ctk.CTkFrame(toplevel, corner_radius=15)
    switches_frame.pack(pady=5, padx=5, fill="both", expand=True)
    
    button_frame = ctk.CTkFrame(switches_frame)
    button_frame.pack(side="bottom", fill="x", padx=5, pady=5)
    
    text_top = ctk.CTkLabel(switches_frame, text="Filtros de Busqueda", font=poppins20)
    text_top.pack(pady=10, padx=10, side="top")

    # Dictionary to store the switch widgets
    column_switches = {}

    # Treeview columns
    columns = [
        'Inmueble', 'Cod-Catastral', 'Uso', 'Contribuyente', 'CI', 'RIF', 
        'Telefono', 'Correo', 'Sector', 'Uso',
         
        'Monto Liquidado Inmueble', 'Monto Derecho-Ocupacion', 'Fecha de Pago Solicitud', 'Fecha de Pago Inmueble'
    ]

    # Define a fixed width for all frames
    frame_width = 186.5

    # Group 1: Inmueble, Cod-Catastral, Uso
    group1_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group1_frame.pack(side="left", padx=5, pady=5, fill="y")
    group1_frame.pack_propagate(False)
    text_1= ctk.CTkLabel(group1_frame, text="Inmuebles", font=poppins16)
    text_1.pack(pady=10, side="top")


    for col_name in ['Inmueble', 'Cod-Catastral', 'Uso', 'RIF']:
        switch = ctk.CTkSwitch(
            group1_frame,
            text=col_name,
            font=poppins12,
            command=lambda c=col_name: toggle_column(column_switches, c)
        )
        switch.pack(side="top", anchor="w", padx=5, pady=20)
        column_switches[col_name] = switch

        # Set the switch state based on the global dictionary
        if column_switch_states[col_name]:
            switch.select()
        else:
            switch.deselect()

    # Group 2: Contribuyente, CI, RIF, Telefono, Correo
    group2_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group2_frame.pack(side="left", padx=5, pady=5, fill="y")
    group2_frame.pack_propagate(False)
    text_2= ctk.CTkLabel(group2_frame, text="Contribuyentes", font=poppins16)
    text_2.pack(pady=10, side="top")


    for col_name in ['Contribuyente', 'Cedula', 'Telefono', 'Correo']:
        switch = ctk.CTkSwitch(
            group2_frame,
            text=col_name,
            font=poppins12,
            command=lambda c=col_name: toggle_column(column_switches, c)
        )
        switch.pack(side="top", anchor="w", padx=5, pady=20)
        column_switches[col_name] = switch

        # Set the switch state based on the global dictionary
        if column_switch_states[col_name]:
            switch.select()
        else:
            switch.deselect()

    # Group 3: Sector, Cod-Sector
    group3_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group3_frame.pack(side="left", padx=5, pady=5, fill="y")
    group3_frame.pack_propagate(False)
    text_3= ctk.CTkLabel(group3_frame, text="Sectores", font=poppins16)
    text_3.pack(pady=10, side="top")


    for col_name in ['Sector', 'Cod-Sector']:
        switch = ctk.CTkSwitch(
            group3_frame,
            text=col_name,
            font=poppins12,
            command=lambda c=col_name: toggle_column(column_switches, c)
        )
        switch.pack(side="top", anchor="w", padx=5, pady=20)
        column_switches[col_name] = switch

        # Set the switch state based on the global dictionary
        if column_switch_states[col_name]:
            switch.select()
        else:
            switch.deselect()

    # Group 4: Liquidacion ID, Monto Liquidado Inmueble, Monto Derecho-Ocupación, Fecha de Pago Solicitud, Fecha de Pago Inmueble
    group4_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group4_frame.pack(side="left", padx=5, pady=5, fill="y")
    group4_frame.pack_propagate(False)
    text_4= ctk.CTkLabel(group4_frame, text="Liquidaciones", font=poppins16)
    text_4.pack(pady=10, side="top")

    
#############################################################################'Monto Liquidado Inmueble'
    for col_name in ['Monto Solicitud', 'Pago Solicitud', 'Monto Impuesto-Ocup',  'Pago Impuesto-Ocup', 'Monto Inm-Urbano', 'Pago Inm-Urbano']:
        switch = ctk.CTkSwitch(
            group4_frame,
            text=col_name,
            font=poppins12,
            command=lambda c=col_name: toggle_column(column_switches, c)
        )
        switch.pack(side="top", anchor="w", padx=5, pady=20)
        column_switches[col_name] = switch

        # Set the switch state based on the global dictionary
        if column_switch_states[col_name]:
            switch.select()
        else:
            switch.deselect()   
    
    

    year_menu = ctk.CTkOptionMenu(
        button_frame,
        values=["2023", "2024", "2025", "2026", "2027", "2028"],
        values=["2023", "2024", "2025", "2026", "2027", "2028"],
        font=poppins12,
    )
    year_menu.set("Seleccionar Año")
    year_menu.pack(side="left", padx=10, pady=10)

    def close_and_refresh(toplevel, treeview, column_switches):
        if year_menu.get() == "Seleccionar Año":
            messagebox.showwarning("Advertencia", "Debe seleccionar un año.")
            return
        toplevel.destroy()  # Close the toplevel window
        refresh_treeview(treeview, column_switches, year_menu.get())  # Refresh the treeview

    refresh_button = ctk.CTkButton(
        button_frame,
        text="Aplicar",
        font=poppins12,
        command=lambda: close_and_refresh(toplevel, treeview, column_switches)
    )
    refresh_button.pack(side="right", padx=10, pady=10)  # Place the button on the right inside the `button_frame`



    column_switches_created = True  # Mark column switches as created



def toggle_column(column_switches, column):
    # Toggle the visibility of the column
    switch = column_switches[column]
    column_switch_states[column] = not column_switch_states[column]
    if column_switch_states[column]:
        switch.select()
    else:
        switch.deselect()
    print(f"Column {column} visibility is now {column_switch_states[column]}")



# Llama a esta función después de configurar las columnas en el Treeview




def toggle_top_frame_visibility(frame_to_show, frame_to_hide):
    """Toggle visibility of the frames."""
    if frame_to_show.winfo_ismapped():
        frame_to_show.pack_forget()  # Hide it
    else:
        frame_to_show.pack(fill="x", padx=10, pady=5, after=top_frame2)  # Show it after top_frame2
        frame_to_hide.pack_forget()
        
        
def consulta(window, last_window):
    for widget in window.winfo_children():
        widget.destroy()

    global search_filter_created
    search_filter_created = False

    global column_switch_states
    column_switch_states = {col: True for col in COLUMN_ORDER}


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

    # Top Frame Content
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")

    window_title = ctk.CTkLabel(top_frame, text="Consulta General", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    # Bottom Frame Content
    my_tree, original_data = bottom_treeview(bottom_frame)

    # Top Frame 2 Content
    busqueda = ctk.CTkButton(top_frame2, text="Buscar", width=80, font=poppins14bold, command=lambda: toggle_top_frame_visibility(top_frame3, top_frame4))
    busqueda.pack(padx=10, pady=5, side="left")
    
    show_filter_btn = ctk.CTkButton(top_frame2, text="Filtros", width=100, font=poppins14bold, command=lambda: display_column_switches(top_frame4, my_tree, original_data, window))
    show_filter_btn.pack(padx=10, pady=5, side="left")
    

    ##################################################################################################
    
    export = ctk.CTkButton(top_frame2, text="Exportar a Excel", font=poppins12, command=lambda: export_treeview_to_xlsx(my_tree, "consulta_general.xlsx"))
    export.pack(side="right", padx=10, pady=5)

    

    searchbtn = display_search_filter(top_frame3, my_tree, original_data, bottomframe = bottom_frame)
    searchbtn = display_search_filter(top_frame3, my_tree, original_data, bottomframe = bottom_frame)
    # print(type(searchbtn)) 

    # create_date_range_selector(top_frame4, searchbtn, my_tree, original_data)



def display_search_filter(frame, my_tree, original_data, bottomframe):
def display_search_filter(frame, my_tree, original_data, bottomframe):
    global search_filter_created
    global selected_columns
    
    
    if search_filter_created:
        return  # Avoid creating widgets multiple times

    poppins12 = ("Poppins", 12, "bold")
    
    top_frame3 = frame

    current_widgets = {"frame": None}

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
                create_date_range_selector(current_widgets["frame"], searchbtn, my_tree, original_data)
            else:
                current_widgets["frame"] = ctk.CTkFrame(top_frame3)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")

                new_entry = ctk.CTkEntry(current_widgets["frame"], placeholder_text=placeholder_text, font=poppins12, width=200)
                new_entry.pack(side="left")

                if switch_name == "Cedula":
                    searchbtn.configure(command=lambda: cedula_search(my_tree, original_data, new_entry, bottomframe))
                    searchbtn.configure(command=lambda: cedula_search(my_tree, original_data, new_entry, bottomframe))
                elif switch_name == "Nombre":
                    searchbtn.configure(command=lambda: nombre_search(my_tree, original_data, new_entry, bottomframe))
                    searchbtn.configure(command=lambda: nombre_search(my_tree, original_data, new_entry, bottomframe))
                elif switch_name == "Sector":
                    searchbtn.configure(command=lambda: sector_search(my_tree, original_data, new_entry, bottomframe))
                    searchbtn.configure(command=lambda: sector_search(my_tree, original_data, new_entry, bottomframe))
                elif switch_name == "Inmueble":
                    searchbtn.configure(command=lambda: inmueble_search(my_tree, original_data, new_entry, bottomframe))
                    searchbtn.configure(command=lambda: inmueble_search(my_tree, original_data, new_entry, bottomframe))
        else:
            if not any(switch.get() == 1 for switch in switches.values()):
                searchbtn.configure(command=lambda: fetch_all_records(my_tree, original_data))


    switches = {}
    switch_labels = ["Cedula", "Nombre", "Sector", "Inmueble", "Rango Fecha"]
    placeholders = ["Ingrese Cedula", "Ingrese Nombre", "Ingrese Sector", "Ingrese Inmueble", "Rango Fecha"]

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

    ########################################################################################################


    

    ########################################################################################################

    return searchbtn

def extract_year(date_str):
    try:
        return date_str.split('-')[-1]
    except Exception as e:
        print(f"Error extracting year from date: {e}")
        return None
def extract_year(date_str):
    try:
        return date_str.split('-')[-1]
    except Exception as e:
        print(f"Error extracting year from date: {e}")
        return None

def refresh_treeview(treeview, column_switches, year): 
    # Clear the Treeview before updating with new data
    for item in treeview.get_children():
        treeview.delete(item)

    # Select columns that are marked as visible in the column_switches
    selected_columns = []
    for col in COLUMN_ORDER:
        try:
            if column_switches[col].get() == 1:
                selected_columns.append(col)
        except KeyError as e:
            print(f"KeyError: {e} for column {col}")
    
    # If no columns are selected, show an error and stop the function
    if not selected_columns:
        print("No columns selected. Please select at least one column.")
        return

    # Map the user-friendly column names to actual database fields
    db_columns = {
        'Contribuyente': "contribuyentes.nombres",
        'Cedula': 'contribuyentes.v_e || "-" || contribuyentes.ci_contribuyente',
        'Sector': 'sectores.nom_sector',
        'Cod-Sector': 'sectores.cod_sector',
        'Cod-Catastral': 'inmuebles.cod_catastral',
        'Monto Solicitud': 'liquidaciones.monto_1',
        'Pago Solicitud': 'liquidaciones.fecha_Liquidacion_1',
        'Monto Impuesto-Ocup': 'liquidaciones.monto_2',
        'Pago Impuesto-Ocup': 'liquidaciones.fecha_Liquidacion_2',
        'Monto Inm-Urbano': 'liquidaciones.monto_3',
        'Pago Inm-Urbano': 'liquidaciones.fecha_Liquidacion_3',
        'Inmueble': 'inmuebles.nom_inmueble',
        'Uso': 'inmuebles.uso',
        'RIF': 'inmuebles.j || "-" || inmuebles.rif',
        'Telefono': 'contribuyentes.telefono',
        'Correo': 'contribuyentes.correo',
    }

    # Map the selected columns to the actual database fields for the SQL query
    selected_db_columns = [db_columns[col] for col in selected_columns]

    # Construct the SQL query dynamically based on selected columns
    query = f"SELECT {', '.join(selected_db_columns)} FROM inmuebles " \
            f"JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente " \
            f"JOIN sectores ON inmuebles.id_sector = sectores.id_sector " \
            f"JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble " \
            f"WHERE extract_year(liquidaciones.fecha_Liquidacion_1) = ? " \
            f"ORDER BY contribuyentes.ci_contribuyente ASC"
            f"WHERE extract_year(liquidaciones.fecha_Liquidacion_1) = ? " \
            f"ORDER BY contribuyentes.ci_contribuyente ASC"

    print(f"Executing Query: {query}\n\n\n")  # Debugging: Show the query being executed
    print(f"Executing Query: {query}\n\n\n")  # Debugging: Show the query being executed
    
    treeview["columns"] = selected_columns
            
    for col in selected_columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center")

    # Try to fetch the data from the database
    try:
        with connection() as conn:
            conn.create_function("extract_year", 1, extract_year)
            conn.create_function("extract_year", 1, extract_year)
            cursor = conn.cursor()
            cursor.execute(query, (year,))
            filtered_data = cursor.fetchall()

            print(f"Fetched {len(filtered_data)} rows from the database.")  # Debugging: Show the number of rows fetched

            print(f"Fetched {len(filtered_data)} rows from the database.")  # Debugging: Show the number of rows fetched

            # Update the Treeview columns and insert the new data into the Treeview

            # Insert the rows fetched from the query into the Treeview
            # Print headers of the tree
            headers = treeview["columns"]
            print("Tree Headers in refresh_treeview:", headers)
            for header in headers:
                print(header)
                # Find the indices of the columns to check for empty values
                try:
                    pago_impuesto_ocup_index = headers.index('Pago Impuesto-Ocup')
                    pago_inm_urbano_index = headers.index('Pago Inm-Urbano')
                except ValueError as e:
                    print(f"Error: {e}")
                    return

                for i, row in enumerate(filtered_data):
                    # Check if the specified columns are empty
                    if not row[pago_impuesto_ocup_index] or not row[pago_inm_urbano_index]:
                        treeview.insert("", "end", values=row, tags=('red',))
                    else:
                        tag = 'gray' if i % 2 == 0 else 'default'
                        treeview.insert("", "end", values=row, tags=(tag,))

                # Apply tag configuration for red and gray rows
                treeview.tag_configure('red', background='red')
                treeview.tag_configure('gray', background='#f0f0f0')
                treeview.tag_configure('default', background='white')
            # Print headers of the tree
            headers = treeview["columns"]
            print("Tree Headers in refresh_treeview:", headers)
            for header in headers:
                print(header)
                # Find the indices of the columns to check for empty values
                try:
                    pago_impuesto_ocup_index = headers.index('Pago Impuesto-Ocup')
                    pago_inm_urbano_index = headers.index('Pago Inm-Urbano')
                except ValueError as e:
                    print(f"Error: {e}")
                    return

                for i, row in enumerate(filtered_data):
                    # Check if the specified columns are empty
                    if not row[pago_impuesto_ocup_index] or not row[pago_inm_urbano_index]:
                        treeview.insert("", "end", values=row, tags=('red',))
                    else:
                        tag = 'gray' if i % 2 == 0 else 'default'
                        treeview.insert("", "end", values=row, tags=(tag,))

                # Apply tag configuration for red and gray rows
                treeview.tag_configure('red', background='red')
                treeview.tag_configure('gray', background='#f0f0f0')
                treeview.tag_configure('default', background='white')
    
    except Exception as e:
        print(f"Error during query execution: {e}")



def fetch_data_by_year_range(treeview, year):
    # Clear the Treeview before updating with new data
    for item in treeview.get_children():
        treeview.delete(item)

    # Updated SQL query filtering by year equality
    query = f'''
    SELECT 
        contribuyentes.nombres,
        contribuyentes.v_e || "-" || contribuyentes.ci_contribuyente AS cedula_completa,
        sectores.nom_sector,
        sectores.cod_sector,
        inmuebles.cod_catastral,
        liquidaciones.monto_1,
        liquidaciones.fecha_Liquidacion_1,
        liquidaciones.monto_2,
        liquidaciones.fecha_Liquidacion_2,
        liquidaciones.monto_3,
        liquidaciones.fecha_Liquidacion_3,
        inmuebles.nom_inmueble,
        inmuebles.uso,
        inmuebles.j || "-" || inmuebles.rif,
        contribuyentes.telefono,
        contribuyentes.correo
    FROM
        inmuebles
    JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente
    JOIN sectores ON inmuebles.id_sector = sectores.id_sector
    JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble 
    WHERE strftime('%Y', liquidaciones.fecha_Liquidacion_1) = ?
    ORDER BY contribuyentes.ci_contribuyente ASC
    '''
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (year,))
            data = cursor.fetchall()
            print(f"Fetched {len(data)} rows for year {year}.")
            for row in data:
                treeview.insert("", "end", values=row)
    except Exception as e:
        print(f"Error during database operation: {e}")

def bottom_treeview(frame):
    # Treeview frame
    treeframe = ctk.CTkFrame(frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)

        # Treeview container
        frame_tree = ctk.CTkScrollableFrame(treeframe, fg_color='white', width=580, height=360, orientation="horizontal")
        frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
        style.configure("Custom.Treeview.Heading", font=("Poppins", 12, "bold"))

        my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
        my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    # Scrollbar
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

        # Use the global COLUMN_ORDER variable
        my_tree["columns"] = COLUMN_ORDER

        for col in COLUMN_ORDER:
            my_tree.heading(col, text=col)
            my_tree.column(col, anchor="center", width=200)

    # Fetch data
    original_data = []
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' SELECT 
            contribuyentes.nombres || ' ' || contribuyentes.apellidos AS contribuyente,
            contribuyentes.v_e || "-" || contribuyentes.ci_contribuyente AS cedula_completa,
            sectores.nom_sector,
            sectores.cod_sector,
            inmuebles.cod_catastral,
            liquidaciones.monto_1,
            liquidaciones.fecha_Liquidacion_1,
            liquidaciones.monto_2,
            liquidaciones.fecha_Liquidacion_2,
            liquidaciones.monto_3,
            liquidaciones.fecha_Liquidacion_3,
            inmuebles.nom_inmueble,
            inmuebles.uso,
            inmuebles.j || "-" || inmuebles.rif,
            contribuyentes.telefono,
            contribuyentes.correo
            FROM
            inmuebles
            JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente
            JOIN sectores ON inmuebles.id_sector = sectores.id_sector
            JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble 
            ORDER BY contribuyentes.ci_contribuyente ASC
            ORDER BY contribuyentes.ci_contribuyente ASC
            '''
            cursor.execute(sql)
            original_data = cursor.fetchall()

            print(f"Fetched {len(original_data)} rows from the database.")

            # Insert all data into Treeview initially
            # Clear the Treeview before inserting new data
            for item in my_tree.get_children():
                my_tree.delete(item)

            headers = my_tree["columns"]
            print("Tree Headers in bottom_treeview:")
            for header in headers:
                print(header)
                # Find the indices of the columns to check for empty values
                try:
                    pago_impuesto_ocup_index = headers.index('Pago Impuesto-Ocup')
                    pago_inm_urbano_index = headers.index('Pago Inm-Urbano')
                except ValueError as e:
                    print(f"Error: {e}")
                    return

                for i, row in enumerate(original_data):
                    # Check if the specified columns are empty
                    if not row[pago_impuesto_ocup_index] or not row[pago_inm_urbano_index]:
                        my_tree.insert("", "end", values=row, tags=('red',))
                    else:
                        tag = 'gray' if i % 2 == 0 else 'default'
                        my_tree.insert("", "end", values=row, tags=(tag,))

                # Apply tag configuration for red and gray rows
                my_tree.tag_configure('red', background='red')
                my_tree.tag_configure('gray', background='#f0f0f0')
                my_tree.tag_configure('default', background='white')
            # Clear the Treeview before inserting new data
            for item in my_tree.get_children():
                my_tree.delete(item)

            headers = my_tree["columns"]
            print("Tree Headers in bottom_treeview:")
            for header in headers:
                print(header)
                # Find the indices of the columns to check for empty values
                try:
                    pago_impuesto_ocup_index = headers.index('Pago Impuesto-Ocup')
                    pago_inm_urbano_index = headers.index('Pago Inm-Urbano')
                except ValueError as e:
                    print(f"Error: {e}")
                    return

                for i, row in enumerate(original_data):
                    # Check if the specified columns are empty
                    if not row[pago_impuesto_ocup_index] or not row[pago_inm_urbano_index]:
                        my_tree.insert("", "end", values=row, tags=('red',))
                    else:
                        tag = 'gray' if i % 2 == 0 else 'default'
                        my_tree.insert("", "end", values=row, tags=(tag,))

                # Apply tag configuration for red and gray rows
                my_tree.tag_configure('red', background='red')
                my_tree.tag_configure('gray', background='#f0f0f0')
                my_tree.tag_configure('default', background='white')

    except Exception as e:
        print(f"Error during database operation: {e}")

    return my_tree, original_data  # Return both my_tree and original_data



def cedula_search(my_tree, original_data, cedula_entry, bottomframe):
def cedula_search(my_tree, original_data, cedula_entry, bottomframe):
    """Filter treeview data based on Cedula."""
    cedula_value = cedula_entry.get().strip()
    if not cedula_value:
        print("Cedula field is empty.")
        return

    # Print headers of the tree
    headers = my_tree["columns"]
    print("Tree Headers:", headers)

    # Print data in the tree
    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])
    # print("Tree Data:", tree_data)
    # print("Tree Data:", tree_data)

    # Print original_data
    print("Original Data:", original_data)

    # Find the index of the Cedula column in the tree headers
    try:
        cedula_index = headers.index('Cedula')
    except ValueError:
        print("Cedula column not found in tree headers.")
        return

    # Filter the data based on the entered Cedula value
    filtered_data = [row for row in tree_data if cedula_value in str(row[cedula_index])]
    
    if not filtered_data:
        messagebox.showinfo("No Results", "No se encontraron resultados para la búsqueda.")
        print("No results found for the search.")
        cedula_entry.delete(0, 'end')
        my_tree, original_data = bottom_treeview(bottomframe, my_tree)
        return
    
    if not filtered_data:
        messagebox.showinfo("No Results", "No se encontraron resultados para la búsqueda.")
        print("No results found for the search.")
        cedula_entry.delete(0, 'end')
        my_tree, original_data = bottom_treeview(bottomframe, my_tree)
        return
    # Print filtered data
    print("Filtered Data:", filtered_data)

    # Update Treeview
    fetch_all_records(my_tree, filtered_data)



def fetch_all_records(tree, data):
    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Print headers of the tree
    headers = tree["columns"]
    print("Tree Headers in fetch_all_records:", headers)

    # Check if the specified columns are present
    try:
        pago_impuesto_ocup_index = headers.index('Pago Impuesto-Ocup')
        pago_inm_urbano_index = headers.index('Pago Inm-Urbano')
    except ValueError as e:
        print(f"Error: {e}")
        messagebox.showinfo("No Results", "No se encontraron las columnas 'Pago Impuesto-Ocup' o 'Pago Inm-Urbano'.")
        return

    # Insert the rows fetched from the query into the Treeview
    for i, row in enumerate(data):
        # Check if the specified columns are None or empty
        if row[pago_impuesto_ocup_index] is None or row[pago_inm_urbano_index] is None or row[pago_impuesto_ocup_index] == 'None' or row[pago_inm_urbano_index] == 'None' or not row[pago_impuesto_ocup_index] or not row[pago_inm_urbano_index]:
            tree.insert("", "end", values=row, tags=('red',))
        else:
            tag = 'gray' if i % 2 == 0 else 'default'
            tree.insert("", "end", values=row, tags=(tag,))

    # Apply tag configuration for red and gray rows
    tree.tag_configure('red', background='red')
    tree.tag_configure('gray', background='#f0f0f0')
    tree.tag_configure('default', background='white')
    # Print headers of the tree
    headers = tree["columns"]
    print("Tree Headers in fetch_all_records:", headers)

    # Check if the specified columns are present
    try:
        pago_impuesto_ocup_index = headers.index('Pago Impuesto-Ocup')
        pago_inm_urbano_index = headers.index('Pago Inm-Urbano')
    except ValueError as e:
        print(f"Error: {e}")
        messagebox.showinfo("No Results", "No se encontraron las columnas 'Pago Impuesto-Ocup' o 'Pago Inm-Urbano'.")
        return

    # Insert the rows fetched from the query into the Treeview
    for i, row in enumerate(data):
        # Check if the specified columns are None or empty
        if row[pago_impuesto_ocup_index] is None or row[pago_inm_urbano_index] is None or row[pago_impuesto_ocup_index] == 'None' or row[pago_inm_urbano_index] == 'None' or not row[pago_impuesto_ocup_index] or not row[pago_inm_urbano_index]:
            tree.insert("", "end", values=row, tags=('red',))
        else:
            tag = 'gray' if i % 2 == 0 else 'default'
            tree.insert("", "end", values=row, tags=(tag,))

    # Apply tag configuration for red and gray rows
    tree.tag_configure('red', background='red')
    tree.tag_configure('gray', background='#f0f0f0')
    tree.tag_configure('default', background='white')


def nombre_search(my_tree, original_data, name_entry, bottomframe):
def nombre_search(my_tree, original_data, name_entry, bottomframe):
    """Filter treeview data based on Nombre (Name)."""
    name_value = name_entry.get().strip()
    if not name_value:
        print("Name field is empty.")
        return

    # Print headers of the tree
    headers = my_tree["columns"]
    print("Tree Headers:", headers)

    # Print data in the tree
    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])
    # print("Tree Data:", tree_data)

    # Print original_data
    print("Original Data:", original_data)

    # Find the index of the Contribuyente column in the tree headers
    try:
        contribuyente_index = headers.index('Contribuyente')
    except ValueError:
        print("Contribuyente column not found in tree headers.")
        return

    # Filter the data based on the entered Name value
    filtered_data = [row for row in tree_data if name_value.lower() in str(row[contribuyente_index]).lower()]

    if not filtered_data:
        messagebox.showinfo("No Results", "No se encontraron resultados para la búsqueda.")
        print("No results found for the search.")
        name_entry.delete(0, 'end')
        my_tree, original_data = bottom_treeview(bottomframe, my_tree)
        return

    # Print filtered data
    print("Filtered Data:", filtered_data)

    # Update Treeview
    fetch_all_records(my_tree, filtered_data)


def sector_search(my_tree, original_data, sector_entry, bottomframe):
    """Filter treeview data based on Sector."""
    sector_value = sector_entry.get().strip()
    if not sector_value:
        print("Sector field is empty.")
        return

    # Print headers of the tree
    headers = my_tree["columns"]
    print("Tree Headers:", headers)

    # Print data in the tree
    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])
    print("Tree Data:", tree_data)

    # Print original_data
    print("Original Data:", original_data)

    # Find the index of the Sector column in the tree headers
    try:
        sector_index = headers.index('Sector')
    except ValueError:
        print("Sector column not found in tree headers.")
        return

    # Filter the data based on the entered Sector value
    filtered_data = [row for row in tree_data if sector_value.lower() in str(row[sector_index]).lower()]

    if not filtered_data:
        messagebox.showinfo("No Results", "No se encontraron resultados para la búsqueda.")
        print("No results found for the search.")
        sector_entry.delete(0, 'end')
        my_tree, original_data = bottom_treeview(bottomframe, my_tree)
        return

    # Print filtered data
    print("Filtered Data:", filtered_data)

    # Update Treeview
    fetch_all_records(my_tree, filtered_data)


def inmueble_search(my_tree, original_data, inmueble_entry, bottomframe):
    """Filter treeview data based on Inmueble (Property)."""
    inmueble_value = inmueble_entry.get().strip()
    if not inmueble_value:
        print("Inmueble field is empty.")
        return

    # Print headers of the tree
    headers = my_tree["columns"]
    print("Tree Headers:", headers)

    # Print data in the tree
    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])
    print("Tree Data:", tree_data)

    # Print original_data
    print("Original Data:", original_data)

    # Find the index of the Inmueble column in the tree headers
    try:
        inmueble_index = headers.index('Inmueble')
    except ValueError:
        print("Inmueble column not found in tree headers.")
        return

    # Filter the data based on the entered Inmueble value
    filtered_data = [row for row in tree_data if inmueble_value.lower() in str(row[inmueble_index]).lower()]

    if not filtered_data:
        messagebox.showinfo("No Results", "No se encontraron resultados para la búsqueda.")
        print("No results found for the search.")
        inmueble_entry.delete(0, 'end')
        my_tree, original_data = bottom_treeview(bottomframe, my_tree)
        return

    # Print filtered data
    print("Filtered Data:", filtered_data)

    # Update Treeview
    fetch_all_records(my_tree, filtered_data)




def export_treeview_to_xlsx(treeview, filename):
    # Create a new workbook and select the active worksheet

    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if not filename:
        messagebox.showwarning("Advertencia", "Debe elegir un nombre de archivo para exportar los datos.")
        return

    workbook = Workbook()
    sheet = workbook.active

    # Get the column headings from the Treeview
    headings = treeview["columns"]
    sheet.append(headings)  # Append headings as the first row

    # Define styles
    bold_font = Font(name='Calibri', bold=True, size=12)
    regular_font = Font(name='Calibri', size=11)
    border_style = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Center align the headings and apply bold font
    for cell in sheet[1]:
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.font = bold_font
        cell.border = border_style

    # Iterate through the Treeview items and append them to the worksheet
    for item in treeview.get_children():
        row = treeview.item(item)["values"]
        sheet.append(row)

    # Center align the data rows and apply regular font and border
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column):
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.font = regular_font
            cell.border = border_style

    # Adjust column widths
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column].width = adjusted_width

    # Save the workbook to the specified filename
    workbook.save(filename)
    print(f"Data exported to {filename} successfully.")
    messagebox.showinfo("información", "Los datos se exportaron correctamente.")



