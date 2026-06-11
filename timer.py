import tkinter as tk
import math
import pygame
from plyer import notification

pygame.mixer.init()

#---------TIMER FUNCTIONS---------
work_min = 25
break_min = 5
timer = None
reps = 0
is_paused = False
is_running = False        # Tracks if the clock is actively ticking
focus_callback = None     
save_callback = None      # Holds the save function reference

#------------AUDIO SETTINGS------------
focus_music_file = "sunshine.mp3"
break_music_file = "happy_home.mp3"
is_muted = False

def apply_settings(muted, focus_music, break_music):
    global is_muted, focus_music_file, break_music_file
    is_muted = muted
    music_files = {
        "Sunshine": "sunshine.mp3",
        "Happy Home": "happy_home.mp3",
        "Lofi": "lofi.mp3",
        "Dance with Me": "dance_with_me.mp3"
    }
    focus_music_file = music_files.get(focus_music, "sunshine.mp3")
    break_music_file = music_files.get(break_music, "happy_home.mp3")

    if is_muted:
        pygame.mixer.music.pause()
    elif not is_paused:
        pygame.mixer.music.unpause()
        
def start_timer(window, timer_text_label, status_label, callback=None, on_save=None):
    global reps, is_paused, focus_callback, is_running, save_callback
    if callback is not None:
        focus_callback = callback            
    if on_save is not None:
        save_callback = on_save              
        
    if is_paused:
        resume_timer(window, timer_text_label, status_label)
        return
        
    reps += 1
    is_running = True
    pygame.mixer.music.stop()

    if reps % 2 == 0:
        print("Break time! Take a rest!(˶ᵔ ᵕ ᵔ˶)")
        status_label.config(text="Break Time! Take a rest!", fg="blue")

        if not is_muted:
            try:
                pygame.mixer.music.load(break_music_file)
                pygame.mixer.music.play(-1)
            except:
                print("Background music file not found!")
                
        # break_sec = break_min * 60
        break_sec = 5
        count_down(break_sec, window, timer_text_label, status_label)
    else:
        print("Timer started!(˶ˆᗜˆ˵)")
        status_label.config(text="Focusing...", fg="green")

        if not is_muted:
            try:
                pygame.mixer.music.load(focus_music_file)
                pygame.mixer.music.play(-1)
            except:
                print("Background music file not found!")
                
        # work_sec = work_min * 60
        work_sec = 5
        count_down(work_sec, window, timer_text_label, status_label)

paused_count = 0
remaining_count = 0

def pause_timer(window, timer_text_label, status_label):
    global paused_count, is_paused, is_running
    if timer is None or is_paused:
        return
    window.after_cancel(timer)
    paused_count = remaining_count
    is_paused = True
    is_running = False
    print("Timer paused.(˶ᵔ ᵕ ᵔ˶)")
    status_label.config(text="Paused", fg="orange") 

    pygame.mixer.music.pause()

    if timer is not None:
        window.after_cancel(timer)

def resume_timer(window, timer_text_label, status_label):
    global is_paused, is_running
    is_paused = False
    is_running = True
    pygame.mixer.music.unpause()
    if reps % 2 == 1:
        status_label.config(text="Focusing...", fg="green")
    else:
        status_label.config(text="Break Time! Take a rest!", fg="blue")
    count_down(paused_count, window, timer_text_label, status_label)

def give_up(window, timer_text_label, status_label):
    global reps, timer, is_paused, is_running
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    reps = 0
    is_paused = False
    is_running = False
    print("User gave up.")
    status_label.config(text="Gave Up...Deducting HP(╥‸╥)", fg="red")
    pygame.mixer.music.stop()
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    timer_text_label.config(text="00:00")

def count_down(count, window, timer_text_label, status_label):
    global remaining_count, reps, is_running, is_paused, timer, paused_count
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
        timer = window.after(1000, count_down, count-1, window, timer_text_label, status_label)
    else:
        is_running = False
        print("Times up!")

        is_running = False
        is_paused = False
        timer = None
        paused_count = 0

        #focus session complete
        if reps % 2 == 1:
            if focus_callback is not None:
                focus_callback()                
            if save_callback is not None:
                save_callback()                 # Save on complete focus automatically

            notification.notify(
                title = "FocusPaw🐾",
                message = "Focus complete! You earned XP & HP!😁",
                app_name = "FocusPaw",
                timeout = 2
            )

            try:
                pygame.mixer.music.load("alarm1.mp3")
                pygame.mixer.music.play()
            except:
                print("Audio file not found!")
            status_label.config(text="Timer finished! Gaining XP & HP!(ᵔᴥᵔ)\nBreak starting...", fg="green")
            window.after(3000, start_timer, window, timer_text_label, status_label)         #after 3s start break
        #break session complete
        else:

            notification.notify(
                title = "FocusPaw🐾",
                message = "Break finished! Ready to focus?🤓",
                app_name = "FocusPaw",
                timeout = 2
            )

            try:
                pygame.mixer.music.load("alarm1.mp3")
                pygame.mixer.music.play()
            except:
                print("Audio file not found!")
            status_label.config(text="Break finished!", fg="blue")

            def next_focus():
                global reps
                reps = 0      #reset back to start new focus session
                pygame.mixer.music.stop()
                status_label.config(text="Break over!\nReady to focus again?(˶ᵔ ᵕ ᵔ˶)", fg="blue")
                timer_text_label.config(text="00:00")

            window.after(2000, next_focus)    #after 2s change to ready foccus status