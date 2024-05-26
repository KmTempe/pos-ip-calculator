<!--
 Copyright (c) 2024 KmTempe
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->
I know that this is a very stupid an unnecessary tool but i made it for a reason. yes the reason is stupid

**IP Address Suggestion Tool**

This simple tool helps users generate a list of usable IP addresses based on their selected Internet Service Provider (ISP) and terminal type.

### How to Use:

1. **Select ISP:** Choose your Internet Service Provider from the dropdown menu. Options include COSMOTE, VODAFONE, and NOVA.

2. **Select Terminal:** Choose your terminal type from the dropdown menu. Options include CLASSIC and Android_Pax.

3. **Generate IPs:** Click this button to generate the list of usable IP addresses based on your selections.

### Running the Application:

To run the IP Address Suggestion Tool:

1. Make sure you have Python 3.12.3 installed on your system. You can download Python from [here](https://www.python.org/downloads/release/python-3123/).

2. Clone or download this repository from GitHub.

3. Open a terminal or command prompt and navigate to the directory where you downloaded the repository. (save your life use VSCODE instead)

4. Run `python -m venv {name} on the root`
   
5. Connect to the venv via `.\{name}\Scripts\Activate.ps1` 
   
6. Let pip do his job `pip install -r requirements.txt`

### Creating an Executable:

To create a standalone executable file:

1. Navigate to the directory containing your Python script (`pos_ip_tool.py`).

2. Run the following command to create the executable: `pyinstaller --onedir -i"icon\posiptool.ico" .\pos_ip_tool.py`

3. PyInstaller will create a `dist` directory with the compiled exe