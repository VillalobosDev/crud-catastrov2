import customtkinter as ctk

from tkcalendar import Calendar
from config.config import centrar_ventana



def open_calendar_popup(entry_widget):
    
    poppins12bold = ("Poppins", 12, "bold")
    poppins14bold = ("Poppins", 14, "bold")


    poppins8bold = ("Poppins", 8)
    
    """Open a calendar popup to select a date."""
    calendar_popup = ctk.CTkToplevel()
    calendar_popup.grab_set()
    calendar_popup.title("Fecha")
    calendar_popup.geometry("390x310")
    calendar_popup.resizable(width=False, height=False)
    
    centrar_ventana(calendar_popup, 340, 310)
    
    top_container = ctk.CTkFrame(calendar_popup, corner_radius=15)
    top_container.pack(fill="both", padx=5, pady=5, expand=True)
    
    frame_calendar=ctk.CTkFrame(top_container, corner_radius=15)
    frame_calendar.pack(pady=5, padx=5)

    # Add Calendar widget
    calendar = Calendar(frame_calendar, date_pattern="dd-mm-yyyy", font=poppins8bold)  # Use desired format
    calendar.pack(padx=10, pady=10)

    # Function to handle date selection
    def select_date():
        selected_date = calendar.get_date()
        entry_widget.delete(0, "end")  # Clear existing value in the entry
        entry_widget.insert(0, selected_date)  # Insert selected date
        calendar_popup.destroy()  # Close the calendar popup

    # Add button to confirm date selection
    select_button = ctk.CTkButton(top_container, text="Seleccionar", command=select_date, font=poppins14bold)
    select_button.pack(pady=10, side="bottom")


def create_date_range_selector(parent_frame, searchbtn, my_tree, original_data):
    poppins12 = ("Poppins", 12, "bold")

    date_range_frame = ctk.CTkFrame(parent_frame)
    date_range_frame.pack(pady=10, padx=10, fill="x")

    start_date_entry = ctk.CTkEntry(date_range_frame, placeholder_text="Fecha Inicio", font=poppins12, width=150)
    start_date_entry.pack(padx=5, pady=5, side="left")

    start_date_button = ctk.CTkButton(
        date_range_frame, text="📅", width=50, command=lambda: open_calendar_popup(start_date_entry)
    )
    start_date_button.pack(pady=5, padx=5, side="left")

    end_date_entry = ctk.CTkEntry(date_range_frame, placeholder_text="Fecha Fin", font=poppins12, width=150)
    end_date_entry.pack(padx=5, pady=5, side="left")

    end_date_button = ctk.CTkButton(
        date_range_frame, text="📅", width=50, command=lambda: open_calendar_popup(end_date_entry)
    )
    end_date_button.pack(pady=5, padx=5, side="left")

    # Set the search button command to call the date range search function
    if searchbtn.winfo_exists():
        print("Btn exist")
        searchbtn.configure(command=lambda: rango_fecha_search(
            my_tree, original_data, 
            start_date_entry.get(), end_date_entry.get()))
    else:
        print("Btn doesn't exist")
    return start_date_entry, end_date_entry

from datetime import datetime

def rango_fecha_search(my_tree, original_data, start_date_str, end_date_str):
    """Filter treeview data based on date range."""
    if not start_date_str or not end_date_str:
        print("Both start and end dates must be provided.")
        return

    # Convert string objects to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return

    # Print the existing columns of the tree
    headers = my_tree["columns"]
    print("\n\n\n\n\n\n\n\nTree Headers:", headers)

    tree_data = []
    for item in my_tree.get_children():
        tree_data.append(my_tree.item(item)["values"])

    # Find the index of the 'Pago Solicitud' column in the tree headers
    try:
        pago_solicitud_index = headers.index('Pago Solicitud')
    except ValueError as e:
        print(f"Date column not found in tree headers: {e}")
        return

    # Filter the data based on the selected date range
    filtered_data = []
    for row in tree_data:
        try:
            pago_solicitud = datetime.strptime(row[pago_solicitud_index], "%d-%m-%Y") if row[pago_solicitud_index] else None

            if pago_solicitud and start_date <= pago_solicitud <= end_date:
                filtered_data.append(row)
        except ValueError:
            continue

    print("\n\n\n\n\n\n\n\n\nFiltered Data:", filtered_data)

    update_treeview(my_tree, filtered_data)

def update_treeview(my_tree, data):
    """Update the treeview with new data."""
    from modulos.consulta_general import fetch_all_records
    fetch_all_records(my_tree, data)