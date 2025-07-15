import tkinter as tk
from tkinter import ttk
import sqlite3

root = tk.Tk()
root.geometry('1000x400')
root.title("Forest")

style = ttk.Style(root)
try:
    root.tk.call("source", "forest-dark.tcl")
except tk.TclError:
    pass  
style.theme_use("forest-dark")

mainframe = ttk.Frame(root)
mainframe.pack(fill='both', expand=True)

students = ttk.Label(mainframe, text="Student Result Management System", font=('Arial', '40'))
students.pack(pady=70)

treeframe = ttk.Frame(mainframe)
treeframe.pack()

cols = ('Username', 'DOB', 'Stream', 'Enroll')
treeview = ttk.Treeview(treeframe, columns=cols, show='headings', height=5)
for col in cols:
    treeview.heading(col, text=col, anchor='center')
    treeview.column(col, width=120, anchor='center')
treeview.pack()

def show_student_result(event):
    selected_item = treeview.focus()
    if not selected_item:
        return
    values = treeview.item(selected_item, 'values')
    username = values[0]  

    # --- Result Window ---
    result_window = tk.Toplevel(root)
    result_window.title(f"Result for {username}")
    result_window.geometry("600x600")

    studentname = ttk.Label(result_window, text=f"Edit marks for {username}", font=('Arial', '40'))
    studentname.pack(pady=50)

    header_frame = ttk.Frame(result_window)
    header_frame.pack(pady=(0, 5))
    headers = [
        'Subject    ',
        'CA marks   ',      
        'Assigh/Projects   ',
        'End-sem marks   ', 
        'Total marks   ',
    ]
    for idx, h in enumerate(headers):
        ttk.Label(header_frame, text=h, font=('Arial', 10, 'bold')).grid(row=0, column=idx, padx=2, pady=2)

    marks_frame = ttk.Frame(result_window)
    marks_frame.pack()

    entry_vars = []

    def load_marks():
        for widget in marks_frame.winfo_children():
            widget.destroy()
        entry_vars.clear()
        conn = sqlite3.connect('dataP.db')
        cursor = conn.cursor()
        cursor.execute("SELECT subjects, CA, assighment, end, Total FROM results WHERE username = ?", (username,))
        rows = cursor.fetchall()
        conn.close()
        for i, row in enumerate(rows):
            subject_var = tk.StringVar(value=row[0])
            ca_var = tk.StringVar(value=row[1])
            assigh_var = tk.StringVar(value=row[2])
            end_var = tk.StringVar(value=row[3])
            total_var = tk.StringVar(value=row[4])
            entry_vars.append((subject_var, ca_var, assigh_var, end_var, total_var))
            tk.Label(marks_frame, textvariable=subject_var, width=15).grid(row=i, column=0, padx=2, pady=2)
            tk.Entry(marks_frame, textvariable=ca_var, width=10).grid(row=i, column=1, padx=2, pady=2)
            tk.Entry(marks_frame, textvariable=assigh_var, width=15).grid(row=i, column=2, padx=2, pady=2)
            tk.Entry(marks_frame, textvariable=end_var, width=12).grid(row=i, column=3, padx=2, pady=2)
            tk.Label(marks_frame, textvariable=total_var, width=12).grid(row=i, column=4, padx=2, pady=2)

    def update_marks():
        conn = sqlite3.connect('dataP.db')
        cursor = conn.cursor()
        for vars_tuple in entry_vars:
            subject, ca, assigh, end, total = [v.get() for v in vars_tuple]
            cursor.execute(
                "UPDATE results SET CA=?, assighment=?, end=?, Total=? WHERE username=? AND subjects=?",
                (ca, assigh, end, total, username, subject)
            )
        conn.commit()
        conn.close()
        load_marks()  

    update_btn = ttk.Button(result_window, text="Update", command=update_marks)
    update_btn.pack(pady=40)

    refresh_btn = ttk.Button(result_window, text="Refresh", command=load_marks)
    refresh_btn.pack(pady=10)

    load_marks()

treeview.bind("<<TreeviewSelect>>", show_student_result)

conn = sqlite3.connect('dataP.db')
cursor = conn.cursor()

cursor.execute("SELECT username, dob, stream, enroll FROM students")
rows = cursor.fetchall()

for row in rows:
    treeview.insert("", "end", values=row)

conn.close()

root.mainloop()