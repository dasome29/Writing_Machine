from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import serial
import time
from tkinter import font
import getpass

from main import *
from svgToGcode import *
s = serial.Serial('COM4', 115200)
s.write("\r\n\r\n".encode())
time.sleep(2)  # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
initial = ["$H", "G92 X0 Y0", "F300"]
for i in initial:
    print(f'Sending {i}')
    s.write(f'{i}\n'.encode())
    grbl_out = s.readline()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip().decode())


root = Tk()
root.title('My Title')
root.geometry('1000x660')
root.resizable(width=False, height=False)

global currentSvg
currentSvg = ""

# Set variable for open file name
global openStatusName
openStatusName = False


def importSvg():
    global currentSvg
    # Grab Filename
    textFile = filedialog.askopenfilename(title="Open File", filetypes=(("Svg Files", "*.svg"), ("All Files", "*.*")))
    currentSvg = textFile
    T.delete("1.0", END)
    T.insert(END, "Import successful")


def printImage():
    if currentSvg:
        mySvg_to_gcode = svg_to_gcode()
        mySvg_to_gcode.complier(currentSvg)
        T.delete("1.0", END)
        T.insert(END, "Print successful")
    else:
        T.delete("1.0", END)
        T.insert(END, "No current .svg file found, please import a .svg file first")


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
        return [lexer.errors[0]]
    else:
        parsed = parser.parse(data)
        if parser.errors:
            return [parser.errors[0]]
        else:
            semantic = Semantic()
            result = semantic.analyze(parsed)
            if semantic.errors:
                return [semantic.errors[0]]
            else:
                return result


# Save as File
def saveAsFile():
    textFile = filedialog.asksaveasfilename(title="Save File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    print(textFile)
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

    # Wake up grbl


    if output:
        for i in output:
            print(f'Sending {i}')
            s.write(f'{i}\n'.encode())
            grbl_out = s.readline()  # Wait for grbl response with carriage return
            print(' : ' + grbl_out.strip().decode())
        # Close file and serial port


# Create Main Frame
myFrame = Canvas(root, width=1200, height=660)
myFrame.place(x=0, y=0)

# Add Button for compilation and execution
btn_exec = Button(myFrame, text="Execute code", fg="black", command=executeCode)
btn_exec.place(x=0, y=0)

btn_print = Button(myFrame, text="Print SVG", fg="black", command=printImage)
btn_print.place(x=120, y=0)

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

# Add Import Menu
importMenu = Menu(myMenu, tearoff=False)
myMenu.add_cascade(label="Import", menu=importMenu)
importMenu.add_command(label="SVG", command=importSvg)

# Add Status Bar to Bottom of App
statusBar = Label(root, text='Ready', anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=5)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        s.close()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
