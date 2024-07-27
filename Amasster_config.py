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
from tkinter import messagebox, filedialog, scrolledtext
import yaml

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

class ConfigWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Configuration File")
        self.window.geometry("800x600")
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Configuration File Setup", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        self.scrollable_frame = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
        self.scrollable_frame.pack(expand=True, fill=tk.BOTH)

        self.config_entries = {}
        config_options = [
            ("mode", "Determines which mode the enumeration is performed in: default, passive or active"),
            ("output_directory", "The directory that stores the graph database and other output files"),
            ("maximum_dns_queries", "The maximum number of concurrent DNS queries that can be performed"),
            ("resolver", "The IP address of a DNS resolver and used globally by the amass package"),
            ("address", "IP address or range (e.g. a.b.c.10-245) that is in scope"),
            ("asn", "ASN that is in scope"),
            ("cidr", "CIDR (e.g. 192.168.1.0/24) that is in scope"),
            ("port", "Specifies a port to be used when actively pulling TLS certificates or crawling"),
            ("domain", "A root DNS domain name to be added to the enumeration scope"),
            ("subdomain", "A DNS subdomain name to be considered out of scope during the enumeration"),
            ("primary", "When set to true, the graph database is specified as the primary db"),
            ("url", "URL in the form of 'postgres://[username:password@]host[:port]/database-name?sslmode=disable' where Amass will connect to a PostgreSQL database"),
            ("options", "Additional PostgreSQL database options"),
            ("enabled", "When set to true, brute forcing is performed during the enumeration"),
            ("recursive", "When set to true, brute forcing is performed on discovered subdomain names as well"),
            ("minimum_for_recursive", "Number of discoveries made in a subdomain before performing recursive brute forcing"),
            ("wordlist_file", "Path to a custom wordlist file to be used during the brute forcing"),
            ("edit_distance", "Number of times an edit operation will be performed on a name sample during fuzzy label searching"),
            ("flip_words", "When set to true, causes words in DNS names to be exchanged for others in the alteration word list"),
            ("flip_numbers", "When set to true, causes numbers in DNS names to be exchanged for other numbers"),
            ("add_words", "When set to true, causes other words in the alteration word list to be added to resolved DNS names"),
            ("add_numbers", "When set to true, causes numbers to be added and removed from resolved DNS names"),
            ("ttl", "The number of minutes that the responses of all data sources for the target are cached"),
            ("apikey", "The API key to be used when accessing the data source"),
            ("secret", "An additional secret to be used with the API key"),
            ("username", "User for the data source account"),
            ("password", "Valid password for the user identified by the 'username' option"),
            ("data_source", "One of the Amass data sources that is not to be used during the enumeration")
        ]

        for option, description in config_options:
            self.scrollable_frame.insert(tk.END, f"{option}: {description}\n")
            entry = tk.Entry(self.scrollable_frame, width=40, bg=BG_COLOR, fg=FG_COLOR)
            self.scrollable_frame.window_create(tk.END, window=entry)
            self.scrollable_frame.insert(tk.END, "\n\n")
            self.config_entries[option] = entry

        self.scrollable_frame.config(state=tk.DISABLED)

        tk.Button(self.window, text="Save Config", command=self.save_config, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        tk.Button(self.window, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

    def save_config(self):
        config_data = {
            'scope': {
                'domains': [self.config_entries['domain'].get()],
                'ips': [self.config_entries['address'].get()],
                'asns': [self.config_entries['asn'].get()],
                'cidrs': [self.config_entries['cidr'].get()],
                'ports': [self.config_entries['port'].get()],
                'blacklist': [self.config_entries['subdomain'].get()]
            },
            'options': {
                'resolvers': [self.config_entries['resolver'].get()],
                'datasources': self.config_entries['data_source'].get(),
                'wordlist': [self.config_entries['wordlist_file'].get()],
                'database': self.config_entries['url'].get(),
                'bruteforce': {
                    'enabled': self.config_entries['enabled'].get().lower() == 'true',
                    'wordlists': [self.config_entries['wordlist_file'].get()]
                },
                'alterations': {
                    'enabled': self.config_entries['enabled'].get().lower() == 'true',
                    'wordlists': [self.config_entries['wordlist_file'].get()]
                }
            }
        }
        try:
            with open('config.yaml', 'w') as config_file:
                yaml.dump(config_data, config_file)
            messagebox.showinfo("Success", "Configuration saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

if __name__ == "__main__":
    check_and_activate_venv()
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = ConfigWindow(root)
    root.mainloop()
