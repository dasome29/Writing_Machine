from tkinter import *
from tkinter import filedialog
from tkinter import font

from main import *


root = Tk()
root.title('My Title')
root.geometry('1000x660')
root.resizable(width=False, height=False)

# Set variable for open file name
global openStatusName
openStatusName = False

# Create a new file
def newFile():
    # Delete previous text
    myText.delete("1.0", END)
    # Update status bars
    root.title('New File')
    statusBar.config(text="New File")
    global openStatusName
    openStatusName = False

# Save as File
def saveAsFile():
    textFile = filedialog.asksaveasfilename(defaultextension=".*", initialdir="/Users/migue/Desktop/files_ide",
                                            title="Save File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if textFile:
        # Update status bars
        name = textFile
        statusBar.config(text="Saved: " + name)
        name = name.replace("/Users/migue/Desktop/files_ide/", "")
        root.title(name)

        # Save the file
        textFile = open(textFile, 'w')
        textFile.write(myText.get(1.0, END))
        # Close the file
        textFile.close()

# Save File
def saveFile():
    global openStatusName
    if openStatusName:
        # Save the file
        textFile = open(openStatusName, 'w')
        textFile.write(myText.get(1.0, END))
        # Close the file
        textFile.close()
        statusBar.config(text="Saved: " + openStatusName)
    else:
        saveAsFile()


# Open an existent file
def openFile():
    # Delete previous text
    myText.delete("1.0", END)

    # Grab Filename
    textFile = filedialog.askopenfilename(initialdir="/Users/migue/Desktop/files_ide", title="Open File", filetypes=(
    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    # Check to see if there's a file name
    if textFile:
        # Make file name global to access later
        global openStatusName
        openStatusName = textFile

    # Update status bars
    name = textFile
    statusBar.config(text=name)
    name = name.replace("/Users/migue/Desktop/files_ide/", "")
    root.title(name)

    # Open the file
    textFile = open(textFile, 'r')
    stuff = textFile.read()
    # Add file to textbox
    myText.insert(END, stuff)
    # Close the opend file
    textFile.close()

def executeCode():
    compiler = Compiler()
    
    output = compiler.compile(myText.get("1.0",END))
    T.configure(state=NORMAL)
    T.delete("1.0",END)
    if output:
        for i in output:
            T.insert(END, i)
        T.configure(state=DISABLED)


# Create Main Frame
myFrame = Canvas(root, width=1200, height=660)
myFrame.place(x=0,y=0)

# Add Button for compilation and execution
btn_exec = Button(myFrame, text="Execute",fg="white", command=executeCode)
btn_exec.place(x=900, y=10)

# Add text field for console
T = Text(myFrame, height=12, width=125)
T.place(x=0,y=484)
T.insert(END, "Algo de texto\nmas texto en la siguiente linea")
T.configure(state=DISABLED)

# Create our Scrollbar for the Text Box
textScroll = Scrollbar(myFrame)
myFrame.pack(side=RIGHT, fill=Y)

# Create Text Box
myText = Text(myFrame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=textScroll.set)
myText.place(x=0,y=0)

# Configure our Scrollbar
textScroll.config(command=myText.yview)

# Create Menu
myMenu = Menu(root)
root.config(menu=myMenu)


# Add File Menu
fileMenu = Menu(myMenu, tearoff=False)
myMenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_command(label="Save As", command=saveAsFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)

# Add Edit Menu
editMenu = Menu(myMenu, tearoff=False)
myMenu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Cut")
editMenu.add_command(label="Copy")
editMenu.add_command(label="Paste")
editMenu.add_command(label="Undo")
editMenu.add_command(label="Redo")

# Add Status Bar to Bottom of App
statusBar = Label(root, text='Ready', anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=5)


root.mainloop()