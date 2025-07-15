from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


window = Tk()
window.geometry('3000x1000')

bgimage = ImageTk.PhotoImage(file='Blue.jpg')

bglabel = Label(window, image=bgimage)
bglabel.place(x=0, y=0)

con = sqlite3.connect('dataP.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS students (
            enrollment TEXT NOT NULL,
            password TEXT NOT NULL)''')
con.commit()
con.close() 

def open_result_page(username):
    conn = sqlite3.connect('dataP.db')
    cursor = conn.cursor()
    cursor.execute("SELECT enroll, stream, dob, username FROM students WHERE enroll = ?", (username,))
    values = cursor.fetchall()

    enrolldata = values[0][0]
    streamdata = values[0][1]
    dobdata = values[0][2]
    userdata = values[0][3]

    conn.close()

    result_window = Tk()
    result_window.geometry('1400x800')
    result_window.title('Result')

    style = ttk.Style(result_window)
    try:
        result_window.tk.call("source", "forest-dark.tcl")
    except Exception:
        pass  
    style.theme_use("forest-dark")

    use = ttk.Label(result_window, text=f"State of marks of {userdata}", font=('Arial', '30'))
    use.pack(pady=40)

    treeframe = ttk.Frame(result_window)
    treeframe.place(x=60,y=220)

    cols = ['subjects', 'CA marks', 'assigh/projects', 'End-sem marks', 'Total marks']
    treeview = ttk.Treeview(treeframe, columns=cols, show='headings', height=5)
    for col in cols:
        treeview.heading(col, text=col, anchor='center')
        treeview.column(col, width=120, anchor='center')
    treeview.pack()

    conn = sqlite3.connect('dataP.db')
    cursor = conn.cursor()

    cursor.execute("SELECT subjects, CA, assighment, end, Total FROM results WHERE enroll = ?", (username,))
    rows = cursor.fetchall()

    for row in rows:
        treeview.insert("", "end", values=row)

    conn.close()

    conn = sqlite3.connect('dataP.db')
    cursor = conn.cursor()
    cursor.execute("SELECT subjects, Total FROM results WHERE enroll = ?", (username,))
    rows = cursor.fetchall()

    marks_data = []
    subjects = []
    for row in rows:
        marks_data.append(row[1])
        subjects.append(row[0])

    max_index = marks_data.index(max(marks_data))
    highest_subject = subjects[max_index]
    highest_marks = marks_data[max_index]     

    conn.close()

    fig1, ax1 = plt.subplots()
    ax1.set_facecolor('#313131')
    fig1.patch.set_facecolor('#414141')
    bars = ax1.bar(subjects, marks_data, color='#515151')
    ax1.set_title('Total marks in subjects chart', color='white')
    ax1.set_xlabel('Subjects', color='white')
    ax1.set_ylabel('marks', color='white')
    for bar, value in zip(bars, marks_data):
        height = bar.get_height()
        ax1.annotate(f'{value}', xy=(bar.get_x() + bar.get_width() / 2, height), ha='center', color='white', fontsize=10)

    ax1.set_yticks([])  
    ax1.set_yticks([10, 30, 50, 70, 90]) 

    ax1.grid(color='#555555', linestyle='--', linewidth=0.5) 
    ax1.tick_params(axis='x', colors='white') 
    ax1.tick_params(axis='y', colors='white')  

    figureframe = ttk.Frame(result_window)
    figureframe.place(x=850,y=100, width=500, height=400)

    canvas1 = FigureCanvasTkAgg(fig1, master=figureframe)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

    proficient = ttk.Label(result_window, text=f"The student is proficient in {highest_subject} with {highest_marks} marks!", font=('Arial', '12'))
    proficient.place(x=860, y=520)

    obtained = ttk.Label(result_window, text=f"Total obtained marks: {sum(marks_data)}/500", font=('Arial', '12'))
    obtained.place(x=60, y=400)

    totalpercentage = ttk.Label(result_window, text=f"Total percentage: {sum(marks_data)/5}%", font=('Arial', '12'))
    totalpercentage.place(x=540, y=400)

    result = ttk.Label(result_window, text=f"Result: {'Pass' if sum(marks_data) >= 250 else 'Fail'}", font=('Arial', '12'))
    result.place(x=60, y=430)

    stname = ttk.Label(result_window, text=f"Student Name: {userdata}", font=('Arial', '12'))
    stname.place(x=60, y=130)

    stenroll = ttk.Label(result_window, text=f"Enrollment No.: {enrolldata}", font=('Arial', '12'))
    stenroll.place(x=60, y=170)

    ststream = ttk.Label(result_window, text=f"Stream: {streamdata}", font=('Arial', '12'))
    ststream.place(x=350, y=130)

    dob = ttk.Label(result_window, text=f"Date of birth: {dobdata}", font=('Arial', '12'))
    dob.place(x=350, y=170)

    session = ttk.Label(result_window, text="Session: 2024-2025", font=('Arial', '12'))
    session.place(x=600, y=130)

    result_window.mainloop()



def whichst():
    if enrollentry.get()=='' or passwentry.get()=='':
        messagebox.showerror(title='Error', message='All fields are Required!')
    else:
        user = enrollentry.get()
        passw = passwentry.get()
        conn = sqlite3.connect('dataP.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE enroll = ? AND password = ?", (user, passw))
        userdata = cursor.fetchone()
        if userdata:
            messagebox.showinfo("Success", "Login Successful!")
            window.destroy()
            open_result_page(user)
        else:
            messagebox.showerror("Failure", "Login Failed. Incorrect Enrollment or password.")

def eye():
    global ceyeimage, oeyeimg
    if passwentry.cget('show') == '*':
        passwentry.config(show='')
        eyebutton.config(image=ceyeimage)
    else:
        passwentry.config(show='*')
        eyebutton.config(image=oeyeimg)
             
loginlabel = Label(window, text='Student Login', font=('Arial Black', '30'), bg='#9AD9EA', fg='#153E7D')
loginlabel.place(x=880, y=130)

enrollment = Label(window, text='Entrollment', font=('Arial', 10,'bold'), bg='#9AD9EA', fg='#153E7D')
enrollment.place(x=880,y=250)

enrollentry = Entry(window, width=40, font=('Arial', 10,'bold'), bd=0, fg='#153E7D', bg='#9AD9EA')
enrollentry.place(x=880,y=270)

f1 = Frame(window, width=280, height=2, bg='#153E7D')
f1.place(x=880, y=288)

password = Label(window, text='Password', font=('Arial', 10,'bold'), bg='#9AD9EA', fg='#153E7D')
password.place(x=880,y=300)

passwentry = Entry(window, width=40, font=('Arial', 10,'bold'), bd=0, fg='#153E7D', bg='#9AD9EA')
passwentry.place(x=880,y=325)
passwentry.config(show='*')

f2= Frame(window, width=280, height=2, bg='#153E7D')
f2.place(x=880, y=343)

Loginbutton = Button(window, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='#153e7D', activeforeground='white', activebackground='#153e7D', cursor='hand2', bd=0, width=20, command=whichst)
Loginbutton.place(x=880, y=400)

image1 = Image.open('oeye.png')
image2 = Image.open('ceye.png')

desired_width = 20
desired_height = 20

image11 = image1.resize((desired_width, desired_height))
image22 = image2.resize((desired_width, desired_height))

ceyeimage = ImageTk.PhotoImage(image22)
oeyeimg = ImageTk.PhotoImage(image11)

eyebutton = Button(window, image=oeyeimg, bg='#9AD9EA', bd=0, activebackground='#153e7D', cursor='hand2', command=eye)
eyebutton.place(x=1150, y=320)

window.mainloop()