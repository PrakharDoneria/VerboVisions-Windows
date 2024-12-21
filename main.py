import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import traceback

def is_user_logged_in():
    try:
        with open("user_session.txt", "r") as session_file:
            user = session_file.read().strip()
            if user:
                print("User is logged in.")
                return True
            else:
                print("User is not logged in.")
    except FileNotFoundError:
        print("User session file not found.")
    except Exception as e:
        handle_error(e)
    return False

def handle_error(error):
    print("An error occurred:", error)
    traceback.print_exc()
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"An unexpected error occurred:\n\n{error}\n\nSee console for details.")
    root.destroy()

def main():
    try:
        if is_user_logged_in():
            subprocess.run(["python", "app/main.py"], check=True)
        else:
            subprocess.run(["python", "login.py"], check=True)
    except subprocess.CalledProcessError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    main()
