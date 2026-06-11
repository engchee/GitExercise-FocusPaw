import tkinter as tk
import tkinter.font as tKFont
from tkinter import messagebox
import os
import json


# Matplotlib integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- IMPORT HELPER MODULES ---
import Pet_Visual
import game_math
import timer
import popup

# --- 1. MAIN WINDOW SETUP ---
window = tk.Tk()
window.title("FocusPaw🐾")

bg_color = "#ADD8E6"  # Light Blue
window.configure(bg=bg_color)

app_width = 500
app_height = 500

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

# --- 2. FONTS & BACKGROUND ---
title_font = tKFont.Font(family="Courier", size=46, weight="bold", slant="italic")
button_font = tKFont.Font(family="Consolas", size=25, weight="bold")
normal_font = tKFont.Font(family="Consolas", size=14)

bg_image = Pet_Visual.get_background_image(app_width, app_height)

# --- TEMPORARY VARIABLES ---
current_xp = 0
current_hp = 100
current_streak = 1
user_history = {} # Caches historical data for graphing updates

# --- AUDIO VARIABLES ---
mute_var = tk.BooleanVar(value=False)
focus_music_var = tk.StringVar(value="Options")
break_music_var = tk.StringVar(value="Options")

focus_options = ["Sunshine", "Lofi"]
break_options = ["Happy Home", "Dance with Me"]

# --- 3. NAVIGATION & LOGIC FUNCTIONS ---
def show_setup():
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_settings():
    #Switches view onto your configurations settings panel.
    timer_frame.place_forget()
    setup_frame.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def leave_settings():
    timer.apply_settings(mute_var.get(), focus_music_var.get(), break_music_var.get())
    #Saves choices and routes view back to Focus dashboard.
    settings_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    global current_xp, current_hp, current_streak, user_history
    
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    chosen_pet = selected_pet.get()
    
    if not userid or not petname:
        messagebox.showwarning("Missing Fields", "Please type your User ID and Pet Name before continuing!")
        return
    #Validate music selection
    if not mute_var.get():
        if focus_music_var.get() == "Options" or break_music_var.get() == "Options":
            messagebox.showwarning("Missing Music", "Please click the 🎵 button to choose your Focus and Break music before continuing!")
            return

    loaded_data = popup.load_data(userid)
    
    if loaded_data:
        print(f"Welcome back, {userid}!")
        current_xp = loaded_data.get("current_xp", 0)
        current_hp = loaded_data.get("current_hp", 100)
        current_streak = loaded_data.get("streak", 1)
        user_history = loaded_data.get("history", {})
        chosen_pet = loaded_data.get("pet type", "Cat")
        selected_pet.set(chosen_pet)
    else:
        print(f"New user {userid} created!")
        current_xp = 0
        current_hp = 100
        current_streak = 1
        user_history = {}

    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    new_image = Pet_Visual.get_pet_image(chosen_pet, "default")
    if new_image:
        pet_placeholder.config(image=new_image, text="", width=150, height=150)
        pet_placeholder.image = new_image 
    else:
        pet_placeholder.config(text="[Image Missing]")
        
    update_stats_ui()

def update_stats_ui():
    current_level = game_math.get_level(current_xp)
    stats_label.config(text=f"XP: {current_xp} | HP: {current_hp}/100 | 🔥Streak: {current_streak}")

def trigger_manual_save():
    #Callback wrapper triggered by timer.py automation flows
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    chosen_pet = selected_pet.get()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, xp_earned_now=0)

# --- UI BUTTON HOOKS ---
def click_start():
    print("Focusing...")
    chosen_pet = selected_pet.get()
    study_image = Pet_Visual.get_pet_image(chosen_pet, "studying")
    if study_image:
        pet_placeholder.config(image=study_image)
        pet_placeholder.image = study_image
        
    timer.start_timer(window, timer_display, timer_status, complete_focus_session, trigger_manual_save)

def click_pause():
    print("Paused")
    timer.pause_timer(window, timer_display, timer_status)

def click_give_up():
    global current_hp
    print("Gave Up...Deducting HP(╥‸╥)")
    
    current_hp = game_math.subtract_hp(current_hp, 10)
    update_stats_ui()
    
    chosen_pet = selected_pet.get()
    cry_image = Pet_Visual.get_pet_image(chosen_pet, "crying")
    if cry_image:
        pet_placeholder.config(image=cry_image)
        pet_placeholder.image = cry_image
        
    timer.give_up(window, timer_display, timer_status)
    
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, xp_earned_now=0)

