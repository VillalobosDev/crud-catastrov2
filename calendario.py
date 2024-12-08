import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel
from tkcalendar import Calendar


def open_calendar_popup(entry_widget):
    """Open a calendar popup to select a date."""
    calendar_popup = Toplevel()
    calendar_popup.title("Seleccionar Fecha")
    calendar_popup.geometry("300x300")
    calendar_popup.resizable(width=False, height=False)

    # Add Calendar widget
    calendar = Calendar(calendar_popup, date_pattern="dd-mm-yyyy")  # Use desired format
    calendar.pack(padx=10, pady=10)

    # Function to handle date selection
    def select_date():
        selected_date = calendar.get_date()
        entry_widget.delete(0, "end")  # Clear existing value in the entry
        entry_widget.insert(0, selected_date)  # Insert selected date
        calendar_popup.destroy()  # Close the calendar popup

    # Add button to confirm date selection
    select_button = ctk.CTkButton(calendar_popup, text="Seleccionar", command=select_date)
    select_button.pack(pady=10)