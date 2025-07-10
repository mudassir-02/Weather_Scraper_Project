import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import sqlite3
import csv
from io import BytesIO
from PIL import Image, ImageTk
from datetime import datetime

API_KEY = "7f1e578054fbda22f36fecec0635a9ef"  # Replace with your API key

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("weather_history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature TEXT,
            condition TEXT,
            humidity TEXT,
            wind TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(city, temp, condition, humidity, wind):
    conn = sqlite3.connect("weather_history.db")
    c = conn.cursor()
    c.execute("INSERT INTO weather (city, temperature, condition, humidity, wind, date) VALUES (?, ?, ?, ?, ?, ?)",
              (city, temp, condition, humidity, wind, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()



















def get_weather():
    city = city_var.get().strip()
    unit = unit_var.get()

    if not city:
        messagebox.showwarning("Missing Input", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"

    try:
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            raise Exception(data.get("message", "Invalid city or error."))

        temp = f"{data['main']['temp']} °{'C' if unit == 'metric' else 'F'}"
        condition = data['weather'][0]['description'].title()
        humidity = f"{data['main']['humidity']} %"
        wind = f"{data['wind']['speed']} m/s"
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        # Update UI
        temp_lbl.config(text=f"Temperature: {temp}")
        cond_lbl.config(text=f"Condition: {condition}")
        hum_lbl.config(text=f"Humidity: {humidity}")
        wind_lbl.config(text=f"Wind: {wind}")

        icon_img = Image.open(BytesIO(requests.get(icon_url).content))
        icon_img = icon_img.resize((100, 100), Image.LANCZOS)
        icon_tk = ImageTk.PhotoImage(icon_img)
        icon_lbl.config(image=icon_tk)
        icon_lbl.image = icon_tk

        save_to_db(city, temp, condition, humidity, wind)

    except Exception as e:
        messagebox.showerror("Error", str(e))






    