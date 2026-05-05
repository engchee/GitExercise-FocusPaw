import tkinter as tk
from tkinter import messagebox
import json

def save_pet_name():
    pet_name = entry_box.get()

    if pet_name.strip() == "":
        messagebox.showwarning("Oops!", "Please enter a pet name!")
        return

    data = {"pet_name": pet_name}

    with open("focuspaw_data.json", "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo("Saved!", f'"{pet_name}" saved!')
    popup.destroy()

# ─── BUILD THE WINDOW ───
popup = tk.Tk()
popup.title("Name Your Pet")

app_width = 500
app_height = 500

# ✅ Center the window on screen
screen_width = popup.winfo_screenwidth()
screen_height = popup.winfo_screenheight()
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
popup.geometry(f"{app_width}x{app_height}+{x}+{y}")

popup.config(bg="#ADD8E6")  # ✅ matched FocusPaw blue

# Title
tk.Label(popup, text="FocusPaw",
         font=("Courier", 36, "bold", "italic"),
         bg="#ADD8E6").pack(pady=40)

# Subtitle
tk.Label(popup, text="Enter your pet's name:",
         font=("Consolas", 14),
         bg="#ADD8E6").pack()

# Entry box
entry_box = tk.Entry(popup, font=("Consolas", 14), width=20)
entry_box.pack(pady=10)

# Save button
tk.Button(popup, text="Save",
          font=("Consolas", 14, "bold"),
          width=12, height=1,
          command=save_pet_name).pack(pady=20)

popup.mainloop()