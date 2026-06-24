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
dark_bg_image = Pet_Visual.get_dark_background_image(app_width, app_height)
is_dark_mode = False

# --- TRACKING VARIABLES ---
current_xp = 0
current_hp = 100
current_streak = 1
current_coins = 0
owned_items = []
equipped_item = None
user_history = {}

# --- AUDIO VARIABLES ---
mute_var = tk.BooleanVar(value=False)
focus_music_var = tk.StringVar(value="Options")
break_music_var = tk.StringVar(value="Options")

focus_options = ["Options", "Sunshine", "Lofi"]
break_options = ["Options", "Happy Home", "Dance with Me"]

# --- 3. NAVIGATION & LOGIC FUNCTIONS ---
def toggle_dark_mode():
    global is_dark_mode
    if not dark_bg_image:
        print("Dark mode image missing! Check file name.")
        return

    if is_dark_mode:
        login_bg_label.config(image=bg_image)
        setup_bg_label.config(image=bg_image)
        timer_bg_label.config(image=bg_image)
        settings_bg_label.config(image=bg_image)
        shop_bg_label.config(image=bg_image)
        is_dark_mode = False
    else:
        login_bg_label.config(image=dark_bg_image)
        setup_bg_label.config(image=dark_bg_image)
        timer_bg_label.config(image=dark_bg_image)
        settings_bg_label.config(image=dark_bg_image)
        shop_bg_label.config(image=dark_bg_image)
        is_dark_mode = True

def show_settings():
    setup_frame.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def save_settings_and_return():
    try:
        timer.apply_settings(mute_var.get(), focus_music_var.get(), break_music_var.get())
    except:
        pass
    settings_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_setup():
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    global current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item, user_history
    
    userid = entry_userid.get().strip()
    chosen_pet = selected_pet.get()
    
    # Music Validation Shield
    if not mute_var.get():
        if focus_music_var.get() == "Options" or break_music_var.get() == "Options":
            messagebox.showwarning("Missing Music", "Please click the 🎵 button to choose your Focus and Break music before continuing!")
            return
            
    try:
        loaded_data = popup.load_data(userid)
        if loaded_data:
            current_xp = loaded_data.get("current_xp", 0)
            current_hp = loaded_data.get("current_hp", 100)
            current_streak = loaded_data.get("streak", 1)
            current_coins = loaded_data.get("coins", 0)
            owned_items = loaded_data.get("owned_items", [])
            equipped_item = loaded_data.get("equipped_item", None)
            user_history = loaded_data.get("history", {})
    except:
        pass

    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    new_image = Pet_Visual.get_pet_image(chosen_pet, "default", equipped_item)
    if new_image:
        pet_placeholder.config(image=new_image, text="")
        pet_placeholder.image = new_image 
        
    update_stats_ui()
    # Lock in daily streak
    popup.save_data(userid, entry_petname.get().strip(), chosen_pet, current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item, xp_earned_now=0)

def update_stats_ui():
    stats_label.config(text=f"XP: {current_xp} | HP: {current_hp}/100 | 🔥: {current_streak} | 🪙: {current_coins}")

def trigger_manual_save():
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    chosen_pet = selected_pet.get()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item, xp_earned_now=0)

# --- SHOP LOGIC ---
def show_shop():
    timer_frame.place_forget()
    shop_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def leave_shop():
    shop_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def buy_item(item_name, price):
    global current_coins, equipped_item
    chosen_pet = selected_pet.get()
    
    if item_name in owned_items:
        print(f"You already own {item_name}! Equipping it now.")
        equipped_item = item_name
    elif current_coins >= price:
        print(f"Bought {item_name}!")
        current_coins -= price
        owned_items.append(item_name)
        equipped_item = item_name
        update_stats_ui() 
    else:
        print(f"Not enough coins! You need {price} but only have {current_coins}.")
        return

    new_image = Pet_Visual.get_pet_image(chosen_pet, "default", equipped_item)
    if new_image:
        pet_placeholder.config(image=new_image)
        pet_placeholder.image = new_image
        
    try:
        popup.save_data(entry_userid.get(), entry_petname.get(), chosen_pet, current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item)
    except Exception as e:
        print(f"Save error in shop: {e}")

def unequip_item():
    global equipped_item
    chosen_pet = selected_pet.get()
    
    if equipped_item is None:
        print("Your pet isn't wearing anything!")
        return
        
    print(f"Removed {equipped_item}!")
    equipped_item = None
    
    new_image = Pet_Visual.get_pet_image(chosen_pet, "default", equipped_item)
    if new_image:
        pet_placeholder.config(image=new_image)
        pet_placeholder.image = new_image
        
    try:
        popup.save_data(entry_userid.get(), entry_petname.get(), chosen_pet, current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item)
    except Exception as e:
        print(f"Save error in shop: {e}")

