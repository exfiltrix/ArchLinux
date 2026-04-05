#!/usr/bin/env python3
import socket
import os
import subprocess
import sys

# Лог для отладки
LOG_FILE = os.path.expanduser("~/.cache/layout_notify.log")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

def notify(layout):
    name = layout
    icon = "input-keyboard"
    if "English" in layout:
        name = "EN"
    elif "Russian" in layout:
        name = "RU"

    log(f"Notifying: {name}")
    # Using Pango markup for a nicer look and -i for an icon
    # -r 9999 replaces the previous notification
    markup_text = f"<span font='20' weight='bold' foreground='#ffffff'>{name}</span>"
    subprocess.run(["notify-send", "-a", "Keyboard", "-t", "800", "-r", "9999", "-i", icon, "Keyboard Layout", markup_text])
def main():
    log("Script started")
    signature = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    
    if not signature:
        log("No HYPRLAND_INSTANCE_SIGNATURE found")
        return

    # Пробуем несколько возможных путей к сокету
    paths = [
        f"{runtime_dir}/hypr/{signature}/.socket2.sock",
        f"/tmp/hypr/{signature}/.socket2.sock"
    ]
    
    sock_path = None
    for p in paths:
        if os.path.exists(p):
            sock_path = p
            break
            
    if not sock_path:
        log(f"Socket not found in paths: {paths}")
        return

    log(f"Connecting to {sock_path}")
    
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(sock_path)
            log("Connected successfully")
            while True:
                data = client.recv(1024).decode("utf-8")
                if not data:
                    break
                
                for line in data.split("\n"):
                    if "activelayout>>" in line:
                        log(f"Event: {line}")
                        parts = line.split(">>")
                        if len(parts) > 1:
                            layout_info = parts[1].split(",")
                            if len(layout_info) > 1:
                                notify(layout_info[1].strip())
    except Exception as e:
        log(f"Error: {e}")

if __name__ == "__main__":
    main()
