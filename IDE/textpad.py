from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('My Title')
root.geometry('1200x660')

# Create Main Frame
myFrame = Frame(root)
myFrame.pack(pady=5)

# Create our Scrollbar for the Text Box
textScroll = Scrollbar(myFrame)
myFrame.pack(side=RIGHT, fill=Y)

# Create Text Box
myText = Text(myFrame, width=97, height=25, font=("Helvetica",16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=textScroll.set)
myText.pack()
root.mainloop()

# Configure our Scrollbar
textScroll.config(command=myText.yview)