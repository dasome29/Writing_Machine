from tkinter import *
from tkinter import filedialog
from tkinter import font
import getpass

from main import *

root = Tk()
root.title('My Title')
root.geometry('1000x660')
root.resizable(width=False, height=False)

# Set variable for open file name
global openStatusName
openStatusName = False

def getPath():
    user = getpass.getuser()
    print(user)

# Create a new file
def newFile():
    # Delete previous text
    myText.delete("1.0", END)
    # Update status bars
    root.title('New File')
    statusBar.config(text="New File")
    global openStatusName
    openStatusName = False


def compile(data):
    lexer = Lexer()
    parser = Parser(Lexer())
    lexer.run(data)
    if lexer.errors:
        return (lexer.errors[0])
    else:
        parsed = parser.parse(data)
        if parser.errors:
            return (parser.errors[0])
        else:
            semantic = Semantic()
            result = semantic.analyze(parsed)
            if semantic.errors:
                return (semantic.errors[0])
            else:
                return result


# Save as File
def saveAsFile():
    textFile = filedialog.asksaveasfilename(defaultextension=".*",title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if textFile:
        # Update status bars
        name = textFile
        statusBar.config(text="Saved: " + name)
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
    textFile = filedialog.askopenfilename(title="Open File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    # Check to see if there's a file name
    if textFile:
        # Make file name global to access later
        global openStatusName
        openStatusName = textFile

    # Update status bars
    name = textFile
    statusBar.config(text=name)
    root.title(name)

    # Open the file
    textFile = open(textFile, 'r')
    stuff = textFile.read()
    # Add file to textbox
    myText.insert(END, stuff)
    # Close the opend file
    textFile.close()


def executeCode():
    T.delete("1.0", END)

    input = myText.get("1.0", END)
    output = compile(input)

    # print("Input: " + input)
    # print("Output: "+output)

    if output:
        for i in output:
            T.insert(END, i + "| ")


# Create Main Frame
myFrame = Canvas(root, width=1200, height=660)
myFrame.place(x=0, y=0)

# Add Button for compilation and execution
btn_exec = Button(myFrame, text="Execute", fg="black", command=executeCode)
btn_exec.place(x=0, y=0)

btn_algo = Button(myFrame, text="algo", fg="black", command=getPath)
btn_algo.place(x=85, y=0)

# Add text field for console
T = Text(myFrame, height=12, width=125)
T.place(x=0, y=484)
T.insert(END, "Welcome to Writing Machine!")
# T.configure(state=DISABLED)

# Create our Scrollbar for the Text Box
textScroll = Scrollbar(myFrame)
myFrame.pack(side=RIGHT, fill=Y)

# Create Text Box
myText = Text(myFrame, width=83, height=18, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black",
              undo=True, yscrollcommand=textScroll.set)
myText.place(x=0, y=25)

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