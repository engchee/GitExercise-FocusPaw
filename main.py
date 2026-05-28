import tkinter as tk
import tkinter.font as tKFont

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

# --- TEMPORARY VARIABLES (Until Lisha's Data is connected) ---
current_xp = 0
current_hp = 100
current_streak = 1

# --- AUDIO VARIABLES ---
mute_var = tk.BooleanVar(value=False)
focus_music_var = tk.StringVar(value="Options")
break_music_var = tk.StringVar(value="Options")

focus_options = ["Sunshine", "Lofi"]
break_options = ["Happy Home", "Dance with Me"]

def show_settings():                   #Hides the Setup frame and opens Settings
    setup_frame.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def save_settings_and_return():        #Sends choices to timer.py and goes back to Setup
    timer.apply_settings(mute_var.get(), focus_music_var.get(), break_music_var.get())
    settings_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# --- 3. NAVIGATION & LOGIC FUNCTIONS ---
def show_setup():
    #Hides Login and shows Setup
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    global current_xp, current_hp, current_streak
    
    # 1. Grab what the user typed in the boxes
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    chosen_pet = selected_pet.get()
    
    # 2. --- TRIGGER POPUP.PY LOAD FUNCTION ---
    loaded_data = popup.load_data(userid)
    
    if loaded_data:
        print(f"Welcome back, {userid}!")
        current_xp = loaded_data.get("current_xp", 0)
        current_hp = loaded_data.get("current_hp", 100)
        current_streak = loaded_data.get("streak", 1)
        # Update the dropdown to match their saved pet
        chosen_pet = loaded_data.get("pet type", "Cat")
        selected_pet.set(chosen_pet)
    else:
        print(f"New user {userid} created!")
        current_xp = 0
        current_hp = 100
        current_streak = 1

    # Hide Setup, shows Timer
    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Ask Pet_Visual for the default image of that pet
    new_image = Pet_Visual.get_pet_image(chosen_pet, "default")
    
    if new_image:
        pet_placeholder.config(image=new_image, text="", width=150, height=150)
        pet_placeholder.image = new_image 
    else:
        pet_placeholder.config(text="[Image Missing]")
        
    update_stats_ui()

def update_stats_ui():
    #Calculates level and updates the text on the screen
    current_level = game_math.get_level(current_xp)
    stats_label.config(text=f"Level: {current_level} | XP: {current_xp} | HP: {current_hp}/100 | 🔥Streak: {current_streak}")

# --- UI BUTTON HOOKS (Connecting UI to Engine) ---
def click_start():
    print("Start/Resume clicked!")
    
    # Check if we are resuming a paused BREAK session (even reps)
    if timer.is_paused and timer.reps % 2 == 0:
        # Keep the default image since they are still on a break
        chosen_pet = selected_pet.get()
        default_image = Pet_Visual.get_pet_image(chosen_pet, "default")
        if default_image:
            pet_placeholder.config(image=default_image)
            pet_placeholder.image = default_image
            
    # Otherwise, it is a FOCUS session (starting fresh or resuming focus)
    else:
        chosen_pet = selected_pet.get()
        study_image = Pet_Visual.get_pet_image(chosen_pet, "studying")
        if study_image:
            pet_placeholder.config(image=study_image)
            pet_placeholder.image = study_image
        
    # Trigger the timer engine
    timer.start_timer(window, timer_display, timer_status, complete_focus_session)

def click_pause():
    print("Paused")
    timer.pause_timer(window, timer_display, timer_status)

def click_give_up():
    global current_hp
    print("Gave Up...Deducting HP(╥‸╥)")
    
    # 1. Math: Take damage
    current_hp = game_math.subtract_hp(current_hp, 10)
    update_stats_ui()
    
    # 2. Visual: Change image to crying
    chosen_pet = selected_pet.get()
    cry_image = Pet_Visual.get_pet_image(chosen_pet, "crying")
    if cry_image:
        pet_placeholder.config(image=cry_image)
        pet_placeholder.image = cry_image
        
    # 3. Stop timer 
    timer.give_up(window, timer_display, timer_status)
    
    # --- TRIGGER AUTO-SAVE ---
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak)

def complete_focus_session():
    global current_xp
    print("Focus complete! Adding 10 XP...")
    current_xp = game_math.add_xp(current_xp, 10)     
    update_stats_ui()                                 
    
    chosen_pet = selected_pet.get()
    default_image = Pet_Visual.get_pet_image(chosen_pet, "default")
    if default_image:
        pet_placeholder.config(image=default_image)
        pet_placeholder.image = default_image
        
    # --- TRIGGER AUTO-SAVE ---
    userid = entry_userid.get().strip()
    petname = entry_petname.get().strip()
    popup.save_data(userid, petname, chosen_pet, current_xp, current_hp, current_streak)

#----------------------FRAME 1: LOGIN-----------------------
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(login_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(login_frame, text="FocusPaw", font=title_font, bg=bg_color).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
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
tk.Button(setup_frame, text="🎵", font=normal_font, command=show_settings).place(x=20, y=20)

#----------------------FRAME 3: TIMER-----------------------
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(timer_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(timer_frame, text="Focus", font=title_font, bg=bg_color).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

pet_placeholder = tk.Label(timer_frame, text="[ Loading Pet... ]", bg="white", width=20, height=8, relief="sunken")
pet_placeholder.place(relx=0.5, rely=0.43, anchor=tk.CENTER)

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

#----------------------FRAME 4: SETTINGS-----------------------
settings_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(settings_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(settings_frame, text="Settings", font=title_font, bg=bg_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# 1. Mute Checkbox
tk.Checkbutton(settings_frame, text="Mute Background Music", variable=mute_var, font=normal_font, bg=bg_color).place(relx=0.5, rely=0.35, anchor=tk.CENTER)

# 2. Focus Music Dropdown
tk.Label(settings_frame, text="Focus Music:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
tk.OptionMenu(settings_frame, focus_music_var, *focus_options).place(relx=0.35, rely=0.45, anchor=tk.W)

# 3. Break Music Dropdown
tk.Label(settings_frame, text="Break Music:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)
tk.OptionMenu(settings_frame, break_music_var, *break_options).place(relx=0.35, rely=0.55, anchor=tk.W)

# Save Button
tk.Button(settings_frame, text="Save & Back", font=normal_font, width=12, command=save_settings_and_return).place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# --- START APP ---
window.mainloop()