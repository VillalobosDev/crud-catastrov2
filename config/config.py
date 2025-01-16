def centrar_ventana(ventana, ancho, alto):
    """Función para centrar una ventana en la pantalla."""
    ventana_ancho = ventana.winfo_screenwidth()
    ventana_alto = ventana.winfo_screenheight()
    
    x = (ventana_ancho // 2) - (ancho // 2)
    y = (ventana_alto // 2) - (alto // 2)
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    

