import os
import subprocess
import sys
import platform

VENV_DIR = "venv"

def is_running_in_venv():
    return sys.prefix != sys.base_prefix

def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    if platform.system() == 'Windows':
        python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    else:
        python_executable = os.path.join(VENV_DIR, 'bin', 'python')
    print(f"Using Python executable: {python_executable}")
    subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_executable, "-m", "pip", "install", "pandas", "pyyaml", "tk"])

def check_and_activate_venv():
    if not is_running_in_venv():
        setup_virtual_environment()
        if platform.system() == 'Windows':
            python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
        else:
            python_executable = os.path.join(VENV_DIR, 'bin', 'python')
        print(f"Re-running script with virtual environment Python: {python_executable}")
        subprocess.run([python_executable] + sys.argv)
        sys.exit(0)

def call_script(script_name):
    try:
        subprocess.Popen([sys.executable, script_name])
    except subprocess.CalledProcessError as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Failed to run {script_name}: {e}")

check_and_activate_venv()

import tkinter as tk
from tkinter import messagebox

# Color scheme
BG_COLOR = "#001f1f"
FG_COLOR = "#2FFFA3"

# Main GUI class
class AmassGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Amasster")
        self.root.geometry("600x220")
        self.root.configure(bg=BG_COLOR)

        title_frame = tk.Frame(root, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Amasster", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        desc_frame = tk.Frame(root, bg=BG_COLOR)
        desc_frame.pack(pady=10)
        tk.Label(desc_frame, text="Collect open source intelligence for investigation of the target organization.", fg=FG_COLOR, bg=BG_COLOR, wraplength=600).pack()

        btn_frame = tk.Frame(root, bg=BG_COLOR)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Run Intel", command=lambda: call_script("Amasster_intel.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Run Enum", command=lambda: call_script("Amasster_enum.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="Manage DB/Viz/Track", command=lambda: call_script("Amasster_db.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(btn_frame, text="Configuration File", command=lambda: call_script("Amasster_config.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=3, padx=10, pady=5)

        tk.Button(root, text="Cancel", command=self.root.quit, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AmassGUI(root)
    root.mainloop()
