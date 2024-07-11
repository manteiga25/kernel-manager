import cpuinfo as cpui
import psutil
import customtkinter as ctk
import cpufreq
import cpuidle
import system
import os
import event_error
import memory
import io_manager
import battery
from CTkMenuBar import *
from tkinter import LabelFrame

def get_core_microcode(core):
    ret = list(range(2))
    try:
        with open(f"/sys/devices/system/cpu/cpu{core}/microcode/version", "r") as f:
            ret[0] = f.read().strip()
    except:
        ret[0] = "Unknown"

    try:
        with open(f"/sys/devices/system/cpu/cpu{core}/microcode/processor_flags", "r") as f:
            ret[1] = f.read().strip()
    except:
        ret[1] = "Unknown"

    return ret

def get_system_info():
    info = {}

    try:
        with open('/sys/class/dmi/id/board_name', "r") as f:
            info['Board Name'] = f.read().strip()
    except:
        info['Board Name'] = "Unknown"

    try:
        # Ler informações sobre a placa-mãe
        with open('/sys/class/dmi/id/board_vendor', "r") as f:
            info['Board Vendor'] = f.read().strip()
    except:
        info['Board Vendor'] = "Unknown"

    try:
        with open('/sys/class/dmi/id/board_version', "r") as f:
            info['Board Version'] = f.read().strip()
    except:
        info['Board Version'] = "Unknown"
        
        # Ler informações sobre o BIOS
    try:
        with open('/sys/class/dmi/id/bios_vendor', "r") as f:
            info['BIOS Vendor'] = f.read().strip()
    except:
         info['BIOS Vendor'] = "Unknown"
    
    try:
        with open('/sys/class/dmi/id/bios_version', "r") as f:
            info['BIOS Version'] = f.read().strip()
    except:
        info['BIOS Version'] = "Unknown"

    try:
        with open('/sys/class/dmi/id/bios_date', "r") as f:
            info['BIOS Date'] = f.read().strip()
    except:
        info['BIOS Date'] = "Unknown"

    try:
        with open('/sys/class/dmi/id/board_asset_tag', "r") as f:
            info['Board_asset_tag'] = f.read().strip()
    except:
        info['Board_asset_tag'] = "Unknown"

    #    with open('/sys/class

    return info

def get_cpu_endian():
    try:
        with open("/sys/kernel/cpu_byteorder", "r") as endian:
            return endian.read().strip() + " endian"
    except:
        return "err"

def get_cpu_erratas():
    info = {}
    try:
        folders = os.listdir("/sys/devices/system/cpu/vulnerabilities/")
        print(folders)
        for folder in folders:
            with open("/sys/devices/system/cpu/vulnerabilities/" + folder, "r") as errata_fd:
                info[folder] = errata_fd.read().strip()
    except:
        pass
    return info

