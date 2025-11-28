import customtkinter as ctk

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_sidebar_button(parent, text, command, icon=None):
    btn = ctk.CTkButton(parent, text=text, command=command, 
                        fg_color="transparent", text_color=("gray10", "gray90"), 
                        hover_color=("gray70", "gray30"), anchor="w", height=40)
    return btn
