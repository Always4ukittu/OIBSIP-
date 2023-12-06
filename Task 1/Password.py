# import random
# import string

# def generate_password(length, character_set):
#     random_password = ''.join(random.choice(character_set) for _ in range(length))
#     return random_password

# try:
#     length = int(input("Enter the length of the password: "))
#     user_creteria = input("Enter option number(s) separated by a single space for the character types you want in the password:\n1 Letters\n2 Numbers\n3 Symbols\n")
# except ValueError:
#     raise ValueError("Invalid Input.")

# # Default character set if the user doesn't select any option
# default_character_set = string.ascii_letters + string.digits + string.punctuation

# # User input for character set
# character_set = ""
# if '1' in user_creteria:
#     character_set += string.ascii_letters
# if '2' in user_creteria:
#     character_set += string.digits
# if '3' in user_creteria:
#     character_set += string.punctuation

# # Use the default character set if the user didn't select any option
# character_set = character_set if character_set else default_character_set

# print("=====================================================PASSWORD===============================================================\n")

# # Output the password
# password = generate_password(length, character_set)
# print(password)






import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import pyperclip  # For clipboard integration

class AdvancedPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")

        self.create_widgets()

    def create_widgets(self):
        # Label
        length_label = ttk.Label(self.root, text="Password Length:")
        length_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry
        self.length_entry = ttk.Entry(self.root)
        self.length_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Checkboxes for complexity
        complexity_label = ttk.Label(self.root, text="Password Complexity:")
        complexity_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.lowercase_var = tk.IntVar()
        lowercase_checkbox = ttk.Checkbutton(self.root, text="Include Lowercase", variable=self.lowercase_var)
        lowercase_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.uppercase_var = tk.IntVar()
        uppercase_checkbox = ttk.Checkbutton(self.root, text="Include Uppercase", variable=self.uppercase_var)
        uppercase_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.digits_var = tk.IntVar()
        digits_checkbox = ttk.Checkbutton(self.root, text="Include Digits", variable=self.digits_var)
        digits_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        self.symbols_var = tk.IntVar()
        symbols_checkbox = ttk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var)
        symbols_checkbox.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        # Button
        generate_button = ttk.Button(self.root, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Display
        self.password_label = ttk.Label(self.root, text="Generated Password:")
        self.password_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        self.password_display = ttk.Entry(self.root, state='readonly')
        self.password_display.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Clipboard Button
        clipboard_button = ttk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        clipboard_button.grid(row=9, column=0, columnspan=2, pady=10)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid password length.")
            return

        characters = ''
        if self.lowercase_var.get():
            characters += string.ascii_lowercase
        if self.uppercase_var.get():
            characters += string.ascii_uppercase
        if self.digits_var.get():
            characters += string.digits
        if self.symbols_var.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "Please select at least one character set.")
            return

        generated_password = ''.join(random.choice(characters) for _ in range(length))
        self.password_display.configure(state='normal')
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, generated_password)
        self.password_display.configure(state='readonly')

    def copy_to_clipboard(self):
        password = self.password_display.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard.")
        else:
            messagebox.showerror("Error", "No password to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPasswordGenerator(root)
    root.mainloop()
