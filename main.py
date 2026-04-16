import tkinter as tk
import tkinter.font as tKFont

window = tk.Tk()
window.title("FocusPaw")
window.geometry("400x400")

title_font = tKFont.Font(family="Courier", size=24, weight="bold", slant="italic")
button_font = tKFont.Font(family="Arial", size=12, weight="bold")

label = tk.Label (window, text="FocusPaw", font=title_font)
label.pack()

start_button = tk.Button(window, text="Start Timer", font=button_font)
start_button.pack()

window.mainloop()








