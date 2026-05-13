import tkinter as tk
import tkinter.font as tKFont
import os
from PIL import Image, ImageTk  # Added for image handling

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Create the main window
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

# 2. Define the Fonts
title_font = tKFont.Font(family="Courier", size=46, weight="bold", slant="italic")
button_font = tKFont.Font(family="Consolas", size=25, weight="bold")
normal_font = tKFont.Font(family="Consolas", size=14)

# --- NEW: Load Background Image ---
try:
    # Use absolute path to the image file
    bg_path = os.path.join(script_dir, "background.jpeg")
    print(f"Looking for image at: {bg_path}")
    # Open the image and resize it to fit the 500x500 app window
    original_img = Image.open(bg_path)
    resized_img = original_img.resize((app_width, app_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_img)
    print("✓ Background image loaded successfully!")
except FileNotFoundError:
    print(f"Error: 'background.jpeg' not found at {bg_path}!")
    bg_image = None
except Exception as e:
    print(f"Error loading image: {e}")
    bg_image = None
    # --- NEW: Load Pet Images ---
pet_images = {}
try:
    # Resize them to 150x150 (or whatever size fits your app best)
    pet_size = (150, 150)
    
    pet_images["Cat"] = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "cat.jpeg")).resize(pet_size, Image.Resampling.LANCZOS))
    pet_images["Dog"] = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "puppy.jpeg")).resize(pet_size, Image.Resampling.LANCZOS))
    print("✓ Pet images loaded successfully!")
except Exception as e:
    print(f"Error loading pet images: {e}. Make sure they are in the same folder!")

# --- Functions ---
def show_setup():
    """Transition from Login to Setup screen"""
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    """Transition from Setup to Timer screen and load correct pet image"""
    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Get the pet the user selected from the dropdown
    chosen_pet = selected_pet.get()
    
    # Check if we successfully loaded an image for that pet
    if chosen_pet in pet_images:
        # Update the placeholder to show the image, remove the text, and remove the fixed text box size
        pet_placeholder.config(image=pet_images[chosen_pet], text="", width=150, height=150)
    else:
        # Fallback just in case the image didn't load
        pet_placeholder.config(image="", text=f"[ {chosen_pet} Image Missing ]", width=20, height=8)
def show_timer_screen():
    """Placeholder for the timer logic"""
    print("Timer logic will go here!")

# --- 1. Login Frame ---
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
# Place the background image at the very bottom layer of the frame using Canvas
if bg_image:
    login_canvas = tk.Canvas(login_frame, width=app_width, height=app_height)
    login_canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)
    login_canvas.place(x=0, y=0, relwidth=1, relheight=1)

login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

login_title = tk.Label(login_frame, text="FocusPaw", font=title_font, bg=bg_color)
login_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

login_button = tk.Button(
    login_frame,
    text="Login/Sign Up",
    font=button_font,
    width=15,
    height=2,
    command=show_setup
)
login_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# --- 2. Setup Frame (User Info & Pet) ---
setup_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    setup_canvas = tk.Canvas(setup_frame, width=app_width, height=app_height)
    setup_canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)
    setup_canvas.place(x=0, y=0, relwidth=1, relheight=1)

setup_title = tk.Label(setup_frame, text="Setup", font=title_font, bg=bg_color)
setup_title.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# User ID Input
tk.Label(setup_frame, text="User ID:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.35, anchor=tk.E)
user_id_entry = tk.Entry(setup_frame, font=normal_font, width=15)
user_id_entry.place(relx=0.35, rely=0.35, anchor=tk.W)

# Pet Name Input
tk.Label(setup_frame, text="Pet Name:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
pet_name_entry = tk.Entry(setup_frame, font=normal_font, width=15)
pet_name_entry.place(relx=0.35, rely=0.45, anchor=tk.W)

# Choose Pet Dropdown
tk.Label(setup_frame, text="Choose Pet:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)
pet_options = ["Cat", "Dog"]
selected_pet = tk.StringVar(window)
selected_pet.set(pet_options[0])
pet_dropdown = tk.OptionMenu(setup_frame, selected_pet, *pet_options)
pet_dropdown.config(font=normal_font, width=12)
pet_dropdown.place(relx=0.35, rely=0.55, anchor=tk.W)

next_button = tk.Button(setup_frame, text="Next", font=normal_font, width=10, command=show_timer)
next_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# --- 3. Timer Frame (Visuals & Placeholders) ---
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
if bg_image:
    tk.Label(timer_frame, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

timer_title = tk.Label(timer_frame, text="Focus", font=title_font, bg=bg_color)
timer_title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Pet Image Placeholder
pet_placeholder = tk.Label(
    timer_frame, 
   text="[ Loading Pet... ]", 
    bg="white", 
    width=20, 
    height=8, 
    relief="sunken"
)
pet_placeholder.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

# Timer Placeholder
timer_display = tk.Label(
    timer_frame, 
    text="25:00", 
    font=("Consolas", 40, "bold"), 
    bg=bg_color, 
    fg="#333333"
)
timer_display.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

# Stats Placeholder
stats_label = tk.Label(
    timer_frame, 
    text="Sessions: 0 | Coins: 0", 
    font=normal_font, 
    bg="#F0F0F0", 
    padx=10, 
    pady=5, 
    relief="groove"
)
stats_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

start_button = tk.Button(
    timer_frame, 
    text="Start Timer",  
    font=normal_font, 
    width=15, 
    command=show_timer_screen
)
start_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

# Start the application
window.mainloop()