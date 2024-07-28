import os
import subprocess
import sys
import platform
import shutil

REPO_URL = "https://github.com/mwhatter/Amasster.git"
REPO_DIR = "Amasster"
VENV_DIR = "venv"

def run_command(command, shell=False):
    try:
        result = subprocess.run(command, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}\n{e}")
        return None

def is_admin():
    if platform.system() == 'Windows':
        try:
            return subprocess.check_call(['net', 'session'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
        except subprocess.CalledProcessError:
            return False
    else:
        return os.geteuid() == 0

def require_admin_privileges():
    if not is_admin():
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "You must run this script as an administrator or root.")
        sys.exit(1)

def check_and_install_packages(packages, python_executable):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            run_command([python_executable, '-m', 'pip', 'install', package])

def get_latest_amass_version():
    import requests
    response = requests.get("https://api.github.com/repos/OWASP/Amass/releases/latest")
    response.raise_for_status()
    latest_release = response.json()
    return latest_release['tag_name']

def install_git():
    if platform.system() == 'Windows':
        git_url = "https://github.com/git-for-windows/git/releases/download/v2.39.2.windows.1/MinGit-2.39.2-64-bit.zip"
        git_zip = "MinGit-2.39.2-64-bit.zip"
        download_command = ["powershell", "-Command", f"Invoke-WebRequest -Uri {git_url} -OutFile {git_zip}"]
        extract_command = ["powershell", "-Command", f"Expand-Archive -Path {git_zip} -DestinationPath .\\git"]
        add_to_path = ["powershell", "-Command", "[System.Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';' + (Resolve-Path .\\git\\cmd), [System.EnvironmentVariableTarget]::Machine)"]
    else:
        download_command = ["sudo", "apt-get", "install", "-y", "git"]

    run_command(download_command, shell=True)
    if platform.system() == 'Windows':
        run_command(extract_command, shell=True)
        run_command(add_to_path, shell=True)

def install_amass(version):
    if platform.system() == 'Windows':
        amass_url = f"https://github.com/OWASP/Amass/releases/download/{version}/amass_windows_amd64.zip"
        amass_zip = "amass_windows_amd64.zip"
        amass_dir = "amass_windows_amd64"
        download_command = ["powershell", "-Command", f"Invoke-WebRequest -Uri {amass_url} -OutFile {amass_zip}"]
        extract_command = ["powershell", "-Command", f"Expand-Archive -Path {amass_zip} -DestinationPath ."]
        move_command = ["move", os.path.join(amass_dir, "amass.exe"), "%SystemRoot%\\System32"]
        cleanup_command = ["powershell", "-Command", f"Remove-Item -Recurse -Force {amass_dir}; Remove-Item {amass_zip}"]
    else:
        amass_url = f"https://github.com/OWASP/Amass/releases/download/{version}/amass_linux_amd64.zip"
        amass_zip = "amass_linux_amd64.zip"
        amass_dir = "amass_linux_amd64"
        download_command = ["wget", amass_url, "-O", amass_zip]
        extract_command = ["unzip", amass_zip]
        move_command = ["sudo", "mv", os.path.join(amass_dir, "amass"), "/usr/local/bin/"]
        cleanup_command = ["rm", "-rf", amass_dir, amass_zip]

    run_command(download_command, shell=True)
    run_command(extract_command, shell=True)
    run_command(move_command, shell=True)
    run_command(cleanup_command, shell=True)

def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        run_command([sys.executable, '-m', 'venv', VENV_DIR])
    if platform.system() == 'Windows':
        python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    else:
        python_executable = os.path.join(VENV_DIR, 'bin', 'python')
    if not os.path.exists(python_executable):
        print(f"Python executable not found at {python_executable}")
        sys.exit(1)
    run_command([python_executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    return python_executable

def clone_repo():
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR, onerror=on_rm_error)
    run_command(['git', 'clone', REPO_URL])

def on_rm_error(func, path, exc_info):
    import stat
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def ensure_executables():
    if platform.system() != 'Windows':
        run_command(['chmod', '-R', '+x', '.'])

def main():
    # Non-root tasks
    if not shutil.which('git'):
        print("Git not found. Installing Git...")
        require_admin_privileges()
        install_git()

    clone_repo()
    os.chdir(REPO_DIR)

    python_executable = setup_virtual_environment()
    check_and_install_packages(['requests', 'pandas', 'pyyaml', 'tkinter'], python_executable)

    ensure_executables()

    # Root tasks
    if not shutil.which('amass'):
        print("Amass not found. Installing Amass...")
        require_admin_privileges()
        latest_version = get_latest_amass_version()
        install_amass(latest_version)
    else:
        print("Amass is already installed.")

    print("Setup complete. Amasster will activate your virtual environment when it is needed.")

if __name__ == '__main__':
    main()
