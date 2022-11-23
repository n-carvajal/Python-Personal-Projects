"""Password Vault App"""

# Imports
import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.filedialog import asksaveasfile
from data import letters, symbols, numbers

# Constants
DEFAULT_KEY_VISIBILITY = False
BACKGROUND_COLOUR = "White"
SCRAMBLER = 5


# Functions
def encode_string(*args):
    """
    Encodes given string or strings.

    Takes strings as arguments. Creates empty list 'coded_strings'. Adds
    '*args' to list 'plain_words'. For each string in 'plain_words' it
    separates the string into individual characters, it then encodes
    each character and joins the resulting encoded characters back into
    a string separating each encoded character by a space. Once the
    string is reconstituted it appends it to 'coded_strings'.

    Returns: 'coded_strings'
    """

    def encode_char(char):
        """
        Encodes given character.

        Replaces a character with its corresponding numerical unicode
        value. Adds SCRAMBLER to it and converts result into a string.

        Returns: 'coded_str'
        """
        num = ord(char)
        coded_num = num + SCRAMBLER
        coded_str = str(coded_num)
        return coded_str

    coded_strings = []
    plain_words = [*args]
    for word in plain_words:
        coded_word = list(map(encode_char, word))
        coded_string = " ".join(coded_word)
        coded_strings.append(coded_string)
    return coded_strings


def decode_string(*args):
    """
    Decodes given string or strings.

    Takes strings as arguments. Creates empty list 'plain_words'. Adds
    '*args'to list 'coded_strings'. For each string in 'coded_strings'
    it separates the string on whitespace and generates a list of
    values, it then decodes each value in the list and joins it back
    into a string with no spacing. Once done appends the string to
    'plain_words'.

    Returns: 'plain_words'
    """

    def decode_num(num):
        """
        Decodes given character.

        Takes a string, converts it into a number, subtracts SCRAMBLER,
        then maps the resulting value to a character based on its
        unicode value.

        Returns: 'decoded_char'
        """
        coded_num = int(num)
        decoded_num = int(coded_num - SCRAMBLER)
        decoded_char = chr(decoded_num)
        return decoded_char

    plain_words = []
    coded_strings = [*args]
    for string in coded_strings:
        coded_nums = string.split()
        decoded_nums = list(map(decode_num, coded_nums))
        plain_word = "".join(decoded_nums)
        plain_words.append(plain_word)
    return plain_words


def show_key():
    """
    Toggles visibility of Master Key in GUI.

    Checks value of global variable 'DEFAULT_key_VISIBILITY'. Sets value
    to its opposite. If subsequent result is True then the Master Key is
    shown. Else Master Key is displayed in the form '****'.
    """
    global DEFAULT_KEY_VISIBILITY
    DEFAULT_KEY_VISIBILITY = not DEFAULT_KEY_VISIBILITY
    if DEFAULT_KEY_VISIBILITY:
        key_ent.config(show="")
    else:
        key_ent.config(show="*")


def submit_key():
    """
    Validates Master Key and provides access to GUI or appropriate
    feedback.

    Obtains 'plain_key' from 'key_ent'. If 'plain_key' is an empty
    string it displays a message informing a key is required. Else it
    encodes 'plain_key' to 'coded_key' using 'encode_string()' and
    converts it into dictionary 'key_data'. It then tries to open
    'key_file.json' and read its contents into 'key_file_data'. If a
    'FileNotFoundError' is generated, displays a message informing key
    successfully setup and creates 'key_file.json' and writes 'key_data'
    to it. It then reads its contents into 'key_file_data'. If coded_key
    is equal to 'key_file_data["key"]' the GUI is changed to enable mode
    selection. Else it warns incorrect key entered.
    """
    plain_key = key_ent.get()
    if not plain_key:
        messagebox.showinfo(
            "key Required", "You must enter your key to continue."
        )
    else:
        coded_key = encode_string(plain_key)[0]
        key_data = {"key": coded_key}
        try:
            with open("02 - Password Vault/key_file.json", "r") as key_file:
                key_file_data = json.load(key_file)
        except FileNotFoundError:
            messagebox.showinfo(
                "Setup Successful",
                "Your Master Key has been setup correctly.\n\nDo not forget "
                "it!",
            )
            with open("02 - Password Vault/key_file.json", "w") as key_file:
                json.dump(key_data, key_file, indent=4)
            with open("02 - Password Vault/key_file.json", "r") as key_file:
                key_file_data = json.load(key_file)
        if coded_key == key_file_data["key"]:
            for widgets in key_frm.winfo_children():
                widgets.destroy()
            key_frm.config(height=1)
            select_frm.pack(padx=10, pady=10)
            save_btn.grid(row=0, column=0, padx=5, pady=5)
            retrieve_btn.grid(row=0, column=1, padx=5, pady=5)
            export_vault_btn.grid(row=0, column=2, padx=5, pady=5)
        else:
            messagebox.showerror(
                "Incorrect key",
                "The Master Key you entered does not match the one stored in "
                "your vault.\n\nTry again.",
            )


