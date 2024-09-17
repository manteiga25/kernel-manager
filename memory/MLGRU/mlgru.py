import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def rende_mglru(frame_memory, messager : Queue):
    def get_mglru_status():
        try:
            with open("/sys/kernel/mm/lru_gen/enabled", "r") as fd:
                return fd.read().strip()
        except:
            return "-1"
    
    def set_mglru_status():
        nonlocal mglru_status
        value = mglru_widget.get()
        try:
            with open("/sys/kernel/mm/lru_gen/enabled", "w") as fd:
                fd.write(value)
            messager.put(f"Memory LRU: Success to set Multi-Gen LRU status from {mglru_status} to {value}")
            mglru_status = value
        except Exception as e:
            if mglru_status == "1":
                mglru_widget.select()
            messager.put(f"Memory LRU: Error to set Multi-Gen LRU status from {mglru_status} to {value}")
            CTkMessagebox(title="Error", message=f"Error to set mglru status to {value}\n{e}", icon="cancel")

    def get_lru_ttl_status():
        try:
            with open("/sys/kernel/mm/lru_gen/lru_gen_min_ttl_ms", "r") as fd:
                return int(fd.read().strip())
        except:
            return -1
    
    def set_lru_ttl_status(value):
        nonlocal lru_ttl_status
        try:
            if value.isdigit() or int(value) < 0:
                raise ValueError
            with open("/sys/kernel/mm/lru_gen/lru_gen_min_ttl_ms", "w") as fd:
                fd.write(value)
            messager.put(f"Memory LRU: Success to set LRU min ttl from {lru_ttl_status} to {value}")
            lru_ttl_status = value
        except ValueError:
            messager.put(f"Memory LRU: Error {value} is a invalid value for LRU min ttl")
            CTkMessagebox(title="Error", message="Invalid value for min ttl, need positive integer", icon="cancel")
        except Exception as e:
            messager.put(f"Memory LRU: Error to set LRU min ttl from {lru_ttl_status} to {value}, {e}")
            CTkMessagebox(title="Error", message=f"Error to set lru min ttl to {value}\n{e}", icon="cancel")
    
    mglru_status = get_mglru_status()
    if mglru_status == "-1": # fatal error
        return

    lru_frame = LabelFrame(frame_memory, text="Multi-Gen LRU", background='#212121', foreground="white", labelanchor="n")
    lru_frame.grid(column=0, row=6, padx=5, pady=5)

    ctk.CTkLabel(lru_frame, text="Multi-Gen LRU:").grid(column=0, row=0)
    mglru_widget = ctk.CTkSwitch(lru_frame, text="Off/On", command=set_mglru_status)
    if mglru_status == "1":
        mglru_widget.select()
    mglru_widget.grid(column=1, row=0)

    lru_ttl_status = get_lru_ttl_status()
    if lru_ttl_status != -1:
        ctk.CTkLabel(lru_frame, text="LRU gen min ttl:").grid(column=0, row=1)
        lru_min_ttl_widget = ctk.CTkEntry(lru_frame, placeholder_text=lru_ttl_status)
        lru_min_ttl_widget.grid(column=1, row=1)
        ctk.CTkButton(lru_frame, text="Aplicar alteração", command=lambda: set_lru_ttl_status(lru_min_ttl_widget.get())).grid(column=2, row=1)