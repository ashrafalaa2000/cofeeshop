from tkinter import *

root = Tk()
root.geometry("700x600")
import sqlite3

mix_category = StringVar()  
# mix_category.set("5555")
radio_sada = Radiobutton(root, text="سادة", variable=mix_category, value="سادة")
radio_mehaweg = Radiobutton(root, text="محوج", variable=mix_category, value="محوج")
radio_ispresso = Radiobutton(root, text="اسبريسو", variable=mix_category, value="اسبريسو")
radio_sada.grid(row=0, column=2, padx=10)
radio_mehaweg.grid(row=0, column=1, padx=10)
radio_ispresso.grid(row=0, column=0, padx=10)
lbl1= Label(root,text=  mix_category.get())
lbl1.grid(row=0,column=4)
def g():
    conn = sqlite3.connect("coffee_shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mixes (customer_id, date, category,details) VALUES (?, ?, ?,? )",
               (1, "5-6-2011", mix_category.get(), "50505050"))
    conn.commit()
    conn.close()
print("success")

    



btn1=Button(root,text= "show category",command=g)
btn1.grid(row=0,column=3)





root.mainloop()