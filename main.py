from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)


def generate_password():
    password_list = []

    [password_list.append(random.choice(letters)) for char in range(nr_letters)]

    [password_list.append(random.choice(symbols)) for char in range(nr_symbols)]

    [password_list.append(random.choice(numbers)) for char in range(nr_numbers)]

    random.shuffle(password_list)

    pwd = "".join(password_list)
    password.delete(0, END)
    password.insert(0, pwd)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():

    url = website.get().capitalize()
    user = username.get()
    pwd = password.get()

    new_data = {
        url: {
            "email": user,
            "password": pwd
        }
    }

    if url == "" or user == "" or pwd == "":
        messagebox.showinfo(title="Error",  message="Please don't leave any fields empty.")
        return

    is_ok = messagebox.askokcancel(title="Confirmation", message=f"Would you like to save the following password?\n\n"
                                                                 f"Website: {website.get()}\nEmail: {username.get()}"
                                                                 f"\nPassword: {password.get()}")
    if is_ok:

        try:
            with open("saved_passwords.json", "r") as f:
                data = json.load(f)
                data.update(new_data)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("saved_passwords.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            with open("saved_passwords.json", "w") as f:
                json.dump(data, f, indent=4)
        finally:
            pyperclip.copy(pwd)
            website.delete(0, END)
            password.delete(0, END)
            website.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    url = website.get().capitalize()
    try:
        with open("saved_passwords.json", "r") as f:
            data = json.load(f)
            if url in data:
                messagebox.showinfo(title="Password information\n",
                                    message=f"Website: {url}\nEmail: {data[url]['email']}\nPassword: {data[url]['password']}")
                pyperclip.copy(data[url]['password'])
            else:
                messagebox.showinfo(title="Error\n", message=f"There are no passwords saved for this website.")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="Error\n", message=f"No data found.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

text_1 = Label(text="Website:")
text_1.grid(row=1, column=0)

website = Entry(width=10)
website.grid(row=1, column=1, pady=1, sticky="ew")
website.focus()

button0 = Button(text="Search", command=find_password)
button0.grid(row=1, column=2, sticky="ew")

text_2 = Label(text="Email/Username:")
text_2.grid(row=2, column=0)

username = Entry(width=10)
username.grid(row=2, column=1, columnspan=2, pady=1, sticky="ew")
username.insert(0, "your_email@email.com")

text_3 = Label(text="Password:")
text_3.grid(row=3, column=0)

password = Entry(width=10)
password.grid(row=3, column=1, pady=1, padx=1, sticky="ew")

button = Button(text="Generate Password", command=generate_password)
button.grid(row=3, column=2, sticky="ew")

button = Button(text="Add", command=save_password)
button.grid(row=4, column=1, columnspan=2, sticky="ew")

window.mainloop()
