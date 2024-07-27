import os
import subprocess
import sys

VENV_DIR = "venv"

def is_running_in_venv():
    return sys.prefix != sys.base_prefix

def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe' if os.name == 'nt' else 'bin', 'python')
    subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_executable, "-m", "pip", "install", "pandas", "pyyaml", "tk"])

def check_and_activate_venv():
    if not is_running_in_venv():
        setup_virtual_environment()
        python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe' if os.name == 'nt' else 'bin', 'python')
        subprocess.run([python_executable] + sys.argv)
        sys.exit(0)

check_and_activate_venv()

import tkinter as tk
from tkinter import messagebox, scrolledtext

# Color scheme
BG_COLOR = "#001f1f"
FG_COLOR = "#2FFFA3"

class ScrollableHelpWindow:
    def __init__(self, root, title, help_text, command_description):
        self.window = tk.Toplevel(root)
        self.window.title(title)
        self.window.geometry("700x600")
        self.window.configure(bg=BG_COLOR)

        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.insert(tk.END, command_description + '\n\n' + help_text.replace('\n', '\n\n'))
        self.text_area.config(state=tk.DISABLED)

        tk.Button(self.window, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

class EnumWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Amasster Enum")
        self.window.geometry("800x580")
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Amasster Enum", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        boolean_flags_frame = tk.Frame(self.window, bg=BG_COLOR)
        boolean_flags_frame.pack(pady=10)
        tk.Label(boolean_flags_frame, text="Boolean Flags", font=("Helvetica", 16, "bold"), fg=FG_COLOR, bg=BG_COLOR).grid(row=0, columnspan=4, pady=5)

        self.boolean_flags = {
            '-active': tk.BooleanVar(),
            '-brute': tk.BooleanVar(),
            '-demo': tk.BooleanVar(),
            '-include-unresolvable': tk.BooleanVar(),
            '-ip': tk.BooleanVar(),
            '-ipv4': tk.BooleanVar(),
            '-ipv6': tk.BooleanVar(),
            '-list': tk.BooleanVar(),
            '-noalts': tk.BooleanVar(),
            '-norecursive': tk.BooleanVar(),
            '-noresolvrate': tk.BooleanVar(),
            '-noresolvscore': tk.BooleanVar(),
            '-passive': tk.BooleanVar(),
            '-src': tk.BooleanVar()
        }

        row = 1
        col = 0
        for flag, var in self.boolean_flags.items():
            tk.Checkbutton(boolean_flags_frame, text=flag, variable=var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).grid(row=row, column=col, padx=5, pady=2, sticky='w')
            col += 1
            if col == 4:
                col = 0
                row += 1

        flags_frame = tk.Frame(self.window, bg=BG_COLOR)
        flags_frame.pack(pady=10)
        tk.Label(flags_frame, text="Flags with Textboxes", font=("Helvetica", 16, "bold"), fg=FG_COLOR, bg=BG_COLOR).grid(row=0, columnspan=6, pady=5)

        self.enum_flags = {
            '-aw': tk.BooleanVar(),
            '-bl': tk.BooleanVar(),
            '-blf': tk.BooleanVar(),
            '-config': tk.BooleanVar(),
            '-d': tk.BooleanVar(),
            '-df': tk.BooleanVar(),
            '-dir': tk.BooleanVar(),
            '-do': tk.BooleanVar(),
            '-ef': tk.BooleanVar(),
            '-exclude': tk.BooleanVar(),
            '-if': tk.BooleanVar(),
            '-include': tk.BooleanVar(),
            '-json': tk.BooleanVar(),
            '-log': tk.BooleanVar(),
            '-max-dns-queries': tk.BooleanVar(),
            '-min-for-recursive': tk.BooleanVar(),
            '-nf': tk.BooleanVar(),
            '-o': tk.BooleanVar(),
            '-oA': tk.BooleanVar(),
            '-p': tk.BooleanVar(),
            '-r': tk.BooleanVar(),
            '-rf': tk.BooleanVar(),
            '-timeout': tk.BooleanVar(),
            '-w': tk.BooleanVar()
        }

        self.enum_entries = {flag: tk.Entry(flags_frame, width=20, bg=BG_COLOR, fg=FG_COLOR) for flag in self.enum_flags}

        row = 1
        col = 0
        for flag, var in self.enum_flags.items():
            tk.Checkbutton(flags_frame, text=flag, variable=var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).grid(row=row, column=col, padx=5, pady=2, sticky='w')
            entry = self.enum_entries[flag]
            entry.grid(row=row, column=col + 1, padx=5, pady=2, sticky='w')
            col += 2
            if col == 6:
                col = 0
                row += 1

        button_frame = tk.Frame(self.window, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Run Enum", command=self.run_enum, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Help", command=self.show_help, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)

    def show_help(self):
        help_text = (
            "-active: Enable active recon methods\n"
            "-aw: Path to a different wordlist file for alterations\n"
            "-bl: Blacklist of subdomain names that will not be investigated\n"
            "-blf: Path to a file providing blacklisted subdomains\n"
            "-brute: Perform brute force subdomain enumeration\n"
            "-config: Path to the INI configuration file\n"
            "-d: Domain names separated by commas (can be used multiple times)\n"
            "-demo: Censor output to make it suitable for demonstrations\n"
            "-df: Path to a file providing root domain names\n"
            "-dir: Path to the directory containing the graph database\n"
            "-do: Path to data operations output file\n"
            "-ef: Path to a file providing data sources to exclude\n"
            "-exclude: Data source names separated by commas to be excluded\n"
            "-if: Path to a file providing data sources to include\n"
            "-include: Data source names separated by commas to be included\n"
            "-include-unresolvable: Output DNS names that did not resolve\n"
            "-ip: Show the IP addresses for discovered names\n"
            "-ipv4: Show the IPv4 addresses for discovered names\n"
            "-ipv6: Show the IPv6 addresses for discovered names\n"
            "-json: Path to the JSON output file\n"
            "-list: Print the names of all available data sources\n"
            "-log: Path to the log file where errors will be written\n"
            "-max-dns-queries: Maximum number of concurrent DNS queries\n"
            "-min-for-recursive: Subdomain labels seen before recursive brute forcing (Default: 1)\n"
            "-nf: Path to a file providing already known subdomain names (from other tools/sources)\n"
            "-noalts: Disable generation of altered names\n"
            "-norecursive: Turn off recursive brute forcing\n"
            "-noresolvrate: Disable resolver rate monitoring\n"
            "-noresolvscore: Disable resolver reliability scoring\n"
            "-o: Path to the text output file\n"
            "-oA: Path prefix used for naming all output files\n"
            "-passive: A purely passive mode of execution\n"
            "-p: Ports separated by commas (default: 443)\n"
            "-r: IP addresses of preferred DNS resolvers (can be used multiple times)\n"
            "-rf: Path to a file providing preferred DNS resolvers\n"
            "-src: Print data sources for the discovered names\n"
            "-timeout: Number of minutes to execute the enumeration\n"
            "-w: Path to a different wordlist file\n"
        )
        command_description = (
            "Subcommand: enum\n"
            "Description: Perform DNS enumeration and network mapping of systems exposed to the Internet\n"
            "This subcommand will perform DNS enumeration and network mapping while populating the selected graph database. All the settings available in the configuration file are relevant to this subcommand."
        )
        ScrollableHelpWindow(self.root, "Enum Help", help_text, command_description)

    def run_enum(self):
        command = ['amass', 'enum']
        for flag, var in self.boolean_flags.items():
            if var.get():
                command.append(flag)
        for flag, var in self.enum_flags.items():
            if var.get():
                value = self.enum_entries[flag].get().strip()
                if value:
                    command.extend([flag, value])
                else:
                    command.append(flag)

        print("Running command:", ' '.join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = EnumWindow(root)
    root.mainloop()
