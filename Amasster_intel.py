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

class IntelWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Amasster Intel")
        self.window.geometry("850x450")
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Amasster Intel", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        boolean_flags_frame = tk.Frame(self.window, bg=BG_COLOR)
        boolean_flags_frame.pack(pady=10)
        tk.Label(boolean_flags_frame, text="Boolean Flags", font=("Helvetica", 16, "bold"), fg=FG_COLOR, bg=BG_COLOR).grid(row=0, columnspan=4, pady=5)

        self.boolean_flags = {
            '-active': tk.BooleanVar(),
            '-demo': tk.BooleanVar(),
            '-ip': tk.BooleanVar(),
            '-ipv4': tk.BooleanVar(),
            '-ipv6': tk.BooleanVar(),
            '-list': tk.BooleanVar(),
            '-v': tk.BooleanVar(),
            '-whois': tk.BooleanVar()
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

        self.intel_flags = {
            '-addr': tk.BooleanVar(),
            '-asn': tk.BooleanVar(),
            '-cidr': tk.BooleanVar(),
            '-df': tk.BooleanVar(),
            '-ef': tk.BooleanVar(),
            '-exclude': tk.BooleanVar(),
            '-if': tk.BooleanVar(),
            '-include': tk.BooleanVar(),
            '-log': tk.BooleanVar(),
            '-o': tk.BooleanVar(),
            '-org': tk.BooleanVar(),
            '-p': tk.BooleanVar(),
            '-r': tk.BooleanVar(),
            '-rf': tk.BooleanVar(),
            '-timeout': tk.BooleanVar()
        }

        self.intel_entries = {flag: tk.Entry(flags_frame, width=20, bg=BG_COLOR, fg=FG_COLOR) for flag in self.intel_flags}

        row = 1
        col = 0
        for flag, var in self.intel_flags.items():
            tk.Checkbutton(flags_frame, text=flag, variable=var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).grid(row=row, column=col, padx=5, pady=2, sticky='w')
            entry = self.intel_entries[flag]
            entry.grid(row=row, column=col + 1, padx=5, pady=2, sticky='w')
            col += 2
            if col == 6:
                col = 0
                row += 1

        button_frame = tk.Frame(self.window, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Run Intel", command=self.run_intel, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Help", command=self.show_help, bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=5)

    def show_help(self):
        help_text = (
            "-active: Enable active recon methods\n"
            "-demo: Censor output to make it suitable for demonstrations\n"
            "-ip: Show the IP addresses for discovered names\n"
            "-ipv4: Show the IPv4 addresses for discovered names\n"
            "-ipv6: Show the IPv6 addresses for discovered names\n"
            "-list: Print the names of all available data sources\n"
            "-v: Output status / debug / troubleshooting info\n"
            "-whois: All discovered domains are run through reverse whois\n"
            "-addr: IPs and ranges (192.168.1.1-254) separated by commas\n"
            "-asn: ASNs separated by commas (can be used multiple times)\n"
            "-cidr: CIDRs separated by commas (can be used multiple times)\n"
            "-df: Path to a file providing root domain names\n"
            "-ef: Path to a file providing data sources to exclude\n"
            "-exclude: Data source names separated by commas to be excluded\n"
            "-if: Path to a file providing data sources to include\n"
            "-include: Data source names separated by commas to be included\n"
            "-log: Path to the log file where errors will be written\n"
            "-o: Path to the text output file\n"
            "-org: Search string provided against AS description information\n"
            "-p: Ports separated by commas (default: 443)\n"
            "-r: IP addresses of preferred DNS resolvers (can be used multiple times)\n"
            "-rf: Path to a file providing preferred DNS resolvers\n"
            "-timeout: Number of minutes to execute the enumeration"
        )
        command_description = (
            "Subcommand: intel\n"
            "Description: Collect open source intelligence for investigation of the target organization\n"
            "The intel subcommand can help you discover additional root domain names associated with the organization you are investigating. The data source sections of the configuration file are utilized by this subcommand in order to obtain passive intelligence, such as reverse whois information."
        )
        ScrollableHelpWindow(self.root, "Intel Help", help_text, command_description)

    def run_intel(self):
        command = ["amass", "intel"]
        for flag, var in self.boolean_flags.items():
            if var.get():
                command.append(flag)
        for flag, var in self.intel_flags.items():
            if var.get():
                value = self.intel_entries[flag].get().strip()
                if value:
                    command.extend([flag, value])
                else:
                    command.append(flag)
        print("Running command:", command)
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print("Output:", result.stdout)
            print("Errors:", result.stderr)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Command failed with exit code {result.returncode}")
            else:
                messagebox.showinfo("Success", "Command executed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run command: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = IntelWindow(root)
    root.mainloop()
