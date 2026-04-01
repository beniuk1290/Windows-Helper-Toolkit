import os
import platform
import subprocess
import shutil
import tkinter as tk
from tkinter import scrolledtext, messagebox

TEMP_FOLDERS = [
    os.getenv('TEMP'),
    os.path.join(os.getenv('SystemRoot'), 'Temp')
]

# --- Funkcje ---
def list_programs():
    try:
        cmd = 'wmic product get Name'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        programs = result.stdout.strip().split('\n')[1:]
        text_box.delete('1.0', tk.END)
        for p in programs:
            if p.strip():
                text_box.insert(tk.END, f"{p.strip()}\n")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można pobrać listy programów:\n{e}")

def clean_temp():
    count = 0
    for folder in TEMP_FOLDERS:
        if folder and os.path.exists(folder):
            for item in os.listdir(folder):
                path = os.path.join(folder, item)
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.unlink(path)
                        count += 1
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                        count += 1
                except Exception:
                    pass
    messagebox.showinfo("Gotowe", f"Wyczyszczono {count} plików/folderów tymczasowych.")

def system_info():
    info = (
        f"System: {platform.system()} {platform.release()}\n"
        f"Wersja: {platform.version()}\n"
        f"Architektura: {platform.architecture()[0]}\n"
        f"Użytkownik: {os.getlogin()}"
    )
    messagebox.showinfo("Informacje o systemie", info)

# --- GUI ---
root = tk.Tk()
root.title("Windows Helper Toolkit")
root.geometry("600x400")
root.resizable(False, False)

# Przyciski
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Informacje o systemie", width=25, command=system_info).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Pokaż zainstalowane programy", width=25, command=list_programs).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Wyczyść foldery tymczasowe", width=25, command=clean_temp).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Wyjdź", width=25, command=root.quit).grid(row=1, column=1, padx=5, pady=5)

# Pole tekstowe do listy programów
text_box = scrolledtext.ScrolledText(root, width=70, height=15)
text_box.pack(pady=10)

root.mainloop()
