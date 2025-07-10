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

    # Weather Info
icon_lbl = tk.Label(main_frame, bg="white")
icon_lbl.pack()

temp_lbl = tk.Label(main_frame, text="Temperature: ", font=("Arial", 12), bg="white")
temp_lbl.pack(pady=4)

cond_lbl = tk.Label(main_frame, text="Condition: ", font=("Arial", 12), bg="white")
cond_lbl.pack(pady=4)

hum_lbl = tk.Label(main_frame, text="Humidity: ", font=("Arial", 12), bg="white")
hum_lbl.pack(pady=4)

wind_lbl = tk.Label(main_frame, text="Wind: ", font=("Arial", 12), bg="white")
wind_lbl.pack(pady=4)

# Export Button
tk.Button(main_frame, text="💾 Export Weather History", font=("Arial", 12), bg="green", fg="white",
          activebackground="#228B22", bd=0, width=28, command=export_history).pack(pady=20)

root.mainloop()



















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

# ---------- UI SETUP ----------
init_db()
root = tk.Tk()
root.title("🌦️ Stylish Weather App (Fullscreen)")
root.state('zoomed')  # Make window full screen
root.configure(bg="#f0f2f5")

# Center Frame
main_frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=640)

tk.Label(main_frame, text="🌤️ Weather Forecast", font=("Helvetica", 20, "bold"), bg="white", fg="#007ACC").pack(pady=20)

# City input
tk.Label(main_frame, text="Enter City Name:", font=("Arial", 13), bg="white").pack(pady=(10, 0))
city_var = tk.StringVar()
tk.Entry(main_frame, textvariable=city_var, font=("Arial", 12), width=35, bd=2, relief="groove").pack(pady=6)

# Unit selection
unit_var = tk.StringVar(value="metric")
unit_frame = tk.Frame(main_frame, bg="white")
tk.Label(unit_frame, text="Units:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(unit_frame, text="Celsius", variable=unit_var, value="metric", bg="white", font=("Arial", 10)).pack(side=tk.LEFT)
tk.Radiobutton(unit_frame, text="Fahrenheit", variable=unit_var, value="imperial", bg="white", font=("Arial", 10)).pack(side=tk.LEFT)
unit_frame.pack(pady=6)

# Get Weather Button
tk.Button(main_frame, text="🔍 Get Weather", font=("Arial", 12), command=get_weather, bg="#007ACC", fg="white",
          activebackground="#005F99", width=25, height=1, bd=0).pack(pady=10)




    