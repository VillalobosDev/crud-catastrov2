import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from login_fun import login

# Configuración de CustomTkinter



window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")

login(window)


window.mainloop()