from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename     
from tkinter import ttk
from tkinter import messagebox
from lex import *

inputList = list()

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

# called to executed the program in the text box
def program():
    global editor
    lexemes = tokenize(editor.get("1.0", 'end-1c'))

    if isinstance(lexemes, str):  # catch if error
        messagebox.showinfo("Error", lexemes)
    else:
        lexeme_col.delete(*lexeme_col.get_children())                 # clear table per execution
        for lex in lexemes:  # insert values of lexemes
            lexeme_col.insert(parent = '', index = 'end', values = (lex[0], lex[1]))

window = Tk()
window.title("LOLCode Interpreter")
window.configure(background="gray")
window.geometry("1165x700")

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
lexeme_col = ttk.Treeview(window, height=13)
lexeme_col['column'] = ("Lexeme", "Classification")
lexeme_col.column("#0", width=0, stretch=NO)
lexeme_col.column("Lexeme", anchor=W, width=180)
lexeme_col.column("Classification", anchor=W, width=180)
lexeme_col.heading("#0", text="", anchor=W)
lexeme_col.heading("Lexeme", text="Lexeme", anchor=W)
lexeme_col.heading("Classification", text="Classification", anchor=W)
lexeme_col.place(x = 426, y = 28)

symbol_label.place(x=930, y=3) 
symbol_col = ttk.Treeview(window, height = 13)
symbol_col['column'] = ("Identifier", "Value")
symbol_col.column("#0", width=0, stretch=NO)
symbol_col.column("Identifier", anchor=W, width=180)
symbol_col.column("Value", anchor=W, width=180)
symbol_col.heading("#0", text="", anchor=W)
symbol_col.heading("Identifier", text="Identifier", anchor=W)
symbol_col.heading("Value", text="Value", anchor=W)
symbol_col.place(x = 792, y = 28)

output_box = Listbox(window, height = 18, width=190)
output_box.place(x = 9, y = 355)

window.mainloop()