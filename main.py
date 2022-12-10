from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename     
from tkinter import ttk
from tkinter import messagebox
from lexical import *
from analyzer import *

userInput = []
terminalStrings = []
command = ""

# function to open a file 
def openFile():  # open lol file 
    fp = askopenfilename(
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")]
    )
    if not fp:
        return
    editor.delete(1.0, END)
    with open(fp, "r") as input_file:
        text = input_file.read()
        editor.insert(END, text)                  
    window.title(f"Text Editor Application - {fp}")

# function to save a file
def saveFile():  # save lol file
    fp = asksaveasfilename(
        defaultextension="lol",
        filetypes=[("LOL CODE Files", "*.lol"), ("All Files", "*.*")],
    )
    if not fp:
        return
    with open(fp, "w") as output_file:
        text = editor.get(1.0, END)
        output_file.write(text)
    window.title(f"Text Editor Application - {fp}")

# function to 
def insert_prompt():
    c = terminal_box.get("end-2c")
    if c != "\n":
        terminal_box.insert(END, "\n")
    terminal_box.insert(END, ">>> ", ("prompt",))
    
    # print(terminal_box.index(INSERT))
    terminal_box.mark_set("end-of-prompt", "end-1c")
    terminal_box.mark_gravity("end-of-prompt", "left")
    return c

# function to 
def process_input(event):
    terminal_box.insert(END, "\n")
    command = terminal_box.get("end-of-prompt", "end-1c")
    # print("command: " + str(command))
    # terminal_box.insert(END, "output: ")
    terminal_box.see(END)
    # insert_prompt()



# called to execute the program in the text box
def program():
    global editor

    lexeme_part.delete(*lexeme_part.get_children())  
    symbol_part.delete(*symbol_part.get_children())
    terminal_box.delete("1.0", END)

    # write lexemes
    lexicalTable = tokenize(editor.get("1.0", 'end-1c'))


    if isinstance(lexicalTable, str):  # catch if error
        messagebox.showinfo("Error", lexicalTable)
    else:               # clear table per execution
        for lexeme in lexicalTable:  # insert values of lexemes
            lexeme_part.insert(parent = '', index = 'end', values = (lexeme[0], lexeme[1]))

    # if isinstance(lexicalTable, str):  # catch if error
    #     messagebox.showinfo("Error", lexicalTable)
    # else:               # clear table per execution
    for lexeme in lexicalTable:  # insert values of lexemes
        # lexeme_part.insert(parent = '', index = 'end', values = (lexeme[0], lexeme[1]))
        if lexeme[1] == "Input Keyword": 
            # terminal_box.bind('<Return>', process_input)
            # command = insert_prompt()
            # print(command)
            # userInput.append(command);
            label = Label(window, text = "Waiting for input.")
            label.place(x = 323, y = 288)
            inputButton.wait_variable(inputFlag)
            userInput.append(inputField.get("1.0", 'end-1c'))
            label.place_forget()

    print(userInput)


    # write syntax
    syntaxAnalyzer = parse(lexicalTable, userInput.copy())

    if isinstance(syntaxAnalyzer[0], str):  # catch if error
        messagebox.showinfo("Error", syntaxAnalyzer[0])
    else:               # clear table per execution
        for syntax in syntaxAnalyzer[0]:  # insert values of lexemes
            symbol_part.insert(parent = '', index = 'end', values = (syntax[0], syntax[1]))

    for printing in syntaxAnalyzer[1]:
        terminal_box.insert(END, printing)
        terminal_box.insert(END, "\n")

    userInput.clear()

window = Tk()
window.title("LOLCode Interpreter")
window.configure(background="gray")
window.geometry("1165x685")

inputFlag = IntVar()        # flag to determine if 

# LABEL PER COLUMN (lexeme and symbols)
lexeme_label = Label(window, text="Lexeme", background="gray")
symbol_label = Label(window, text="Symbols", background="gray")
is_enter_pressed = IntVar()

# BOX FOR VIEWING AND EDITING FILE CONTENTS 
editor = Text(window, height = 18, width = 53)
editor.config(height = 17, width = 51)
editor.place(x = 10, y = 33)

# FRAME FOR OPEN AND SAVE FILE BUTTONS 
file_btns = Frame(window, relief = RAISED, bd = 2)
file_btns.grid(row = 0, column = 0, sticky = "ns")

# OPEN FILE BUTTON
btn_open = Button(file_btns, text = "Open", command = openFile, height = 1)
btn_open.grid(row=0, column=0, sticky = "ew")

# SAVE FILE BUTTON
btn_save = Button(file_btns, text = "Save As...", command = saveFile)
btn_save.grid(row = 0, column = 1, sticky = "ew")

# LEXICAL TABLE 
lexeme_label.place(x=580, y=3)  
lexeme_part = ttk.Treeview(window, height=13)
lexeme_part['column'] = ("Lexeme", "Classification")
lexeme_part.column("#0", width=0, stretch=NO)
lexeme_part.column("Lexeme", anchor=W, width=180)
lexeme_part.column("Classification", anchor=W, width=180)
lexeme_part.heading("#0", text="", anchor=W)
lexeme_part.heading("Lexeme", text="Lexeme", anchor=W)
lexeme_part.heading("Classification", text="Classification", anchor=W)
lexeme_part.place(x = 426, y = 28)

# SYMBOL TABLE 
symbol_label.place(x=930, y=3) 
symbol_part = ttk.Treeview(window, height = 13)
symbol_part['column'] = ("Identifier", "Value")
symbol_part.column("#0", width=0, stretch=NO)
symbol_part.column("Identifier", anchor=W, width=180)
symbol_part.column("Value", anchor=W, width=180)
symbol_part.heading("#0", text="", anchor=W)
symbol_part.heading("Identifier", text="Identifier", anchor=W)
symbol_part.heading("Value", text="Value", anchor=W)
symbol_part.place(x = 792, y = 28)

# input field and enter button
inputField = Text(window, height = 1.4, width = 130)
inputButton = Button(window, text="Input", height = 1, width = 12, command=lambda: inputFlag.set(1))
inputField.place(x = 9, y = 322)
inputButton.place(x = 1060, y = 320)

# INTERPRET THE PROGRAM 
executeButton = Button(window, text = "Execute", command = program, width = 162)
executeButton.place(x = 10, y = 355)

# TO SIMULATE TERMINAL (get user input / print output)
    # ref: https://stackoverflow.com/questions/17839468/tkinter-input-and-output-in-one-widget
terminal_box = Text(window, wrap = "word", height = 17, width = 142)
terminal_box.place(x = 11, y = 393)
# terminal_box.bind('<Return>', process_input)
# insert_prompt()

window.mainloop()