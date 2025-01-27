import customtkinter as ctk
import tkinter as tk
from modulos2.menubar import menubar
from functions.functions import * 
from tkinter import ttk, messagebox
from functions.rectangle import rectangle
import tkinter
from config.config import centrar_ventana


def contribuyentes(window, last_window):
    global busquedainm, busquedabtn, recargarbusqueda
    
    for widget in window.winfo_children():
        widget.destroy()


    
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
    
    window_title = ctk.CTkLabel(top_frame, text="", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")
    window_title.configure(text="Gestión Contribuyentes")

    #Contenido del top frame 2


    
    
    recargarbusqueda = ctk.CTkButton(top_frame2, text="🔁", font=poppins14bold, width=30, command=lambda: loaddata(my_tree))
    recargarbusqueda.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    #Contenido del bottom frame

    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)
    
    # Creando el treeview para mostrar los registros


    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both", side="left")

    # Configuración del estilo del Treeview (usando ttk dentro de CustomTkinter)
    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    # Crear el Treeview
    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    # Crear el scrollbar vertical con CustomTkinter

    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")


    my_tree['columns'] = ('ID', 'nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')
    
    my_tree.column('ID', width=0, stretch=tk.NO)
    my_tree.heading('ID', text='', anchor='center')
    
    
    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    

    my_tree.bind("<<TreeviewSelect>>")  # Selección básica
    my_tree.bind("<Double-1>", lambda event: mostrar_modal_contribuyente(my_tree))  # Doble clic
    my_tree.bind("<Return>", lambda event: mostrar_modal_contribuyente(my_tree))  # Tecla Enter

    loaddata(my_tree)
    return window, last_window


def reload_treeviewsearch(treeview, ci):
    ci = ci.get()
    if not ci:
        messagebox.showwarning("Advertencia", "Por favor ingrese una cedula para buscar.")
        loaddata(treeview)
        return
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' 
            SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo,
            telefono, correo FROM contribuyentes where ci_contribuyente = ?
            '''
            cursor.execute(sql,(ci,))
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)
                

            if not results:
                messagebox.showerror("Error", "No se ha encontrado la cédula del contribuyente.")
                loaddata(treeview)
                return

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row)
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")
        
def loaddata(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = 'SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo, telefono, correo FROM contribuyentes'
            cursor.execute(sql)
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row)
            
    except Exception as e:
        print(f'Ocurrio un error: {e}')



def mostrar_modal_contribuyente(treeview):
    poppins14bold = ("Poppins", 14, "bold")
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 25, "bold")
    
    # Obtener el elemento seleccionado
    seleccion = treeview.selection()
    if seleccion:
        item = treeview.item(seleccion[0])  # Obtener datos del elemento
        datos = item['values']  # Recuperar los valores de las columnas
        if not datos:
            print("No hay datos seleccionados.")
            return
        
        id_contribuyente = datos[0]
        datos_contribuyente = cargar_datoss(id_contribuyente)
        
        if not datos_contribuyente:
            print("No se encontraron datos del contribuyente.")
            return







        # config
        modal = ctk.CTkToplevel()
        modal.title("Contribuyente")
        modal.geometry("600x500")  
        modal.grab_set()  
        modal.resizable(False, False)
        centrar_ventana(modal, 600, 500)
        
        
        cerrar_btn = ctk.CTkButton(modal, text="Cerrar", command=modal.destroy, font=poppins14bold)
        cerrar_btn.pack(pady=10, padx=10, side="bottom", anchor="e") 
        
        
        frame_left = ctk.CTkFrame(modal, corner_radius=15, width=250)
        frame_left.pack(padx=5, pady=5, side="left", fill="both", expand=True)
        

        # Mostrar datos en la ventana modal
        nombre = datos_contribuyente[0][0]
        cedula = datos_contribuyente[0][1]
        rif = datos_contribuyente[0][2]
        telefono = datos_contribuyente[0][3]
        correo = datos_contribuyente[0][4]
        
        text= ctk.CTkLabel(frame_left, text="Datos del Contribuyente", font=poppins20bold)
        text.pack(pady=5)
        
        frame_nombre= ctk.CTkFrame(frame_left, corner_radius=15)
        frame_nombre.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_cedula=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_cedula.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_rif=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_rif.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_telefono=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_telefono.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        frame_correo=ctk.CTkFrame(frame_left, corner_radius=15)
        frame_correo.pack(fill="both", anchor="s", pady=5, padx=5, expand=True)
        
        
        
        ###############labels##########
        
        label_nombre = ctk.CTkLabel(frame_nombre, text=(f"Nombre: {nombre}"), font=poppins14bold)
        label_nombre.pack(pady=10, padx=10)
        
        label_cedula = ctk.CTkLabel(frame_cedula, text=(f"Cédula: {cedula}"), font=poppins14bold)
        label_cedula.pack(pady=10)
        
        label_rif = ctk.CTkLabel(frame_rif, text=(f"RIF: {rif}"), font=poppins14bold)
        label_rif.pack(pady=10)
        
        label_telefono = ctk.CTkLabel(frame_telefono, text=(f"Teléfono: {telefono}"), font=poppins14bold)
        label_telefono.pack(pady=10)
        
        label_correo = ctk.CTkLabel(frame_correo, text=(f"Correo: {correo}"), font=poppins14bold)
        label_correo.pack(pady=10)
        
        # Botón para cerrar la ventana modal

    else:
        print("No se ha seleccionado ningún elemento en el Treeview.")

def cargar_datoss(ID):
    original_data = []
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = '''
            SELECT 
                contribuyentes.nombres || ' ' || contribuyentes.apellidos AS contribuyente,
                v_e || "-" || ci_contribuyente AS cedula_completa,
                j_c_g || "-" || rif AS rif_completo,
                contribuyentes.telefono,
                contribuyentes.correo
            FROM contribuyentes
            WHERE id_contribuyente = ?
            ORDER BY contribuyentes.ci_contribuyente ASC
            '''
            cursor.execute(sql, (ID,))
            original_data = cursor.fetchall()
            
            print(f"Fetched {len(original_data)} rows from the database.")
    except Exception as e:
        print(f"Error during database operation: {e}")

    return original_data
