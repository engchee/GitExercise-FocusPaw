import tkinter as tk
from tkinter import messagebox
import json
import os

# --- FILE PATH SETUP ---
# This ensures it finds 'pets.json' in the same folder as this script[cite: 2]
script_dir = os.path.dirname(__file__) 
file_path = os.path.join(script_dir, 'pets.json')

# 1. Create a dictionary to hold stats so they stay persistent in the session
pet_stats = {"xp": 0, "hp": 100}

def load_data():
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                entry_user_id.insert(0, data.get("user id", ""))
                entry_pet_name.insert(0, data.get("pet name", ""))
                
                saved_pet = data.get("pet type", "Cat")
                if saved_pet in pet_options:
                    selected_pet.set(saved_pet)

                # Update the session stats with what was found in the file[cite: 8, 9]
                pet_stats["xp"] = data.get("current_xp", 0)
                pet_stats["hp"] = data.get("current_hp", 100)
        except Exception as e:
            print(f"Error loading data: {e}")

def save_data():
    userid = entry_user_id.get()
    petname = entry_pet_name.get()
    pettype = selected_pet.get()

    if userid.strip() == "" or petname.strip() == "":
        messagebox.showwarning("Oops!", "Please fill in both fields!")
        return

    data = {
        "user id": userid,
        "pet name": petname,
        "pet type": pettype,
        # Use the stored stats instead of resetting to 0/100[cite: 8, 9]
        "current_xp": pet_stats["xp"],
        "current_hp": pet_stats["hp"]
    }

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Saved!", f"Progress for {petname} has been preserved!")
# ─── BUILD THE WINDOW ───
popup = tk.Tk()
popup.title("Set up your pet")
popup.geometry("500x600") # Slightly taller to fit dropdown
popup.config(bg="#ADD8E6")

# Title[cite: 2]
tk.Label(popup, text="FocusPaw", font=("Courier", 36, "bold"), bg="#ADD8E6").pack(pady=40)

# User ID Input[cite: 2]
tk.Label(popup, text="Enter your user id:", bg="#ADD8E6", font=("Consolas", 12)).pack()
entry_user_id = tk.Entry(popup, font=("Consolas", 14))
entry_user_id.pack(pady=10)

# Pet Name Input[cite: 2]
tk.Label(popup, text="Enter your pet's name:", bg="#ADD8E6", font=("Consolas", 12)).pack()
entry_pet_name = tk.Entry(popup, font=("Consolas", 14))
entry_pet_name.pack(pady=10)

# --- NEW: Pet Selection Dropdown ---[cite: 4]
tk.Label(popup, text="Choose your pet type:", bg="#ADD8E6", font=("Consolas", 12)).pack()
pet_options = ["Cat", "Dog"]
selected_pet = tk.StringVar(popup)
selected_pet.set(pet_options[0]) # Default to Cat[cite: 4]

pet_dropdown = tk.OptionMenu(popup, selected_pet, *pet_options)
pet_dropdown.config(font=("Consolas", 12), width=10)
pet_dropdown.pack(pady=10)

# --- LOAD EXISTING DATA ---
# This updates entry boxes and the dropdown if data exists[cite: 2, 4]
load_data()

# Save Button[cite: 2]
tk.Button(popup, text="Save", font=("Consolas", 14, "bold"), command=save_data).pack(pady=20)

popup.mainloop()