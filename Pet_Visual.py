import tkinter as tk
import tkinter.font as tKFont
import os
from PIL import Image, ImageTk

# Connects to your math logic file!
import game_math  

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- 1. Create the main window ---
window = tk.Tk()
window.title("FocusPaw")

# We keep your original light blue for text label backgrounds to match the sky!
bg_color = "#ADD8E6" 
window.configure(bg=bg_color)

app_width = 500
app_height = 500

# Center the window on your screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

# --- 2. Define the Fonts ---
title_font = tKFont.Font(family="Courier", size=46, weight="bold", slant="italic")
button_font = tKFont.Font(family="Consolas", size=25, weight="bold")
normal_font = tKFont.Font(family="Consolas", size=14)

# --- Pet Stats ---
pet_hp = 100
pet_xp = 0

# --- Load Background Image ---
try:
    bg_path = os.path.join(script_dir, "background.jpeg")
    original_img = Image.open(bg_path)
    resized_img = original_img.resize((app_width, app_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_img)
    print("✓ Background image loaded successfully!")
except Exception as e:
    print(f"Error loading background image: {e}")
    bg_image = None

# --- Load Pet Images (With Multiple States) ---
pet_images = {}
try:
    pet_size = (150, 150)
    
    # Cat Images
    pet_images["Cat"] = {
        "default": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "cat.jpeg")).resize(pet_size, Image.Resampling.LANCZOS)),
        "studying": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "cat_studying.jpeg")).resize(pet_size, Image.Resampling.LANCZOS)),
        "crying": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "cat_crying.jpeg")).resize(pet_size, Image.Resampling.LANCZOS))
    }
    
    # Dog Images
    pet_images["Dog"] = {
        "default": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "puppy.jpeg")).resize(pet_size, Image.Resampling.LANCZOS)),
        "studying": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "dog_studying.jpeg")).resize(pet_size, Image.Resampling.LANCZOS)),
        "crying": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "dog_crying.jpeg")).resize(pet_size, Image.Resampling.LANCZOS))
    }
    
    # Ebee Images
    pet_images["Ebee"] = {
        "default": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "ebee.jpeg")).resize(pet_size, Image.Resampling.LANCZOS)),
        "studying": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "ebee_studying.jpeg")).resize(pet_size, Image.Resampling.LANCZOS)),
        "crying": ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "ebee_crying.jpeg")).resize(pet_size, Image.Resampling.LANCZOS))
    }
    
    print("✓ All Pet states (default, studying, crying) loaded successfully!")
except Exception as e:
    print(f"Error loading pet images: {e}")


# --- Functions ---
def show_setup():
    """Transition from Login to Setup screen"""
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    """Transition from Setup to Timer screen and load correct default pet image"""
    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    chosen_pet = selected_pet.get()
    
    # Load the "default" image when first entering the screen
    if chosen_pet in pet_images:
        pet_placeholder.config(image=pet_images[chosen_pet]["default"], text="", width=150, height=150)
    else:
        pet_placeholder.config(image="", text=f"[ {chosen_pet} Image Missing ]", width=20, height=8)
    
    # Show initial stats when the timer screen loads
    update_stats_ui()

def update_stats_ui():
    """Updates the text on the screen using the math file."""
    current_level = game_math.get_level(pet_xp)
    stats_label.config(text=f"Level: {current_level} | XP: {pet_xp} | HP: {pet_hp}/100")

def start_timer():
    global pet_xp
    print("Start clicked! Pretending a session just finished...")
    pet_xp = game_math.add_xp(pet_xp, 25)
    
    # Swap to Studying Image!
    chosen_pet = selected_pet.get()
    if chosen_pet in pet_images:
        pet_placeholder.config(image=pet_images[chosen_pet]["studying"])
        
    update_stats_ui()

def pause_timer():
    print("Pause button clicked! Timer is paused.")

def give_up():
    global pet_hp
    print("Give Up clicked! Taking 10 damage...")
    pet_hp = game_math.subtract_hp(pet_hp, 10)
    
    chosen_pet = selected_pet.get()
    
    if not game_math.is_alive(pet_hp):
        print("Oh no! Your pet ran out of HP!")
        # Hide the image and show fainting text
        pet_placeholder.config(text="[ Pet Fainted! ]", image="", width=20, height=8) 
    else:
        # Swap to Crying Image! (if they are still alive)
        if chosen_pet in pet_images:
            pet_placeholder.config(image=pet_images[chosen_pet]["crying"])
            
    update_stats_ui()


# --- 1. Login Frame ---
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    login_canvas = tk.Canvas(login_frame, width=app_width, height=app_height)
    login_canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)
    login_canvas.place(x=0, y=0, relwidth=1, relheight=1)

login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(login_frame, text="FocusPaw", font=title_font, bg=bg_color).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
tk.Button(login_frame, text="Login/Sign Up", font=button_font, width=15, height=2, command=show_setup).place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# --- 2. Setup Frame (User Info & Pet) ---
setup_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    setup_canvas = tk.Canvas(setup_frame, width=app_width, height=app_height)
    setup_canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)
    setup_canvas.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(setup_frame, text="Setup", font=title_font, bg=bg_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

tk.Label(setup_frame, text="User ID:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.35, anchor=tk.E)
tk.Entry(setup_frame, font=normal_font, width=15).place(relx=0.35, rely=0.35, anchor=tk.W)

tk.Label(setup_frame, text="Pet Name:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
tk.Entry(setup_frame, font=normal_font, width=15).place(relx=0.35, rely=0.45, anchor=tk.W)

tk.Label(setup_frame, text="Choose Pet:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)
# Ebee added to the options list here!
pet_options = ["Cat", "Dog", "Ebee"] 
selected_pet = tk.StringVar(window)
selected_pet.set(pet_options[0])
pet_dropdown = tk.OptionMenu(setup_frame, selected_pet, *pet_options)
pet_dropdown.config(font=normal_font, width=12)
pet_dropdown.place(relx=0.35, rely=0.55, anchor=tk.W)

tk.Button(setup_frame, text="Next", font=normal_font, width=10, command=show_timer).place(relx=0.5, rely=0.75, anchor=tk.CENTER)


# --- 3. Timer Frame (Visuals & Placeholders) ---
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(timer_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(timer_frame, text="Focus", font=title_font, bg=bg_color).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

pet_placeholder = tk.Label(timer_frame, text="[ Loading Pet... ]", bg="white", width=20, height=8, relief="sunken")
pet_placeholder.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

tk.Label(timer_frame, text="25:00", font=("Consolas", 40, "bold"), bg=bg_color, fg="#333333").place(relx=0.5, rely=0.55, anchor=tk.CENTER)

stats_label = tk.Label(timer_frame, text="Level: 0 | XP: 0 | HP: 100/100", font=normal_font, bg="#F0F0F0", padx=10, pady=5, relief="groove")
stats_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Start, Pause, Give Up Buttons
tk.Button(timer_frame, text="Start", font=normal_font, width=8, command=start_timer).place(relx=0.25, rely=0.85, anchor=tk.CENTER)
tk.Button(timer_frame, text="Pause", font=normal_font, width=8, command=pause_timer).place(relx=0.5, rely=0.85, anchor=tk.CENTER)
tk.Button(timer_frame, text="Give Up", font=normal_font, width=8, command=give_up).place(relx=0.75, rely=0.85, anchor=tk.CENTER)

# --- Start the Application ---
window.mainloop()