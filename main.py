import tkinter as tk
import tkinter.font as tKFont

window = tk.Tk()
window.title("FocusPaw")

app_width = 500
app_height = 500

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

title_font = tKFont.Font(
    family="Courier", 
    size=46, 
    weight="bold", 
    slant="italic"
)
button_font = tKFont.Font(
    family="Consolas", 
    size=25, 
    weight="bold"
)

label = tk.Label (window, text="FocusPaw", font=title_font)
label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

#login frame
login_frame = tk.Frame(window, width=500, height=500)
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#put title in login frame
login_title = tk.Label(login_frame, text="FocusPaw", font=title_font)
login_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

login_button = tk.Button(
    login_frame,
    text="Login/Sign Up",
    font=button_font,
    width=15,
    height=2,
)
login_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()