def save_gui():
    """
    Configures the SAVE GUI as well as controls its operation.
    """

    def generate_password():
        """
        Generates a random password.

        Generates a random password consisting of 6 letters, 2 numbers,
        and 2 symbols in random order and places it in 'password_ent'.
        It first deletes the contents of 'password_ent' and creates
        empty 'password_list'. It then picks a random 'letter' from
        'letters' in 'data.py', checks if the 'letter' exists in
        'password_list'. If True it picks another random 'letter'. If
        False, it appends 'letter' to 'password_list'. Repeats until 6
        unique random letters have been appended to 'password_list'.
        Performs the same procedure with 'symbol' and 'symbols' as well
        as 'number' and 'numbers' except it stops once 2 unique values
        of each have been added to 'password_list'. It then shuffles the
        contents of 'password_list' and joins them into a string called
        'password'. Inserts 'password' into 'password_ent', clears the
        user's clipboard and then appends 'password' to it.
        """
        password_ent.delete(0, tk.END)
        password_list = []
        for _ in range(6):
            letter = random.choice(letters)
            while letter in password_list:
                letter = random.choice(letters)
            password_list.append(letter)
        for _ in range(2):
            symbol = random.choice(symbols)
            number = random.choice(numbers)
            while symbol in password_list:
                symbol = random.choice(symbols)
            while number in password_list:
                number = random.choice(numbers)
            password_list.append(symbol)
            password_list.append(number)
        random.shuffle(password_list)
        password = "".join(password_list)
        password_ent.insert(0, password)
        root.clipboard_clear()
        root.clipboard_append(password)

    def submit_info():
        """
        Validates input and submits it for encoding and saving.

        Gets login details from entry boxes and saves as
        'plain_website', 'plain_username', and 'plain_password'. Adds
        'plain_*' as arguments to 'encode_string()'. Saves result as
        'coded_website', 'coded_username' and 'coded_password'. Creates
        dictionary 'login_data' using 'coded_*'. If any 'coded_*' is
        equal to a blank string. Informs all fields must be completed.
        Else tries to open 'logins.json' and read its contents into
        'logins_file_data'. Except a 'FileNotFoundError' it writes
        'login_data' to 'logins.json'. Else if 'coded_website' in
        'logins_file_data' and 'coded_username' in
        'logins_file_data["username"]' informs a duplicate has been
        found and asks to overwrite. If true, indexes 'coded_username'
        in 'logins_file_data[coded_website]["username"] and replaces the
        values at 'logins_file_data[coded_website]["username"][index]'
        and 'logins_file_data[coded_website]["password"][index]' with
        'coded_username' and 'coded_password' respectively. Else if
        'coded_website' in 'logins_file_data' appends 'coded_username'
        and 'coded_password' to
        'logins_file_data[coded_website]["username"]'
        and 'logins_file_data[coded_website]["username"]' respectively.
        Else updates 'logins.json' with 'login_data'. Finally, it
        deletes the input in all the entry boxes.
        """
        plain_website = website_ent.get().lower()
        plain_username = username_ent.get().lower()
        plain_password = password_ent.get()
        coded_website, coded_username, coded_password = encode_string(
            plain_website, plain_username, plain_password
        )
        login_data = {
            coded_website: {
                "username": [coded_username],
                "password": [coded_password],
            }
        }
        if coded_website == "" or coded_username == "" or coded_password == "":
            messagebox.showinfo(
                "No Blanks Allowed", "All fields are required to proceed."
            )
        else:
            try:
                with open(
                    "02 - Password Vault/logins.json", "r"
                ) as login_file:
                    login_file_data = json.load(login_file)
            except FileNotFoundError:
                with open(
                    "02 - Password Vault/logins.json", "w"
                ) as login_file:
                    json.dump(login_data, login_file, indent=4)
            else:
                if (
                    coded_website in login_file_data
                    and coded_username
                    in login_file_data[coded_website]["username"]
                ):
                    overwrite = messagebox.askyesno(
                        "Duplicate Entry",
                        "An entry for that Website and username already "
                        "exists.\nOverwrite?",
                    )
                    if overwrite:
                        index = login_file_data[coded_website][
                            "username"
                        ].index(coded_username)
                        login_file_data[coded_website]["username"][
                            index
                        ] = coded_username
                        login_file_data[coded_website]["password"][
                            index
                        ] = coded_password
                        with open(
                            "02 - Password Vault/logins.json", "w"
                        ) as login_file:
                            json.dump(login_file_data, login_file, indent=4)
                elif coded_website in login_file_data:
                    login_file_data[coded_website]["username"].append(
                        coded_username
                    )
                    login_file_data[coded_website]["password"].append(
                        coded_password
                    )
                    with open(
                        "02 - Password Vault/logins.json", "w"
                    ) as login_file:
                        json.dump(login_file_data, login_file, indent=4)
                else:
                    with open(
                        "02 - Password Vault/logins.json", "w"
                    ) as login_file:
                        login_file_data.update(login_data)
                        json.dump(login_file_data, login_file, indent=4)
        website_ent.delete(0, tk.END)
        username_ent.delete(0, tk.END)
        password_ent.delete(0, tk.END)

    # Sets Up Frame and Widgets of SAVE GUI
    save_btn.config(state=tk.DISABLED)
    retrieve_btn.config(state=tk.NORMAL)
    export_vault_btn.config(state=tk.NORMAL)
    for widgets in entry_frm.winfo_children():
        widgets.destroy()
    entry_frm.configure(height=1)
    save_frm = tk.Frame(entry_frm, bg=BACKGROUND_COLOUR)
    website_lbl = tk.Label(save_frm, text="Website", bg=BACKGROUND_COLOUR)
    website_ent = tk.Entry(save_frm, width=35)
    username_lbl = tk.Label(save_frm, text="Username", bg=BACKGROUND_COLOUR)
    username_ent = tk.Entry(save_frm, width=35)
    password_lbl = tk.Label(save_frm, text="Password", bg=BACKGROUND_COLOUR)
    password_ent = tk.Entry(save_frm, width=35)
    auto_password_btn = tk.Button(
        save_frm, text="Generate", command=generate_password
    )
    submit_details_btn = tk.Button(
        save_frm, text="Submit", command=submit_info
    )
    save_frm.pack(padx=5)
    website_lbl.grid(row=0, column=0, pady=5)
    website_ent.grid(row=0, column=1, pady=5)
    username_lbl.grid(row=1, column=0, pady=5)
    username_ent.grid(row=1, column=1, pady=5)
    password_lbl.grid(row=2, column=0, pady=5)
    password_ent.grid(row=2, column=1, pady=5)
    auto_password_btn.grid(row=2, column=2, padx=5, pady=5)
    submit_details_btn.grid(row=3, column=1, padx=5, pady=5)


