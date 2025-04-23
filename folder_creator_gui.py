import os
import tkinter as tk
from tkinter import filedialog, messagebox

# === App Setup ===
root = tk.Tk()
root.title("ChillVibez Folder Creator")
root.geometry("550x600")
root.resizable(False, False)

selected_path = tk.StringVar()

# === Folder Functions ===
def browse_directory():
    path = filedialog.askdirectory(title="Select Folder Location")
    if path:
        selected_path.set(path)

def create_folders():
    base_path = selected_path.get().strip()
    raw_input = entry_folders.get("1.0", "end").strip()

    if not base_path or not os.path.exists(base_path):
        messagebox.showerror("Error", "Please select a valid folder location.")
        return

    if not raw_input:
        messagebox.showwarning("Warning", "Please enter folder names.")
        return

    folders = [f.strip().replace("/", "\\") for f in raw_input.split(",") if f.strip()]
    created, skipped = [], []

    for folder in folders:
        full_path = os.path.join(base_path, folder)
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
                created.append(folder)
            except Exception as e:
                skipped.append(f"{folder} ❌ ({str(e)})")
        else:
            skipped.append(f"{folder} ⚠️ (Already exists)")

    summary = f"Created: {len(created)}\n" + "\n".join(created)
    if skipped:
        summary += f"\n\nSkipped: {len(skipped)}\n" + "\n".join(skipped)

    messagebox.showinfo("Summary", summary)

def clear_all():
    selected_path.set("")
    entry_folders.delete("1.0", "end")
    preview_box.delete("1.0", "end")

def update_preview(event=None):
    preview_box.delete("1.0", "end")
    raw_input = entry_folders.get("1.0", "end").strip()

    if not raw_input:
        return

    folders = [f.strip().replace("/", "\\") for f in raw_input.split(",") if f.strip()]
    for path in folders:
        parts = path.split("\\")
        indent = ""
        for part in parts:
            preview_box.insert("end", f"{indent}{part}\n")
            indent += "   "

# === Layout ===
frame = tk.Frame(root, padx=15, pady=15)
frame.pack(fill="both", expand=True)

# Path selection
tk.Label(frame, text="Folder Destination Path:").pack(anchor="w")
tk.Entry(frame, textvariable=selected_path, width=55, state="readonly").pack(anchor="w", pady=(2, 5))
tk.Button(frame, text="Browse", command=browse_directory).pack(anchor="w", pady=(0, 10))

# Folder input
tk.Label(frame, text="Folder/Subfolders (comma-separated):").pack(anchor="w")
entry_folders = tk.Text(frame, height=5, width=65, wrap="none")
entry_folders.insert("1.0", "Example: Projects/2025, Clients/Photos, ChillVibez/Assets")
entry_folders.pack(pady=(2, 8))
entry_folders.bind("<KeyRelease>", update_preview)

# Folder tree preview
tk.Label(frame, text="Folder Tree Preview:").pack(anchor="w")

preview_frame = tk.Frame(frame)
preview_frame.pack(pady=(2, 10), fill="both", expand=False)

preview_scrollbar = tk.Scrollbar(preview_frame)
preview_scrollbar.pack(side="right", fill="y")

preview_box = tk.Text(
    preview_frame,
    height=14,
    width=65,
    wrap="none",
    yscrollcommand=preview_scrollbar.set
)
preview_box.pack(side="left", fill="both")
preview_scrollbar.config(command=preview_box.yview)

# Buttons
btn_frame = tk.Frame(frame)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Create Folders", command=create_folders, width=20).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear All", command=clear_all, width=20).grid(row=0, column=1, padx=5)

# Tip
tk.Label(frame, text="Tip: Use / or \\ to separate subfolders.").pack(anchor="w", pady=(10, 0))

# Footer credits
footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", pady=5)

tk.Label(
    footer_frame,
    text="2025 © ChillVibez Studios, Developed by Ethan Tyler Bonser"
).pack(side="top")

def open_link(event):
    import webbrowser
    webbrowser.open_new("https://www.linkedin.com/in/ethanbonser/")

link = tk.Label(
    footer_frame,
    text="View Developer on LinkedIn",
    fg="blue",
    cursor="hand2"
)
link.pack(side="top")
link.bind("<Button-1>", open_link)

# === Run Application ===
root.mainloop()
