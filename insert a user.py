import sqlite3

conn = sqlite3.connect("coffee_shop.db")
cursor = conn.cursor()
# Insert a default admin record
cursor.execute("INSERT INTO employees (name, username, password) VALUES (?, ?, ?)",
               ("Admin", "admin", "admin"))
conn.commit()
conn.close()
