from tkinter import *
from PIL import Image, ImageTk

# =========================
# WINDOW SETUP
# =========================
root = Tk()
root.title("FocusPaw System")
root.geometry("900x600")
root.configure(bg="#0b1f3a")

# =========================
# LOAD IMAGES
# =========================
idle_img = Image.open("focuspaw.png").resize((200, 200))
happy_img = Image.open("focuspaw.png").resize((200, 200)) 

idle_pet = ImageTk.PhotoImage(idle_img)
happy_pet = ImageTk.PhotoImage(happy_img)

# =========================
# LEFT FRAME (CONTROLS)
# =========================
left_frame = Frame(root, bg="#1f7a1f", width=250)
left_frame.pack(side="left", fill="y", padx=20, pady=20)

user_label = Label(
    left_frame,
    text="User\n(MMU Student / Staff)",
    bg="#1f7a1f",
    fg="white",
    font=("Arial", 12, "bold")
)
user_label.pack(pady=20)

# =========================
# CENTER FRAME (PET)
# =========================
center_frame = Frame(root, bg="#0b1f3a")
center_frame.pack(side="left", expand=True)

pet_label = Label(center_frame, image=idle_pet, bg="#0b1f3a")
pet_label.pack(pady=20)

status_label = Label(
    center_frame,
    text="Pet Status: Idle",
    font=("Arial", 14),
    bg="#0b1f3a",
    fg="white"
)
status_label.pack(pady=10)

timer_label = Label(
    center_frame,
    text="00:00",
    font=("Arial", 20, "bold"),
    bg="#0b1f3a",
    fg="white"
)
timer_label.pack(pady=10)

# =========================
# TIMER LOGIC
# =========================
time_left = 10  # demo (10 sec). Change to 1500 for 25 mins
running = False

def update_timer():
    global time_left, running

    if running and time_left > 0:
        mins = time_left // 60
        secs = time_left % 60
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

        time_left -= 1
        root.after(1000, update_timer)
    else:
        end_session()

def start_session():
    global running, time_left
    running = True
    time_left = 10  # change to 1500 for real use

    status_label.config(text="Pet Status: Studying 😄")
    pet_label.config(image=happy_pet)

    update_timer()

def reset_session():
    global running, time_left
    running = False
    time_left = 10

    timer_label.config(text="00:00")
    status_label.config(text="Pet Status: Idle 😴")
    pet_label.config(image=idle_pet)

def end_session():
    global running
    running = False

    status_label.config(text="Pet Status: Resting 😴")
    pet_label.config(image=idle_pet)

# =========================
# BUTTONS
# =========================
start_btn = Button(left_frame, text="Start Session", width=20, command=start_session)
start_btn.pack(pady=10)

reset_btn = Button(left_frame, text="Give Up / Reset", width=20, command=reset_session)
reset_btn.pack(pady=10)

# =========================
# RUN APP
# =========================
root.mainloop()