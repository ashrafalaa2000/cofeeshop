from tkinter import *
from tkinter import ttk,Tk, messagebox, filedialog
import sqlite3
from datetime import datetime
import os
import shutil
from PIL import Image,ImageFile



window = Tk()
window.geometry('500x400')
logo_image = PhotoImage(file="my_logo.jpg" )
logo_label = Label(window,image=logo_image, bg="white",)
logo_label.pack(pady=10)



window.mainloop()