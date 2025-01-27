from datetime import datetime
from functions.functions import connection

# def rango_fecha_search(my_tree, original_data, start_date, end_date):
#     """Filter treeview data based on Date Range (Rango Fecha) via DB query."""
#     if not start_date or not end_date:
#         print("Please provide both start and end date.")
#         return

#     # Assuming the date format in the entries is dd-mm-yyyy
#     try:
#         # Convert string dates to datetime objects to check validity if needed
#         start_date = datetime.strptime(start_date, "%d-%m-%Y")
#         end_date = datetime.strptime(end_date, "%d-%m-%Y")
#     except ValueError:
#         print("Invalid date format. Please use dd-mm-yyyy.")
#         return

#     # Assuming you're using SQLite here, but you can adjust this based on your DB.
#     with connection() as conn:
#         cursor = conn.cursor()

#         # Modify your SQL query to filter by date range
#         sql = '''
#         SELECT 
#             inmuebles.nom_inmueble,
#             inmuebles.cod_catastral,
#             inmuebles.uso,
#             contribuyentes.nombres || ' ' || contribuyentes.apellidos AS contribuyente,
#             contribuyentes.ci_contribuyente,
#             contribuyentes.rif,
#             contribuyentes.telefono,
#             contribuyentes.correo,
#             sectores.nom_sector,
#             sectores.ubic_sector,
#             liquidaciones.id_liquidacion,
#             liquidaciones.monto_1,
#             liquidaciones.monto_2,
#             liquidaciones.fecha_Liquidacion_1,
#             liquidaciones.fecha_Liquidacion_2
#         FROM
#             inmuebles
#         JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente
#         JOIN sectores ON inmuebles.id_sector = sectores.id_sector
#         JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble
#         WHERE liquidaciones.fecha_Liquidacion_1 BETWEEN ? AND ?
#         ORDER BY contribuyentes.ci_contribuyente ASC
#         '''

#         # Execute the query with the date range parameters
#         cursor.execute(sql, (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

#         # Fetch the filtered data from the query
#         filtered_data = cursor.fetchall()

#     # Now update your treeview with the fetched data
#     update_treeview(my_tree, filtered_data)
from datetime import datetime

def rango_fecha_search(my_tree, original_data, start_date_str, end_date_str):
    """Filter treeview data based on date range."""
    if not start_date_str or not end_date_str:
        print("Both start and end dates must be provided.")
        return

    # Convert date strings to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return

    # Print headers of the tree
    headers = my_tree["columns"]
    print("\n\n\n\n\n\n\n\nTree Headers:", headers)

    # Print data in the tree
    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])
    print("\n\n\n\n\n\n\n\nTree Data:", tree_data)

    # Print original_data
    print("\n\n\n\n\n\n\nOriginal Data:", original_data)

    # Find the indices of the date columns in the tree headers
    try:
        fecha_pago_solicitud_index = headers.index('Fecha de Pago Solicitud')
        fecha_pago_inmueble_index = headers.index('Fecha de Pago Inmueble')
    except ValueError as e:
        print(f"Date column not found in tree headers: {e}")
        return

    # Filter the data based on the date range
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

    # Print filtered data
    print("\n\n\n\n\n\n\n\n\nFiltered Data:", filtered_data)

    # Update Treeview directly
    update_treeview(my_tree, filtered_data)

def update_treeview(my_tree, data):
    """Update the treeview with new data."""
    for item in my_tree.get_children():
        my_tree.delete(item)

    for row in data:
        my_tree.insert("", "end", values=row)