def complete_focus_session(): 
    global current_xp, user_history
    print("Focus complete! Adding 10 XP...")
    current_xp = game_math.add_xp(current_xp, 10)     
    update_stats_ui()                                 
    
    chosen_pet = selected_pet.get()
    default_image = Pet_Visual.get_pet_image(chosen_pet, "default")
    if default_image:
        pet_placeholder.config(image=default_image)
        pet_placeholder.image = default_image
        
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, xp_earned_now=10)
    
    refreshed_data = popup.load_data(userid)
    if refreshed_data:
        user_history = refreshed_data.get("history", {})

def click_reset_pet():
    global current_xp, current_hp, current_streak, user_history
    
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    chosen_pet = selected_pet.get()
    
    if not userid:
        messagebox.showwarning("Error", "No active User ID found to reset!")
        return
        
    # Double check confirmation with user so they don't click it accidentally
    confirm = messagebox.askyesno("Reset Pet", "Are you sure you want to reset your pet's levels, HP, and stats to baseline zero?")
    if not confirm:
        return
        
    # 1. Reset memory variables to 0
    current_xp = 0
    current_hp = 0
    current_streak = 0
    user_history = {} # Wipes current history log cache
    
    # 2. Update UI indicators immediately
    update_stats_ui()
    
    # 3. Swap current animation image panel view back to default profile state
    default_image = Pet_Visual.get_pet_image(chosen_pet, "default")
    if default_image:
        pet_placeholder.config(image=default_image)
        pet_placeholder.image = default_image

    # 4. Save clean data state structure back down onto file disk 
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, xp_earned_now=0)
    
    # Force rewrite JSON directly to purge history structural dictionary clean
    path = popup.get_file_path(userid)
    if path and os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            data["history"] = {} # Hard wipe historical logging structure 
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error resetting history mapping records: {e}")
            
    messagebox.showinfo("Reset Complete", "Pet stats and history maps successfully reset to 0!")

# --- TASK 4: FRONTEND POPUP CONTROL ---
def reset_progress():
    global current_xp, current_hp, current_streak, user_history
    
    userid = entry_userid.get().strip()
    if not userid:
        messagebox.showwarning("No User ID", "Cannot reset progress without a valid User ID!")
        return

    confirm = messagebox.askyesno(
        "Reset Progress", 
        "Are you sure you want to delete this pet? All XP and Streaks will be lost forever!"
    )
    
    if confirm:
        popup.delete_data(userid)
        
        current_xp = 0
        current_hp = 100
        current_streak = 1
        user_history = {}
        
        timer_frame.place_forget()
        setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        update_stats_ui()
        print(f"All progress wiped for {userid}.")

def open_progress_chart():
    userid = entry_userid.get().strip()
    if not userid:
        return
        
    # Re-sync newest tracking details
    refreshed_data = popup.load_data(userid)
    history = refreshed_data.get("history", {}) if refreshed_data else user_history

    chart_window = tk.Toplevel(window)
    chart_window.title(f"{userid}'s Academic Progress")
    chart_window.geometry("500x400") # Expanded slightly for better label clearance
    
    # Match the window background color
    chart_window.configure(bg="#ADD8E6") 

    # --- DYNAMIC & CORRECT WEEK ORDERING ---
    # 1. Define standard weeks
    academic_weeks = [f"Week {i}" for i in range(1, 15)]
    
    # 2. Add Pre-Sem at the beginning if it exists in history
    if "Pre-Sem" in history:
        academic_weeks.insert(0, "Pre-Sem")
        
    # 3. Add Post-Sem at the end if it exists in history
    if "Post-Sem" in history:
        academic_weeks.append("Post-Sem")
        
    # 4. Include any other unexpected keys present in the history file
    for key in history.keys():
        if key not in academic_weeks:
            academic_weeks.append(key)

    # Extract corresponding values safely
    xp_values = [history.get(week, 0) for week in academic_weeks]

    # Create Figure and explicitly set facecolor to light blue
    fig, ax = plt.subplots(figsize=(6, 4), dpi=90, facecolor='#ADD8E6')
    ax.set_facecolor('#ADD8E6')
    
    # Draw bars with a darker blue border so they pop nicely
    ax.bar(academic_weeks, xp_values, color='#1E90FF', edgecolor='#00008B')
    
    ax.set_title("XP Earned per Academic Week", fontsize=12, fontweight='bold')
    ax.set_xlabel("Academic Cycle Weeks", fontsize=10)
    ax.set_ylabel("XP Gains Balance", fontsize=10)
    
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()

    # Pack it into the canvas frame
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Change canvas widget background configuration to eliminate gray borders
    canvas.get_tk_widget().configure(bg="#ADD8E6")