# --- UI BUTTON HOOKS ---
def click_start():
    # Eng Chee's Anti-Spam Shield
    if timer.is_running:
        print("Timer is already active. Ignoring click.")
        return

    print("Focusing...")
    chosen_pet = selected_pet.get()
    
    try:
        # Check if we are resuming a paused BREAK session
        if timer.is_paused and timer.reps % 2 == 0:
            rest_img = Pet_Visual.get_pet_image(chosen_pet, "resting", equipped_item)
            if rest_img:
                pet_placeholder.config(image=rest_img)
                pet_placeholder.image = rest_img
        else:
            study_img = Pet_Visual.get_pet_image(chosen_pet, "studying", equipped_item)
            if study_img:
                pet_placeholder.config(image=study_img)
                pet_placeholder.image = study_img
                
        timer.start_timer(window, timer_display, timer_status, complete_focus_session, trigger_manual_save)
    except Exception as e:
        print(f"Timer started error: {e}")

def click_pause():
    try:
        timer.pause_timer(window, timer_display, timer_status)
    except Exception as e:
        print(f"Timer paused: {e}")

def click_give_up():
    global current_hp
    current_hp = game_math.subtract_hp(current_hp, 10)
    update_stats_ui()
    
    chosen_pet = selected_pet.get()
    cry_img = Pet_Visual.get_pet_image(chosen_pet, "crying", equipped_item)
    if cry_img:
        pet_placeholder.config(image=cry_img)
        pet_placeholder.image = cry_img
        
    try:
        timer.give_up(window, timer_display, timer_status)
        userid = entry_userid.get().strip()
        petname = entry_petname.get().strip()
        popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item, xp_earned_now=0)
    except Exception as e:
        print(f"Give up error: {e}")

def complete_focus_session():
    global current_xp, current_hp, current_coins, current_streak, user_history
    print("Focus complete! Adding 10 XP...")
    current_xp = game_math.add_xp(current_xp, 10)     
    current_hp = min(100, current_hp + 10) # Fixed missing add_hp crash
    current_coins += 10
   
    chosen_pet = selected_pet.get()
    rest_img = Pet_Visual.get_pet_image(chosen_pet, "resting", equipped_item)
    if rest_img:
        pet_placeholder.config(image=rest_img)
        pet_placeholder.image = rest_img
        
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    
    # Check calendar just in case app was left open overnight
    refreshed_data = popup.load_data(userid)
    if refreshed_data:
        current_streak = refreshed_data.get("streak", 1)
        user_history = refreshed_data.get("history", {})

    update_stats_ui()
    
    try:
        popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak, current_coins, owned_items, equipped_item, xp_earned_now=10)
    except Exception as e:
        print(f"Save error: {e}")

# --- TASK 4: FRONTEND POPUP CONTROL (Lisha's Code) ---
def reset_progress():
    global current_xp, current_hp, current_streak, user_history, current_coins, owned_items, equipped_item
    
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
        current_coins = 0
        owned_items = []
        equipped_item = None
        user_history = {}
        
        timer_frame.place_forget()
        setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        update_stats_ui()
        print(f"All progress wiped for {userid}.")

def open_progress_chart():
    userid = entry_userid.get().strip()
    if not userid:
        return
        
    refreshed_data = popup.load_data(userid)
    history = refreshed_data.get("history", {}) if refreshed_data else user_history

    chart_window = tk.Toplevel(window)
    chart_window.title(f"{userid}'s Academic Progress")
    chart_window.geometry("500x400")
    chart_window.configure(bg="#ADD8E6") 

    academic_weeks = [f"Week {i}" for i in range(1, 15)]
    
    if "Pre-Sem" in history:
        academic_weeks.insert(0, "Pre-Sem")
    if "Post-Sem" in history:
        academic_weeks.append("Post-Sem")
        
    for key in history.keys():
        if key not in academic_weeks:
            academic_weeks.append(key)

    xp_values = [history.get(week, 0) for week in academic_weeks]

    fig, ax = plt.subplots(figsize=(6, 4), dpi=90, facecolor='#ADD8E6')
    ax.set_facecolor('#ADD8E6')
    ax.bar(academic_weeks, xp_values, color='#1E90FF', edgecolor='#00008B')
    
    ax.set_title("XP Earned per Academic Week", fontsize=12, fontweight='bold')
    ax.set_xlabel("Academic Cycle Weeks", fontsize=10)
    ax.set_ylabel("XP Gains Balance", fontsize=10)
    
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.get_tk_widget().configure(bg="#ADD8E6")

#----------------------FRAME 1: LOGIN-----------------------
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    login_bg_label = tk.Label(login_frame, image=bg_image)
    login_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Button(login_frame, text="🌙", font=normal_font, command=toggle_dark_mode).place(x=20, y=20)
tk.Label(login_frame, text="FocusPaw🐾", font=title_font, bg=bg_color).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
tk.Button(login_frame, text="Login/Sign Up", font=button_font, width=15, height=2, command=show_setup).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# ---------------------- FRAME 2: SETUP -----------------------
setup_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    setup_bg_label = tk.Label(setup_frame, image=bg_image)
    setup_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Button(setup_frame, text="🎵", font=normal_font, command=show_settings).place(x=20, y=20)
