import tkinter as tk
from tkinter import ttk, filedialog 
import requests
from PIL import Image, ImageTk
import os
import io

current_image = None
themes = {
    "light": {"bg": "#ffffff", "fg": "#000000", "btn_bg": "#e0e0e0"},
    "dark":  {"bg": "#1e1e1e", "fg": "#ffffff", "btn_bg": "#3c3c3c"}
}
current_theme = "light"

def download_image(entry):
    global current_image
    url = entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        current_image = Image.open(io.BytesIO(response.content))
        
        img = current_image.resize((225, 200))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk 

        format_menu.grid(row=5, column=0, pady=5)
        convert_btn.grid(row=6, column=0, pady=5)

    except requests.exceptions.MissingSchema:
        entry.delete(0, tk.END)
        entry.insert(0, "Неверный URL")
    except requests.exceptions.HTTPError as e:
        entry.delete(0, tk.END)
        entry.insert(0, f"HTTP ошибка: {e}")
    except requests.exceptions.ConnectionError:
        entry.delete(0, tk.END)
        entry.insert(0, "Нет соединения")
    except requests.exceptions.Timeout:
        entry.delete(0, tk.END)
        entry.insert(0, "Время ожидания истекло")

def convert_image():
    if current_image is None:
        return
    
    fmt = format_var.get()
    ext = fmt.lower()
    
    save_path = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=[(fmt, f"*.{ext}")],
        initialfile=f"image.{ext}"
    )
    
    if save_path:
        img = current_image.copy()
        if fmt == "JPG":
            img = img.convert("RGB")
        img.save(save_path)

def on_closing():
    if os.path.exists("image.jpg"):
        os.remove("image.jpg")
    root.destroy()

def handle_hotkeys(event):
    if event.keycode == 86:  # V - paste
        entry.event_generate("<<Paste>>")
        return "break"
    elif event.keycode == 67:  # C - copy
        entry.event_generate("<<Copy>>")
        return "break"
    elif event.keycode == 88:  # X - cut
        entry.event_generate("<<Cut>>")
        return "break"
    elif event.keycode == 65:  # A - select all
        entry.select_range(0, tk.END)
        return "break"
    elif event.keycode == 90:  # Z - cancel
        entry.event_generate("<<Undo>>")
        return "break"

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    t = themes[current_theme]
    
    root.config(bg=t["bg"])
    h1.config(bg=t["bg"], fg=t["fg"])
    entry.config(bg=t["btn_bg"], fg=t["fg"], insertbackground=t["fg"])
    Download_button.config(bg="#4CAF50")  # зелёная — не меняем
    convert_btn.config(bg="#2196F3")      # синяя — не меняем
    image_label.config(bg=t["bg"])
    theme_btn.config(bg=t["btn_bg"], fg=t["fg"])

root = tk.Tk()
root.title("Image convertor")
root.geometry("505x450")

h1 = tk.Label(root, text='Enter url to download', font=("Arial", 14))
h1.grid(row=0, column=0)

entry = tk.Entry(root, font=("Arial", 14), width=45)
entry.grid(row=1, column=0, pady=5, padx=2.5)
entry.bind("<Control-KeyPress>", handle_hotkeys)

Download_button = tk.Button(root, text="Download", bg="#4CAF50", fg="white", font=("Arial", 12), command=lambda: download_image(entry))
Download_button.grid(row=2, column=0, pady=5)

theme_btn = tk.Button(root, text="🌙 Тема", font=("Arial", 10), command=toggle_theme)
theme_btn.grid(row=3, column=0, padx=5)

image_label = tk.Label(root)
image_label.grid(row=4, column=0, pady=5)

format_var = tk.StringVar(value="PNG")
format_menu = ttk.Combobox(root, textvariable=format_var, 
                            values=["PNG", "JPG", "WEBP", "BMP", "GIF"], 
                            width=10, state="readonly")

convert_btn = tk.Button(root, text="Конвертировать", bg="#2196F3", fg="white",
                        font=("Arial", 12), command=convert_image)




root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()