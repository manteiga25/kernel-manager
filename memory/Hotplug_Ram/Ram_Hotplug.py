import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def memory_hotplug(frame_memory, ram_size, messager):
    def get_hotplug_mem_status():
        try:
            with open("/sys/module/memory_hotplug/parameters/auto_movable_numa_aware", "r") as fd:
                return fd.read().strip()
        except:
            print("ejfv")

    def set_hotplug_mem_status(value):
        try:
            with open("/sys/module/memory_hotplug/parameters/auto_movable_numa_aware", "w") as fd:
                fd.write(hotplug_button.get()) # value
            messager.put("Memory hotplug: Success to set value in hotplug memory state")
        except Exception as e:
            messager.put(f"Memory hotplug: Error to set value in hotplug memory state {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + e, icon="cancel")

    def get_hotplug_map_mem_status():
        try:
            with open("/sys/module/memory_hotplug/parameters/memmap_on_memory", "r") as fd:
                return fd.read().strip()
        except:
            print("ejfv")

    def set_hotplug_map_mem_status(value):
        try:
            with open("/sys/module/memory_hotplug/parameters/memmap_on_memory", "w") as fd:
                fd.write(value)
            messager.put("Memory hotplug: Success to set value in hotplug map memory state")
        except Exception as e:
            messager.put(f"Memory hotplug: Error to set value in hotplug map memory state {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + e, icon="cancel")

    def get_hotplug_ratio_status():
        try:
            with open("/sys/module/memory_hotplug/parameters/ratio", "r") as fd:
                return int(fd.read().strip())
        except:
            print("ejfv")
            return 0

    def set_hotplug_ratio_status():
        ref_max_val = int((ram_size / 1024 / 1024) * 0.2)
        try:
            new_ratio = int(hotplug_ratio_entry.get())
            if new_ratio > ref_max_val:
                raise ValueError
            with open("/sys/module/memory_hotplug/parameters/ratio", "w") as fd:
                fd.write(str(new_ratio))
        except ValueError:
            hotplug_ratio_entry.configure(text=str(get_hotplug_ratio_status()))
            messager.put(f"Memory hotplug: Error {new_ratio} is invalid value")
            CTkMessagebox(title="Valor invalido", message=f"Só é permitido valores inteiros entre 0 e {ref_max_val}.")
        except Exception as e:
            hotplug_ratio_entry.configure(text=str(get_hotplug_ratio_status()))
            messager.put(f"Memory hotplug: Error to set hotplug ratio value to {ref_max_val}, {e}")
            CTkMessagebox(title="Error", message=f"Error to set hotplug ratio memory size.\n{e}", icon="cancel")

    hotplug_ram_frame = LabelFrame(frame_memory, text="Hotplug Ram", background='#212121', foreground="white", labelanchor="n")
    hotplug_ram_frame.grid(row=5, column=1, padx=5, pady=5)
    ctk.CTkLabel(hotplug_ram_frame, text="O Hotplug Ram é um mecanismo que permite mudar os modulos fisicos de RAM mesmo que o sistema esteja em execução.", justify="center", wraplength=400).grid(padx=5, pady=5, row=0, column=0, columnspan=4)
    ctk.CTkLabel(hotplug_ram_frame, text="Hotplug Ram:").grid(row=1, column=0, padx=5, pady=5)
    hotplug_button = ctk.CTkSwitch(hotplug_ram_frame, text="off/on", command=set_hotplug_mem_status, onvalue="Y", offvalue="N")
    if get_hotplug_mem_status() == "Y":
        hotplug_button.select()
    hotplug_button.grid(row=1, column=1, pady=5)
    ctk.CTkLabel(hotplug_ram_frame, text="Memmap on memory:").grid(row=2, column=0, padx=5, pady=5)
    hotplug_map_button = ctk.CTkSwitch(hotplug_ram_frame, text="off/on", command=set_hotplug_map_mem_status, onvalue="Y", offvalue="N")
    if get_hotplug_map_mem_status() == "Y":
        hotplug_map_button.select()
    hotplug_map_button.grid(row=2, column=1, pady=5)

    ratio_init = get_hotplug_ratio_status() * 0.20
    ctk.CTkLabel(hotplug_ram_frame, text="Memory ratio (MB):").grid(row=3, column=0, padx=5, pady=5)
    hotplug_ratio_entry = ctk.CTkEntry(hotplug_ram_frame, placeholder_text=ratio_init)
    hotplug_ratio_entry.grid(row=3, column=1, rowspan=2, pady=5)
    ctk.CTkButton(hotplug_ram_frame, text="save ratio val", command=set_hotplug_ratio_status).grid(row=3, column=3, padx=5)