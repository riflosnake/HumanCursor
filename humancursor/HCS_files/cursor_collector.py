import os
import random
import sys
import tkinter as tk
from time import time
from tkinter import ttk, filedialog

import pyautogui


class MouseTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HCS")
        self.coordinates = []

        self.bg = '#3e99de'
        self.root.geometry("340x320")
        self.root.config(bg=self.bg)
        self.root.wm_attributes('-topmost', True)
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Roboto', 11))

        self.label = ttk.Label(self.root, text="Cursor Position", background=self.bg)
        self.label.pack(pady=10)

        self.coordinates_label = ttk.Label(self.root, text="", background=self.bg)
        self.coordinates_label.pack(pady=10)

        self.file_name_label = ttk.Label(self.root, text="File Name (optional)", font=("Roboto", 10), background=self.bg)
        self.file_name_label.pack()

        self.file_name = ttk.Entry(self.root)
        self.file_name.pack(pady=5)

        self.destination_label = ttk.Label(self.root, text="File Destination", font=("Roboto", 10), background=self.bg)
        self.destination_label.pack()

        self.entry_var = tk.StringVar()
        self.destination = ttk.Entry(self.root, textvariable=self.entry_var, width=20)
        self.destination.pack(pady=5)

        self.browse_button = ttk.Button(self.root, text="Browse", command=self.browse_directory, style="TButton", width=6)
        self.browse_button.pack(anchor=tk.S, pady=3)

        self.activate_button = ttk.Button(self.root, text="ON/OFF", command=self.toggle_color, style="TButton")
        self.activate_button.pack(side=tk.LEFT, anchor=tk.S, padx=3, pady=3)

        self.confirm_button = ttk.Button(self.root, text="Finish", command=self.confirm, style="TButton")
        self.confirm_button.pack(side=tk.RIGHT, anchor=tk.S, padx=3, pady=3)

        self.indicator_color = "red"

        self.indicator = tk.Canvas(self.root, width=50, height=100, background='#577b96')
        self.indicator.pack()

        self.indicator.create_rectangle(15, 10, 38, 33, fill=self.indicator_color)

        self.root.bind("<Button-1>", self.remove_focus)
        self.activate_button.bind("<Button-1>", self.remove_focus)

        self.file = None
        self.dest = None

        self.ctrl_pressed = False
        self.press_time = 0.0
        self.index = -1

        self.hold_time_threshold = 0.5

        self.update_coordinates()
        self.root.mainloop()

    def __call__(self):
        return self.coordinates, self.file, self.dest

    def browse_directory(self):
        folder_selected = filedialog.askdirectory()
        self.entry_var.set(folder_selected)

    def draw_indicator(self):
        self.indicator.delete("all")
        self.indicator.create_rectangle(15, 10, 38, 33, fill=self.indicator_color)

    def remove_focus(self, event):
        if event.widget != self.file_name and event.widget != self.destination:
            self.root.focus_force()

    def toggle_color(self):
        # Binding and unbinding of CTRL and Z to capture mouse coordinates
        if self.indicator_color == "red":
            self.root.bind("<KeyPress>", self.on_press_ctrl)
            self.root.bind("<KeyRelease>", self.on_release_ctrl)
            self.root.bind("<z>", self.move)
            self.indicator_color = "green"
        else:
            self.root.unbind("<KeyPress>")
            self.root.unbind("<KeyRelease>")
            self.root.unbind("<z>")
            self.indicator_color = "red"

        self.draw_indicator()

    def confirm(self):
        # Set return values before destroying window
        self.file = self.file_name.get()
        self.dest = self.destination.get()

        if not self.file:
            self.file = f'humancursor_{random.randint(1, 10000)}'

        if self.is_valid_file_location(self.dest):
            self.root.destroy()
        else:
            self.destination_label.config(background='red')

    @staticmethod
    def is_valid_file_location(file_path):
        return os.path.exists(file_path)

    def update_coordinates(self):
        # Update coordinates every 10 milliseconds
        x, y = pyautogui.position()
        self.coordinates_label.config(text=f"x: {x}, y: {y}")
        self.root.after(10, self.update_coordinates)

    def move(self, event):
        x, y = pyautogui.position()
        self.coordinates.append([x, y])
        self.index += 1

    def on_press_ctrl(self, event):
        if event.keysym == "Control_L" and not self.ctrl_pressed:
            self.ctrl_pressed = True
            x, y = pyautogui.position()
            self.press_time = time()
            self.coordinates.append([(x, y)])
            self.index += 1

    def on_release_ctrl(self, event):
        if event.keysym == "Control_L":
            self.ctrl_pressed = False
            x, y = pyautogui.position()
            if time() - self.press_time > self.hold_time_threshold:
                self.coordinates[self.index].append((x, y))
            else:
                self.coordinates[self.index] = self.coordinates[self.index][0]
            self.press_time = 0.0
