import tkinter as tk
import tkinter.font as tkFont
import math
import pygame

pygame.mixer.init()

#---------timer function---------
work_min = 25
break_min = 5
timer = None
reps = 0
is_paused = False

def start_timer():
    global reps, is_paused
    if is_paused:
        resume_timer()
        return
    reps += 1
    if reps % 2 == 0:
        print("Break time! Take a rest!(˶ᵔ ᵕ ᵔ˶)")
        status_label.config(text="Break Time! Take a rest!", fg="blue")
        try:
            pygame.mixer.music.load("break1.mp3")
            pygame.mixer.music.play(-1)
        except:
            print("Background music file not found!")
        #break_sec = break_min * 60
        break_sec = 5
        count_down(break_sec)
    else:
        print("Timer started!(˶ˆᗜˆ˵)")
        status_label.config(text="Focusing...", fg="green")
        try:
            pygame.mixer.music.load("study1.mp3")
            pygame.mixer.music.play(-1)
        except:
            print("Background music file not found!")
        #work_sec = work_min * 60
        work_sec = 5
        count_down(work_sec)

paused_count = 0
remaining_count = 0

def pause_timer():
    global paused_count, is_paused
    if timer is None or is_paused:
        return
    paused_count = remaining_count
    is_paused = True

    print("Timer paused.(˶ᵔ ᵕ ᵔ˶)")
    status_label.config(text="Paused", fg="orange") 

    pygame.mixer.music.pause()

    if timer is not None:
        window.after_cancel(timer)

def resume_timer():
    global is_paused
    is_paused = False
    pygame.mixer.music.unpause()
    if reps % 2 == 1:
        status_label.config(text="Focusing...", fg="green")
    else:
        status_label.config(text="Break Time! Take a rest!", fg="blue")
    count_down(paused_count)

def give_up():
    global reps, timer, is_paused
    reps = 0
    is_paused = False

    print("User gave up.")
    status_label.config(text="Gave Up...Deducting HP(╥‸╥)", fg="red")
    pygame.mixer.music.stop()
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    timer_text.config(text="00:00")

def count_down(count):
    global remaining_count, reps
    remaining_count = count

    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    timer_text.config(text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        print("Times up!")

        if reps % 2 == 1:
            #--------play alarm sound--------
            try:
                pygame.mixer.music.load("alarm1.mp3")
                pygame.mixer.music.play()
            except:
                print("Audio file not found!")
            status_label.config(text="Timer finished! Gaining HP!(ᵔᴥᵔ)\nBreak starting...", fg="green")
            window.after(3000, start_timer)
        else:
            try:
                pygame.mixer.music.load("alarm1.mp3")
                pygame.mixer.music.play()
            except:
                print("Audio file not found!")
            status_label.config(text="Break finished!", fg="blue")

            def next_focus():
                global reps
                reps = 0
                pygame.mixer.music.stop()
                status_label.config(text="Break over!\nReady to focus again?(˶ᵔ ᵕ ᵔ˶)", fg="blue")
                timer_text.config(text="00:00")

            window.after(2000, next_focus)

#----------switch screen---------
def show_timer():
    start_timer_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

#---------window setup---------
window = tk.Tk()
window.title("Timer")

app_width = 500
app_height = 500

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

#---------font style---------
start_timer_button_font = tkFont.Font(
    family="Consolas",
    size=20,
    weight="bold"
)

button_font = tkFont.Font(
    family="Consolas",
    size=12,
    weight="bold"
)

start_title_font = tkFont.Font(
    family="Courier",
    size=46,
    weight="bold",
    slant="italic"
)

title_font = tkFont.Font(
    family="Courier",
    size=46,
    weight="bold",
)

#---------first screen: start_timer_frame---------
start_timer_frame = tk.Frame(window, width=500, height=500)

start_timer_title = tk.Label(start_timer_frame, text="FocusPaw", font=start_title_font)
start_timer_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

start_timer_button = tk.Button(
    start_timer_frame, 
    text="Start Timer",  
    font=start_timer_button_font, 
    width=15, 
    height=3,
    command=show_timer
)
start_timer_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

start_timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#---------second screen: timer_frame---------
timer_frame = tk.Frame(window, width=500, height=500)

timer_frame.grid_columnconfigure([0, 1, 2], weight=1)
timer_frame.grid_rowconfigure(2, weight=1)

#---------title and status label--------
title_label = tk.Label(
    timer_frame,
    text="Timer",
    font=title_font
)
title_label.grid(column=0, row=0, columnspan=3, pady=(30, 0))

status_label = tk.Label(
    timer_frame,
    text="Are you ready to FOCUS?",
    font=("Consolas", 14)
)
status_label.grid(column=0, row=1, columnspan=3, pady=20)

timer_text = tk.Label(
    timer_frame,
    text="00:00", 
    font=("Consolas", 70, "bold") 
)
timer_text.grid(column=0, row=2, columnspan=3, pady=(5, 40))

#---------buttons---------
btn_start = tk.Button(
    timer_frame,
    text="Start",
    font=button_font,
    width=12,
    command=start_timer
)
btn_start.grid(column=0, row=3, pady=20)

btn_pause = tk.Button(
    timer_frame,
    text="Pause",
    font=button_font,
    width=12,
    command=pause_timer
)
btn_pause.grid(column=1, row=3, pady=20)

btn_give_up = tk.Button(
    timer_frame,
    text="Give up",
    font=button_font,
    width=12,
    command=give_up
)
btn_give_up.grid(column=2, row=3, pady=20)

window.mainloop()