def retrieve_gui():
    """
    Configures the RETRIEVE GUI as well as controls its operation.
    """

    def retrieve_info():
        """
        Validates input, encodes it, compares with saved encoded and if
        a match found returns decoded complete entry. If no match found
        prompts to save.

        Gets details from entry boxes and saves as 'plain_website' and
        'plain_username'. If 'plain_website' or 'plain_username' is a
        blank string, inform no blanks allowed. Else adds 'plain_*' as
        arguments to 'encode_string()' and saves result as
        'coded_website', 'coded_username'. Then it tries to open
        'logins.json' and read its contents into 'login_file_data'.
        Except 'FileNotFoundError' inform the vault is empty and details
        must be saved before an item can be retrieved. Else if
        'coded_website' in 'login_file_data' and 'coded_username' in
        'login_file_data[coded_website]["username"]', index
        'coded_username' in 'login_file_data[coded_website]["username"]'
        and then retrieve 'coded_password' using
        'login_file_data[coded_website]["password"][index]'. Input
        'coded_password' into 'decode_string()' and save result as
        'plain_password'. Display 'plain_website', 'plain_username' and
        'plain_password' info in messagebox and append plain password to
        user clipboard. Else inform the details entered have no matching
        information and ask if they want to add them to the vault. If
        yes, open save GUI.
        """
        plain_website = website_ent.get().lower()
        plain_username = username_ent.get().lower()
        if plain_website == "" or plain_username == "":
            messagebox.showinfo(
                "No Blanks Allowed", "All fields are required to proceed."
            )
        else:
            coded_website, coded_username = encode_string(
                plain_website, plain_username
            )
            try:
                with open("02 - Password Vault/logins.json") as login_file:
                    login_file_data = json.load(login_file)
            except FileNotFoundError:
                messagebox.showinfo(
                    "Empty Vault",
                    "Your vault is empty.\nSave some details before searching "
                    "the vault.",
                )
            else:
                if (
                    coded_website in login_file_data
                    and coded_username
                    in login_file_data[coded_website]["username"]
                ):
                    index = login_file_data[coded_website]["username"].index(
                        coded_username
                    )
                    coded_password = login_file_data[coded_website][
                        "password"
                    ][index]
                    plain_password = decode_string(coded_password)[0]
                    messagebox.showinfo(
                        f"{plain_website.title()}",
                        f"Your {plain_website.title()} login is:\n\n"
                        f"Username: {plain_username}\nPassword: "
                        f"{plain_password}\n\nFor convenience your password"
                        f" has been saved to your clipboard.",
                    )
                    root.clipboard_clear()
                    root.clipboard_append(plain_password)
                else:
                    save = messagebox.askyesno(
                        "No Match",
                        "That website and username combination does not exist "
                        "in the vault.\nDo you wish to add details for this "
                        "site?",
                    )
                    if save:
                        save_gui()

    # Sets Up Frame and Widgets of RETRIEVE GUI.
    save_btn.config(state=tk.NORMAL)
    retrieve_btn.config(state=tk.DISABLED)
    for widgets in entry_frm.winfo_children():
        widgets.destroy()
    entry_frm.configure(height=1)
    retrieve_frm = tk.Frame(entry_frm, bg=BACKGROUND_COLOUR)
    website_lbl = tk.Label(retrieve_frm, text="Website", bg=BACKGROUND_COLOUR)
    website_ent = tk.Entry(retrieve_frm, width=35)
    username_lbl = tk.Label(
        retrieve_frm, text="Username", bg=BACKGROUND_COLOUR
    )
    username_ent = tk.Entry(retrieve_frm, width=35)
    lookup_details_btn = tk.Button(
        retrieve_frm, text="Retrieve", command=retrieve_info
    )
    retrieve_frm.pack(padx=5)
    website_lbl.grid(row=0, column=0)
    website_ent.grid(row=0, column=1)
    username_lbl.grid(row=1, column=0)
    username_ent.grid(row=1, column=1)
    lookup_details_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


