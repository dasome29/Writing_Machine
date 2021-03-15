from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('My Title')
root.geometry('1200x660')

def newFile():
    # Delete previous text
    myText.delete("1.0", END)
    # Update status bars
    root.title('New File')
    statusBar.config(text="New File")

# Save as File
def save_as_file():
    textFile = filedialog.asksaveasfilename(defaultextension=".*",initialdir="/Users/migue/Desktop/files_ide", title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if textFile:
        # Update status bars
        name = textFile
        statusBar.config(text="Saved: " +name)
        name = name.replace("/Users/migue/Desktop/files_ide/", "")
        root.title(name)

        # Save the file
        textFile = open(textFile, 'w')
        textFile.write(myText.get(1.0, END))
        # Close the file
        textFile.close()

def openFile():
    # Delete previous text
    myText.delete("1.0", END)

    # Grab Filename
    textFile = filedialog.askopenfilename(initialdir="/Users/migue/Desktop/files_ide", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    
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


# Create Main Frame
myFrame = Frame(root)
myFrame.pack(pady=5)

# Create our Scrollbar for the Text Box
textScroll = Scrollbar(myFrame)
myFrame.pack(side=RIGHT, fill=Y)

# Create Text Box
myText = Text(myFrame, width=97, height=25, font=("Helvetica",16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=textScroll.set)
myText.pack()

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
fileMenu.add_command(label="Save")
fileMenu.add_command(label="Save As", command=save_as_file)
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
statusBar.pack(fill=X, side= BOTTOM, ipady=5)


root.mainloop()