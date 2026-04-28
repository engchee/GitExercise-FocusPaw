import tkinter as tk
import tkinter.font as tkFont

#timer function
def start_timer():
    print("Timer started!(˶ˆᗜˆ˵)")
    status_label.config(text="Focusing...", fg="green")

def pause_timer():
    print("Timer paused.(˶ᵔ ᵕ ᵔ˶)")
    status_label.config(text="Paused", fg="orange")

def give_up():
    print("User gave up. Deducting HP...(╥‸╥)")
    status_label.config(text="Gave Up", fg="red")

#switch screen
def show_timer():
    start_timer_frame.place_forget()
    timer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

#window setup
window = tk.Tk()
window.title("Timer")

app_width = 500
app_height = 500

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

#font style
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

#first screen: start_timer_frame
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

#second screen: timer_frame
timer_frame = tk.Frame(window, width=500, height=500)

timer_frame.grid_columnconfigure([0, 1, 2], weight=1)
timer_frame.grid_rowconfigure(2, weight=1)

#title and status label
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

#buttons
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
