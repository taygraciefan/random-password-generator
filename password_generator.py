import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- Password Generator ---
def generate_strong_password(length, use_upper, use_lower, use_digits, use_symbols):
    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("Please select at least one character type!")

    if length < 4:
        raise ValueError("Password length must be at least 4 characters long.")

    password_chars = []
    if use_upper:
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password_chars.append(random.choice(string.digits))
    if use_symbols:
        password_chars.append(random.choice(string.punctuation))

    remaining = [random.choice(char_pool) for _ in range(length - len(password_chars))]
    password_chars += remaining
    random.shuffle(password_chars)
    return ''.join(password_chars)

# --- Generate Multiple Passwords ---
def generate_passwords():
    try:
        count = int(entry_count.get())
        length = int(entry_length.get())
        use_upper = var_upper.get()
        use_lower = var_lower.get()
        use_digits = var_digits.get()
        use_symbols = var_symbols.get()

        passwords = [
            generate_strong_password(length, use_upper, use_lower, use_digits, use_symbols)
            for _ in range(count)
        ]

        # Clear previous output
        for widget in password_frame.winfo_children():
            widget.destroy()

        # Display new passwords with copy buttons
        for i, pw in enumerate(passwords, 1):
            pw_label = ttk.Label(password_frame, text=f"{i}. {pw}", font=("Consolas", 10))
            pw_label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            copy_btn = ttk.Button(password_frame, text="📋 Copy", command=lambda p=pw: copy_to_clipboard(p))
            copy_btn.grid(row=i, column=1, padx=5, pady=2)

        global last_generated
        last_generated = passwords

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# --- Copy Password to Clipboard ---
def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()  # keeps it in clipboard after window closes
    messagebox.showinfo("Copied", f"Password copied to clipboard:\n{password}")

# --- Save to File ---
def save_passwords():
    if not last_generated:
        messagebox.showwarning("Warning", "No passwords to save!")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("passwords.txt", "a", encoding="utf-8") as f:
        f.write(f"\n=== Passwords generated on {timestamp} ===\n")
        for i, pw in enumerate(last_generated, 1):
            f.write(f"{i}. {pw}\n")

    messagebox.showinfo("Saved", f"✅ {len(last_generated)} passwords saved to 'passwords.txt'")

# --- Smooth Dark/Light Transition ---
def fade_color(start, end, step):
    start_rgb = root.winfo_rgb(start)
    end_rgb = root.winfo_rgb(end)
    ratio = step / 20
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
    return f'#{r//256:02x}{g//256:02x}{b//256:02x}'

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    start_color = "#121212" if not dark_mode else "white"
    end_color = "white" if not dark_mode else "#121212"

    def animate(step=0):
        if step > 20:
            return
        color = fade_color(start_color, end_color, step)
        root.config(bg=color)
        password_frame.config(bg=color)
        style.configure("TLabel", background=color, foreground="white" if dark_mode else "black")
        style.configure("TCheckbutton", background=color, foreground="white" if dark_mode else "black")
        style.configure("TButton", background="#333333" if dark_mode else "#E0E0E0", foreground="white" if dark_mode else "black")
        root.after(15, animate, step + 1)

    animate()
    toggle_btn.config(text="☀️ Light Mode" if dark_mode else "🌙 Dark Mode")

# --- GUI Setup ---
root = tk.Tk()
root.title("🔐 Customizable Password Generator")
root.geometry("580x600")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

root.config(bg="white")
dark_mode = False
last_generated = []

# --- Widgets ---
title_label = ttk.Label(root, text="🔐 Random Password Generator", font=("Segoe UI", 16, "bold"))
label_count = ttk.Label(root, text="Number of passwords:")
entry_count = ttk.Entry(root, width=10, justify="center")
label_length = ttk.Label(root, text="Length of each password:")
entry_length = ttk.Entry(root, width=10, justify="center")

# Character type checkboxes
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

frame_options = ttk.LabelFrame(root, text="Include in password:")
ttk.Checkbutton(frame_options, text="Uppercase (A-Z)", variable=var_upper).grid(row=0, column=0, sticky="w", padx=10, pady=3)
ttk.Checkbutton(frame_options, text="Lowercase (a-z)", variable=var_lower).grid(row=1, column=0, sticky="w", padx=10, pady=3)
ttk.Checkbutton(frame_options, text="Digits (0-9)", variable=var_digits).grid(row=0, column=1, sticky="w", padx=10, pady=3)
ttk.Checkbutton(frame_options, text="Symbols (!@#$...)", variable=var_symbols).grid(row=1, column=1, sticky="w", padx=10, pady=3)

# Buttons
generate_btn = ttk.Button(root, text="Generate Passwords", command=generate_passwords)
save_btn = ttk.Button(root, text="Save to File", command=save_passwords)
toggle_btn = ttk.Button(root, text="🌙 Dark Mode", command=toggle_mode)

# Frame for displaying passwords
password_frame = tk.Frame(root, bg="white")

# Layout
title_label.pack(pady=15)
label_count.pack()
entry_count.pack(pady=5)
label_length.pack()
entry_length.pack(pady=5)
frame_options.pack(pady=10)
generate_btn.pack(pady=10)
save_btn.pack(pady=5)
toggle_btn.pack(pady=5)
password_frame.pack(pady=15, fill="x")

root.mainloop()
