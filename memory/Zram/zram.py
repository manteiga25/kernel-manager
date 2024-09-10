import customtkinter as ctk
from os import path, uname, system
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def rende_zram(frame_memory, ram_size, messager):

    def switch_zram():
        if zram_button.get():
            system("sudo modprobe zram")
            zram_button.configure(text="Desativar zram")
            zram_status.configure(text="Zram habilitado")
            create_zram()
        else:
            if zram_used:
                zram_used = False
                system("sudo swapoff /dev/zram0")
                system("sudo echo 1 > /sys/block/zram0/reset")
            system("sudo rmmod zram")
            for widget in frame_zram.winfo_children():
                widget.destroy()
            frame_zram.destroy()
            rende_zram()
            #    zram_button.configure(text="Ativar zram")
             #   zram_status.configure(text="Zram desabilitado")

    frame_zram = LabelFrame(frame_memory, text="ZRAM", background='#212121', foreground="white", labelanchor="n")
    frame_zram.grid(row=6, column=1, rowspan=2, padx=5, pady=5)

    zram_status = ctk.CTkLabel(frame_zram, text="Zram desabilitado")
    zram_status.grid(row=0, column=0, padx=5, pady=5)
    zram_init = path.exists("/sys/devices/virtual/block/zram0")
    print(zram_init)
    zram_button = ctk.CTkSwitch(frame_zram, text="Ativar Zram", command=switch_zram)
    zram_used = False
    if zram_init:
        zram_button.select()
        zram_status.configure(text="Zram habilitado.")
        zram_button.configure(text="Desativar zram")
        create_zram()
    zram_button.grid(row=0, column=1)

    def create_zram():
        def get_zram_algorithm():
                try:
                    with open("/sys/block/zram0/comp_algorithm", "r") as fd:
                        return fd.read().strip()
                except:
                    return "err"

        def set_zram_algorithm(value):
            print(zram_used)
            if zram_used:
                system("sudo swapoff /dev/zram0")
                system("sudo echo 1 > /sys/block/zram0/reset")
            system(f"echo {value} > /sys/block/zram0/comp_algorithm")
            if zram_used:
                system(f"swapon --priority {zram_priority.get()} /dev/zram0")

        def change_slide_val(event):
            zram_s.configure(text=str(round(zram_size.get() / 1024 / 1024 / 1024, 1)) + " GB")

        def set_zram_size(prio):
            zram_nsize = zram_size.get()
            print(round(zram_nsize / 1024 / 1024 / 1024, 1), " GB")
            try:
                if zram_used:
                    system("swapoff /dev/zram0")
                    system("mkswap -U clear /dev/zram0")
                    system("sudo echo 1 > /sys/block/zram0/reset")
                with open("/sys/block/zram0/disksize", "w") as f:
                    f.write(str(zram_nsize))
                system("mkswap -U clear /dev/zram0")
                system(f"swapon --priority {prio} /dev/zram0")
            except:
                zram_val = get_zram_size()
                zram_s.configure(text=str(round(zram_val / 1024 / 1024 / 1024, 1)) + " GB")
                zram_size.set(zram_val)
                CTkMessagebox(title="Dispositivo ocupado", message="Não foi possivel aplicar parametro ao dispositivo Zram,\n Zram ocupado", icon="cancel")

        def get_zram_algorithms():
            try:
                with open("/sys/block/zram0/comp_algorithm", "r") as fd:
                    algorithms = fd.read().strip()
                    algorithms = algorithms.replace("[", '')
                    algorithms = algorithms.replace("]", '')
                    algorithms_list = algorithms.split()
                    return algorithms_list
            except:
                return "err"

        def get_zram_algorithm():
            try:
                with open("/sys/block/zram0/comp_algorithm", "r") as fd:
                    algorithms = fd.read().strip()
                    algorithms = algorithms.split()
                    print(algorithms)
                    default_algorithm = [algorithm for algorithm in algorithms if not algorithm.find("[")]
                    print("euihrhtue", default_algorithm)
                    default_algorithm = default_algorithm[0].replace("[", "")
                    default_algorithm = default_algorithm.replace("]", "")
                    return default_algorithm
            except:
                return "err"

        def get_zram_size():
            try:
                with open("/sys/block/zram0/disksize", "r") as f:
                    return int(f.read())
            except:
                print("e")
                return 0

        def get_zram_max_comp():
            try:
                with open("/sys/block/zram0/max_comp_streams", "r") as fd:
                    return fd.read().strip()
            except:
                return "err"
            
        def set_zram_max_comp():
            try:
                with open("/sys/block/zram0/max_comp_streams", "w") as fd:
                    fd.write(zram_max_comp_entry.get())
            except:
                return "err"

        def get_zram_disk_prio():
            zram_prio = 100 # default val
            try:
                with open("/proc/swaps", "r") as fd:
                    for swap_text in fd:
                        if not swap_text.find("Filename"):
                            continue
                        swap_ar = swap_text.split()
                        print(swap_ar)
                        if not swap_ar[0].find("/dev/zram0"):
                            zram_prio = swap_ar[5]
            except:
                pass
            return zram_prio
        
        
        zram_priority = ctk.StringVar(value=get_zram_disk_prio())
        ctk.CTkLabel(frame_zram, text="Tamanho do zram:").grid(row=1, column=0, padx=5, pady=5)
        zram_size = ctk.CTkSlider(frame_zram, from_=0, to=ram_size // 2)
        print(get_zram_size() / 1024 / 1024 / 1024)
        zram_size.set(get_zram_size())
        zram_size.bind('<Button-1>', change_slide_val)
        zram_size.bind("<B1-Motion>", change_slide_val)
        zram_size.grid(row=1, column=1, padx=5, pady=5)
        zram_disp_size = get_zram_size()
        nonlocal zram_used
        zram_used = True if zram_disp_size else False
        zram_s = ctk.CTkLabel(frame_zram, text=str(round(zram_disp_size / 1024 / 1024 / 1024, 1)) + " GB")
        zram_s.grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkLabel(frame_zram, text="Zram disk priority:").grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkEntry(frame_zram, textvariable=zram_priority).grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_zram, text="Zram algorithm:").grid(row=3, column=0, padx=5, pady=5)
        zram_comp_wid = ctk.CTkComboBox(frame_zram, state="readonly", values=get_zram_algorithms(), command=set_zram_algorithm)
        zram_comp_wid.set(get_zram_algorithm())
        zram_comp_wid.grid(row=3, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_zram, text="max comp streams:").grid(row=4, column=0, padx=5, pady=5)
        zram_max_comp_entry = ctk.CTkEntry(frame_zram, placeholder_text=get_zram_max_comp())
        zram_max_comp_entry.grid(row=4, column=1, padx=5, pady=5)
        ctk.CTkButton(frame_zram, text="Aplicar alteração", command=set_zram_max_comp).grid(row=4, column=2, padx=5, pady=5)
        ctk.CTkButton(frame_zram, text="Criar dispositivo Zram", command=lambda: set_zram_size(zram_priority.get())).grid(row=5, column=0, columnspan=3, pady=5, padx=5)