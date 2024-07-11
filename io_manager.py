import customtkinter as ctk
from os import listdir, path

class io_manager:

    def get_io_devices(self):
        try:
            devices_dr = listdir("/sys/block/")
            devices = [device for device in devices_dr if path.isdir(f"/sys/block/{device}")]
            return devices
        except:
            return "err"

    def io_graf(self):
        devices = self.get_io_devices()
        devices_len = len(devices)
        self.device_frame = list(range(devices_len))
        for device_idx in range(devices_len):
            self.device_frame[device_idx] = ctk.CTkFrame(self.menu, fg_color="blue", corner_radius=15, width=100, height=100)
            self.device_frame[device_idx].grid(row=device_idx // 2, column=device_idx % 2)
            ctk.CTkLabel(self.device_frame[device_idx], text=devices[device_idx]).pack()

    def rende_io(self, menu):
        self.menu = menu
        self.io_graf()