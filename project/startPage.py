from tkinter import *
from PIL import ImageTk

window = Tk()
window.geometry('3000x1400')

def student():
    window.destroy()
    import Stloginpage

def teacher():
    window.destroy()
    import Tloginpage

bgimage = ImageTk.PhotoImage(file='Blue.jpg')

bglabel = Label(window, image=bgimage)
bglabel.place(x=0, y=0)

headinglabel = Label(window, text='Hello There', font=('Arial Black', '30'), bg='#9AD9EA', fg='#153E7D')
headinglabel.place(x=905, y=130)

wholabel = Label(window, text='Who are you?', font=('Arial', '15'), bg='#9AD9EA', fg='#153E7D')
wholabel.place(x=880,y=270)

studentbutton = Button(window, text='Student', font=('Open Sans', 16, 'bold'), fg='white', bg='#153e7D', activeforeground='white', activebackground='#153e7D', cursor='hand2', bd=0, width=20, command=student)
studentbutton.place(x=880, y=320)

teacherbutton = Button(window, text='Teacher', font=('Open Sans', 16, 'bold'), fg='white', bg='#153e7D', activeforeground='white', activebackground='#153e7D', cursor='hand2', bd=0, width=20, command=teacher)
teacherbutton.place(x=880, y=370)


window.mainloop()
