import platform
import customtkinter as ctk
from psutil import users
from os import path

class system:

    def rende_system_info(menu):
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
         #   if path.exists(f"/lib/modules/{kernel_version}/vdso/vdso64.so"):
          #      vdso[0] = "Supported"
            return vdso

        kernel_version = platform.uname().release
        vdso_status = check_vdso()
        user = users()
        frame_system = ctk.CTkScrollableFrame(menu, width=880, height=380)
        frame_system.grid(column=0, row=3)
        # operating system + release
        ctk.CTkLabel(frame_system, text="Operating system: " + platform.system() + " " + platform.release()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Version: " + platform.version()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Target: " + platform.machine()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Host user: " + user[0][0]).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Host user: " + platform.node()).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Kernel version: " + kernel_version).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Vdso: " + vdso_status[0]).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Vdso32: " + vdso_status[1]).pack(padx=5, anchor="w")
        ctk.CTkLabel(frame_system, text="Kernel build: " + kernel_build(), wraplength=800, justify="left").pack(padx=5, anchor="w")