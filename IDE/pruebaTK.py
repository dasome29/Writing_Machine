from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('My Title')
root.geometry('1000x660')
root.resizable(width=False, height=False)

myFrame = Canvas(root, width=1200, height=660)
myFrame.place(x=0,y=0)

# Add Button for compilation and execution
btn_exec = Button(myFrame, text="Execute",fg="white")
btn_exec.place(x=900,y=50)

root.mainloop()