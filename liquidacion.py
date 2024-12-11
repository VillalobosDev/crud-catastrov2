import customtkinter as ctk
from menubar import menubar
from liquidacion_agg import liquidacion_agg
from liquidacion_gestion import liquidacion_gestion
from functions import * 
from tkinter import ttk
from rectangle import rectangle

# def liquidacion(window, last_window):
#     for widget in window.winfo_children():
#         widget.destroy()

#     ctk.set_appearance_mode('dark')
#     ctk.set_default_color_theme('dark-blue')
    
#     poppins30bold = ("Poppins", 30, "bold")
#     poppins20bold = ("Poppins", 20, "bold")
#     poppins14bold = ("Poppins", 14, "bold")
#     poppins12 = ("Poppins", 12)
    
#     menubar(window)
    
#     top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
#     top_frame.pack(fill="x", padx=10, pady=10)
    
#     left_frame = ctk.CTkFrame(window, corner_radius=15)
#     left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    
#     right_frame = ctk.CTkFrame(window, corner_radius=15)
#     right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
#     #Contenido del frame top
    
#     volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: last_window(window), font=poppins20bold)
#     volver_btn.pack(padx=10, pady=10, side="left")
    
#     window_title = ctk.CTkLabel(top_frame, text="Sección de Gestion Liquidacion", font=poppins30bold)
#     window_title.pack(padx=10, pady=10, side="left")
    
#     #Contenido del left frame
#     menu = last_window

#     #                                                                                                       (window, last window, last_window2) 
#     l_liquidacion_btn = ctk.CTkButton(left_frame, text="Agregar liquidacion", command=lambda: liquidacion_agg(window, menu, liquidacion), width=190, font=poppins20bold)
#     l_liquidacion_btn.pack(pady=105, padx=50, anchor="center", expand=True)
    
#     #Contenido del right frame
    
#     r_liquidacion_btn = ctk.CTkButton(right_frame, text="Gestionar liquidacion", command=lambda: liquidacion_gestion(window, menu, liquidacion), width=190, font=poppins20bold)
#     r_liquidacion_btn.pack(pady=105, padx=50, anchor="center", expand=True)

def ifasignar(bottom_frame):
        
        poppins14bold = ("Poppins", 14, "bold")


        for widget in bottom_frame.winfo_children():
            widget.destroy()

        frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
        frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

        frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
        frame_left.pack(padx=5, pady=5, side="left", fill="y")

        #Contenido del frame left #########################################################################

        contribuyenteci_frame = ctk.CTkFrame(frame_left)
        contribuyenteci_frame.pack(padx=10, pady=5, fill="x")

        contribuyentenombre_frame = ctk.CTkFrame(frame_left)
        contribuyentenombre_frame.pack(padx=10, pady=5, fill="x")

        inmueble_frame = ctk.CTkFrame(frame_left)
        inmueble_frame.pack(padx=10, pady=5, anchor="w")

        inmueblecod_frame = ctk.CTkFrame(frame_left)
        inmueblecod_frame.pack(padx=10, pady=5, fill="x")

        monto1_frame = ctk.CTkFrame(frame_left)
        monto1_frame.pack(padx=10, pady=5, fill="x")

        monto2_frame = ctk.CTkFrame(frame_left)
        monto2_frame.pack(padx=10, pady=5, fill="x")

        fecha_frame = ctk.CTkFrame(frame_left)
        fecha_frame.pack(padx=10, pady=5,fill="x")

        # Entrys del frame contribuyente

        contribuyenteci = ctk.CTkEntry(contribuyenteci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold, width=250)
        contribuyenteci.pack(pady=5, padx=5, side="left")

        contribuyentenombre = ctk.CTkEntry(contribuyentenombre_frame, placeholder_text="Contribuyente", font=poppins14bold, width=250)
        contribuyentenombre.pack(pady=5, padx=5, side="left")

        valuesinmuebles = ["Inmuebles"]
        inmueble = ctk.CTkOptionMenu(inmueble_frame, values=valuesinmuebles, font=poppins14bold)
        inmueble.pack(padx=5, pady=5, side="left")

        inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
        inmueblecod.pack(pady=5, padx=5, side="left")

        monto1 = ctk.CTkEntry(monto1_frame, placeholder_text="Monto 1", font=poppins14bold, width=250)
        monto1.pack(pady=5, padx=5, side="left")

        monto2 = ctk.CTkEntry(monto2_frame, placeholder_text="Monto 2", font=poppins14bold, width=250)
        monto2.pack(pady=5, padx=5, side="left")

        fecha = ctk.CTkEntry(fecha_frame, placeholder_text="Fecha Liquidacion", font=poppins14bold, width=250)
        fecha.pack(pady=5, padx=5, side="left")

        btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: print("Aca la funcion guardar"), font=poppins14bold)
        btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

        # Fin del contenido del left frame #########################################################################

        # Contenido del RIGHT FRAME
        
        # Creando el treeview para mostrar los registros
        frame_tree = ctk.CTkFrame(frame_right, fg_color='white')
        frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  
    
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
        style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 
    
        my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
        my_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    
        my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    
        horizontal_scrollbar.pack(side="bottom", fill="x")
    
        my_tree['columns'] = ( 'CI', 'Contribuyente', 'Inmueble', 'Codigo Catastral', 'Monto 1', 'Monto 2', 'Fecha Liquidacion')
    
        for col in my_tree['columns']:
            my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
            my_tree.column(col, anchor='center')
    
        canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
        canvas.pack()  # Posicionamos el canvas
        rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
        
        try:
            with connection() as conn:
                print("Database connection established.")
                cursor = conn.cursor()
                sql = 'SELECT * FROM liquidaciones'
                cursor.execute(sql)
                results = cursor.fetchall()
                print(f"Query executed successfully, fetched results: {results}")

                # Ensure data fits Treeview structure
                for row in results:
                    my_tree.insert("", "end", values=row)

        except Exception as e:
            print(f"Error during database operation: {e}")


        # FIN del Contenido del RIGHT FRAME


def liquidacionv2(window, last_window):
    
    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)
    
    menubar(window)
    
    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)

    top_frame2 = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame2.pack(fill="x", padx=10)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    #Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestion Liquidacion", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    crearliq = ctk.CTkButton(top_frame2, text="Asignar", command=lambda: ifasignar(bottom_frame), font=poppins14bold)
    crearliq.pack(padx=5, pady=5, side="left")

    gestionarliq = ctk.CTkButton(top_frame2, text="Gestionar", command=lambda: print("Example"), font=poppins14bold)
    gestionarliq.pack(padx=5, pady=5, side="left")

    eliminarliq = ctk.CTkButton(top_frame2, text="Eliminar", command=lambda: print("Example"), font=poppins14bold)
    eliminarliq.pack(padx=5, pady=5, side="left")

    busquedaliq = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedaliq.pack(padx=5, pady=5, side="right")

    #Contenido del bottom frame

    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)
    
    # Creando el treeview para mostrar los registros
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

    my_tree['columns'] = ( 'CI', 'Contribuyete', 'Inmueble', 'Codigo Catastral', 'Monto 1', 'Monto 2', 'Fecha Liquidacion')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    
    try:
        with connection() as conn:
            print("Database connection established.")
            cursor = conn.cursor()
            sql = 'SELECT * FROM liquidaciones'
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Query executed successfully, fetched results: {results}")

            # Ensure data fits Treeview structure
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during database operation: {e}")
    

