import os
import subprocess
import sys

VENV_DIR = "venv"

# Color scheme
BG_COLOR = "#001f1f"
FG_COLOR = "#2FFFA3"

def is_running_in_venv():
    return sys.prefix != sys.base_prefix

def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe' if os.name == 'nt' else 'bin', 'python')
    subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_executable, "-m", "pip", "install", "pandas", "pyyaml"])

def check_and_activate_venv():
    if not is_running_in_venv():
        setup_virtual_environment()
        python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe' if os.name == 'nt' else 'bin', 'python')
        subprocess.run([python_executable] + sys.argv)
        sys.exit(0)

check_and_activate_venv()
import tkinter as tk
from tkinter import messagebox, filedialog

class DBWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Manage DB & Viz")
        self.window.geometry("870x500")
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Manage Database and Visualizations", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        command_frame = tk.Frame(self.window, bg=BG_COLOR)
        command_frame.pack(pady=10)

        self.create_viz_section(command_frame)
        self.create_track_section(command_frame)
        self.create_db_section(command_frame)

        button_frame = tk.Frame(self.window, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Help", command=self.show_help, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)

    def create_viz_section(self, parent_frame):
        viz_frame = tk.LabelFrame(parent_frame, text="viz Subcommand", fg=FG_COLOR, bg=BG_COLOR, font=("Helvetica", 12, "bold"), width=400)
        viz_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        self.viz_checkbuttons = {}
        self.viz_entries = {}

        flags_with_entries = ["-config", "-d", "-df", "-dir", "-enum", "-i"]
        flags_without_entries = ["-d3", "-gexf", "-graphistry", "-maltego", "-visjs"]

        boolean_frame = tk.Frame(viz_frame, bg=BG_COLOR)
        boolean_frame.pack(pady=5)

        for i, flag in enumerate(flags_without_entries):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(boolean_frame, text=flag, variable=var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
            chk.grid(row=i//3, column=i%3, padx=5, pady=2, sticky='w')
            self.viz_checkbuttons[flag] = var

        entry_frame = tk.Frame(viz_frame, bg=BG_COLOR)
        entry_frame.pack(pady=5)

        for i, flag in enumerate(flags_with_entries):
            tk.Label(entry_frame, text=flag, fg=FG_COLOR, bg=BG_COLOR).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            entry = tk.Entry(entry_frame, bg=BG_COLOR, fg=FG_COLOR)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            self.viz_entries[flag] = entry

        tk.Button(viz_frame, text="Run Viz", command=self.run_viz, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

    def create_track_section(self, parent_frame):
        track_frame = tk.LabelFrame(parent_frame, text="track Subcommand", fg=FG_COLOR, bg=BG_COLOR, font=("Helvetica", 12, "bold"), width=400)
        track_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        self.track_checkbuttons = {}
        self.track_entries = {}

        flags_with_entries = ["-config", "-d", "-df", "-dir", "-last", "-since"]
        flags_without_entries = ["-history"]

        boolean_frame = tk.Frame(track_frame, bg=BG_COLOR)
        boolean_frame.pack(pady=5)

        for i, flag in enumerate(flags_without_entries):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(boolean_frame, text=flag, variable=var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
            chk.grid(row=i//3, column=i%3, padx=5, pady=2, sticky='w')
            self.track_checkbuttons[flag] = var

        entry_frame = tk.Frame(track_frame, bg=BG_COLOR)
        entry_frame.pack(pady=5)

        for i, flag in enumerate(flags_with_entries):
            tk.Label(entry_frame, text=flag, fg=FG_COLOR, bg=BG_COLOR).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            entry = tk.Entry(entry_frame, bg=BG_COLOR, fg=FG_COLOR)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            self.track_entries[flag] = entry

        tk.Button(track_frame, text="Run Track", command=self.run_track, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

    def create_db_section(self, parent_frame):
        db_frame = tk.LabelFrame(parent_frame, text="db Subcommand", fg=FG_COLOR, bg=BG_COLOR, font=("Helvetica", 12, "bold"), width=400)
        db_frame.grid(row=0, column=2, padx=10, pady=10, sticky='n')

        self.db_checkbuttons = {}
        self.db_entries = {}

        flags_with_entries = ["-config", "-d", "-df", "-dir", "-enum", "-import", "-show"]
        flags_without_entries = ["-demo", "-ip", "-ipv4", "-ipv6", "-list", "-src"]

        boolean_frame = tk.Frame(db_frame, bg=BG_COLOR)
        boolean_frame.pack(pady=5)

        for i, flag in enumerate(flags_without_entries):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(boolean_frame, text=flag, variable=var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
            chk.grid(row=i//3, column=i%3, padx=5, pady=2, sticky='w')
            self.db_checkbuttons[flag] = var

        entry_frame = tk.Frame(db_frame, bg=BG_COLOR)
        entry_frame.pack(pady=5)

        for i, flag in enumerate(flags_with_entries):
            tk.Label(entry_frame, text=flag, fg=FG_COLOR, bg=BG_COLOR).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            entry = tk.Entry(entry_frame, bg=BG_COLOR, fg=FG_COLOR)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            self.db_entries[flag] = entry

        tk.Button(db_frame, text="Run DB", command=self.run_db, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

    def show_help(self):
        help_text = """
The 'viz' Subcommand:
Create enlightening network graph visualizations that add structure to the information gathered. This subcommand only leverages the 'output_directory' and remote graph database settings from the configuration file.

Flags for outputting the DNS and infrastructure findings as a network graph:
-config  Path to the INI configuration file
-d       Domain names separated by commas (can be used multiple times)
-d3      Output a D3.js v4 force simulation HTML file
-df      Path to a file providing root domain names
-dir     Path to the directory containing the graph database
-enum    Identify an enumeration via an index from the db listing
-gexf    Output to Graph Exchange XML Format (GEXF)
-graphistry  Output Graphistry JSON
-i       Path to the Amass data operations JSON input file
-maltego Output a Maltego Graph Table CSV file
-visjs   Output HTML that employs VisJS

The 'track' Subcommand:
Shows differences between enumerations that included the same target(s) for monitoring a target's attack surface. This subcommand only leverages the 'output_directory' and remote graph database settings from the configuration file.

Flags for performing Internet exposure monitoring across the enumerations in the graph database:
-config  Path to the INI configuration file
-d       Domain names separated by commas (can be used multiple times)
-df      Path to a file providing root domain names
-dir     Path to the directory containing the graph database
-history Show the difference between all enumeration pairs
-last    The number of recent enumerations to include in the tracking
-since   Exclude all enumerations before a specified date (format: 01/02 15:04:05 2006 MST)

The 'db' Subcommand:
Performs viewing and manipulation of the graph database. This subcommand only leverages the 'output_directory' and remote graph database settings from the configuration file.

Flags for interacting with the enumeration findings in the graph database:
-config  Path to the INI configuration file
-d       Domain names separated by commas (can be used multiple times)
-demo    Censor output to make it suitable for demonstrations
-df      Path to a file providing root domain names
-dir     Path to the directory containing the graph database
-enum    Identify an enumeration via an index from the listing
-import  Import an Amass data operations JSON file to the graph database
-ip      Show the IP addresses for discovered names
-ipv4    Show the IPv4 addresses for discovered names
-ipv6    Show the IPv6 addresses for discovered names
-list    Print enumerations in the database and filter on domains specified
-show    Print the results for the enumeration index + domains provided
-src     Print data sources for the discovered names
        """
        ScrollableHelpWindow(self.root, "DB Help", help_text)

    def run_viz(self):
        command = ["amass", "viz"]
        for flag, var in self.viz_checkbuttons.items():
            if var.get():
                command.append(flag)
        for flag, entry in self.viz_entries.items():
            value = entry.get().strip()
            if value:
                command.extend([flag, value])
        self.execute_command(command)

    def run_track(self):
        command = ["amass", "track"]
        for flag, var in self.track_checkbuttons.items():
            if var.get():
                command.append(flag)
        for flag, entry in self.track_entries.items():
            value = entry.get().strip()
            if value:
                command.extend([flag, value])
        self.execute_command(command)

    def run_db(self):
        command = ["amass", "db"]
        for flag, var in self.db_checkbuttons.items():
            if var.get():
                command.append(flag)
        for flag, entry in self.db_entries.items():
            value = entry.get().strip()
            if value:
                command.extend([flag, value])
        self.execute_command(command)

    def execute_command(self, command):
        output = os.popen(" ".join(command)).read()
        messagebox.showinfo("Command Output", output)

class ScrollableHelpWindow:
    def __init__(self, parent, title, help_text):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.configure(bg=BG_COLOR)
        
        frame = tk.Frame(self.window, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(frame, wrap=tk.WORD, bg=BG_COLOR, fg=FG_COLOR)
        self.text_widget.insert(tk.END, help_text)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.window, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = DBWindow(root)
    root.mainloop()
