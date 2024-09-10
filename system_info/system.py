import platform
import customtkinter as ctk
from tkinter import LabelFrame
from psutil import users
from os import path

class system:

    def get_motherboard_info(self):
        info = {}

        folders = ["board_name", "board_vendor", "board_version", "bios_vendor", "bios_version", "bios_date", "board_asset_tag"]
        keys = ["Board Name", "Board Vendor", "BIOS Vendor", "BIOS Version", "BIOS Date", "Board_asset_tag"]
        bin_folders = ["board_serial", "product_serial", "product_uuid"]
        bin_keys = ["Board serial", "Product serial", "Product uuid"]
        
        for folder, key in zip(folders, keys):
            try:
                with open(f'/sys/class/dmi/id/{folder}', "r") as f:
                    info[key] = f.read().strip()
            except:
                info[key] = "Unknown"

        for folder, key in zip(bin_folders, bin_keys):
            try:
                with open(f'/sys/class/dmi/id/{folder}', "rb") as f:
                    info[key] = f.read().strip().decode("ascii")
                #info[key] = info[key].decode("ascii")
            except:
                info[key] = "Unknown"

        return info

    def rende_placa_mae_info(self):
        info = self.get_motherboard_info()
        frame_mother_board = LabelFrame(self.frame_system, text="Motherboard info", background='#212121', foreground="white")
        frame_mother_board.grid(padx=5, row=0, column=1)
        for key in info.keys():
            ctk.CTkLabel(frame_mother_board, text=key + ": " + info[key]).pack(anchor="w", padx=5)

    def rende_system_info(self, menu):
        def kernel_build():
            try:
                with open("/proc/version", "r") as k:
                    return k.read().strip()
            except:
                return "err"

        def check_vdso():
            vdso = list(range(2))
            vdso[0] = "Supported " if path.exists(f"/lib/modules/{kernel_version}/vdso/vdso64.so") else "Unsupported"
            vdso[1] = "Supported " if path.exists(f"/lib/modules/{kernel_version}/vdso/vdso32.so") else "Unsupported"
            return vdso

        kernel_version = platform.uname().release
        vdso_status = check_vdso()
        user = users()
        self.frame_system = ctk.CTkScrollableFrame(menu, width=880, height=380)
        self.frame_system.grid(column=0, row=3)
        frame_os = LabelFrame(self.frame_system, text="Operating system info", background='#212121', foreground="white")
        frame_os.grid(row=0, column=0, padx=5, pady=5)
        # operating system + release
        ctk.CTkLabel(frame_os, text="Operating system: " + platform.system() + " " + platform.release()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Version: " + platform.version()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Target: " + platform.machine()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Host user: " + user[0][0]).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Host user: " + platform.node()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Kernel version: " + kernel_version).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Vdso: " + vdso_status[0]).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Vdso32: " + vdso_status[1]).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_os, text="Kernel build: " + kernel_build(), wraplength=500, justify="left").pack(padx=5, anchor="w")
        self.rende_placa_mae_info()