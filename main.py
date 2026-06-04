import tkinter as tk
import tkinter.font as tKFont
import os

# --- IMPORT HELPER MODULES ---
import Pet_Visual 
import game_math
import timer
import popup

# --- 1. MAIN WINDOW SETUP ---
window = tk.Tk()
window.title("FocusPaw")

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

# Ask Pet_Visual.py for the background image
bg_image = Pet_Visual.get_background_image(app_width, app_height)

# --- TRACKING VARIABLES ---
current_xp = 0
current_hp = 100
current_streak = 1

# --- 3. NAVIGATION & LOGIC FUNCTIONS ---
def show_setup():
    """Hides Login and shows Setup"""
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    """Hides Setup, shows Timer, and loads saved data"""
    global current_xp, current_hp, current_streak
    
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    chosen_pet = selected_pet.get()
    
    # Trigger popup.py load function
    loaded_data = popup.load_data(userid)
    
    if loaded_data:
        print(f"Welcome back, {userid}!")
        current_xp = loaded_data.get("current_xp", 0)
        current_hp = loaded_data.get("current_hp", 100)
        current_streak = loaded_data.get("streak", 1)
    else:
        print(f"New user {userid} created!")
        current_xp = 0
        current_hp = 100
        current_streak = 1

    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Load initial pet image
    new_image = Pet_Visual.get_pet_image(chosen_pet, "default")
    
    if new_image:
        pet_placeholder.config(image=new_image, text="")
        pet_placeholder.image = new_image 
    else:
        pet_placeholder.config(text="[Image Missing]")
        
    update_stats_ui()

def update_stats_ui():
    """Calculates level and updates the UI stats bar"""
    current_level = game_math.get_level(current_xp)
    stats_label.config(text=f"Level: {current_level} | XP: {current_xp} | HP: {current_hp}/100 | 🔥Streak: {current_streak}")

# --- UI BUTTON HOOKS ---
def click_start():
    """Starts the timer and updates pet visual to studying or resting"""
    print("Start/Resume clicked!")
    chosen_pet = selected_pet.get()
    
    # Check if we are resuming a paused BREAK session (even reps)
    if timer.is_paused and timer.reps % 2 == 0:
        rest_image = Pet_Visual.get_pet_image(chosen_pet, "resting")
        if rest_image:
            pet_placeholder.config(image=rest_image)
            pet_placeholder.image = rest_image
            
    # Otherwise, it is a FOCUS session
    else:
        study_image = Pet_Visual.get_pet_image(chosen_pet, "studying")
        if study_image:
            pet_placeholder.config(image=study_image)
            pet_placeholder.image = study_image
        
    timer.start_timer(window, timer_display, timer_status, complete_focus_session)

def click_pause():
    """Pauses the timer"""
    print("Paused")
    timer.pause_timer(window, timer_display, timer_status)

def click_give_up():
    """Subtracts HP and shows crying pet state"""
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
    
    # Auto-save current progress
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak)

def complete_focus_session():
    """Awards XP/HP and switches pet to resting state for the break"""
    global current_xp, current_hp
    print("Focus complete! Adding XP and recovering HP...")
    
    current_xp = game_math.add_xp(current_xp, 10)     
    current_hp = game_math.add_hp(current_hp, 10)
    update_stats_ui()
   
    chosen_pet = selected_pet.get()
    rest_image = Pet_Visual.get_pet_image(chosen_pet, "resting")
    if rest_image:
        pet_placeholder.config(image=rest_image)
        pet_placeholder.image = rest_image
        
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak)

# ---------------------- FRAME 1: LOGIN -----------------------
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(login_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(login_frame, text="FocusPaw", font=title_font, bg=bg_color).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
tk.Button(login_frame, text="Login/Sign Up", font=button_font, width=15, height=2, command=show_setup).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# ---------------------- FRAME 2: SETUP -----------------------
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

# ---------------------- FRAME 3: TIMER -----------------------
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(timer_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(timer_frame, text="Focus", font=title_font, bg=bg_color).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# --- LOCKED UI PLACEHOLDER FIX ---
# This frame acts as a rigid container so the layout doesn't "jump"
pet_box = tk.Frame(timer_frame, width=150, height=150, bg="white", relief="sunken", borderwidth=2)
pet_box.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
pet_box.pack_propagate(False) # Prevents the box from shrinking

pet_placeholder = tk.Label(pet_box, text="[ Loading Pet... ]", bg="white")
pet_placeholder.pack(expand=True, fill="both")

timer_status = tk.Label(timer_frame, text="Ready to focus?", bg="#D7F6FD", font=normal_font, fg="blue")
timer_status.place(relx=0.5, rely=0.23, anchor=tk.CENTER)

timer_display = tk.Label(timer_frame, text="25:00", font=("Consolas", 40, "bold"), bg=bg_color, fg="#333333")
timer_display.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

stats_label = tk.Label(timer_frame, text="Level: 0 | XP: 0 | HP: 100/100", font=normal_font, bg="#F0F0F0", padx=10, pady=5, relief="groove")
stats_label.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

# Controls
tk.Button(timer_frame, text="Start", font=normal_font, width=8, command=click_start).place(relx=0.25, rely=0.85, anchor=tk.CENTER)
tk.Button(timer_frame, text="Pause", font=normal_font, width=8, command=click_pause).place(relx=0.5, rely=0.85, anchor=tk.CENTER)
tk.Button(timer_frame, text="Give Up", font=normal_font, width=8, command=click_give_up).place(relx=0.75, rely=0.85, anchor=tk.CENTER)

# --- START APP ---
window.mainloop()