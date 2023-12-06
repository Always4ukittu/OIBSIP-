import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        # GUI elements
        self.location_entry = ttk.Entry(self.root, width=30)
        self.get_weather_button = ttk.Button(self.root, text="Get Weather", command=self.get_weather)
        self.weather_label = ttk.Label(self.root, text="", font=("Helvetica", 14))
        self.weather_icon_label = ttk.Label(self.root)

        # Temperature unit radio buttons
        self.temperature_unit_var = tk.StringVar()
        self.celsius_radio = ttk.Radiobutton(self.root, text="Celsius", variable=self.temperature_unit_var, value="metric")
        self.fahrenheit_radio = ttk.Radiobutton(self.root, text="Fahrenheit", variable=self.temperature_unit_var, value="imperial")
        self.temperature_unit_var.set("metric")  # Set default unit to Celsius

        # Grid layout
        self.location_entry.grid(row=0, column=0, padx=10, pady=10)
        self.get_weather_button.grid(row=0, column=1, padx=10, pady=10)
        self.celsius_radio.grid(row=0, column=2, padx=10, pady=10)
        self.fahrenheit_radio.grid(row=0, column=3, padx=10, pady=10)
        self.weather_label.grid(row=1, column=0, columnspan=4, pady=10)
        self.weather_icon_label.grid(row=2, column=0, columnspan=4, pady=10)

    def get_weather(self):
        # API Key and endpoint
        api_key = "b834d100667d85b9dc5c25d3d4f49894"
        endpoint = "https://api.openweathermap.org/data/2.5/weather"

        # User input
        location = self.location_entry.get()

        # API request
        params = {"q": location, "appid": api_key, "units": self.temperature_unit_var.get()}
        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            # Parse JSON data
            weather_data = response.json()
            self.display_weather(weather_data)
        else:
            self.weather_label["text"] = "Error fetching weather data."

    def display_weather(self, data):
        # Extract relevant weather information
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        unit_label = "°C" if self.temperature_unit_var.get() == "metric" else "°F"
        
        # Display weather information
        self.weather_label["text"] = f"Temperature: {temperature}{unit_label}, {description.capitalize()}"
        
        # Display weather icon
        icon_id = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/w/{icon_id}.png"
        icon_image = self.load_image_from_url(icon_url)
        self.weather_icon_label.configure(image=icon_image)
        self.weather_icon_label.image = icon_image

    def load_image_from_url(self, url):
        response = requests.get(url, stream=True)
        img = Image.open(response.raw)
        img = img.resize((50, 50), Image.NEAREST)
        return ImageTk.PhotoImage(img)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
