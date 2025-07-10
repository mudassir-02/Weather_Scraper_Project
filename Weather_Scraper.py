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