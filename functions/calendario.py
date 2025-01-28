import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel
from tkcalendar import Calendar
from functions.rango_fecha import rango_fecha_search
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