import tkinter as tk
import tkinter.font as tkFont
import math
import pygame

pygame.mixer.init()

#---------TIMER FUNCTIONS---------
work_min = 25
break_min = 5
timer = None
reps = 0
is_paused = False

def start_timer(window, timer_text_label, status_label):
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

def pause_timer(window, timer_text_label, status_label):
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

def resume_timer(window, timer_text_label, status_label):
    global is_paused
    is_paused = False
    pygame.mixer.music.unpause()
    if reps % 2 == 1:
        status_label.config(text="Focusing...", fg="green")
    else:
        status_label.config(text="Break Time! Take a rest!", fg="blue")
    count_down(paused_count)

def give_up(window, timer_text_label, status_label):
    global reps, timer, is_paused
    reps = 0
    is_paused = False

    print("User gave up.")
    status_label.config(text="Gave Up...Deducting HP(╥‸╥)", fg="red")
    pygame.mixer.music.stop()
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    timer_text_label.config(text="00:00")

def count_down(count):
    global remaining_count, reps
    remaining_count = count

    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    timer_text_label.config(text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        print("Times up!")

        if reps % 2 == 1:
            #--------PLAY ALARM SOUND--------
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
                timer_text_label.config(text="00:00")

            window.after(2000, next_focus)

#----------SWITCH SCREENS---------
def show_timer():
    start_timer_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

#---------TITLE AND STATUS LABELS---------
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

#---------BUTTONS---------
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

