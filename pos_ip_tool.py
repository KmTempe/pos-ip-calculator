import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# Define ISP Information
isps = {
    "COSMOTE": {"gateway": "192.168.1.1", "prefix": 24},
    "VODAFONE": {"gateway": "192.168.2.1", "prefix": 24},
    "NOVA": {"gateway": "192.168.1.254", "prefix": 24}
}

# Function to calculate the usable IP range
def calculate_ips():
    isp = isp_var.get()
    advanced = advanced_var.get()
    
    if isp not in isps:
        messagebox.showerror("Error", "Please select a valid ISP")
        return
    
    if not advanced:
        terminal = terminal_var.get()
        if terminal not in ["CLASSIC", "Android_Pax"]:
            messagebox.showerror("Error", "Please select a valid terminal type")
            return
    
    if advanced:
        try:
            start = int(start_entry.get())
            end = int(end_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid start and end values")
            return
        
        if start < 1 or end > 254 or start >= end:
            messagebox.showerror("Error", "Please enter a valid range (1-254) with start < end")
            return
    else:
        if terminal == "CLASSIC":
            start, end = 1, 99
        else:
            start, end = 1, 254
    
    gateway_ip = isps[isp]["gateway"]
    ip_prefix = gateway_ip.rsplit('.', 1)[0] + "."
    
    usable_ips = [f"{ip_prefix}{i}" for i in range(start, end + 1) if f"{ip_prefix}{i}" != gateway_ip]

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "\n".join(usable_ips))

def toggle_advanced_options():
    if advanced_var.get():
        terminal_combobox.config(state='disabled')
        start_label.grid()
        start_entry.grid()
        start_entry.delete(0, tk.END)  # Clear the entry field
        start_entry.insert(0, "1")  # Set default start value
        end_label.grid()
        end_entry.grid()
        end_entry.delete(0, tk.END)  # Clear the entry field
        end_entry.insert(0, "254")  # Set default end value
    else:
        terminal_combobox.config(state='normal')
        start_label.grid_remove()
        start_entry.grid_remove()
        end_label.grid_remove()
        end_entry.grid_remove()

# Function to toggle theme
def toggle_theme():
    current_theme = theme_var.get()
    if current_theme == "Light":
        apply_dark_theme()
        theme_var.set("Dark")
    else:
        apply_light_theme()
        theme_var.set("Light")

def apply_light_theme():
    root.config(bg="white")
    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type == 'Label':
            widget.config(bg="white", fg="black")
        elif widget_type == 'TCombobox':
            widget.config(background="white", foreground="black")
        elif widget_type == 'Checkbutton':
            widget.config(bg="white", fg="black", selectcolor="white")
        elif widget_type == 'Button':
            widget.config(bg="lightgrey", fg="black")
        elif widget_type == 'Entry':
            widget.config(bg="white", fg="black", insertbackground="black")
    result_text.config(bg="white", fg="black", insertbackground="black")

def apply_dark_theme():
    darkgray="#101010"
    offdwhite="#d1d1d1"
    root.config(bg=darkgray)
    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type == 'Label':
            widget.config(bg=offdwhite, fg="black")
        elif widget_type == 'TCombobox':
            widget.config(background="darkgray", foreground=darkgray)
        elif widget_type == 'Checkbutton':
            widget.config(bg=darkgray, fg=offdwhite, selectcolor="black")
        elif widget_type == 'Button':
            widget.config(bg="grey", fg=offdwhite)
        elif widget_type == 'Entry':
            widget.config(bg=darkgray, fg="white", insertbackground=offdwhite)
    result_text.config(bg=darkgray, fg="white", insertbackground=offdwhite)
# Create main window
root = tk.Tk()
root.title("IP Address Suggestion Tool")
root.geometry("400x600")

# Theme toggle button
theme_var = tk.StringVar(value="Light")
theme_button = tk.Button(root, textvariable=theme_var, command=toggle_theme)
theme_button.grid(row=0, column=2, padx=10, pady=5, sticky="ne")

# ISP selection
tk.Label(root, text="Select ISP:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
isp_var = tk.StringVar()
isp_combobox = ttk.Combobox(root, textvariable=isp_var)
isp_combobox['values'] = list(isps.keys())
isp_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Terminal selection
tk.Label(root, text="Select Terminal:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
terminal_var = tk.StringVar()
terminal_combobox = ttk.Combobox(root, textvariable=terminal_var)
terminal_combobox['values'] = ["CLASSIC", "Android_Pax"]
terminal_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Advanced options
advanced_var = tk.BooleanVar()
advanced_checkbox = tk.Checkbutton(root, text="Advanced Options", variable=advanced_var, command=toggle_advanced_options)
advanced_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

# Range input (initially hidden)
start_label = tk.Label(root, text="Start of range:")
start_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
start_entry = tk.Entry(root)
start_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

end_label = tk.Label(root, text="End of range:")
end_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
end_entry = tk.Entry(root)
end_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

toggle_advanced_options()  # Hide advanced options initially

# Button to generate IPs
generate_button = tk.Button(root, text="Generate IPs", command=calculate_ips)
generate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Scrollable text area to display results
result_text = ScrolledText(root, wrap=tk.WORD)
result_text.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Configure grid weights to make the window and text area resizable
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start with light theme
apply_light_theme()

# Start the main loop
root.mainloop()