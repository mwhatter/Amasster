# Amasster 

Amasster is a powerful, cross-platform tool designed to streamline the process of collecting open source intelligence, performing DNS enumeration, and managing graph databases for security investigations. With a user-friendly GUI and seamless integration with Amass, Amasster provides a comprehensive solution for cybersecurity professionals.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [One-Liner Installation](#one-liner-installation)
- [Usage](#usage)
  - [Running the GUI](#running-the-gui)
  - [Command Line Interface](#command-line-interface)
- [Scripts Overview](#scripts-overview)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Cross-Platform**: Works on both Windows and Linux.
- **Virtual Environment Management**: Automated setup, activation, and deactivation of a Python virtual environment.
- **GUI Integration**: User-friendly interface to interact with Amass functionalities.
- **Amass Integration**: Leverage the powerful Amass tool for DNS enumeration and intelligence gathering.
- **Graph Database Management**: Manage and visualize graph databases storing enumeration results.

## Requirements

- Python 3.6+
- Internet Connection (for downloading dependencies and Amass)
- Git(manual installation only, setup script will do this for you)

## Installation

### One-Liner Installation

Run the following command in your terminal or command prompt to clone the repository, set up the virtual environment, and install all dependencies:

```sh
curl -fsSL https://github.com/mwhatter/Amasster/raw/main/Amasster_setup.py -o Amasster_setup.py && python Amasster_setup.py
```

### Manual Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/mwhatter/Amasster.git
    cd Amasster
    ```

2. **Set Up the Virtual Environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install Dependencies**:
    ```sh
    pip install --upgrade pip
    pip install pandas tk pyyaml
    ```

5. **Install Amass**:
    - On Windows:
        ```sh
        powershell -Command "Invoke-WebRequest -Uri https://github.com/OWASP/Amass/releases/download/v3.13.3/amass_windows_amd64.zip -OutFile amass_windows_amd64.zip"
        powershell -Command "Expand-Archive -Path amass_windows_amd64.zip -DestinationPath ."
        move amass_windows_amd64\amass.exe %SystemRoot%\System32
        rmdir /s /q amass_windows_amd64
        del amass_windows_amd64.zip
        ```
    - On Linux:
        ```sh
        wget https://github.com/OWASP/Amass/releases/download/v3.13.3/amass_linux_amd64.zip -O amass_linux_amd64.zip
        unzip amass_linux_amd64.zip
        sudo mv amass_linux_amd64/amass /usr/local/bin/
        rm -rf amass_linux_amd64 amass_linux_amd64.zip
        ```

## Usage

### Running the GUI

After the installation, you can launch the Amasster GUI to start using the tool:

```sh
python amass_int.py
```

### Command Line Interface

You can also use the individual scripts directly:

- **Set Up the Virtual Environment**:
    ```sh
    python amass_venv.py setup
    ```

- **Activate the Virtual Environment**:
    ```sh
    python amass_venv.py activate
    ```

- **Deactivate the Virtual Environment**:
    ```sh
    python amass_venv.py deactivate
    ```

## Scripts Overview

- **amass_int.py**: Main GUI script to interact with all functionalities.
- **amass_enum.py**: Perform DNS enumeration and network mapping.
- **amass_intel.py**: Collect open source intelligence.
- **amass_db.py**: Manage and visualize graph databases.
- **amass_config.py**: Configure settings for the tool.
- **amass_venv.py**: Manage the virtual environment setup, activation, and deactivation.
- **setup_amasster.py**: One-liner setup script for the entire project.

## Contributing

We welcome contributions to Amasster! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Test your changes thoroughly.
5. Submit a pull request with a detailed description of your changes.

## License

Amasster is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for using Amasster! If you have any questions, suggestions, or feedback, feel free to open an issue on GitHub.


