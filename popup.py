import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date # --- STEP 1: Import date from datetime ---

# --- FILE PATH SETUP ---
script_dir = os.path.dirname(__file__) 

# STEP 2: Update session stats to include streak and last_login
pet_stats = {"xp": 0, "hp": 100, "streak": 0, "last_login": ""}

def get_file_path():
    userid = entry_user_id.get().strip()
    if not userid:
        return None
    return os.path.join(script_dir, f"{userid}_pet.json")

# --- STEP 3: NEW STREAK CALCULATION LOGIC ---
def calculate_streak(saved_date_str, current_streak):
    today = date.today()
    
    # FIX: If there is no date OR the current streak is 0, start it at 1
    if not saved_date_str or current_streak == 0:
        return 1 

    last_login = date.fromisoformat(saved_date_str)
    delta = (today - last_login).days

    if delta == 1:
        return current_streak + 1  # Next day
    elif delta > 1:
        return 1                   # Missed a day, reset to 1
    else:
        return max(current_streak, 1) # Same day, ensure it's at least 1
    
def view_history():
    path = get_file_path()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "No history found for this User ID.")
        return

    history_win = tk.Toplevel(popup)
    history_win.title("Pet History")
    history_win.geometry("300x400")
    history_win.config(bg="#FFFDD0")

    try:
        with open(path, "r") as f:
            data = json.load(f)
            
        tk.Label(history_win, text="📜 PET PROGRESS", font=("Courier", 18, "bold"), bg="#FFFDD0").pack(pady=20)
        
        stats_text = (
            f"User ID: {data.get('user id')}\n\n"
            f"Pet Name: {data.get('pet name')}\n"
            f"Pet Type: {data.get('pet type')}\n"
            f"-------------------\n"
            f"Current XP: {data.get('current_xp')}\n"
            f"Current HP: {data.get('current_hp')}\n"
            f"Current Streak: {data.get('streak', 0)} Days" # Show streak in history
        )
        
        tk.Label(history_win, text=stats_text, font=("Consolas", 12), bg="#FFFDD0", justify="left").pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read history: {e}")

def load_data():
    path = get_file_path()
    if path and os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                entry_pet_name.delete(0, tk.END)
                entry_pet_name.insert(0, data.get("pet name", ""))
                selected_pet.set(data.get("pet type", "Cat"))
                
                # Update stats from file
                pet_stats["xp"] = data.get("current_xp", 0)
                pet_stats["hp"] = data.get("current_hp", 100)
                
                # --- STEP 4: Calculate streak on load ---
                saved_date = data.get("last_login", "")
                old_streak = data.get("streak", 0)
                new_streak = calculate_streak(saved_date, old_streak)
                pet_stats["streak"] = new_streak
                
                # Update the UI label
                lbl_streak.config(text=f"🔥 Current Streak: {new_streak} Days")
                
        except Exception as e:
            print(f"Error loading: {e}")

def save_data():
    userid = entry_user_id.get().strip()
    petname = entry_pet_name.get().strip()
    if not userid or not petname:
        messagebox.showwarning("Oops!", "Fill in both fields!")
        return
    
    path = get_file_path()
    data = {
        "user id": userid,
        "pet name": petname,
        "pet type": selected_pet.get(),
        "current_xp": pet_stats["xp"],
        "current_hp": pet_stats["hp"],
        "streak": pet_stats["streak"], # Save the streak
        "last_login": date.today().isoformat() # --- STEP 5: Save today's date ---
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Saved!", "Progress preserved!")

# --- UI SETUP ---
popup = tk.Tk()
popup.title("FocusPaw Setup")
popup.geometry("500x700")
popup.config(bg="#ADD8E6")

tk.Label(popup, text="FocusPaw", font=("Courier", 36, "bold"), bg="#ADD8E6").pack(pady=30)

# STEP 6: Add a label to display the streak
lbl_streak = tk.Label(popup, text="🔥 Current Streak: 0 Days", font=("Consolas", 12, "bold"), bg="#ADD8E6", fg="#D2691E")
lbl_streak.pack()

tk.Label(popup, text="Enter your user id:", bg="#ADD8E6").pack(pady=(10, 0))
entry_user_id = tk.Entry(popup, font=("Consolas", 14))
entry_user_id.pack(pady=5)

btn_frame = tk.Frame(popup, bg="#ADD8E6")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Find My Pet", command=load_data).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="View History", command=view_history, bg="#FFD700").grid(row=0, column=1, padx=5)

tk.Label(popup, text="Enter your pet's name:", bg="#ADD8E6").pack()
entry_pet_name = tk.Entry(popup, font=("Consolas", 14))
entry_pet_name.pack(pady=5)

tk.Label(popup, text="Choose your pet type:", bg="#ADD8E6").pack()
pet_options = ["Cat", "Dog"]
selected_pet = tk.StringVar(popup)
selected_pet.set(pet_options[0])
tk.OptionMenu(popup, selected_pet, *pet_options).pack(pady=5)

tk.Button(popup, text="Save", font=("Consolas", 14, "bold"), command=save_data).pack(pady=20)

popup.mainloop()