def export_vault():
    """
    Decodes and exports contents of vault to file.

    Shows warning about export being in plain text. Enters a while loop.
    Shows dialogue asking for Master Key in order to continue and saves
    it as 'plain_key'. If 'plain_key' is 'None' (user cancelled
    dialogue) breaks the loop. Else if 'plain_key' is an empty string,
    informs the user a key must be entered to proceed and prompts again
    for 'plain_key'. Else uses 'encode_string()' to create 'coded_key'.
    Opens 'key_file.json' and reads contents to 'key_file_data'. If
    coded_key' is equal to 'key_file_data["key"]' it decodes the
    'logins.txt' file and exports it to a file of the user's choosing.
    Else informs the 'plain_key' provided is not the one stored in
    'key_file.json' and prompts again.
    """

    messagebox.showwarning(
        "Warning",
        "You are about to export the contents of your vault.\nAll details will"
        " be exported in plain text.\n\nProceed at your own risk.",
    )
    while True:
        plain_key = simpledialog.askstring(
            "key Validation",
            "For security, enter your Master Key to continue.",
            parent=root,
            show="*",
        )
        if plain_key is None:
            break
        elif not plain_key:
            messagebox.showinfo(
                "key Required", "You must enter your key to continue."
            )
        else:
            coded_key = encode_string(plain_key)[0]
            with open("02 - Password Vault/key_file.json", "r") as key_file:
                key_file_data = json.load(key_file)
            if coded_key == key_file_data["key"]:
                messagebox.showinfo(
                    "Save Location",
                    "Please choose a safe location for your files.",
                )
                with open("02 - Password Vault/logins.json") as login_file:
                    login_file_data = json.load(login_file)
                plain_logins = {}
                for coded_website in login_file_data:
                    plain_usernames = []
                    plain_passwords = []
                    plain_key = decode_string(coded_website)[0]
                    for coded_username in login_file_data[coded_website][
                        "username"
                    ]:
                        plain_username = decode_string(coded_username)[0]
                        plain_usernames.append(plain_username)
                        plain_logins[plain_key] = {"username": plain_usernames}
                    for coded_password in login_file_data[coded_website][
                        "password"
                    ]:
                        plain_password = decode_string(coded_password)[0]
                        plain_passwords.append(plain_password)
                        plain_logins[plain_key].update(
                            {"password": plain_passwords}
                        )
                export_data = ""
                for website in plain_logins:
                    for index, _ in enumerate(
                        plain_logins[website]["username"]
                    ):
                        export_data += (
                            f"{website} | "
                            f'{plain_logins[website]["username"][index]} | '
                            f'{plain_logins[website]["password"][index]} |\n'
                        )
                file = asksaveasfile(
                    defaultextension=".txt",
                    filetypes=[
                        ("All Files", "*.*"),
                        ("Text Documents", "*.txt"),
                    ],
                )
                if file:
                    file.write(export_data)
                    file.close()
                    messagebox.showinfo(
                        "Success", "Your vault export completed successfully."
                    )
                    break
                else:
                    break
            else:
                messagebox.showerror(
                    "Incorrect key",
                    "The Master Key you entered does not match the one stored "
                    "in your vault.\n\nTry again.",
                )
    # Disables Export Button when pressed.
    export_vault_btn.config(state=tk.DISABLED)


