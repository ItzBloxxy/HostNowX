import os
import subprocess
import shutil
import json
import tkinter as tk
from tkinter import messagebox, filedialog

APPDATA = os.getenv("APPDATA")
SERVERS_FOLDER = os.path.join(APPDATA, "MC_Servers")
os.makedirs(SERVERS_FOLDER, exist_ok=True)
CONFIG_FILE = os.path.join(SERVERS_FOLDER, "servers.json")

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        servers = json.load(f)
else:
    servers = {}

def save_servers():
    with open(CONFIG_FILE, "w") as f:
        json.dump(servers, f, indent=4)

def add_server():
    name = name_entry.get()
    if not name or name in servers:
        messagebox.showerror("Error", "Invalid or duplicate server name!")
        return
    
    server_jar = filedialog.askopenfilename(title="Select server.jar", filetypes=[("JAR Files", "*.jar")])
    if not server_jar:
        messagebox.showerror("Error", "No server.jar selected!")
        return
    
    ram = ram_entry.get()
    try:
        ram = int(ram)
        if ram < 512:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid RAM amount!")
        return
    
    server_path = os.path.join(SERVERS_FOLDER, name)
    os.makedirs(server_path, exist_ok=True)
    shutil.copy(server_jar, os.path.join(server_path, "server.jar"))
    
    servers[name] = {"path": server_path, "ram": ram}
    save_servers()
    messagebox.showinfo("Success", f"Server '{name}' added!")
    update_server_list()

def remove_server():
    selected = server_listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showerror("Error", "No server selected!")
        return
    
    shutil.rmtree(servers[selected]["path"], ignore_errors=True)
    del servers[selected]
    save_servers()
    messagebox.showinfo("Success", f"Server '{selected}' removed!")
    update_server_list()

def run_server():
    selected = server_listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showerror("Error", "No server selected!")
        return
    
    server_path = servers[selected]["path"]
    ram = servers[selected]["ram"]
    
    cmd = ["java", "-Xmx{}M".format(ram), "-Xms{}M".format(ram), "-jar", os.path.join(server_path, 'server.jar')]
    
    try:
        process = subprocess.Popen(cmd, cwd=server_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.communicate()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start server: {e}")

def update_server_list():
    server_listbox.delete(0, tk.END)
    for server in servers.keys():
        server_listbox.insert(tk.END, server)

def create_gui():
    global name_entry, ram_entry, server_listbox, root
    root = tk.Tk()
    root.title("Minecraft Server Hoster")
    root.geometry("500x300")
    root.minsize(400, 250)
    
    root.columnconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)
    
    tk.Label(root, text="Server Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=10, pady=5)
    
    tk.Label(root, text="RAM (MB):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    ram_entry = tk.Entry(root)
    ram_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=10, pady=5)
    
    add_button = tk.Button(root, text="Add Server", command=add_server, width=15)
    add_button.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
    
    server_listbox = tk.Listbox(root, height=5)
    server_listbox.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
    update_server_list()
    
    button_frame = tk.Frame(root)
    button_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
    
    remove_button = tk.Button(button_frame, text="Remove Server", command=remove_server, width=10)
    remove_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    run_button = tk.Button(button_frame, text="Run Server", command=run_server, width=10)
    run_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
