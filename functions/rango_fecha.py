from datetime import datetime

def rango_fecha_search(my_tree, original_data, start_date_str, end_date_str):
    """Filter treeview data based on date range."""
    if not start_date_str or not end_date_str:
        print("Both start and end dates must be provided.")
        return

    # Convertimos loss objetos strings a datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return

    # Print de las columnas existentes del arbol
    headers = my_tree["columns"]
    print("\n\n\n\n\n\n\n\nTree Headers:", headers)

    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])

    # Buscamos los indices de las columnas en donde se encuentran las  fechas
    try:
        fecha_pago_solicitud_index = headers.index('Fecha de Pago Solicitud')
        fecha_pago_inmueble_index = headers.index('Fecha de Pago Inmueble')
    except ValueError as e:
        print(f"Date column not found in tree headers: {e}")
        return

    #  Filtramos los datos basandonos en la fecha seleccionada
    filtered_data = []
    for row in tree_data:
        try:
            fecha_pago_solicitud = datetime.strptime(row[fecha_pago_solicitud_index], "%d-%m-%Y") if row[fecha_pago_solicitud_index] else None
            fecha_pago_inmueble = datetime.strptime(row[fecha_pago_inmueble_index], "%d-%m-%Y") if row[fecha_pago_inmueble_index] else None

            if fecha_pago_solicitud and fecha_pago_inmueble:
                if start_date <= fecha_pago_solicitud <= end_date and start_date <= fecha_pago_inmueble <= end_date:
                    filtered_data.append(row)
        except ValueError:
            continue

    print("\n\n\n\n\n\n\n\n\nFiltered Data:", filtered_data)

    update_treeview(my_tree, filtered_data)

def update_treeview(my_tree, data):
    """Update the treeview with new data."""
    for item in my_tree.get_children():
        my_tree.delete(item)

    for row in data:
        my_tree.insert("", "end", values=row)