# Sets Up Frame and Widgets of WELCOME GUI.
root = tk.Tk()
root.title("Password Vault")
root.config(bg=BACKGROUND_COLOUR)
# Canvas Frame and Widgets.
canvas_frm = tk.Frame(root, bg=BACKGROUND_COLOUR)
canvas = tk.Canvas(root, width=500, highlightthickness=0)
canvas_img = tk.PhotoImage(file="02 - Password Vault/logo.png")
canvas.create_image(0, 0, image=canvas_img, anchor="nw")
canvas_frm.pack()
canvas.pack()
# Show Setup Master Key messagebox on first use.
try:
    with open("02 - Password Vault/key_file.json", "r") as first_use_file:
        first_use_check = json.load(first_use_file)
except FileNotFoundError:
    root.withdraw()
    messagebox.showinfo(
        "Setup Master Key",
        "Welcome to Password Vault.\n\nAs it is your first time using the "
        "program, please setup your Master Key.\n\nYour key can be up to 35 "
        "characters long and can include any number of letters (upper and "
        "lower case), numbers, symbols, and spaces.\n\nIt is important you do "
        "not forget your Master Key once setup as it is not recoverable.",
    )
    root.deiconify()
# key Frame and Widgets.
key_frm = tk.Frame(root, bg=BACKGROUND_COLOUR)
key_lbl = tk.Label(key_frm, text="Enter Master Key", bg=BACKGROUND_COLOUR)
key_ent = tk.Entry(key_frm, show="*", width=35)
key_visibility_btn = tk.Button(key_frm, text="Show/Hide", command=show_key)
key_submit_btn = tk.Button(key_frm, text="Submit key", command=submit_key)
key_frm.pack(padx=5)
key_lbl.grid(row=0, column=0)
key_ent.grid(row=1, column=0)
key_visibility_btn.grid(row=1, column=1, padx=5, pady=5)
key_submit_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
key_ent.focus()
# Select Frame and Widgets.
select_frm = tk.Frame(root, bg=BACKGROUND_COLOUR)
select_frm.pack()
save_btn = tk.Button(
    select_frm, text="Save Details", width=15, command=save_gui
)
retrieve_btn = tk.Button(
    select_frm, text="Retrieve Details", width=15, command=retrieve_gui
)
export_vault_btn = tk.Button(
    select_frm, text="Export Vault", width=15, command=export_vault
)
try:
    with open("02 - Password Vault/logins.json") as vault_check:
        vault_data = json.load(vault_check)
except FileNotFoundError:
    export_vault_btn.config(state=tk.DISABLED)
# Entry Frame.
entry_frm = tk.Frame(root, bg=BACKGROUND_COLOUR)
entry_frm.pack()
# Root mainloop.
root.mainloop()
