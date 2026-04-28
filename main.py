import tkinter as tk
import tkinter.font as tKFont

window = tk.Tk()
window.title("FocusPaw")

# Define the background color
bg_color = "#ADD8E6"  # Light Blue
window.configure(bg=bg_color)

app_width = 500
app_height = 500

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

title_font = tKFont.Font(family="Courier", size=46, weight="bold", slant="italic")
button_font = tKFont.Font(family="Consolas", size=25, weight="bold")
normal_font = tKFont.Font(family="Consolas", size=14)

# --- Functions for switching screens ---

def show_setup():
    login_frame.place_forget()
    setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer():
    setup_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def show_timer_screen():
    pass

# --- Login Frame ---
# Added bg=bg_color
login_frame = tk.Frame(window, width=500, height=500, bg=bg_color)
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


# --- Setup Frame ---
# Added bg=bg_color
setup_frame = tk.Frame(window, width=500, height=500, bg=bg_color)

setup_title = tk.Label(setup_frame, text="FocusPaw", font=title_font, bg=bg_color)
setup_title.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# User ID
tk.Label(setup_frame, text="User ID:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.35, anchor=tk.E)
user_id_entry = tk.Entry(setup_frame, font=normal_font, width=15)
user_id_entry.place(relx=0.35, rely=0.35, anchor=tk.W)

# Pet Name
tk.Label(setup_frame, text="Pet Name:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.45, anchor=tk.E)
pet_name_entry = tk.Entry(setup_frame, font=normal_font, width=15)
pet_name_entry.place(relx=0.35, rely=0.45, anchor=tk.W)

# Choose Pet
tk.Label(setup_frame, text="Choose Pet:", font=normal_font, bg=bg_color).place(relx=0.3, rely=0.55, anchor=tk.E)

pet_options = ["Cat", "Dog", "Rabbit", "Bird"]
selected_pet = tk.StringVar(window)
selected_pet.set(pet_options[0])

pet_dropdown = tk.OptionMenu(setup_frame, selected_pet, *pet_options)
pet_dropdown.config(font=normal_font, width=12)
pet_dropdown.place(relx=0.35, rely=0.55, anchor=tk.W)

next_button = tk.Button(
    setup_frame,
    text="Next",
    font=normal_font,
    width=10,
    command=show_timer
)
next_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)


# --- Timer Frame ---
# Added bg=bg_color
timer_frame = tk.Frame(window, width=500, height=500, bg=bg_color)

timer_title = tk.Label(timer_frame, text="FocusPaw", font=title_font, bg=bg_color)
timer_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

start_button = tk.Button(
    timer_frame, 
    text="Start Timer",  
    font=button_font, 
    width=15, 
    height=2,
    command=show_timer_screen
)
start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()