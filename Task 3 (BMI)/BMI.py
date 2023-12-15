

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os

class BMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # User Management
        self.current_user = None
        self.user_data = {}

        self.user_label = ttk.Label(root, text="User Name:")
        self.user_label.grid(row=0, column=0, padx=10, pady=10)

        self.user_entry = ttk.Entry(root)
        self.user_entry.grid(row=0, column=1, padx=10, pady=10)

        self.weight_label = ttk.Label(root, text="Weight (kg):")
        self.weight_label.grid(row=1, column=0, padx=10, pady=10)

        self.weight_entry = ttk.Entry(root)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10)

        self.height_label = ttk.Label(root, text="Height (cm):")
        self.height_label.grid(row=2, column=0, padx=10, pady=10)

        self.height_entry = ttk.Entry(root)
        self.height_entry.grid(row=2, column=1, padx=10, pady=10)

        self.calculate_button = ttk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(root, text="Save Data", command=self.save_data)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.plot_button = ttk.Button(root, text="Plot BMI Trends", command=self.plot_data)
        self.plot_button.grid(row=6, column=0, columnspan=2, pady=10)

        # User Selection Dropdown
        self.user_dropdown_label = ttk.Label(root, text="Select User:")
        self.user_dropdown_label.grid(row=7, column=0, padx=10, pady=10)
        self.user_var = tk.StringVar()
        self.user_dropdown = ttk.Combobox(root, textvariable=self.user_var, state="readonly")
        self.user_dropdown.grid(row=7, column=1, padx=10, pady=10)
        self.user_dropdown.bind("<<ComboboxSelected>>", self.load_user_data)

        # Load Users Button
        self.load_users_button = ttk.Button(root, text="Load Users", command=self.load_users)
        self.load_users_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Historical Data Button
        self.historical_data_button = ttk.Button(root, text="View Historical Data", command=self.view_historical_data)
        self.historical_data_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Scrolling setup
        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        

    def calculate_bmi(self):
        try:
            user_name = self.user_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # convert height to meters
            bmi = weight / (height ** 2)
            bmi_category = self.categorize_bmi(bmi)
            result_text = f"BMI: {bmi:.2f}, Category: {bmi_category}"
            self.result_label.config(text=result_text)

            if user_name:
                if user_name not in self.user_data:
                    self.user_data[user_name] = []

                # Add BMI data to the user's entry
                entry = {"date": datetime.now(), "weight": weight, "height": height, "bmi": bmi}
                self.user_data[user_name].append(entry)

               

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for weight and height")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal Weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def save_data(self):
        try:
            user_name = self.user_entry.get()
            if user_name:
                with open(f"assets/{user_name}_bmi_data.txt", "a") as file:
                    for entry in self.user_data[user_name]:
                        file.write(f"{user_name}: {entry['date']} - Weight: {entry['weight']}, Height: {entry['height']}, BMI: {entry['bmi']}\n")
                messagebox.showinfo("Success", "Data saved successfully")
            else:
                messagebox.showinfo("Info", "Please enter a user name before saving data")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def load_user_data(self, event=None):
        self.current_user = self.user_var.get()
        self.bmi_data = [entry["bmi"] for entry in self.user_data[self.current_user]]
        self.plot_data()

    def load_users(self):
        try:
            user_files = [filename for filename in os.listdir("./assets/") if filename.endswith("_bmi_data.txt")]
            users = [filename.split("_")[0] for filename in user_files]
            self.user_dropdown["values"] = users
        except Exception as e:
            messagebox.showerror("Error", f"Error loading users: {str(e)}")

    def view_historical_data(self):
        if not self.current_user:
            messagebox.showinfo("Info", "Please select a user first.")
            return

        historical_data = "\n".join([f"{self.current_user}: {entry['date']} - Weight: {entry['weight']}, Height: {entry['height']}, BMI: {entry['bmi']}" for entry in self.user_data[self.current_user]])
        messagebox.showinfo("Historical Data", historical_data)

    def plot_data(self):
        all_bmi_data = []
        for user, data in self.user_data.items():
            all_bmi_data.extend([entry["bmi"] for entry in data])

        if not all_bmi_data:
            messagebox.showinfo("Info", "No data to plot. Please calculate BMI first.")
            return

        fig, ax = plt.subplots()
        ax.bar(range(1, len(all_bmi_data) + 1), all_bmi_data)
        ax.set_xlabel("Data Point")
        ax.set_ylabel("BMI")
        ax.set_title("BMI Trends Over Time")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=11, column=0, columnspan=2, pady=10)

        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()