class janela_prin:

    def cpu_has_ht(self, isa):
        try:
            with open("/sys/devices/system/cpu/smt/active", "r") as ht_fd:
                op = ht_fd.read().strip()
                if not isa.find("ht"): # não tem ht
                    return 0
                elif op == "1": # tem ht e esta habilitado
                    return 1
                else:
                    return 2 # tem mas esta desabilitado
        except:
            pass

    def get_microcode(self):
        with open("/sys/devices/system/cpu/microcode/version", "r") as mc_fd:
            return mc_fd.read().strip()

    def cpu_info(self):
        self.cpu_info = cpui.get_cpu_info()
        self.core_num = str(psutil.cpu_count(logical=False))
        self.thread_num = str(psutil.cpu_count())
        self.hyper_state = self.cpu_has_ht(str(self.cpu_info["flags"]))

    def frame_cpu_info(self):
        def update_cpu_util():
            cpu_avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
            cpu_util = psutil.cpu_percent(interval=None, percpu=True)
        #    print(psutil.getloadavg())
            # print(os.getloadavg())
            cpu_utilization.configure(text="CPU utilization: " + str(int(sum(cpu_util) / self.num_cores)) + "%")
            self.frame_cpu.after(1000, update_cpu_util)
        titulo_cpu_rotulos = ["CPU Name: ", "Vendor: ", "Architecture: "]
        titulo_cpu_rotulos2 = ["Model: ", "Family: ", "Stepping: ", "Bits: ", "Microcode: "]
        titulo_cpu_cache = ["Cache L1i: ", "Cache L1d: ", "Cache L2: "]
        cpu_hash = ["brand_raw", "vendor_id_raw", "arch"]
        global_cache_ref = [self.get_core_l1i_cache, self.get_core_l1d_cache, self.get_core_l2_cache]
        cpu_hash2 = ["model", "family", "stepping", "bits"]
        self.num_cores = int(self.thread_num) if self.hyper_state == 1 else int(self.core_num)
        isa = ""
        for feature in self.cpu_info["flags"]:
            isa += feature + ", "
        hyper_state = self.cpu_has_ht(str(self.cpu_info["flags"]))
        self.frame_cpuinfo_global = ctk.CTkScrollableFrame(self.cpu_info_tab, width=770, height=800)
        self.frame_cpuinfo_global.grid(row=3, column=0)
        self.frame_cpu = LabelFrame(self.frame_cpuinfo_global, width=500, height=500, text="CPU info", background='#212121', foreground="white")
        self.frame_cpu.pack(padx=5, pady=5, anchor="w")
        for info, hash_cpu in zip(titulo_cpu_rotulos, cpu_hash):
            ctk.CTkLabel(self.frame_cpu, text=info + self.cpu_info[hash_cpu]).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu, text="Cores: " + str(psutil.cpu_count(logical=False))).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu, text="Threads: " + str(psutil.cpu_count())).pack(anchor="w", padx=5, pady=5)
        if hyper_state == 0:
            ctk.CTkLabel(self.frame_cpu, text="Hyperthreading: " + "Not supported").pack(anchor="w", padx=5, pady=5)
        elif hyper_state == 1:
            ctk.CTkLabel(self.frame_cpu, text="Hyperthreading: " + "Supported and enabled").pack(anchor="w", padx=5, pady=5)
        else:
            ctk.CTkLabel(self.frame_cpu, text="Hyperthreading: " + "Supported (disabled)").pack(anchor="w", padx=5, pady=5)
        cpu_utilization = ctk.CTkLabel(self.frame_cpu)
        cpu_utilization.pack(anchor="w", padx=5, pady=5)
        update_cpu_util()
        for cache_tit, cache_func in zip(titulo_cpu_cache, global_cache_ref):
            ctk.CTkLabel(self.frame_cpu, text=cache_tit + cache_func() + " X" + str(psutil.cpu_count(logical=False))).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu, text="Cache L3: " + self.get_l3_cache()).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu, text="Cache L4: " + self.get_l4_cache()).pack(anchor="w", padx=5, pady=5)
        for info, hash_cpu in zip(titulo_cpu_rotulos2, cpu_hash2):
            ctk.CTkLabel(self.frame_cpu, text=info + str(self.cpu_info[hash_cpu])).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu, text="CPU endian: " + get_cpu_endian()).pack(anchor="w", padx=5, pady=5)
        cpu_errada_frame = LabelFrame(self.frame_cpu, text="CPU bugs (Errata)", background='#212121', foreground="white")
        cpu_errada_frame.pack(anchor="w", padx=5, pady=5)
        cpu_errata = get_cpu_erratas()
        for errata in cpu_errata.keys():
            ctk.CTkLabel(cpu_errada_frame, text=errata + ": " + cpu_errata[errata], wraplength=400, justify="left").pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu, text="ISA: " + isa, wraplength=750, justify="left").pack(anchor="w", padx=5, pady=5)

    def get_core_l1d_cache(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index0/size", "r") as cache_1d_info:
                return cache_1d_info.read().strip() + "B"
        except:
            return "Unsupported"

    def get_core_l1i_cache(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index1/size", "r") as cache_1i_info:
                return cache_1i_info.read().strip() + "B"
        except:
            return "Unsupported"
    
    def get_core_l2_cache(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index2/size", "r") as cache_2_info:
                return cache_2_info.read().strip() + "B"
        except:
            return "Unsupported"
        
    # L3 is a global cache (I think)
    def get_l3_cache(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index3/size", "r") as cache_3_info:
                return cache_3_info.read().strip() + "B"
        except:
            return "unsupported"
    
    # poucos processadores tem cache L4 
    def get_l4_cache(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index4/size", "r") as cache_4_info:
                return cache_4_info.read().strip() + "B"
        except:
            return "unsupported"
        
    def get_core_l1d_way(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index0/ways_of_associativity", "r") as cache_1d_info:
                return cache_1d_info.read().strip() + " ways"
        except:
            return "Unsupported"

    def get_core_l1i_way(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index1/ways_of_associativity", "r") as cache_1i_info:
                return cache_1i_info.read().strip() + " ways"
        except:
            return "Unsupported"
    
    def get_core_l2_way(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index2/ways_of_associativity", "r") as cache_2_info:
                return cache_2_info.read().strip() + " ways"
        except:
            return "Unsupported"
        
    # L3 is a global cache (I think)
    def get_l3_way(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index3/ways_of_associativity", "r") as cache_3_info:
                return cache_3_info.read().strip() + " ways"
        except:
            return "unsupported"
    
    # poucos processadores tem cache L4 
    def get_l4_way(self):
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cache/index4/ways_of_associativity", "r") as cache_4_info:
                return cache_4_info.read().strip() + " ways"
        except:
            return "unsupported"

    def frame_core_info(self):
        def render_microcode(core):
            microcode = get_core_microcode(core)
            frame_micro_code = LabelFrame(frame_core, text="Microcode", background='#212121', foreground="white")
            frame_micro_code.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
            ctk.CTkLabel(frame_micro_code, text="microcode version: " + microcode[0]).grid()
            ctk.CTkLabel(frame_micro_code, text="microcode flags: " + microcode[1]).grid()

        def rende_cache_way():
            func_ref_way = [self.get_core_l1i_way, self.get_core_l1d_way, self.get_core_l2_way, self.get_l3_way, self.get_l4_way]
            cache_rotulo_way = ["Cache L1i (instruction) ways: ", "Cache L1d (Data) ways: ", "Cache L2 ways: ", "Cache L3 ways (Global): ", "Cache L4 ways (Global): "]
            frame_cache_way = LabelFrame(frame_cache, text="Cache ways", background='#212121', foreground="white")
            frame_cache_way.grid(row=0, column=1, padx=5, pady=5)
            for func, tit in zip(func_ref_way, cache_rotulo_way):
                ctk.CTkLabel(frame_cache_way, text=tit + str(func())).pack()

        func_ref = [self.get_core_l1i_cache, self.get_core_l1d_cache, self.get_core_l2_cache, self.get_l3_cache, self.get_l4_cache]
        cache_rotulo = ["Cache L1i (instruction) size: ", "Cache L1d (Data) size: ", "Cache L2 size: ", "Cache L3 size (Global): ", "Cache L4 size (Global): "]
        frame_core_global = ctk.CTkFrame(self.frame_cpuinfo_global, width=800)
        print(frame_core_global.cget("fg_color"))
        frame_core_global.pack(anchor="w")
        for cache_info in range(self.num_cores):
            frame_core = LabelFrame(frame_core_global, width=800, text="core " + str(cache_info), background='#212121', foreground="white")
            frame_core.grid(row=cache_info // 3, column=cache_info % 3, padx=5, pady=5)
            render_microcode(cache_info)
            frame_cache = LabelFrame(frame_core, text="Cache system", background='#212121', foreground="white", labelanchor="n")
            frame_cache.grid(row=1, column=0, padx=5, pady=5)
            frame_cache_size = LabelFrame(frame_cache, text="Cache size", background='#212121', foreground="white")
            frame_cache_size.grid(row=0, column=0, padx=5, pady=5)
            for func, tit in zip(func_ref, cache_rotulo):
                ctk.CTkLabel(frame_cache_size, text=tit + str(func())).pack()
            rende_cache_way()


    def rende_placa_mae_info(self):
        info = get_system_info()
        frame_mother_board = LabelFrame(self.frame_cpuinfo_global, text="Motherboard info", background='#212121', foreground="white")
        frame_mother_board.pack(padx=5, pady=5, anchor="w")
        for key in info.keys():
            ctk.CTkLabel(frame_mother_board, text=key + ": " + info[key]).pack(anchor="w", padx=5)


    def rende_cpu_info(self):
         self.frame_cpu_info()
         self.rende_placa_mae_info()
         self.frame_core_info()

    def __init__(self) -> None:
         self.janela : ctk.CTk = ctk.CTk() # nome tempoprario
         self.janela.title("Kernel manager")
         self.frame_atual = "CPU info"
         self.inicialize_objects()
         self.init_title_menu()
         self.cpu_info()
         self.init_menu()
         self.rende_cpu_info()
         self.janela.mainloop()

    def inicialize_objects(self):
        self.error = event_error.io_error()
        self.system_module = system.system
        self.cpufreq_module = cpufreq.cpu_freq()
        self.cpuidle_module = cpuidle.cpu_idle()
        self.memory_module = memory.memory()
        self.io_module = io_manager.io_manager()
        self.battery_module = battery.battery()

    def ver_registo(self):
        conteudo = self.error.le_registro()
        janela_reg = ctk.CTkToplevel(self.janela)
        janela_reg.title("errors")
        frame = ctk.CTkFrame(janela_reg)
        frame.pack(fill="both", expand=True)
        self.textbox = ctk.CTkTextbox(frame, wrap="word", width=600, height=200)
        self.textbox.insert("0.0", conteudo)
        self.textbox.configure(state="disabled")
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

    def init_title_menu(self):
        title_menu = CTkMenuBar(self.janela)
        menu_file = title_menu.add_cascade("File")
        dropdown1 = CustomDropdownMenu(widget=menu_file)
        dropdown1.add_option(option="Open", command=self.ver_registo)
        dropdown1.add_separator()

    def init_menu(self):
        self.menu = ctk.CTkTabview(master=self.janela, command=self.mudar_pagina)
        self.menu.pack(padx=5)
        self.cpu_info_tab = self.menu.add("CPU info")  # add tab at the end
        self.cpu_system_tab = self.menu.add("System info")  # add tab at the end
        self.cpu_freq_tab = self.menu.add("CPU frequency")  # add tab at the end
        self.cpu_idle_tab = self.menu.add("CPU idle")  # add tab at the end
        self.cpu_menu_tab = self.menu.add("Memory")  # add tab at the end
        self.io_menu_tab = self.menu.add("I/O")  # add tab at the end
        self.battery_menu_tab = self.menu.add("Battery")  # add tab at the end

    def mudar_pagina(self):
        novo_frame = self.menu.get()
        if novo_frame == self.frame_atual:
            return
        print(self.frame_atual)
        for widget in self.menu._tab_dict[self.frame_atual].winfo_children():
            widget.destroy()
        self.frame_atual = novo_frame

        match novo_frame:
            case "CPU info":
                self.rende_cpu_info()
            case "System info":
                self.system_module.rende_system_info(self.cpu_system_tab)
            case "CPU frequency":
              #  self.rende_cpu_freq()
                self.cpufreq_module.rende_cpu_freq(menu=self.cpu_freq_tab, num_cores=self.thread_num)
            case "CPU idle":
                self.cpuidle_module.rende_cpu_idle(menu=self.cpu_idle_tab)
            case "Memory":
                self.memory_module.rende_memory(menu=self.cpu_menu_tab)
            case "I/O":
                self.io_module.rende_io(self.io_menu_tab)
            case "Battery":
                self.battery_module.rende_battery(self.battery_menu_tab)

#button = customtkinter.CTkButton(master=tabview.tab("tab 1"))
#button.pack(padx=20, pady=20)
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("dark")
main = janela_prin()
