import customtkinter as ctk
from tkinter import LabelFrame
from os import path

class battery:

    def get_battery_dinamic_status(self):
        for folder in self.bat_folder_dinamic:
            try:
                with open(f"/sys/class/power_supply/BAT0/{folder}", "r") as fd:
                    self.bat_label_dinamic[folder].configure(text=fd.read().strip())
            except:
                self.bat_label_dinamic[folder].configure(text="Unsupported")
        self.task = self.battery_dinamic_frame.after(1000, self.get_battery_dinamic_status)

    def get_battery_dinamic_info(self):
        self.battery_dinamic_frame = LabelFrame(self.menu, text="Battery status", background='#212121', foreground="white")
        self.battery_dinamic_frame.grid(row=0, column=1, padx=5, pady=5)
        self.bat_folder_dinamic = ["capacity", "charge_now", "status", "current_now", "voltage_now"]
        self.bat_label_dinamic = {}
        for folder, row in zip(self.bat_folder_dinamic, range(5)):
            ctk.CTkLabel(self.battery_dinamic_frame, text=folder.replace("_", " ") + ":").grid(column=0, row=row, padx=5, pady=5)
            self.bat_label_dinamic[folder] = ctk.CTkLabel(self.battery_dinamic_frame)
            self.bat_label_dinamic[folder].grid(column=1, row=row, padx=5, pady=5)
        self.get_battery_dinamic_status()

    def battery_info(self):
        if not path.exists("/sys/class/power_supply/BAT0"):
            return

        def get_battery_static_info():
            bat_folder_static = ["model_name", "manufacturer", "device", "serial_number", "capacity_level", "charge_full", "charge_full_design", "cycle_count", "energy_full", "energy_full_design", "energy_now", "voltage_min_design", "technology"] # ainda por completar
            for folder, row in zip(bat_folder_static, range(13)):
                try:
                    with open(f"/sys/class/power_supply/BAT0/{folder}", "r") as fd:
                        ctk.CTkLabel(battery_static_frame, text=folder.replace("_", " ") + ":").grid(column=0, row=row, padx=5)
                        ctk.CTkLabel(battery_static_frame, text=fd.read().strip()).grid(column=1, row=row, padx=5, pady=5)
                except:
                    print(folder, "unsupported")


        battery_static_frame = LabelFrame(self.menu, text="Battery info", background='#212121', foreground="white")
        battery_static_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=3)
        get_battery_static_info()
        self.get_battery_dinamic_info()
      #  battery_percentage = ctk.CTkLabel(battery_frame, )

    def start_task(self):
        self.get_battery_dinamic_status()
    
    def cancel_task(self):
        self.battery_dinamic_frame.after_cancel(self.task)

    def rende_battery(self, menu):
        self.task = None
        self.menu = menu
        self.battery_info()