import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import Button, Label, PhotoImage, font
from PIL import Image, ImageTk

def clear_temp_files():
    user_temp_dir = os.environ.get('TEMP')
    if user_temp_dir:
        try:
            print(f"Clearing user temporary files in {user_temp_dir}...")
            shutil.rmtree(user_temp_dir, ignore_errors=True)
            os.makedirs(user_temp_dir, exist_ok=True)
            print("User temporary files cleared successfully.")
        except Exception as e:
            print(f"An error occurred while clearing user temporary files: {e}")
    else:
        print("Unable to retrieve the user TEMP environment variable.")

    # Clear system-wide temporary folder (C:\Windows\Temp)
    system_temp_dir = 'C:\\Windows\\Temp'
    try:
        print(f"Clearing system temporary files in {system_temp_dir}...")
        for root, dirs, files in os.walk(system_temp_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f"Error deleting directory {dir_path}: {e}")
        print("System temporary files cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing system temporary files: {e}")

def flush_dns_cache():
    try:
        print("Flushing DNS cache...")
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while flushing DNS cache: {e}")

def clear_browser_data(browser_name):
    try:
        print(f"Clearing {browser_name} temporary files...")
        if browser_name.lower() == 'chrome':
            chrome_cache_path = os.path.join(os.environ.get('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default',
                                             'Cache')
            shutil.rmtree(chrome_cache_path, ignore_errors=True)
        elif browser_name.lower() == 'edge':
            edge_cache_path = os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default',
                                           'Cache')
            shutil.rmtree(edge_cache_path, ignore_errors=True)
        else:
            print(f"Unsupported browser: {browser_name}")
            return

        print(f"{browser_name} temporary files cleared successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

        def flush_dns_cache():
            try:
                print("Flushing DNS cache...")
                subprocess.run(["ipconfig", "/flushdns"], check=True)
                print("DNS cache flushed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while flushing DNS cache: {e}")

def gp_update():
    try:
        print("Running Group Policy Update...")
        subprocess.run(["gpupdate", "/force"], check=True)
        print("Group Policy Updated.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while updating Group Policy.: {e}")

def cleanup_button_clicked():
    clear_temp_files()
    flush_dns_cache()
    clear_browser_data('chrome')
    clear_browser_data('edge')
    gp_update()

    print("Cleanup successful. Exiting program.")
    sys.exit()


def run_wmic_task(schedule_id):
    try:
        # Construct the command to run the WMIC task
        command = f'WMIC /namespace:\\\\root\\ccm path sms_client CALL TriggerSchedule "{{{schedule_id}}}" /NOINTERACTIVE'

        # Run the command
        subprocess.run(command, check=True, shell=True)

        print(f'Successfully triggered WMIC task with schedule ID: {schedule_id}')
    except subprocess.CalledProcessError as e:
        print(f'Error triggering WMIC task with schedule ID: {schedule_id}\nError details: {e}')


if __name__ == "__main__":
    # Replace the schedule IDs with the actual IDs you want to trigger
    schedule_ids_to_trigger = [
        "00000000-0000-0000-0000-000000000021",
        "00000000-0000-0000-0000-000000000022",
        "00000000-0000-0000-0000-000000000114",
        "00000000-0000-0000-0000-000000000113"
    ]

    for schedule_id in schedule_ids_to_trigger:
        run_wmic_task(schedule_id)

def create_gui():
    root = tk.Tk()
    root.title("Centera CleanUP")

    # Add an image in the middle
    image_path = "C:/Users/wchristner/Pictures/Cetera.jpg"  # Replace with the correct image path
    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)
    image_label = Label(root, image=img)
    image_label.pack(side="top", pady=10)

    # Add a button underneath the image
    button_font = ("", 20)
    cleanup_button = Button(root, text="Centera Clean UP", command=cleanup_button_clicked)
    cleanup_button.pack(side="top", pady=10)


    root.mainloop()


if __name__ == "__main__":
    create_gui()
