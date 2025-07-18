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

# ---------- EXPORT ----------
def export_history():
    conn = sqlite3.connect("weather_history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM weather")
    rows = c.fetchall()
    conn.close()

    if not rows:
        messagebox.showwarning("No Data", "No data to export.", parent=root)  # Added parent=root for better focus
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'City', 'Temperature', 'Condition', 'Humidity', 'Wind', 'Date'])
            writer.writerows(rows)
        messagebox.showinfo("Success", f"Data saved to {file_path}", parent=root)  # Added parent=root

# ---------- WEATHER FETCH ----------
def get_weather():
    city = city_var.get().strip()
    unit = unit_var.get()

    if not city:
        messagebox.showwarning("Missing Input", "Please enter a city name.", parent=root)  # Added parent=root
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
        messagebox.showerror("Error", str(e), parent=root)  # Added parent=root

# ---------- CLEAR INPUT ----------
def clear_input():
    city_var.set("")  # Clear the city input field

# ---------- UI SETUP ----------
init_db()
root = tk.Tk()
root.title("🌦️ Stylish Weather App (Fullscreen)")
root.state('zoomed')  # Make window full screen
root.configure(bg="#E6F3FA")  # Changed background to soft blue

# Center Frame
main_frame = tk.Frame(root, bg="#F5FAFF", bd=2, relief="ridge")  # Changed to light blue-ish
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=640)

tk.Label(main_frame, text="🌤️ Weather Forecast", font=("Segoe UI", 20, "bold"), bg="#F5FAFF", fg="#007ACC").pack(pady=20)  # Changed font

# City input
tk.Label(main_frame, text="Enter City Name:", font=("Segoe UI", 13), bg="#F5FAFF", fg="#333333").pack(pady=(10, 0))  # Changed font and text color
city_var = tk.StringVar()
city_entry = tk.Entry(main_frame, textvariable=city_var, font=("Segoe UI", 12), width=35, bd=2, relief="groove")  # Changed font
city_entry.pack(pady=6)

# Unit selection
unit_var = tk.StringVar(value="metric")
unit_frame = tk.Frame(main_frame, bg="#F5FAFF")  # Updated background
tk.Label(unit_frame, text="Units:", font=("Segoe UI", 11), bg="#F5FAFF", fg="#333333").pack(side=tk.LEFT, padx=5)  # Changed font and text color
tk.Radiobutton(unit_frame, text="Celsius", variable=unit_var, value="metric", bg="#F5FAFF", font=("Segoe UI", 10), fg="#333333").pack(side=tk.LEFT)  # Changed font and text color
tk.Radiobutton(unit_frame, text="Fahrenheit", variable=unit_var, value="imperial", bg="#F5FAFF", font=("Segoe UI", 10), fg="#333333").pack(side=tk.LEFT)  # Changed font and text color
unit_frame.pack(pady=6)

# Button Frame for Get Weather and Clear
button_frame = tk.Frame(main_frame, bg="#F5FAFF")  # New frame for buttons
button_frame.pack(pady=10)

# Get Weather Button with Hover
get_weather_btn = tk.Button(button_frame, text="🔍 Get Weather", font=("Segoe UI", 12), command=get_weather, bg="#008080", fg="white",
                           activebackground="#006666", width=15, height=1, bd=0)  # Changed to teal
get_weather_btn.pack(side=tk.LEFT, padx=5)
def on_enter_get(e): get_weather_btn.config(bg="#006666")  # Hover effect
def on_leave_get(e): get_weather_btn.config(bg="#008080")
get_weather_btn.bind("<Enter>", on_enter_get)
get_weather_btn.bind("<Leave>", on_leave_get)

# Clear Button
clear_btn = tk.Button(button_frame, text="🗑️ Clear", font=("Segoe UI", 12), command=clear_input, bg="#FF6F61", fg="white",
                      activebackground="#E55A50", width=15, height=1, bd=0)  # New clear button with coral color
clear_btn.pack(side=tk.LEFT, padx=5)
def on_enter_clear(e): clear_btn.config(bg="#E55A50")  # Hover effect
def on_leave_clear(e): clear_btn.config(bg="#FF6F61")
clear_btn.bind("<Enter>", on_enter_clear)
clear_btn.bind("<Leave>", on_leave_clear)

# Weather Info
icon_lbl = tk.Label(main_frame, bg="#F5FAFF")  # Updated background
icon_lbl.pack()

temp_lbl = tk.Label(main_frame, text="Temperature: ", font=("Segoe UI", 12), bg="#F5FAFF", fg="#333333")  # Changed font and text color
temp_lbl.pack(pady=4)

cond_lbl = tk.Label(main_frame, text="Condition: ", font=("Segoe UI", 12), bg="#F5FAFF", fg="#333333")  # Changed font and text color
cond_lbl.pack(pady=4)

hum_lbl = tk.Label(main_frame, text="Humidity: ", font=("Segoe UI", 12), bg="#F5FAFF", fg="#333333")  # Changed font and text color
hum_lbl.pack(pady=4)

wind_lbl = tk.Label(main_frame, text="Wind: ", font=("Segoe UI", 12), bg="#F5FAFF", fg="#333333")  # Changed font and text color
wind_lbl.pack(pady=4)

# Export Button with Hover
export_btn = tk.Button(main_frame, text="💾 Export Weather History", font=("Segoe UI", 12), bg="#2ECC71", fg="white",
                       activebackground="#27AE60", bd=0, width=28, command=export_history)  # Changed to emerald
export_btn.pack(pady=20)
def on_enter_export(e): export_btn.config(bg="#27AE60")  # Hover effect
def on_leave_export(e): export_btn.config(bg="#2ECC71")
export_btn.bind("<Enter>", on_enter_export)
export_btn.bind("<Leave>", on_leave_export)

root.mainloop()
