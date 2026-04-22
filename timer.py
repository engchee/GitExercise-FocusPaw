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
button_font = tkFont.Font(
    family="Monospace",
    size=12,
    weight="bold"
)

title_font = tkFont.Font(
    family="Courier",
    size=46,
    weight="bold"
)

#title and status label
title_label = tk.Label(
    window,
    text="Timer",
    font=title_font
)
title_label.grid(column=1, row=0)

status_label = tk.Label(
    window,
    text="Are you ready to FOCUS?",
    font=("Monospace", 14)
)
status_label.grid(column=1, row=1)

#buttons
btn_start = tk.Button(
    window,
    text="Start",
    font=button_font,
    width=12,
    command=start_timer
)
btn_start.grid(column=0, row=3)

btn_pause = tk.Button(
    window,
    text="Pause",
    font=button_font,
    width=12,
    command=pause_timer
)
btn_pause.grid(column=1, row=3)

btn_give_up = tk.Button(
    window,
    text="Give up",
    font=button_font,
    width=12,
    command=give_up
)
btn_give_up.grid(column=2, row=3)

window.mainloop()