#----------------------FRAME 1: LOGIN-----------------------
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(login_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(login_frame, text="FocusPaw🐾", font=title_font, bg=bg_color).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
tk.Button(login_frame, text="Login/Sign Up", font=button_font, width=15, height=2, command=show_setup).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#----------------------FRAME 2: SETUP-----------------------
setup_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(setup_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(setup_frame, text="Setup", font=title_font, bg=bg_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

tk.Label(setup_frame, text="User ID:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.35, anchor=tk.E)
entry_userid = tk.Entry(setup_frame, font=normal_font, width=15)
entry_userid.place(relx=0.35, rely=0.35, anchor=tk.W)

tk.Label(setup_frame, text="Pet Name:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
entry_petname = tk.Entry(setup_frame, font=normal_font, width=15)
entry_petname.place(relx=0.35, rely=0.45, anchor=tk.W)

tk.Label(setup_frame, text="Choose Pet:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)
pet_options = ["Cat", "Dog", "Ebee"]
selected_pet = tk.StringVar(window)
selected_pet.set(pet_options[0])
pet_dropdown = tk.OptionMenu(setup_frame, selected_pet, *pet_options)
pet_dropdown.config(font=normal_font, width=12)
pet_dropdown.place(relx=0.35, rely=0.55, anchor=tk.W)

tk.Button(setup_frame, text="Next", font=normal_font, width=10, command=show_timer).place(relx=0.5, rely=0.75, anchor=tk.CENTER)

#----------------------FRAME 3: TIMER-----------------------
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(timer_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(timer_frame, text="Focus", font=title_font, bg=bg_color).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# FIXED: Removed the escaped backslashes syntax anomaly (\"sunken\") that caused terminal failure
pet_placeholder = tk.Label(timer_frame, text="[ Loading Pet... ]", bg="white", width=20, height=8, relief="sunken")
pet_placeholder.place(relx=0.5, rely=0.43, anchor=tk.CENTER)

timer_status = tk.Label(timer_frame, text="Ready to focus?", bg="#D7F6FD", font=normal_font, fg="blue")
timer_status.place(relx=0.5, rely=0.23, anchor=tk.CENTER)

timer_display = tk.Label(timer_frame, text="25:00", font=("Consolas", 40, "bold"), bg=bg_color, fg="#333333")
timer_display.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

stats_label = tk.Label(timer_frame, text="XP: 0 | HP: 100/100", font=normal_font, bg="#F0F0F0", padx=10, pady=5, relief="groove")
stats_label.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

# Musical Navigation Button Hook
tk.Button(setup_frame, text="🎵", font=normal_font, command=show_settings).place(x=20, y=20)

# Controls & Analytics View Button Dashboard
tk.Button(timer_frame, text="Start", font=normal_font, width=8, command=click_start).place(relx=0.2, rely=0.83, anchor=tk.CENTER)
tk.Button(timer_frame, text="Pause", font=normal_font, width=8, command=click_pause).place(relx=0.5, rely=0.83, anchor=tk.CENTER)
tk.Button(timer_frame, text="Give Up", font=normal_font, width=8, command=click_give_up).place(relx=0.8, rely=0.83, anchor=tk.CENTER)

# Graph shortcut button added to bottom floor level
tk.Button(timer_frame, text="📶", font=normal_font, command=open_progress_chart, bg="#FFF8DC").place(x=20, y=20)

# TASK 3: Reset Progress button placed safely inside window limits
tk.Button(
    timer_frame, 
    text="Reset Progress", 
    font=normal_font, 
    width=22, 
    command=reset_progress, 
    bg="#FFC0CB",      # Light pink background
    fg="#D8000C"       # Dark red text
).place(relx=0.5, rely=0.96, anchor=tk.CENTER)
tk.Button(timer_frame, text="Reset Pet", font=normal_font, width=12, command=click_reset_pet, bg="#FFC0CB").place(relx=0.5, rely=0.32, anchor=tk.CENTER)

#----------------------FRAME 4: SETTINGS-----------------------
settings_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(settings_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(settings_frame, text="Settings", font=title_font, bg=bg_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# 1. Mute Checkbox
tk.Checkbutton(settings_frame, text="Mute Background Music", variable=mute_var, font=normal_font, bg=bg_color).place(relx=0.3, rely=0.35, anchor=tk.W)

# 2. Focus Music Dropdown
tk.Label(settings_frame, text="Focus Music:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
tk.OptionMenu(settings_frame, focus_music_var, *focus_options).place(relx=0.35, rely=0.45, anchor=tk.W)

# 3. Break Music Dropdown
tk.Label(settings_frame, text="Break Music:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)
tk.OptionMenu(settings_frame, break_music_var, *break_options).place(relx=0.35, rely=0.55, anchor=tk.W)

# Save Button
tk.Button(settings_frame, text="Save & Back", font=normal_font, width=12, command=leave_settings).place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# --- START APP ---
# This loop stays at the absolute bottom of the script!
window.mainloop()