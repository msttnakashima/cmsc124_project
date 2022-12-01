from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename     
from tkinter import ttk
from tkinter import messagebox
from lex import *
from syntax import *

userInput = []

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

# called to execute the program in the text box
def program():
    global editor
    
    userInput = []

    lexeme_part.delete(*lexeme_part.get_children())  
    symbol_part.delete(*symbol_part.get_children())

    # write lexemes
    lexicalTable = tokenize(editor.get("1.0", 'end-1c'))

    if isinstance(lexicalTable, str):  # catch if error
        messagebox.showinfo("Error", lexicalTable)
    else:               # clear table per execution
        for lexeme in lexicalTable:  # insert values of lexemes
            lexeme_part.insert(parent = '', index = 'end', values = (lexeme[0], lexeme[1]))

    # write syntax
    syntaxAnalyzer = parse(lexicalTable, userInput.copy())
    if isinstance(syntaxAnalyzer, str):  # catch if error
        messagebox.showinfo("Error", syntaxAnalyzer)
    else:               # clear table per execution
        for syntax in syntaxAnalyzer:  # insert values of lexemes
            symbol_part.insert(parent = '', index = 'end', values = (syntax[0], syntax[1]))

window = Tk()
window.title("LOLCode Interpreter")
window.configure(background="gray")
window.geometry("1165x700")

inputFlag = IntVar()

lexeme_label = Label(window, text="Lexeme", background="gray")
symbol_label = Label(window, text="Symbols", background="gray")
is_enter_pressed = IntVar()

editor = Text(window, height = 18, width = 53)
editor.config(height = 17, width = 51)
editor.place(x = 10, y = 33)

file_btns = Frame(window, relief = RAISED, bd = 2)
file_btns.grid(row = 0, column = 0, sticky = "ns")

btn_open = Button(file_btns, text = "Open", command = openFile, height = 1)
btn_open.grid(row=0, column=0, sticky = "ew")

btn_save = Button(file_btns, text = "Save As...", command = saveFile)
btn_save.grid(row = 0, column = 1, sticky = "ew")

executeButton = Button(window, text = "Execute", command = program, width = 162)
executeButton.place(x = 10, y = 320)

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

# # input field and enter button
# inputField = Text(window, height=1.3, width=15)
# inputButton = Button(window, text="Enter",
#                      command=lambda: inputFlag.set(1))
# inputField.place(x=590, y=313)
# inputButton.place(x=710, y=313)

output_box = Listbox(window, height = 18, width=190)
output_box.place(x = 9, y = 355)

window.mainloop()