tk.Button(setup_frame, text="🌙", font=normal_font, command=toggle_dark_mode).place(x=70, y=20)

tk.Label(setup_frame, text="Setup", font=title_font, bg=bg_color).place(relx=0.5, rely=0.22, anchor=tk.CENTER)
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
tk.OptionMenu(setup_frame, selected_pet, *pet_options).place(relx=0.35, rely=0.55, anchor=tk.W)

tk.Button(setup_frame, text="Next", font=normal_font, width=10, command=show_timer).place(relx=0.5, rely=0.75, anchor=tk.CENTER)

#----------------------FRAME 3: TIMER-----------------------
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    timer_bg_label = tk.Label(timer_frame, image=bg_image)
    timer_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Button(timer_frame, text="🛒 Shop", font=normal_font, command=show_shop).place(x=20, y=20)
tk.Button(timer_frame, text="📶", font=normal_font, command=open_progress_chart, bg="#FFF8DC").place(x=130, y=20)

tk.Label(timer_frame, text="Focus", font=title_font, bg=bg_color).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Thana's new dynamic pet box!
pet_box = tk.Frame(timer_frame, width=150, height=150, bg="white", relief="sunken", borderwidth=2)
pet_box.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
pet_box.pack_propagate(False)

pet_placeholder = tk.Label(pet_box, text="[ Loading Pet... ]", bg="white")
pet_placeholder.pack(expand=True, fill="both")

timer_status = tk.Label(timer_frame, text="Ready to focus?", bg="#D7F6FD", font=normal_font, fg="blue")
timer_status.place(relx=0.5, rely=0.23, anchor=tk.CENTER)

timer_display = tk.Label(timer_frame, text="25:00", font=("Consolas", 40, "bold"), bg=bg_color, fg="#333333")
timer_display.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

# UPDATED: Level removed from default text
stats_label = tk.Label(timer_frame, text="XP: 0 | HP: 100/100 | 🔥: 1 | 🪙: 0", font=normal_font, bg="#F0F0F0", padx=10, pady=5, relief="groove")
stats_label.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

tk.Button(timer_frame, text="Start", font=normal_font, width=8, command=click_start).place(relx=0.25, rely=0.85, anchor=tk.CENTER)
tk.Button(timer_frame, text="Pause", font=normal_font, width=8, command=click_pause).place(relx=0.5, rely=0.85, anchor=tk.CENTER)
tk.Button(timer_frame, text="Give Up", font=normal_font, width=8, command=click_give_up).place(relx=0.75, rely=0.85, anchor=tk.CENTER)

tk.Button(
    timer_frame, 
    text="Reset Progress", 
    font=normal_font, 
    width=22, 
    command=reset_progress, 
    bg="#FFC0CB",
    fg="#D8000C"
).place(relx=0.5, rely=0.94, anchor=tk.CENTER)

#----------------------FRAME 4: SETTINGS-----------------------
settings_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    settings_bg_label = tk.Label(settings_frame, image=bg_image)
    settings_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(settings_frame, text="Settings", font=title_font, bg=bg_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

tk.Checkbutton(settings_frame, text="Mute Background Music", variable=mute_var, font=normal_font, bg=bg_color).place(relx=0.3, rely=0.35, anchor=tk.W)

tk.Label(settings_frame, text="Focus Music:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
tk.OptionMenu(settings_frame, focus_music_var, *focus_options).place(relx=0.35, rely=0.45, anchor=tk.W)
tk.Label(settings_frame, text="Break Music:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)
tk.OptionMenu(settings_frame, break_music_var, *break_options).place(relx=0.35, rely=0.55, anchor=tk.W)
tk.Button(settings_frame, text="Save & Back", font=normal_font, width=12, command=save_settings_and_return).place(relx=0.5, rely=0.75, anchor=tk.CENTER)

#----------------------FRAME 5: VIRTUAL SHOP-----------------------
shop_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    shop_bg_label = tk.Label(shop_frame, image=bg_image)
    shop_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(shop_frame, text="Pet Shop", font=title_font, bg=bg_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)
tk.Label(shop_frame, text="Welcome! Buy items for your pet.", font=normal_font, bg=bg_color).place(relx=0.5, rely=0.25, anchor=tk.CENTER)

tk.Button(shop_frame, text="🎩 Top Hat (50 Coins)", font=normal_font, width=25, command=lambda: buy_item("Top Hat", 50)).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
tk.Button(shop_frame, text="👓 Cool Glasses (30 Coins)", font=normal_font, width=25, command=lambda: buy_item("Glasses", 30)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
tk.Button(shop_frame, text="🎀 Cute Bowtie (20 Coins)", font=normal_font, width=25, command=lambda: buy_item("Bowtie", 20)).place(relx=0.5, rely=0.6, anchor=tk.CENTER)
tk.Button(shop_frame, text="🚫 Remove Item", font=normal_font, width=25, command=unequip_item).place(relx=0.5, rely=0.7, anchor=tk.CENTER)

tk.Button(shop_frame, text="Back to Focus", font=normal_font, width=15, command=leave_shop).place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# --- START APP ---
window.mainloop()