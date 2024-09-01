from CTkMessagebox import CTkMessagebox
from tkinter import LabelFrame
import customtkinter as ctk
from os import stat
from queue import Queue

def rende_worqueue(frame_cpu_freq, row, messager : Queue):
    def set_cpu_workewe_state(widget):
        value = widget.get()
        try:
            with open("/sys/module/workqueue/parameters/power_efficient", "w") as fd:
                fd.write(value)
            messager.put(f"Info Worqueue: Worqueue state changed to {value}")
        except Exception as e:
            widget.select() if value == "N" else widget.deselect()
            messager.put(f"Error Worqueue: Error to set worqueue state {e}")
            CTkMessagebox(title="Error", message=f"An error ocurred to try to write the value\n{e}", icon="cancel")

    def get_cpu_workewe_state():
        try:
            with open("/sys/module/workqueue/parameters/power_efficient", "r") as fd:
                return fd.read().strip()
        except Exception as e:
            messager.put(f"Error Worqueue: Error to get worqueue state {e}")
            return ""

    def set_cpu_workewe_debug_state(widget):
        value = widget.get()
        try:
            with open("/sys/module/workqueue/parameters/debug_force_rr_cpu", "w") as fd:
                fd.write(value)
            messager.put(f"Info Worqueue: debug changed to {value}")
        except Exception as e:
            widget.select() if value == "N" else widget.deselect()
            messager.put(f"Error Worqueue: Error to set worqueue debug state {e}")
            CTkMessagebox(title="Error", message=f"An error ocurred to try to write the value\n{e}", icon="cancel")

    def get_cpu_workewe_debug_state():
        try:
            with open("/sys/module/workqueue/parameters/debug_force_rr_cpu", "r") as fd:
                return int(fd.read().strip())
        except Exception as e:
            messager.put(f"Error Worqueue: Error to get worqueue debug state {e}")
            print("err")
            return ""

    def get_cpu_workewe_thresh():
        try:
            with open("/sys/module/workqueue/parameters/cpu_intensive_thresh_us", "r") as fd:
                return fd.read().strip()
        except Exception as e:
            messager.put(f"Error Worqueue: Error to get worqueue thresh {e}")
            return "err"

    def set_cpu_workewe_thresh(value):
        try:
            with open("/sys/module/workqueue/parameters/cpu_intensive_thresh_us", "w") as fd:
                fd.write(value)
            messager.put(f"Info Worqueue: thresh changed to {value}")
        except Exception as e:
            messager.put(f"Error Worqueue: Error to set worqueue thresh {e}")
            CTkMessagebox(title="Error", message=f"An error ocurred to try to write the value\n{e}", icon="cancel")
    
    cpu_eficiency = LabelFrame(frame_cpu_freq, text="Power eficiency", background='#212121', foreground="white")
    cpu_eficiency.grid(column=1, row=row, padx=5, pady=5)
    del row
    if stat("/sys/module/workqueue/parameters/power_efficient") == 33188:
        ctk.CTkLabel(cpu_eficiency, text="power efficient:").grid(column=0, row=0, padx=5)
        power_eficiency = ctk.CTkSwitch(cpu_eficiency, text="Off/On", command=lambda: set_cpu_workewe_state(power_eficiency), onvalue="Y", offvalue="N")
        if get_cpu_workewe_state() == "Y":
            power_eficiency.select()
        power_eficiency.grid(column=1, row=0, padx=5, pady=5)
    ctk.CTkLabel(cpu_eficiency, text="Debug worqueue:").grid(column=0, row=1)
    debug_worqueue = ctk.CTkSwitch(cpu_eficiency, text="Off/On", command=lambda: set_cpu_workewe_debug_state(debug_worqueue), onvalue="Y", offvalue="N")
    if get_cpu_workewe_debug_state() == "Y":
        debug_worqueue.select()
    debug_worqueue.grid(column=1, row=1, padx=5, pady=5)
    ctk.CTkLabel(cpu_eficiency, text="cpu intensity thresh:").grid(column=0, row=2, padx=5)
    cpu_intensity_thresh = ctk.CTkEntry(cpu_eficiency, placeholder_text=get_cpu_workewe_thresh())
    cpu_intensity_thresh.grid(column=1, row=2, padx=5, pady=5)
    ctk.CTkButton(cpu_eficiency, text="Aplicar alteração", command=lambda: set_cpu_workewe_thresh(cpu_intensity_thresh.get())).grid(column=2, row=2, padx=5, pady=5)