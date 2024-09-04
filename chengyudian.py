import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import textwrap
import pygame
import time

version = "1.0.38"
release_date = "2024-08-29"

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

file_path = os.path.join(base_dir, 'mnt', 'data', 'dict_idioms_2020_20240627.xls')
sound_path = os.path.join(base_dir, 'mnt', 'data', 'start_sound.wav')
image_path = os.path.join(base_dir, 'mnt', 'data', 'splash_image.png')

user_dir = os.path.expanduser("~")
save_file = os.path.join(user_dir, 'current_index.txt')

pygame.mixer.init()
pygame.mixer.music.load(sound_path)
pygame.mixer.music.play()

splash_root = tk.Tk()
splash_root.overrideredirect(True)
splash_root.title("啟動畫面")

screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()

splash_image_pil = Image.open(image_path)
splash_image = ImageTk.PhotoImage(splash_image_pil)

img_width, img_height = splash_image_pil.size
x = (screen_width // 2) - (img_width // 2)
y = (screen_height // 2) - (img_height // 2)

splash_root.geometry(f"{img_width}x{img_height}+{x}+{y}")

label = tk.Label(splash_root, image=splash_image)
label.pack()

splash_root.update()

while pygame.mixer.music.get_busy():
    splash_root.update()

splash_root.destroy()

df = pd.read_excel(file_path, engine='xlrd')

if os.path.exists(save_file):
    with open(save_file, 'r') as f:
        current_idiom_index = int(f.read().strip())
else:
    current_idiom_index = 0

def wrap_text(text, width=40):
    if isinstance(text, float) and pd.isna(text):
        return "(None)"
    text = str(text).replace('\r\n', '\n').replace('\r', '\n')
    wrapped_lines = []
    for line in text.splitlines():
        wrapped_lines.extend(textwrap.wrap(line, width=width))
    return '\n'.join(wrapped_lines)

def calculate_window_size(text):
    canvas.delete("all")
    lines = text.splitlines()
    max_width = max(canvas.bbox(canvas.create_text(0, 0, text=line, font=("標楷體", 20), anchor="nw"))[2] for line in lines)
    total_height = sum(canvas.bbox(canvas.create_text(0, 0, text=line, font=("標楷體", 20), anchor="nw"))[3] for line in lines)
    return max_width + 40, total_height + 100

def show_idiom(index):
    idiom = df.iloc[index]
    
    idiom_info = (
        f"編號：{index + 1}\n"
        f"成語：{wrap_text(idiom['成語'])}\n"
        f"注音：{wrap_text(idiom.get('注音', '(None)'))}\n"
        f"釋義：{wrap_text(idiom.get('釋義', '(None)'))}\n"
        f"書證：\n{wrap_text(idiom.get('書證', '(None)'))}\n"
        f"近義-同：{wrap_text(idiom.get('近義-同', '(None)'))}\n"
        f"近義-反：{wrap_text(idiom.get('近義-反', '(None)'))}"
    )
    
    new_width, new_height = calculate_window_size(idiom_info)
    root.geometry(f"{new_width}x{new_height}")

    canvas.delete("all")
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    
    canvas.create_text(20, 20, text=idiom_info, font=("標楷體", 20), fill="black", anchor="nw")
    
    update_version_position()

def update_version_position():
    canvas.delete("version_tag")
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    canvas.create_text(canvas_width // 2, canvas_height - 20, 
                      text=f"Version: {version}", font=("Helvetica", 16), fill="black", anchor="s", tags="version_tag")

def prev_idiom():
    global current_idiom_index
    current_idiom_index = max(0, current_idiom_index - 1)
    show_idiom(current_idiom_index)

def next_idiom():
    global current_idiom_index
    current_idiom_index = min(len(df) - 1, current_idiom_index + 1)
    show_idiom(current_idiom_index)

def on_closing():
    with open(save_file, 'w') as f:
        f.write(str(current_idiom_index))
    root.destroy()

def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("關於成語典")

    canvas = tk.Canvas(about_window)
    canvas.pack(fill="both", expand=True)

    width = 600
    height = 400

    frame = tk.Frame(canvas)
    frame.place(relwidth=1, relheight=1)

    logo = tk.PhotoImage(file=os.path.join(base_dir, 'mnt', 'data', 'logo.png'))
    logo_label = tk.Label(frame, image=logo)
    logo_label.grid(row=0, column=0, rowspan=4, padx=20, pady=20, sticky='n')

    title_label = tk.Label(frame, text="成語典 《Dictionary of Chinese Idioms》", font=("Helvetica", 18), justify="left")
    title_label.grid(row=0, column=1, sticky='nw', padx=(0, 10))

    author_label = tk.Label(frame, text="關於作者", font=("Helvetica", 18), justify="left")
    author_label.grid(row=1, column=1, sticky='nw', padx=(0, 10), pady=(10, 0))

    inst_frame = tk.Frame(frame)
    inst_frame.grid(row=2, column=1, sticky='nw', padx=(0, 10), pady=(5, 0))
    inst_label = tk.Label(inst_frame, text="Instagram: ", font=("Helvetica", 18), justify="left")
    inst_label.pack(side=tk.LEFT)
    inst_link = tk.Label(inst_frame, text="@phys.cpp", font=("Helvetica", 18), fg="blue", cursor="hand2")
    inst_link.pack(side=tk.LEFT)
    inst_link.bind("<Button-1>", lambda e: os.system("start https://www.instagram.com/phys.cpp"))

    github_frame = tk.Frame(frame)
    github_frame.grid(row=3, column=1, sticky='nw', padx=(0, 10), pady=(5, 0))
    github_label = tk.Label(github_frame, text="GitHub: ", font=("Helvetica", 18), justify="left")
    github_label.pack(side=tk.LEFT)
    github_link = tk.Label(github_frame, text="@dev-eecs", font=("Helvetica", 18), fg="blue", cursor="hand2")
    github_link.pack(side=tk.LEFT)
    github_link.bind("<Button-1>", lambda e: os.system("start https://github.com/dev-eecs"))
    github_description = tk.Label(github_frame, text=" —— 開放原始碼資料庫", font=("Helvetica", 18), justify="left")
    github_description.pack(side=tk.LEFT)

    version_info = f"版本號: {version}\n發布日期: {release_date}"
    version_label = tk.Label(frame, text=version_info, font=("Helvetica", 18), justify="left")
    version_label.grid(row=4, column=1, sticky='nw', padx=(0, 10), pady=(10, 0))

    logo_label.image = logo

    about_window.update_idletasks()
    new_width = frame.winfo_reqwidth() + 40
    new_height = frame.winfo_reqheight() + 40
    about_window.geometry(f"{new_width}x{new_height}")

root = tk.Tk()
root.title("成語典 《Dictionary of Chinese Idioms》")
root.geometry("600x400+0+0")

bg_image_path = os.path.join(base_dir, 'mnt', 'data', 'bg.jpg')
bg_image_pil = Image.open(bg_image_path)
bg_image_pil = bg_image_pil.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image_pil)

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)

def on_resize(event):
    update_version_position()

root.bind("<Configure>", on_resize)

show_idiom(current_idiom_index)

menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="關於成語典(A)...", command=show_about)
menu_bar.add_cascade(label="說明(H)", menu=help_menu)
root.config(menu=menu_bar)

prev_button = tk.Button(root, text="上一個成語", command=prev_idiom, font=("標楷體", 18))
prev_button.place(relx=0, rely=1, anchor='sw', x=10, y=-10)

next_button = tk.Button(root, text="下一個成語", command=next_idiom, font=("標楷體", 18))
next_button.place(relx=1, rely=1, anchor='se', x=-10, y=-10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
