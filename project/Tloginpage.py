from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3


root = Tk()
root.geometry('3000x1000')
bgimage = ImageTk.PhotoImage(file='Blue.jpg')

con = sqlite3.connect('dataT.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Teachers (
            username TEXT NOT NULL,
            password TEXT NOT NULL)''')
con.commit()
con.close() 


def eye():
    global ceyeimage, oeyeimg
    if passwentry.cget('show') == '*':
        passwentry.config(show='')
        eyebutton.config(image=ceyeimage)
    else:
        passwentry.config(show='*')
        eyebutton.config(image=oeyeimg)

def Teacher():
    if userentry.get()=='' or passwentry.get()=='':
        messagebox.showerror(title='Error', message='All fields are Required!')
    else:
        user = userentry.get()
        passw = passwentry.get()
        conn = sqlite3.connect('dataT.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Teachers WHERE username = ? AND password = ?", (user, passw))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login Successful!")
            root.destroy()
            import Tresultpage
        else:
            messagebox.showerror("Failure", "Login Failed. Incorrect username or password.")

bglabel = Label(root, image=bgimage)
bglabel.place(x=0, y=0)

loginlabel = Label(root, text='Teacher Login', font=('Arial Black', '30'), bg='#9AD9EA', fg='#153E7D')
loginlabel.place(x=880, y=130)

userentry = Entry(root, width=40, font=('Arial', 10,'bold'), bd=0, fg='#153E7D', bg='#9AD9EA')
userentry.place(x=880,y=270)

userlabel = Label(root, text='Username', font=('Arial', 10,'bold'), bg='#9AD9EA', fg='#153E7D')
userlabel.place(x=880,y=250)

f1 = Frame(root, width=280, height=2, bg='#153E7D')
f1.place(x=880, y=288)

passwentry = Entry(root, width=40, font=('Arial', 10,'bold'), bd=0, fg='#153E7D', bg='#9AD9EA', show='*')
passwentry.place(x=880,y=322)

passwlabel = Label(root, text='Password', font=('Arial', 10,'bold'), bg='#9AD9EA', fg='#153E7D')
passwlabel.place(x=880,y=300)

f2 = Frame(root, width=280, height=2, bg='#153E7D')
f2.place(x=880, y=340)

Loginbutton = Button(root, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='#153e7D', activeforeground='white', activebackground='#153e7D', cursor='hand2', bd=0, width=20, command=Teacher)
Loginbutton.place(x=880, y=380)

image1 = Image.open('oeye.png')
image2 = Image.open('ceye.png')

desired_width = 20
desired_height = 20

image11 = image1.resize((desired_width, desired_height))
image22 = image2.resize((desired_width, desired_height))

ceyeimage = ImageTk.PhotoImage(image22)
oeyeimg = ImageTk.PhotoImage(image11)

eyebutton = Button(root, image=oeyeimg, bg='#9AD9EA', bd=0, activebackground='#153e7D', cursor='hand2', command=eye)
eyebutton.place(x=1150, y=310)

root.mainloop()