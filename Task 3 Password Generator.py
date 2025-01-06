import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
db.commit()
db.close()

class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        root.title('Password Generator')
        root.geometry('660x500')
        root.config(bg='#FFCCCC')  # Light red background
        root.resizable(False, False)

        # Title Label
        self.label = Label(text=":PASSWORD GENERATOR:", anchor=N, fg='darkblue', bg='#FFCCCC', font='arial 20 bold underline')
        self.label.grid(row=0, column=1)

        # Spacing
        for i in range(1, 4):
            Label(text="", bg='#FFCCCC').grid(row=i, column=0, columnspan=2)

        # Username Entry
        self.user = Label(text="Enter User Name: ", font='times 15 bold', bg='#FFCCCC', fg='darkblue')
        self.user.grid(row=4, column=0)
        self.textfield = Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=4, column=1)
        self.textfield.focus_set()

        # Spacing
        Label(text="", bg='#FFCCCC').grid(row=5, column=0)

        # Password Length Entry
        self.length = Label(text="Enter Password Length: ", font='times 15 bold', bg='#FFCCCC', fg='darkblue')
        self.length.grid(row=6, column=0)
        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=6, column=1)

        # Spacing
        Label(text="", bg='#FFCCCC').grid(row=7, column=0)

        # Generated Password Display
        self.generated_password = Label(text="Generated Password: ", font='times 15 bold', bg='#FFCCCC', fg='darkblue')
        self.generated_password.grid(row=8, column=0)
        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#DC143C')
        self.generated_password_textfield.grid(row=8, column=1)

        # Spacing
        for i in range(9, 11):
            Label(text="", bg='#FFCCCC').grid(row=i, column=0)

        # Buttons
        self.generate = Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_pass)
        self.generate.grid(row=11, column=1)

        Label(text="", bg='#FFCCCC').grid(row=12, column=0)

        self.accept = Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields)
        self.accept.grid(row=13, column=1)

        Label(text="", bg='#FFCCCC').grid(row=14, column=1)

        self.reset = Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields)
        self.reset.grid(row=15, column=1)

    def generate_pass(self):
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        chars = "@#%&()\"?!"
        numbers = string.digits
        name = self.textfield.get()
        leng = self.length_textfield.get()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.textfield.delete(0, END)
            return

        try:
            length = int(leng)
        except ValueError:
            messagebox.showerror("Error", "Password length must be a number")
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        self.generated_password_textfield.delete(0, END)

        password = (
            random.sample(upper, random.randint(1, length - 3)) +
            random.sample(lower, random.randint(1, length - 3)) +
            random.sample(chars, random.randint(1, length - 3)) +
            random.sample(numbers, random.randint(1, length - 3))
        )
        random.shuffle(password)
        self.generated_password_textfield.insert(0, ''.join(password[:length]))

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username = ?", (self.n_username.get(),))
            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
            else:
                cursor.execute("INSERT INTO users(Username, GeneratedPassword) VALUES (?, ?)", (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success", "Password generated and saved successfully")

    def reset_fields(self):
        self.textfield.delete(0, END)
        self.length_textfield.delete(0, END)
        self.generated_password_textfield.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()
