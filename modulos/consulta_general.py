import customtkinter as ctk
from modulos.menubar import menubar
from functions.functions import * 
from functions.calendario import create_date_range_selector
from config.config import centrar_ventana
from tkinter import ttk
from tkinter import filedialog
from functions.rango_fecha import *
from openpyxl import Workbook
from tkinter import messagebox
import tkinter

# Global flags
search_filter_shown = False
column_switch_shown = False
search_filter_created = False
column_switches_created = False

# Global dictionary to store the switch states
column_switch_states = {
    'Inmueble': True,
    'Codigo Catastral': True,
    'Uso': True,
    'Contribuyente': True,
    'CI': True,
    'RIF': True,
    'Telefono': True,
    'Correo': True,
    'Sector': True,
    'Codigo del Sector': True,
    'Liquidacion ID': True,
    'Monto 1': True,
    'Monto 2': True,
    'Fecha Liquidacion 1': True,
    'Fecha Liquidacion 2': True
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
    
    text_top = ctk.CTkLabel(switches_frame, text="Filtros de Busqueda", font=poppins20)
    text_top.pack(pady=10, padx=10, side="top")

    # Dictionary to store the switch widgets
    column_switches = {}

    # Treeview columns
    columns = [
        'Inmueble', 'Codigo Catastral', 'Uso', 'Contribuyente', 'CI', 'RIF', 
        'Telefono', 'Correo', 'Sector', 'Codigo del Sector', 
        'Liquidacion ID', 'Monto 1', 'Monto 2', 'Fecha Liquidacion 1', 'Fecha Liquidacion 2'
    ]

    # Define a fixed width for all frames
    frame_width = 186.5

    # Group 1: Inmueble, Codigo Catastral, Uso
    group1_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group1_frame.pack(side="left", padx=5, pady=5, fill="y")
    group1_frame.pack_propagate(False)
    text_1= ctk.CTkLabel(group1_frame, text="Inmuebles", font=poppins16)
    text_1.pack(pady=10, side="top")


    for col_name in ['Inmueble', 'Codigo Catastral', 'Uso']:
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


    for col_name in ['Contribuyente', 'CI', 'RIF', 'Telefono', 'Correo']:
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

    # Group 3: Sector, Ubicacion Sector
    group3_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group3_frame.pack(side="left", padx=5, pady=5, fill="y")
    group3_frame.pack_propagate(False)
    text_3= ctk.CTkLabel(group3_frame, text="Sectores", font=poppins16)
    text_3.pack(pady=10, side="top")


    for col_name in ['Sector', 'Codigo del Sector']:
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

    # Group 4: Liquidacion ID, Monto 1, Monto 2, Fecha Liquidacion 1, Fecha Liquidacion 2
    group4_frame = ctk.CTkFrame(switches_frame, width=frame_width)
    group4_frame.pack(side="left", padx=5, pady=5, fill="y")
    group4_frame.pack_propagate(False)
    text_4= ctk.CTkLabel(group4_frame, text="Liquidaciones", font=poppins16)
    text_4.pack(pady=10, side="top")

    for col_name in ['Liquidacion ID', 'Monto 1', 'Monto 2', 'Fecha Liquidacion 1', 'Fecha Liquidacion 2']:
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
            
    def close_and_refresh(toplevel, treeview, column_switches):
        toplevel.destroy()  # Close the toplevel window
        refresh_treeview(treeview, column_switches)  # Refresh the treeview

    refresh_button = ctk.CTkButton(
        toplevel,
        text="Aplicar",
        font=poppins12,
        command=lambda: close_and_refresh(toplevel, treeview, column_switches)
    )
    refresh_button.pack(side="bottom", anchor="e", padx=10, pady=10)  # Place the button on the right inside the `button_frame`

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

    export = ctk.CTkButton(top_frame2, text="Exportar a Excel", font=poppins12, command=lambda: export_treeview_to_xlsx(my_tree, "consulta_general.xlsx"))
    export.pack(side="right", padx=10, pady=5)

    searchbtn = display_search_filter(top_frame3, my_tree, original_data)
    print(type(searchbtn)) 

    # create_date_range_selector(top_frame4, searchbtn, my_tree, original_data)

def display_search_filter(frame, my_tree, original_data):
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
                    searchbtn.configure(command=lambda: cedula_search(my_tree, original_data, new_entry))
                elif switch_name == "Nombre":
                    searchbtn.configure(command=lambda: nombre_search(my_tree, original_data, new_entry))
                elif switch_name == "Sector":
                    searchbtn.configure(command=lambda: sector_search(my_tree, original_data, new_entry))
                elif switch_name == "Inmueble":
                    searchbtn.configure(command=lambda: inmueble_search(my_tree, original_data, new_entry))
        else:
            if not any(switch.get() == 1 for switch in switches.values()):
                searchbtn.configure(command=lambda: fetch_all_records(my_tree, original_data))


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
    return searchbtn

def refresh_treeview(treeview, column_switches):
    # Clear the Treeview before updating with new data
    for item in treeview.get_children():
        treeview.delete(item)

    # Select columns that are marked as visible in the column_switches
    selected_columns = [col for col, switch in column_switches.items() if switch.get() == 1]
    
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
        'CI': 'contribuyentes.v_e || "-" || contribuyentes.ci_contribuyente',
        'RIF': 'contribuyentes.j_c_g || "-" || contribuyentes.rif',
        'Telefono': 'contribuyentes.telefono',
        'Correo': 'contribuyentes.correo',
        'Sector': 'sectores.nom_sector',
        'Codigo del Sector': 'sectores.cod_sector',
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
    
    treeview["columns"] = selected_columns
            
    for col in selected_columns:
        treeview.heading(col, text=col)
        print(f"Setting width for column {col} to 200")
        treeview.column(col, anchor="center")


    # Try to fetch the data from the database
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filtered_data = cursor.fetchall()

            # Update the Treeview columns and insert the new data into the Treeview

            # Insert the rows fetched from the query into the Treeview
            for row in filtered_data:
                treeview.insert("", "end", values=row)
    
    except Exception as e:
        print(f"Error during query execution: {e}")

# Asegúrate de llamar a esta función después de configurar las columnas en el Treeview
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

    ################SCROLLBAR X
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")
    
    # Define the columns
    columns = [
        'Contribuyente',
        'Cedula',
        'Sector', 
        'Cod-Sector', 
        'Cod-Catastral', 

        'Fecha de Pago Solicitud', 
        'Monto Liquidado Inmueble', 
        'Monto Pago Derecho-Ocupacion', 
        'Fecha de Pago Inmueble', 
        
        'Correo', 
        'Sector', 
        'Codigo del Sector', 
        'Liquidacion ID', 
        'Monto 1', 
        'Monto 2', 
        'Fecha Liquidacion 1', 
        'Fecha Liquidacion 2'
    ]
    my_tree["columns"] = columns

    for col in columns:
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
            liquidaciones.fecha_Liquidacion_1,
            liquidaciones.monto_1,
            liquidaciones.monto_2,
            liquidaciones.fecha_Liquidacion_2,




            inmuebles.nom_inmueble,
            inmuebles.ubicacion,
            inmuebles.uso,
            contribuyentes.j_c_g || "-" || contribuyentes.rif,
            contribuyentes.telefono,
            contribuyentes.correo,
            liquidaciones.id_liquidacion,
        FROM
            inmuebles
        JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente
        JOIN sectores ON inmuebles.id_sector = sectores.id_sector
        JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble 
        ORDER BY contribuyentes.ci_contribuyente ASC
        '''
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


def cedula_search(my_tree, original_data, cedula_entry):
    """Filter treeview data based on Cédula."""
    cedula_value = cedula_entry.get().strip()
    if not cedula_value:
        print("Cédula field is empty.")
        return

    # Filter the data based on the entered Cédula value
    filtered_data = [row for row in original_data if cedula_value in str(row[4])]  # Assuming CI (index 4) matches

    # Update Treeview
    update_treeview(my_tree, filtered_data)

def fetch_all_records(tree, data):
    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert all records from the original data
    for record in data:
        tree.insert("", "end", values=record)

def nombre_search(my_tree, original_data, name_entry):
    """Filter treeview data based on Nombre (Name)."""
    name_value = name_entry.get().strip()
    if not name_value:
        print("Name field is empty.")
        return

    # Filter the data based on the entered Name value
    filtered_data = [row for row in original_data if name_value.lower() in str(row[3]).lower()]  # Assuming `row[3]` is "Contribuyente"

    # Update Treeview
    update_treeview(my_tree, filtered_data)

def sector_search(my_tree, original_data, sector_entry):
    """Filter treeview data based on Sector."""
    sector_value = sector_entry.get().strip()
    if not sector_value:
        print("Sector field is empty.")
        return

    # Filter the data based on the entered Sector value
    filtered_data = [row for row in original_data if sector_value.lower() in str(row[8]).lower()]  # Assuming `row[8]` is "Sector"

    # Update Treeview
    update_treeview(my_tree, filtered_data)

def inmueble_search(my_tree, original_data, inmueble_entry):
    """Filter treeview data based on Inmueble (Property)."""
    inmueble_value = inmueble_entry.get().strip()
    if not inmueble_value:
        print("Inmueble field is empty.")
        return

    # Filter the data based on the entered Inmueble value
    filtered_data = [row for row in original_data if inmueble_value.lower() in str(row[0]).lower()]  # Assuming `row[0]` is "Inmueble"

    # Update Treeview
    update_treeview(my_tree, filtered_data)

def export_treeview_to_xlsx(treeview, filename):
    # Create a new workbook and select the active worksheet

    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if not filename:
        tkinter.messagebox.showinfo("Export Cancelled", "Debe elegir un nombre de archivo para exportar los datos.")
        return

    workbook = Workbook()
    sheet = workbook.active

    # Get the column headings from the Treeview
    headings = treeview["columns"]
    sheet.append(headings)  # Append headings as the first row

    # Iterate through the Treeview items and append them to the worksheet
    for item in treeview.get_children():
        row = treeview.item(item)["values"]
        sheet.append(row)

    # Save the workbook to the specified filename
    workbook.save(filename)
    print(f"Data exported to {filename} successfully.")
    
    
    
    
