import tkinter as tk
import tkinter.font as tKFont

window = tk.Tk()
window.title("FocusPaw")
window.geometry("500x500")

title_font = tKFont.Font(
    family="Courier", 
    size=46, 
    weight="bold", 
    slant="italic"
)
button_font = tKFont.Font(
    family="Arial", 
    size=25, 
    weight="bold"
)

label = tk.Label (window, text="FocusPaw", font=title_font)
label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

start_button = tk.Button(
    window, 
    text="Start Timer", 
    font=button_font, 
    width=15, 
    height=2
)
start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()








