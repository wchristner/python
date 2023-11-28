import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import Button, Label, font
from PIL import Image, ImageTk
import ctypes


ctypes.windll.user32.MessageBoxW(0, "Preforming System Cleanup", "Cetera", 64)
def clear_temp_files():
    user_temp_dir = os.environ.get('TEMP')
    if user_temp_dir:
        try:
            print(f"Clearing user temporary files in {user_temp_dir}...")
            shutil.rmtree(user_temp_dir, ignore_errors=True)
            os.makedirs(user_temp_dir, exist_ok=True)
            print("User temporary files cleared successfully.")
        except OSError as e:
            print(f"Error clearing user temporary files: {e}")
    else:
        print("Unable to retrieve the user TEMP environment variable.")

    system_temp_dir = 'C:\\Windows\\Temp'
    try:
        print(f"Clearing system temporary files in {system_temp_dir}...")
        for root, dirs, files in os.walk(system_temp_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                except OSError as e:
                    print(f"Error deleting directory {dir_path}: {e}")
        print("System temporary files cleared successfully.")
    except OSError as e:
        print(f"Error clearing system temporary files: {e}")

def flush_dns_cache():
    try:
        print("Flushing DNS cache...")
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error flushing DNS cache: {e}")

def clear_browser_data(browser_name):
    try:
        print(f"Clearing {browser_name} temporary files...")
        if browser_name.lower() == 'chrome':
            chrome_cache_path = os.path.join(os.environ.get('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
            shutil.rmtree(chrome_cache_path, ignore_errors=True)
        elif browser_name.lower() == 'edge':
            edge_cache_path = os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache')
            shutil.rmtree(edge_cache_path, ignore_errors=True)
        else:
            print(f"Unsupported browser: {browser_name}")
            return

        print(f"{browser_name} temporary files cleared successfully.")
    except OSError as e:
        print(f"Error clearing browser temporary files: {e}")

def gp_update():
    try:
        print("Running Group Policy Update...")
        subprocess.run(["gpupdate", "/force"], check=True)
        print("Group Policy Updated.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating Group Policy: {e}")

def cleanup_button_clicked():
    clear_temp_files()
    flush_dns_cache()
    clear_browser_data('chrome')
    clear_browser_data('edge')
    gp_update()

    print("Cleanup successful. Displaying system cleanup message.")
    ctypes.windll.user32.MessageBoxW(0, "System Cleanup Complete", "Cetera", 48)
    sys.exit()

def run_wmic_task(schedule_id):
    try:
        command = f'WMIC /namespace:\\\\root\\ccm path sms_client CALL TriggerSchedule "{{{schedule_id}}}" /NOINTERACTIVE'
        subprocess.run(command, check=True, shell=True)
        print(f'Successfully triggered WMIC task with schedule ID: {schedule_id}')
    except subprocess.CalledProcessError as e:
        print(f'Error triggering WMIC task with schedule ID: {schedule_id}\nError details: {e}')

def create_gui():
    root = tk.Tk()
    root.title("Cetera Clean Up Utility")
    root.configure(bg="#282c34")  # Set a dark background color

    icon_path = os.path.join("C:/Users/wchristner/Pictures", "ceteraicon.ico")
    root.iconbitmap(default=icon_path)

    image_path = os.path.join("C:/Users/wchristner/Pictures", "Cetera.jpg")
    if os.path.exists(icon_path) and os.path.exists(image_path):
        with Image.open(image_path) as img:
            img = ImageTk.PhotoImage(img)
            image_label = Label(root, image=img, bg="#282c34")  # Set a dark background color
            image_label.pack(side="top", pady=0)
    else:
        print("Image files not found.")

    button_font = font.Font(family='Arial', size=12, weight='normal')
    cleanup_button = Button(root, text="Click To Run Clean Up", command=cleanup_button_clicked, font=button_font,
                            bg="#5B0ABC", fg="white", relief=tk.RAISED)
    cleanup_button.pack(side="top", pady=10)

    # Additional actions to trigger
    additional_actions = [
        "00000000-0000-0000-0000-000000000021",
        "00000000-0000-0000-0000-000000000022",
        "00000000-0000-0000-0000-000000000114",
        "00000000-0000-0000-0000-000000000113"
    ]

    for schedule_id in additional_actions:
        run_wmic_task(schedule_id)

    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred in the GUI: {e}")



if __name__ == "__main__":
    create_gui()