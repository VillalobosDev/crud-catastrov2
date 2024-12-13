import customtkinter as ctk
from menubar import menubar
from functions import * 
from calendario import open_calendar_popup
from calendario import create_date_range_selector

def consulta(window, last_window):
    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    # Fonts
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)

    menubar(window)

    # Frames
    top_frame = ctk.CTkFrame(window, height=80, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=5)

    top_frame2 = ctk.CTkFrame(window, height=150, corner_radius=15)
    top_frame2.pack(fill="x", padx=10, pady=5)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=5, fill="both", expand=True)

    bottom_frame2 = ctk.CTkFrame(window, corner_radius=15, height=100)
    bottom_frame2.pack(padx=10, pady=5, fill="x")

    # Top Frame Content
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")

    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestión Liquidación", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    # Top Frame 2 Content
    current_widgets = {"frame": None}

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
            if switch_name == "Rango Fecha":
                # Create date range selector
                current_widgets["frame"] = ctk.CTkFrame(top_frame2)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")
                create_date_range_selector(current_widgets["frame"])
            else:
                # Create a single entry
                current_widgets["frame"] = ctk.CTkFrame(top_frame2)
                current_widgets["frame"].pack(padx=5, pady=5, side="right")

                new_entry = ctk.CTkEntry(current_widgets["frame"], placeholder_text=placeholder_text, font=poppins12, width=200)
                new_entry.pack(side="left")

    # Switches
    switches = {}
    switch_labels = ["Cedula", "Nombre", "Sector", "Inmueble", "Rango Fecha"]
    placeholders = ["Ingrese Cédula", "Ingrese Nombre", "Ingrese Sector", "Ingrese Inmueble", "Rango Fecha"]

    for label, placeholder in zip(switch_labels, placeholders):
        switch = ctk.CTkSwitch(
            top_frame2,
            text=label,
            font=poppins12,
            command=lambda l=label, p=placeholder: toggle_entry(l, p),
        )
        switch.pack(padx=5, pady=5, side="left")
        switches[label] = switch

    # Search Button
    searchbtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins12, width=70)
    searchbtn.pack(side="right", pady=15, padx=5)
