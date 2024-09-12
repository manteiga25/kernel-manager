import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def memory_hotplug(frame_memory, ram_size, messager : Queue):
    def get_hotplug_mem_status():
        try:
            with open("/sys/module/memory_hotplug/parameters/auto_movable_numa_aware", "r") as fd:
                return fd.read().strip()
        except:
            return "e"

    def set_hotplug_mem_status():
        value = hotplug_button.get()
        nonlocal hotplug_ram_status
        try:
            with open("/sys/module/memory_hotplug/parameters/auto_movable_numa_aware", "w") as fd:
                fd.write(value) # value
            messager.put(f"Memory hotplug: Success to set value in hotplug memory state from {hotplug_ram_status} to {value}")
            hotplug_ram_status = value
        except Exception as e:
            if hotplug_ram_status == "Y":
                hotplug_button.select()
            else:
                hotplug_button.deselect()
            messager.put(f"Memory hotplug: Error to set value in hotplug memory state {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + e, icon="cancel")

    def get_hotplug_map_mem_status():
        try:
            with open("/sys/module/memory_hotplug/parameters/memmap_on_memory", "r") as fd:
                return fd.read().strip()
        except:
            return "e"

    def set_hotplug_map_mem_status():
        value = hotplug_map_button.get()
        nonlocal hotplug_map_status
        try:
            with open("/sys/module/memory_hotplug/parameters/memmap_on_memory", "w") as fd:
                fd.write(value)
            messager.put(f"Memory hotplug: Success to set value in hotplug map memory state from {hotplug_map_status} to {value}")
            hotplug_map_status = value
        except Exception as e:
            if hotplug_map_status == "Y":
                hotplug_map_button.select()
            else:
                hotplug_map_button.deselect()
            messager.put(f"Memory hotplug: Error to set value in hotplug map memory state from {hotplug_map_status} to {value}, {e}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_hotplug_ratio_status():
        try:
            with open("/sys/module/memory_hotplug/parameters/auto_movable_ratio", "r") as fd:
                return int(fd.read().strip())
        except Exception as e:
            CTkMessagebox(title="error", message=f"{e}", icon="cancel")
            return -1

    def set_hotplug_ratio_status():
        nonlocal ratio_init
        new_ratio = hotplug_ratio_entry.get()
        if str(ratio_init) == new_ratio:
            return
        try:
            if not new_ratio.isdigit() or int(new_ratio) > ref_max_val:
                raise ValueError
            with open("/sys/module/memory_hotplug/parameters/auto_movable_ratio", "w") as fd:
                fd.write(str(new_ratio))
            messager.put(f"Memory hotplug: Success to set value in hotplug ratio from {ratio_init} to {new_ratio}")
            ratio_init = new_ratio
        except ValueError:
            messager.put(f"Memory hotplug: Error {new_ratio} is invalid value")
            CTkMessagebox(title="Error", message=f"{new_ratio} is invalid value for hotplug ratio", icon="cancel")
        except Exception as e:
            messager.put(f"Memory hotplug: Error to set hotplug ratio value to {ref_max_val}, {e}")
            CTkMessagebox(title="Error", message=f"Error to set hotplug ratio memory size from {ratio_init} to {new_ratio}.\n{e}", icon="cancel")

    hotplug_ram_frame = LabelFrame(frame_memory, text="Hotplug Ram", background='#212121', foreground="white", labelanchor="n")
    hotplug_ram_frame.grid(row=5, column=1, padx=5, pady=5)
    ctk.CTkLabel(hotplug_ram_frame, text="O Hotplug Ram é um mecanismo que permite mudar os modulos fisicos de RAM mesmo que o sistema esteja em execução.", justify="center", wraplength=400).grid(padx=5, pady=5, row=0, column=0, columnspan=4)
    ctk.CTkLabel(hotplug_ram_frame, text="Hotplug Ram:").grid(row=1, column=0, padx=5, pady=5)
    hotplug_ram_status = get_hotplug_mem_status()
    if hotplug_ram_status != "e":
        hotplug_button = ctk.CTkSwitch(hotplug_ram_frame, text="off/on", command=set_hotplug_mem_status, onvalue="Y", offvalue="N")
        if hotplug_ram_status == "Y":
            hotplug_button.select()
        hotplug_button.grid(row=1, column=1, pady=5)

    hotplug_map_status = get_hotplug_map_mem_status()
    if hotplug_map_status != "e":
        ctk.CTkLabel(hotplug_ram_frame, text="Memmap on memory:").grid(row=2, column=0, padx=5, pady=5)
        hotplug_map_button = ctk.CTkSwitch(hotplug_ram_frame, text="off/on", command=set_hotplug_map_mem_status, onvalue="Y", offvalue="N")
        if hotplug_map_status == "Y":
            hotplug_map_button.select()
        hotplug_map_button.grid(row=2, column=1, pady=5)

    ratio_init = get_hotplug_ratio_status()
    if ratio_init != -1:
        ref_max_val = int(ram_size * 0.20) // 1024 // 1000
        ctk.CTkLabel(hotplug_ram_frame, text="Memory ratio (MB):").grid(row=3, column=0, padx=5, pady=5)
        hotplug_ratio_entry = ctk.CTkEntry(hotplug_ram_frame, placeholder_text=ratio_init)
        hotplug_ratio_entry.grid(row=3, column=1, rowspan=2, pady=5)
        ctk.CTkButton(hotplug_ram_frame, text="save ratio val", command=set_hotplug_ratio_status).grid(row=3, column=3, padx=5)
