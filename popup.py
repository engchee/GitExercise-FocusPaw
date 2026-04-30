import tkinter as tk
from tkinter import messagebox
import json
import os

# ─── FUNCTION: Save pet name to JSON ───
def save_pet_name():
    pet_name = entry_box.get()  # Grabs what the user typed

    if pet_name.strip() == "":
        messagebox.showwarning("Oops!", "Please enter a pet name first!")
        return

    # Load existing data if file exists, else start fresh
    if os.path.exists("pets.json"):
        with open("pets.json", "r") as f:
            data = json.load(f)
    else:
        data = {"pets": []}

    # Add the new pet name
    data["pets"].append(pet_name)

    # Save back to JSON
    with open("pets.json", "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Success!", f'"{pet_name}" has been saved!')
    entry_box.delete(0, tk.END)  # Clear the box after saving

# ─── FUNCTION: Read & display pets from JSON ───
def load_pets():
    if not os.path.exists("pets.json"):
        messagebox.showinfo("No Data", "No pets saved yet!")
        return

    with open("pets.json", "r") as f:
        data = json.load(f)

    pets = data.get("pets", [])
    if pets:
        result_label.config(text="Pets: " + ", ".join(pets))
    else:
        result_label.config(text="No pets found.")

# ─── BUILD THE WINDOW ───
window = tk.Tk()
window.title("Pet Name Entry")
window.geometry("350x250")
window.config(bg="#f0f4f8")

# Title label
tk.Label(window, text="🐾 Enter Your Pet's Name",
         font=("Arial", 14, "bold"), bg="#f0f4f8").pack(pady=15)

# Entry box
entry_box = tk.Entry(window, font=("Arial", 12), width=25)
entry_box.pack(pady=5)

# Save button
tk.Button(window, text="Save Pet Name", font=("Arial", 11),
          bg="#4CAF50", fg="white", command=save_pet_name).pack(pady=8)

# Load button
tk.Button(window, text="Load Pets from JSON", font=("Arial", 11),
          bg="#2196F3", fg="white", command=load_pets).pack(pady=5)

# Result display
result_label = tk.Label(window, text="", font=("Arial", 11),
                        bg="#f0f4f8", fg="#333")
result_label.pack(pady=10)

window.mainloop()