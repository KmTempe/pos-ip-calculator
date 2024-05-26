import logging
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import json

class PosIpTool(tk.Tk):
    isps = {
        "COSMOTE": {"gateway": "192.168.1.1", "prefix": 24},
        "VODAFONE": {"gateway": "192.168.2.1", "prefix": 24},
        "NOVA": {"gateway": "192.168.1.254", "prefix": 24}
    }

    def __init__(self):
        super().__init__()
        self.title("IP Address Suggestion Tool")
        self.geometry("550x400")
        self.theme_var = tk.StringVar(value="Light")
        
        if self.check_theme_exists("secret"):
            self.theme_var.set("secret")  # (͡° ͜ʖ ͡°)
        else:
            self.theme_var.set("Light") 
        
        self.theme_names = self.get_theme_names()

        self.style = ttk.Style(self)  #

        self.create_widgets()
        self.apply_theme()
        self.toggle_advanced_options()  # Ensure advanced options are hidden initially

    def create_widgets(self):
        self.create_theme_button()
        self.create_isp_selection()
        self.create_terminal_selection()
        self.create_advanced_options()
        self.create_range_input()
        self.create_generate_button()
        self.create_result_text()

    def create_theme_button(self):
        self.theme_button = tk.Button(self, textvariable=self.theme_var, command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=10, pady=5, sticky="ne")

    def get_theme_names(self):
        theme_files = os.listdir("themes/") #just create the directory "themes" bug fixed :)
        theme_names = [os.path.splitext(theme)[0] for theme in theme_files if theme.endswith(".json")]
        return theme_names

    def create_isp_selection(self):
        self.isp_var = tk.StringVar()
        self.isp_combobox = ttk.Combobox(self, textvariable=self.isp_var)
        self.isp_combobox['values'] = list(PosIpTool.isps.keys())
        tk.Label(self, text="Select ISP:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.isp_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    def create_terminal_selection(self):
        self.terminal_var = tk.StringVar()
        self.terminal_combobox = ttk.Combobox(self, textvariable=self.terminal_var)
        self.terminal_combobox['values'] = ["CLASSIC", "Android_Pax"]
        tk.Label(self, text="Select Terminal:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.terminal_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    def create_advanced_options(self):
        self.advanced_var = tk.BooleanVar()
        self.advanced_checkbox = tk.Checkbutton(self, text="Advanced Options", variable=self.advanced_var, command=self.toggle_advanced_options)
        self.advanced_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

    def create_range_input(self):
        self.start_label = tk.Label(self, text="Start of range:")
        self.start_entry = tk.Entry(self)
        self.end_label = tk.Label(self, text="End of range:")
        self.end_entry = tk.Entry(self)

    def create_generate_button(self):
        self.generate_button = tk.Button(self, text="Generate IPs", command=self.calculate_ips)
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=10)

    def create_result_text(self):
        self.result_text = ScrolledText(self, wrap=tk.WORD, state='disabled')
        self.result_text.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def load_theme(self, theme_name):
        theme_file = f"themes/{theme_name}.json"
        if not os.path.exists(theme_file):
            # Create the theme file with default values if it doesn't exist
            default_theme = {
                "name": theme_name,
                "properties": {
                    "bg": "white",
                    "text_color": "black",
                    "bg_color": "lightgrey",
                    "text_bg": "white",
                    "entry_bg": "white",
                    "entry_fg": "black"
            }}
            with open(theme_file, "w") as f:
                json.dump(default_theme, f, indent=4)

        # Load the theme properties from the JSON file
        with open(theme_file, "r") as f:
            theme_config = json.load(f)
        return theme_config["properties"]
    
    def check_theme_exists(self, theme_name):
        return os.path.exists(f"themes/{theme_name}.json")

    def apply_theme(self):
        current_theme = self.theme_var.get()
        theme_config = self.load_theme(current_theme)

        self.config(bg=theme_config["bg"])
        text_color = theme_config["text_color"]
        bg_color = theme_config["bg_color"]
        text_bg = theme_config["text_bg"]
        entry_bg = theme_config["entry_bg"]
        entry_fg = theme_config["entry_fg"]

        for widget in self.winfo_children():
            widget_type = widget.winfo_class()
            if widget_type == 'Label':
                widget.config(bg=self["bg"], fg=text_color)
            elif widget_type == 'TCombobox':
                widget.config(style='TCombobox')
                self.style.configure('TCombobox', fieldbackground=text_bg, background=bg_color, foreground=text_color)
            elif widget_type == 'Checkbutton':
                widget.config(bg=self["bg"], fg=text_color, selectcolor=self["bg"])
            elif widget_type == 'Button':
                widget.config(bg=bg_color, fg=text_color)
            elif widget_type == 'Entry':
                widget.config(bg=entry_bg, fg=entry_fg, insertbackground=text_color)

        self.result_text.config(bg=entry_bg, fg=text_color, insertbackground=text_color)

    def toggle_theme(self):
        available_themes = self.get_theme_names() 
        current_theme = self.theme_var.get()
        
        if current_theme not in available_themes:
            new_theme = available_themes[0]
        else:
            current_index = available_themes.index(current_theme)
            next_index = (current_index + 1) % len(available_themes)
            new_theme = available_themes[next_index]

        self.theme_var.set(new_theme)
        self.apply_theme()
        

    def toggle_advanced_options(self):
        if self.advanced_var.get():
            self._show_advanced_options()
        else:
            self._hide_advanced_options()

    def _show_advanced_options(self):
        self.terminal_combobox.config(state='disabled')
        self.start_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.start_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.end_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.end_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")        

    def _hide_advanced_options(self):
        self.terminal_combobox.config(state='normal')
        self.start_label.grid_remove()
        self.start_entry.grid_remove()
        self.end_label.grid_remove()
        self.end_entry.grid_remove() 

    def _validate_isp(self, isp):
        if isp not in PosIpTool.isps:
            messagebox.showerror("Error", "Please select a valid ISP")
            return False
        return True

    def _validate_terminal(self, terminal):
        if terminal not in ["CLASSIC", "Android_Pax"]:
            messagebox.showerror("Error", "Please select a valid terminal type")
            return False
        return True

    def _get_start_and_end(self):
        start = self.start_entry.get()
        end = self.end_entry.get()

        if not (start.isdigit() and end.isdigit()):
            messagebox.showerror("Error", "Please enter valid start and end values")
            return None, None

        start = int(start)
        end = int(end)

        if not (1 <= start <= 254 and 1 <= end <= 255 and start < end):
            messagebox.showerror("Error", "Please enter a valid range (1-255) with start < end")
            return None, None

        return start, end

    def _get_default_start_and_end(self, terminal):
        if terminal == "CLASSIC":
            return 1, 99
        else:
            return 1, 255

    def calculate_ips(self):
        isp = self.isp_var.get()
        advanced = self.advanced_var.get()

        if not self._validate_isp(isp):
            return

        if not advanced:
            terminal = self.terminal_var.get()
            if not self._validate_terminal(terminal):
                return

        if advanced:
            start, end = self._get_start_and_end()
            if start is None or end is None:
                return
        else:
            start, end = self._get_default_start_and_end(terminal)

        gateway_ip = PosIpTool.isps[isp]["gateway"]
        ip_prefix = gateway_ip.rsplit('.', 1)[0] + "."

        usable_ips = [f"{ip_prefix}{i}" for i in range(start, end + 1) if f"{ip_prefix}{i}" != gateway_ip]

        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)  # Clear previous content

        self.result_text.insert(tk.END, f"The default gateway for {isp} is {gateway_ip}\n")
        self.result_text.insert(tk.END, f"Add the same value {gateway_ip} as DNS1 in the terminal options.\nFor DNS2 use 8.8.8.8 and as network mask use 255.255.255.0\n\n")
        self.result_text.insert(tk.END, "\n".join(usable_ips))  # Insert usable IPs

        self.result_text.config(state='disabled')

if __name__ == "__main__":
    app = PosIpTool()
    app.mainloop()

