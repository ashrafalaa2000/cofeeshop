
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import os
import shutil

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

DB_FILE = "coffee_shop.db"
BACKUP_FOLDER = "backups"

def init_db():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    if not os.path.exists(DB_FILE):
        # Create database if it doesn't exist
        conn = sqlite3.connect(DB_FILE)
        conn.close()
    backup_database()  # Auto-backup on launch

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        employer TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mixes (
        mix_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        date TEXT,
        category TEXT,
        details TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def backup_database(destination=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{timestamp}.db"
    if destination:
        dest_path = os.path.join(destination, backup_name)
    else:
        dest_path = os.path.join(BACKUP_FOLDER, backup_name)
    try:
        shutil.copy(DB_FILE, dest_path)
    except Exception as e:
        print("Backup failed:", e)









###############   old code ###############

   
   


# ------------------------------ #
# Main Application Class
# ------------------------------ #
class CoffeeShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("بن البركة")
        self.root.geometry("500x450")
        self.root.resizable(True, True)
        try:
            self.root.iconbitmap("coffee.ico")
        except Exception:
            pass
        # Start with the login screen; on success, the main screen is created.
        self.show_login_screen()

    # ------------- Login Screen ------------- #
    def show_login_screen(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("تسجيل الدخول")
        login_win.geometry("400x250")
        login_win.resizable(False, False)
        lbl_title = tk.Label(login_win, text="تسجيل الدخول", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=10)
        frame = tk.Frame(login_win)
        frame.pack(pady=10)
        lbl_username = tk.Label(frame, text="اسم المستخدم:", width=15, anchor="e")
        lbl_username.grid(row=0, column=0, padx=5, pady=5)
        entry_username = tk.Entry(frame, justify="right")
        entry_username.grid(row=0, column=1, padx=5, pady=5)
        lbl_password = tk.Label(frame, text="كلمة المرور:", width=15, anchor="e")
        lbl_password.grid(row=1, column=0, padx=5, pady=5)
        entry_password = tk.Entry(frame, show="*", justify="right")
        entry_password.grid(row=1, column=1, padx=5, pady=5)

        def attempt_login():
            username = entry_username.get().strip()
            password = entry_password.get().strip()
            if not username or not password:
                messagebox.showwarning("تنبيه", "يرجى إدخال اسم المستخدم وكلمة المرور", parent=login_win)
                return
            conn = sqlite3.connect("coffee_shop.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                messagebox.showinfo("نجاح", "تم تسجيل الدخول بنجاح", parent=login_win)
                login_win.destroy()
                self.create_main_screen()  # Show main screen after successful login
            else:
                messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة", parent=login_win)

        btn_login = tk.Button(login_win, text="تسجيل الدخول", font=("Arial", 12, "bold"), command=attempt_login)
        btn_login.pack(pady=10)
        login_win.transient(self.root)
        login_win.grab_set()
        self.root.wait_window(login_win)

    # ------------- Main Screen ------------- #
        def create_main_screen(self):
         for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#f0f0f0")
        try:
            self.logo_image = tk.PhotoImage(file="my_logo.png")
            logo_label = tk.Label(self.root, image=self.logo_image, bg="#f0f0f0")
            logo_label.pack(pady=10)
        except Exception:
            pass
        label_title = tk.Label(self.root, text="بن البركة", font=("Arial", 20, "bold"), fg="brown", bg="#f0f0f0")
        label_title.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="تسجيل عميل جديد", font=("Arial", 12), width=22, command=self.open_add_customer).pack(pady=5)
        tk.Button(btn_frame, text="بحث", font=("Arial", 12), width=22, command=self.open_search).pack(pady=5)
        tk.Button(btn_frame, text="تسجيل موظف جديد", font=("Arial", 12), width=22, command=self.open_employee_screen).pack(pady=5)
        tk.Button(btn_frame, text="عرض العملاء", font=("Arial", 12), width=22, command=self.open_all_customers_screen).pack(pady=5)
        tk.Button(btn_frame, text="🔄 إنشاء نسخة احتياطية", font=("Arial", 12), width=22, command=self.manual_backup).pack(pady=5)

    def manual_backup(self):
        folder = filedialog.askdirectory(title="اختر مجلد النسخة الاحتياطية")
        if folder:
            backup_database(destination=folder)
            messagebox.showinfo("نجاح", "تم حفظ نسخة احتياطية من قاعدة البيانات.")


    # ------------- New Customer Screen ------------- #
    def open_add_customer(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("تسجيل عميل جديد")
        add_win.geometry("500x450")
        add_win.resizable(True, True)
        try:
            add_win.iconbitmap("coffee.ico")
        except Exception:
            pass

        # Title
        title_frame = tk.Frame(add_win)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        title = tk.Label(title_frame, text="تسجيل عميل جديد", font=("Arial", 16, "bold"), fg="brown")
        title.pack(pady=5)
        # Customer form using grid
        form_frame = tk.Frame(add_win)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        lbl_customer_id = tk.Label(form_frame, text="رقم العميل", anchor="e", width=12)
        lbl_customer_id.grid(row=0, column=1, padx=5, pady=5)
        self.entry_customer_id = tk.Entry(form_frame, justify="right")
        self.entry_customer_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_customer_id.config(state='disabled')
        lbl_first_name = tk.Label(form_frame, text="الاسم الأول", anchor="e", width=12)
        lbl_first_name.grid(row=1, column=1, padx=5, pady=5)
        self.entry_first_name = tk.Entry(form_frame, justify="right")
        self.entry_first_name.grid(row=1, column=0, padx=5, pady=5)
        lbl_last_name = tk.Label(form_frame, text="الاسم الثانى", anchor="e", width=12)
        lbl_last_name.grid(row=2, column=1, padx=5, pady=5)
        self.entry_last_name = tk.Entry(form_frame, justify="right")
        self.entry_last_name.grid(row=2, column=0, padx=5, pady=5)
        lbl_phone = tk.Label(form_frame, text="رقم التليفون", anchor="e", width=12)
        lbl_phone.grid(row=3, column=1, padx=5, pady=5)
        self.entry_phone = tk.Entry(form_frame, justify="right")
        self.entry_phone.grid(row=3, column=0, padx=5, pady=5)
        # Instead of free text entry, use a Combobox for employee names
        lbl_employee = tk.Label(form_frame, text="الموظف", anchor="e", width=12)
        lbl_employee.grid(row=4, column=1, padx=5, pady=5)
        self.employee_combobox = ttk.Combobox(form_frame, justify="right")
        self.employee_combobox['values'] = self.get_employee_names()
        self.employee_combobox.grid(row=4, column=0, padx=5, pady=5)

        separator = ttk.Separator(add_win, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=10)
        # Mix Details area (Master-Detail)
        detail_frame = tk.Frame(add_win)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        mix_label = tk.Label(detail_frame, text="التوليفات", font=("Arial", 14, "bold"), fg="brown")
        mix_label.pack(pady=5)
        input_mix_frame = tk.Frame(detail_frame)
        input_mix_frame.pack(fill=tk.X, pady=5)
        self.var_sada = tk.IntVar()
        self.var_mehaweg = tk.IntVar()
        self.var_ispresso = tk.IntVar()
        chk_sada = tk.Checkbutton(input_mix_frame, text="سادة", variable=self.var_sada, anchor="e", justify="right")
        chk_sada.pack(side=tk.RIGHT, padx=5)
        chk_mehaweg = tk.Checkbutton(input_mix_frame, text="محوج", variable=self.var_mehaweg, anchor="e", justify="right")
        chk_mehaweg.pack(side=tk.RIGHT, padx=5)
        chk_ispresso = tk.Checkbutton(input_mix_frame, text="اسبريسو", variable=self.var_ispresso, anchor="e", justify="right")
        chk_ispresso.pack(side=tk.RIGHT, padx=5)
        lbl_mix_details = tk.Label(input_mix_frame, text="التوليفة:", anchor="e", width=8)
        lbl_mix_details.pack(side=tk.RIGHT, padx=5)
        self.entry_mix_details = tk.Entry(input_mix_frame, justify="right")
        self.entry_mix_details.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        btn_add_mix = tk.Button(input_mix_frame, text="اضف توليفة", command=self.add_mix_row)
        btn_add_mix.pack(side=tk.RIGHT, padx=5)
        tree_frame = tk.Frame(detail_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        columns = ("mix_id", "date", "category", "details")
        self.tree_mixes = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree_mixes.heading("mix_id", text="رقم التوليفة")
        self.tree_mixes.heading("date", text="التاريخ")
        self.tree_mixes.heading("category", text="نوع التوليفة")
        self.tree_mixes.heading("details", text="التوليفة")
        self.tree_mixes.column("mix_id", width=80, anchor="center")
        self.tree_mixes.column("date", width=100, anchor="center")
        self.tree_mixes.column("category", width=100, anchor="center")
        self.tree_mixes.column("details", width=150, anchor="w")
        self.tree_mixes.pack(fill=tk.BOTH, expand=True)
        btn_frame = tk.Frame(add_win)
        btn_frame.pack(pady=10)
        btn_save = tk.Button(btn_frame, text="حفظ", width=10, command=self.save_customer)
        btn_save.pack(side=tk.RIGHT, padx=10)
        btn_cancel = tk.Button(btn_frame, text="الغاء", width=10, command=add_win.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=10)
        self.mix_rows = []
        self.entry_first_name.focus_set()

    def add_mix_row(self):
        detail_text = self.entry_mix_details.get().strip()
        if not detail_text:
            messagebox.showwarning("تحذير", "يرجى إدخال تفاصيل التوليفة")
            return
        categories = []
        if self.var_sada.get():
            categories.append("سادة")
        if self.var_mehaweg.get():
            categories.append("محوج")
        if self.var_ispresso.get():
            categories.append("اسبريسو")
        if not categories:
            messagebox.showwarning("تحذير", "يرجى اختيار نوع التوليفة")
            return
        current_date = datetime.now().strftime("%Y-%m-%d")
        for cat in categories:
            temp_id = len(self.mix_rows) + 1
            row = (temp_id, current_date, cat, detail_text)
            self.tree_mixes.insert("", "end", values=row)
            self.mix_rows.append(row)
        self.entry_mix_details.delete(0, tk.END)
        self.var_sada.set(0)
        self.var_mehaweg.set(0)
        self.var_ispresso.set(0)

    def save_customer(self):
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get().strip()
        phone = self.entry_phone.get().strip()
        employer = self.employee_combobox.get().strip()
        if not (first_name and last_name and phone and employer):
            messagebox.showwarning("تنبيه", "جميع الحقول مطلوبة")
            return
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (first_name, last_name, phone, employer) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, phone, employer))
        customer_id = cursor.lastrowid
        for child in self.tree_mixes.get_children():
            values = self.tree_mixes.item(child, "values")
            date_val = values[1]
            category = values[2]
            details = values[3]
            cursor.execute("INSERT INTO mixes (customer_id, date, category, details) VALUES (?, ?, ?, ?)",
                           (customer_id, date_val, category, details))
        conn.commit()
        conn.close()
        messagebox.showinfo("نجاح", "تم حفظ بيانات العميل والتوليفات")
        self.create_main_screen()

    def get_employee_names(self):
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM employees")
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]

    # ------------- Search Screen ------------- #
    def open_search(self):
        search_win = tk.Toplevel(self.root)
        search_win.title("بحث")
        search_win.geometry("700x550")
        search_win.resizable(True, True)
        try:
            search_win.iconbitmap("coffee.ico")
        except Exception:
            pass
        lbl_title = tk.Label(search_win, text="بحث", font=("Arial", 16, "bold"), fg="brown")
        lbl_title.pack(pady=5)
        criteria_frame = tk.Frame(search_win)
        criteria_frame.pack(pady=5, fill=tk.X, padx=10)
        self.search_by_name = tk.IntVar()
        self.search_by_phone = tk.IntVar()
        self.search_by_id = tk.IntVar()
        chk_name = tk.Checkbutton(criteria_frame, text="بحث بالاسم", variable=self.search_by_name, anchor="e", justify="right")
        chk_name.pack(side=tk.RIGHT, padx=5)
        chk_phone = tk.Checkbutton(criteria_frame, text="رقم التليفون", variable=self.search_by_phone, anchor="e", justify="right")
        chk_phone.pack(side=tk.RIGHT, padx=5)
        chk_id = tk.Checkbutton(criteria_frame, text="رقم العميل", variable=self.search_by_id, anchor="e", justify="right")
        chk_id.pack(side=tk.RIGHT, padx=5)
        self.search_text = tk.Entry(criteria_frame, justify="right")
        self.search_text.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        btn_frame = tk.Frame(search_win)
        btn_frame.pack(pady=5)
        btn_search = tk.Button(btn_frame, text="بحث", command=lambda: self.perform_search(search_win))
        btn_search.pack(side=tk.RIGHT, padx=5)
        btn_next = tk.Button(btn_frame, text="التالى", command=lambda: self.next_search_result(search_win))
        btn_next.pack(side=tk.RIGHT, padx=5)
        master_frame = tk.Frame(search_win)
        master_frame.pack(pady=5, fill=tk.X, padx=10)
        lbl_cust_id = tk.Label(master_frame, text="رقم العميل", anchor="e", width=12)
        lbl_cust_id.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry_id = tk.Entry(master_frame, justify="right")
        self.search_entry_id.grid(row=0, column=0, padx=5, pady=5)
        lbl_cust_name = tk.Label(master_frame, text="اسم العميل", anchor="e", width=12)
        lbl_cust_name.grid(row=1, column=1, padx=5, pady=5)
        self.search_entry_name = tk.Entry(master_frame, justify="right")
        self.search_entry_name.grid(row=1, column=0, padx=5, pady=5)
        lbl_cust_phone = tk.Label(master_frame, text="رقم التليفون", anchor="e", width=12)
        lbl_cust_phone.grid(row=2, column=1, padx=5, pady=5)
        self.search_entry_phone = tk.Entry(master_frame, justify="right")
        self.search_entry_phone.grid(row=2, column=0, padx=5, pady=5)
        lbl_cust_employer = tk.Label(master_frame, text="اسم الموظف", anchor="e", width=12)
        lbl_cust_employer.grid(row=3, column=1, padx=5, pady=5)
        self.search_entry_employer = tk.Entry(master_frame, justify="right")
        self.search_entry_employer.grid(row=3, column=0, padx=5, pady=5)
        for entry in [self.search_entry_id, self.search_entry_name, self.search_entry_phone, self.search_entry_employer]:
            entry.config(state='readonly')
        self.edit_mode = False
        # Mix filter section
        mix_frame = tk.Frame(search_win)
        mix_frame.pack(pady=5)
        self.filter_sada = tk.IntVar(value=1)
        self.filter_mehaweg = tk.IntVar(value=1)
        self.filter_ispresso = tk.IntVar(value=1)
        chk_filter_sada = tk.Checkbutton(mix_frame, text="سادة", variable=self.filter_sada, anchor="e", justify="right", command=self.update_mix_filter)
        chk_filter_sada.pack(side=tk.RIGHT, padx=5)
        chk_filter_mehaweg = tk.Checkbutton(mix_frame, text="محوج", variable=self.filter_mehaweg, anchor="e", justify="right", command=self.update_mix_filter)
        chk_filter_mehaweg.pack(side=tk.RIGHT, padx=5)
        chk_filter_ispresso = tk.Checkbutton(mix_frame, text="اسبريسو", variable=self.filter_ispresso, anchor="e", justify="right", command=self.update_mix_filter)
        chk_filter_ispresso.pack(side=tk.RIGHT, padx=5)
        tree_frame = tk.Frame(search_win)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("date", "details", "category")
        self.search_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.search_tree.heading("date", text="التاريخ")
        self.search_tree.heading("details", text="التوليفة")
        self.search_tree.heading("category", text="النوع")
        self.search_tree.column("date", width=120, anchor="center")
        self.search_tree.column("details", width=250, anchor="w")
        self.search_tree.column("category", width=120, anchor="center")
        self.search_tree.pack(fill=tk.BOTH, expand=True)
        self.search_tree.bind("<Double-1>", self.on_mix_double_click)
        update_frame = tk.Frame(search_win)
        update_frame.pack(pady=5)
        btn_edit = tk.Button(update_frame, text="تعديل بيانات العميل", command=self.enable_update)
        btn_edit.pack(side=tk.RIGHT, padx=5)
        btn_save_update = tk.Button(update_frame, text="حفظ بيانات العميل", command=self.save_update)
        btn_save_update.pack(side=tk.RIGHT, padx=5)
        details_button_frame = tk.Frame(search_win)
        details_button_frame.pack(pady=5)
        btn_add_new_mix = tk.Button(details_button_frame, text="اضافة توليفة جديدة", command=self.add_new_mix_record)
        btn_add_new_mix.pack(side=tk.RIGHT, padx=5)
        self.search_results = []
        self.search_index = 0

    def perform_search(self, win):
        query = self.search_text.get().strip()
        if not query:
            messagebox.showwarning("تنبيه", "يرجى إدخال نص البحث")
            return
        cond = []
        params = []
        if self.search_by_name.get():
            cond.append("(first_name LIKE ? OR last_name LIKE ?)")
            params.extend(['%' + query + '%', '%' + query + '%'])
        if self.search_by_phone.get():
            cond.append("phone LIKE ?")
            params.append('%' + query + '%')
        if self.search_by_id.get():
            cond.append("id = ?")
            params.append(query)
        if not cond:
            messagebox.showwarning("تنبيه", "يرجى اختيار معيار البحث")
            return
        sql = "SELECT * FROM customers WHERE " + " OR ".join(cond)
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute(sql, params)
        self.search_results = cursor.fetchall()
        conn.close()
        if not self.search_results:
            messagebox.showinfo("نتيجة", "لم يتم العثور على نتائج")
            return
        self.search_index = 0
        self.display_search_result()

    def display_search_result(self):
        if not self.search_results or self.search_index >= len(self.search_results):
            return
        customer = self.search_results[self.search_index]
        cust_id, first_name, last_name, phone, employer = customer
        full_name = first_name + " " + last_name
        self.current_customer_id = cust_id
        for entry in [self.search_entry_id, self.search_entry_name, self.search_entry_phone, self.search_entry_employer]:
            entry.config(state='normal')
        self.search_entry_id.delete(0, tk.END)
        self.search_entry_id.insert(0, str(cust_id))
        self.search_entry_name.delete(0, tk.END)
        self.search_entry_name.insert(0, full_name)
        self.search_entry_phone.delete(0, tk.END)
        self.search_entry_phone.insert(0, phone)
        self.search_entry_employer.delete(0, tk.END)
        self.search_entry_employer.insert(0, employer)
        if not self.edit_mode:
            for entry in [self.search_entry_id, self.search_entry_name, self.search_entry_phone, self.search_entry_employer]:
                entry.config(state='readonly')
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT mix_id, date, details, category FROM mixes WHERE customer_id = ?", (cust_id,))
        mixes = cursor.fetchall()
        conn.close()
        self.all_mixes = mixes
        self.update_mix_filter()

    def update_mix_filter(self):
        for child in self.search_tree.get_children():
            self.search_tree.delete(child)
        if not hasattr(self, "all_mixes"):
            return
        selected_categories = []
        if self.filter_sada.get():
            selected_categories.append("سادة")
        if self.filter_mehaweg.get():
            selected_categories.append("محوج")
        if self.filter_ispresso.get():
            selected_categories.append("اسبريسو")
        for row in self.all_mixes:
            mix_id, date_val, details_val, category_val = row
            if category_val in selected_categories:
                self.search_tree.insert("", "end", iid=mix_id, values=(date_val, details_val, category_val))

    def next_search_result(self, win):
        if not self.search_results:
            return
        self.search_index += 1
        if self.search_index >= len(self.search_results):
            messagebox.showinfo("نتيجة", "لا توجد نتائج أخرى")
            self.search_index = len(self.search_results) - 1
        else:
            self.display_search_result()

    def enable_update(self):
        for entry in [self.search_entry_name, self.search_entry_phone, self.search_entry_employer]:
            entry.config(state='normal')
        self.edit_mode = True
        messagebox.showinfo("تنبيه", "يمكنك تعديل بيانات العميل والتوليفات الآن")

    def save_update(self):
        cust_id = self.search_entry_id.get().strip()
        full_name = self.search_entry_name.get().strip()
        phone = self.search_entry_phone.get().strip()
        employer = self.search_entry_employer.get().strip()
        if not (cust_id and full_name and phone and employer):
            messagebox.showwarning("تنبيه", "يرجى ملء جميع الحقول")
            return
        parts = full_name.split()
        first_name = parts[0] if parts else ""
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE customers SET first_name = ?, last_name = ?, phone = ?, employer = ? WHERE id = ?",
                       (first_name, last_name, phone, employer, cust_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("نجاح", "تم تحديث بيانات العميل")
        for entry in [self.search_entry_name, self.search_entry_phone, self.search_entry_employer]:
            entry.config(state='readonly')
        self.edit_mode = False

    def on_mix_double_click(self, event):
        if not self.edit_mode:
            messagebox.showinfo("تنبيه", "يرجى الضغط على زر تعديل لتمكين تعديل التوليفات")
            return
        mix_id = self.search_tree.identify_row(event.y)
        if not mix_id:
            return
        values = self.search_tree.item(mix_id, "values")
        if not values:
            return
        date_val, details_val, category_val = values
        edit_win = tk.Toplevel(self.root)
        edit_win.title("تعديل التوليفة")
        edit_win.geometry("400x200")
        tk.Label(edit_win, text="التاريخ", anchor="e", width=12).grid(row=0, column=1, padx=5, pady=5)
        entry_date = tk.Entry(edit_win, justify="right")
        entry_date.grid(row=0, column=0, padx=5, pady=5)
        entry_date.insert(0, date_val)
        tk.Label(edit_win, text="التوليفة", anchor="e", width=12).grid(row=1, column=1, padx=5, pady=5)
        entry_details = tk.Entry(edit_win, justify="right")
        entry_details.grid(row=1, column=0, padx=5, pady=5)
        entry_details.insert(0, details_val)
        tk.Label(edit_win, text="النوع", anchor="e", width=12).grid(row=2, column=1, padx=5, pady=5)
        category_var = tk.StringVar()
        category_var.set(category_val)
        options = ["سادة", "محوج", "اسبريسو"]
        optionmenu = tk.OptionMenu(edit_win, category_var, *options)
        optionmenu.grid(row=2, column=0, padx=5, pady=5)
        def save_mix_update():
            new_date = entry_date.get().strip()
            new_details = entry_details.get().strip()
            new_category = category_var.get().strip()
            if not new_date or not new_details or not new_category:
                messagebox.showwarning("تنبيه", "جميع الحقول مطلوبة", parent=edit_win)
                return
            conn = sqlite3.connect("coffee_shop.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE mixes SET date = ?, details = ?, category = ? WHERE mix_id = ?",
                           (new_date, new_details, new_category, mix_id))
            conn.commit()
            conn.close()
            self.search_tree.item(mix_id, values=(new_date, new_details, new_category))
            messagebox.showinfo("نجاح", "تم تحديث التوليفة", parent=edit_win)
            edit_win.destroy()
            self.update_mix_filter()
        btn_save = tk.Button(edit_win, text="حفظ", command=save_mix_update)
        btn_save.grid(row=3, column=0, columnspan=2, pady=10)

    def add_new_mix_record(self):
        if not hasattr(self, "current_customer_id"):
            messagebox.showwarning("تنبيه", "لا يوجد عميل محدد")
            return
        new_win = tk.Toplevel(self.root)
        new_win.title("اضافة توليفة جديدة")
        new_win.geometry("400x200")
        tk.Label(new_win, text="التاريخ", anchor="e", width=12).grid(row=0, column=1, padx=5, pady=5)
        entry_date = tk.Entry(new_win, justify="right")
        entry_date.grid(row=0, column=0, padx=5, pady=5)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        tk.Label(new_win, text="التوليفة", anchor="e", width=12).grid(row=1, column=1, padx=5, pady=5)
        entry_details = tk.Entry(new_win, justify="right")
        entry_details.grid(row=1, column=0, padx=5, pady=5)
        tk.Label(new_win, text="النوع", anchor="e", width=12).grid(row=2, column=1, padx=5, pady=5)
        new_category_var = tk.StringVar()
        new_category_var.set("سادة")
        options = ["سادة", "محوج", "اسبريسو"]
        optionmenu = tk.OptionMenu(new_win, new_category_var, *options)
        optionmenu.grid(row=2, column=0, padx=5, pady=5)
        def save_new_mix():
            new_date = entry_date.get().strip()
            new_details = entry_details.get().strip()
            new_category = new_category_var.get().strip()
            if not new_date or not new_details or not new_category:
                messagebox.showwarning("تنبيه", "جميع الحقول مطلوبة", parent=new_win)
                return
            cust_id = self.current_customer_id
            conn = sqlite3.connect("coffee_shop.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mixes (customer_id, date, category, details) VALUES (?, ?, ?, ?)",
                           (cust_id, new_date, new_category, new_details))
            conn.commit()
            conn.close()
            messagebox.showinfo("نجاح", "تم اضافة التوليفة الجديدة", parent=new_win)
            new_win.destroy()
            self.update_mix_details()
        btn_save_new = tk.Button(new_win, text="حفظ", command=save_new_mix)
        btn_save_new.grid(row=3, column=0, columnspan=2, pady=10)

    def update_mix_details(self):
        if not hasattr(self, "current_customer_id"):
            return
        cust_id = self.current_customer_id
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT mix_id, date, details, category FROM mixes WHERE customer_id = ?", (cust_id,))
        mixes = cursor.fetchall()
        conn.close()
        self.all_mixes = mixes
        self.update_mix_filter()

    # ------------- Employee Registration Screen ------------- #
    def open_employee_screen(self):
        emp_win = tk.Toplevel(self.root)
        emp_win.title("تسجيل موظف جديد")
        emp_win.geometry("400x300")
        emp_win.resizable(False, False)
        lbl_title = tk.Label(emp_win, text="تسجيل موظف جديد", font=("Arial", 16, "bold"), fg="brown")
        lbl_title.pack(pady=10)
        form_frame = tk.Frame(emp_win)
        form_frame.pack(pady=10, padx=10)
        lbl_name = tk.Label(form_frame, text="الاسم", anchor="e", width=12)
        lbl_name.grid(row=0, column=1, padx=5, pady=5)
        entry_name = tk.Entry(form_frame, justify="right")
        entry_name.grid(row=0, column=0, padx=5, pady=5)
        lbl_username = tk.Label(form_frame, text="اسم المستخدم", anchor="e", width=12)
        lbl_username.grid(row=1, column=1, padx=5, pady=5)
        entry_username = tk.Entry(form_frame, justify="right")
        entry_username.grid(row=1, column=0, padx=5, pady=5)
        lbl_password = tk.Label(form_frame, text="كلمة المرور", anchor="e", width=12)
        lbl_password.grid(row=2, column=1, padx=5, pady=5)
        entry_password = tk.Entry(form_frame, show="*", justify="right")
        entry_password.grid(row=2, column=0, padx=5, pady=5)
        def save_employee():
            name = entry_name.get().strip()
            username = entry_username.get().strip()
            password = entry_password.get().strip()
            if not (name and username and password):
                messagebox.showwarning("تنبيه", "جميع الحقول مطلوبة", parent=emp_win)
                return
            conn = sqlite3.connect("coffee_shop.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO employees (name, username, password) VALUES (?, ?, ?)",
                               (name, username, password))
                conn.commit()
                messagebox.showinfo("نجاح", "تم تسجيل الموظف بنجاح", parent=emp_win)
                emp_win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "اسم المستخدم موجود مسبقاً", parent=emp_win)
            finally:
                conn.close()
        btn_frame = tk.Frame(emp_win)
        btn_frame.pack(pady=10)
        btn_save = tk.Button(btn_frame, text="حفظ", command=save_employee)
        btn_save.pack(side=tk.RIGHT, padx=5)
        btn_cancel = tk.Button(btn_frame, text="الغاء", command=emp_win.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    # ------------- All Customers Screen ------------- #
    def open_all_customers_screen(self):
        all_cust_win = tk.Toplevel(self.root)
        all_cust_win.title("عرض جميع العملاء")
        all_cust_win.geometry("800x600")
        all_cust_win.resizable(True, True)
        # Frame for the customers list
        cust_frame = tk.Frame(all_cust_win)
        cust_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        lbl_cust = tk.Label(cust_frame, text="قائمة العملاء", font=("Arial", 14, "bold"), fg="brown")
        lbl_cust.pack(pady=5)
        # Total count label
        self.lbl_total_cust = tk.Label(cust_frame, text="عدد العملاء الكلي: 0", font=("Arial", 12), fg="blue")
        self.lbl_total_cust.pack(pady=5)
        columns = ("id", "name", "phone", "employer")
        self.all_customers_tree = ttk.Treeview(cust_frame, columns=columns, show="headings")
        self.all_customers_tree.heading("id", text="رقم العميل")
        self.all_customers_tree.heading("name", text="الاسم")
        self.all_customers_tree.heading("phone", text="رقم التليفون")
        self.all_customers_tree.heading("employer", text="اسم الموظف")
        self.all_customers_tree.column("id", width=80, anchor="center")
        self.all_customers_tree.column("name", width=200, anchor="center")
        self.all_customers_tree.column("phone", width=120, anchor="center")
        self.all_customers_tree.column("employer", width=150, anchor="center")
        self.all_customers_tree.pack(fill=tk.BOTH, expand=True)
        self.load_all_customers()
        self.all_customers_tree.bind("<<TreeviewSelect>>", self.on_customer_select)
        # Frame for mix details
        details_frame = tk.Frame(all_cust_win)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        lbl_details = tk.Label(details_frame, text="تفاصيل التوليفات", font=("Arial", 14, "bold"), fg="brown")
        lbl_details.pack(pady=5)
        mix_columns = ("date", "category", "details")
        self.customer_mix_tree = ttk.Treeview(details_frame, columns=mix_columns, show="headings")
        self.customer_mix_tree.heading("date", text="التاريخ")
        self.customer_mix_tree.heading("category", text="النوع")
        self.customer_mix_tree.heading("details", text="التوليفة")
        self.customer_mix_tree.column("date", width=120, anchor="center")
        self.customer_mix_tree.column("category", width=100, anchor="center")
        self.customer_mix_tree.column("details", width=400, anchor="w")
        self.customer_mix_tree.pack(fill=tk.BOTH, expand=True)

    def load_all_customers(self):
        for child in self.all_customers_tree.get_children():
            self.all_customers_tree.delete(child)
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, phone, employer FROM customers ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        self.lbl_total_cust.config(text="عدد العملاء الكلي: " + str(len(rows)))
        for row in rows:
            cust_id = row[0]
            full_name = row[1] + " " + row[2]
            phone = row[3]
            employer = row[4]
            self.all_customers_tree.insert("", "end", iid=cust_id, values=(cust_id, full_name, phone, employer))

    def on_customer_select(self, event):
        selected = self.all_customers_tree.selection()
        if not selected:
            return
        cust_id = selected[0]
        self.load_customer_mixes(cust_id)

    def load_customer_mixes(self, cust_id):
        for child in self.customer_mix_tree.get_children():
            self.customer_mix_tree.delete(child)
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT date, category, details FROM mixes WHERE customer_id = ?", (cust_id,))
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.customer_mix_tree.insert("", "end", values=row)

# ------------------------------ #
# Entry Point
# ------------------------------ #
if __name__ == "__main__":
    init_db()  # Initialize database and tables
    root = tk.Tk()
    app = CoffeeShopApp(root)
    root.mainloop()
