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

def get_cpu_microcode():
    ret = list(range(2))
    try:
        with open(f"/sys/devices/system/cpu/cpu0/microcode/version", "r") as f:
            ret[0] = "Microcode version: " + f.read().strip()
    except:
        ret[0] = "Microcode version: " + "Unknown"

    try:
        with open(f"/sys/devices/system/cpu/cpu0/microcode/processor_flags", "r") as f:
            ret[1] = "Microcode flags: " + f.read().strip()
    except:
        ret[1] = "Microcode version: " + "Unknown"

    return ret

def get_system_info():
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

    def get_architecture_extension(self, isa):
        if isa.find("avx512f"):
            return "V4"
        elif isa.find("avx2"):
            return "V3"
        elif isa.find("ssse3"):
            return "V2"
        else:
            return "V1"

    def get_microcode(self):
        with open("/sys/devices/system/cpu/cpu0/microcode/version", "r") as mc_fd:
            return mc_fd.read().strip()

    def cpu_info(self):
        self.cpu_info = cpui.get_cpu_info()
        self.core_num = str(psutil.cpu_count(logical=False))
        self.thread_num = str(psutil.cpu_count())
        self.hyper_state = self.cpu_has_ht(str(self.cpu_info["flags"]))

    def frame_cpu_info(self):

        def rende_microcode():
            microcode_frame = LabelFrame(self.frame_cpu_brand, text="CPU Microcode", background='#212121', foreground="white")
            microcode_frame.pack(padx=5, pady=5)
            microcode_info = get_cpu_microcode()
            for micro_info in microcode_info:
                ctk.CTkLabel(microcode_frame, text=micro_info).pack(padx=5, pady=5, anchor="w")

        def rende_cache_system():
            def rende_cache_perf_core():
                perf_phisical_cores = self.p_cores
                p_core_cache_frame = LabelFrame(cache_frame, text="Performance cores cache", background='#212121', foreground="white")
                p_core_cache_frame.pack(padx=5, pady=5)
                if self.hyper_state == 1:
                    perf_phisical_cores //= 2
                for cache_tit, cache_func, way_func in zip(titulo_cpu_cache, global_cache_ref, func_ref_way):
                    ctk.CTkLabel(p_core_cache_frame, text=cache_tit + cache_func(0) + " X" + str(perf_phisical_cores) + " Ways: " + way_func(0)).pack(anchor="w", padx=5, pady=5)
                ctk.CTkLabel(p_core_cache_frame, text="Cache L3: " + self.get_l3_cache(0) + " Ways: " + self.get_l3_way(0)).pack(anchor="w", padx=5, pady=5)
                ctk.CTkLabel(p_core_cache_frame, text="Cache L4: " + self.get_l4_cache(0) + " Ways: " + self.get_l4_way(0)).pack(anchor="w", padx=5, pady=5)

            def rende_cache_eco_cores():
                e_core_cache_frame = LabelFrame(cache_frame, text="Eficiency cores cache", background='#212121', foreground="white")
                e_core_cache_frame.pack(padx=5, pady=5)
                core = self.p_cores + self.e_cores - 1
                for cache_tit, cache_func, way_func in zip(titulo_cpu_cache, global_cache_ref, func_ref_way):
                    ctk.CTkLabel(e_core_cache_frame, text=cache_tit + cache_func(core) + " Ways: " + way_func(core)).pack(anchor="w", padx=5, pady=5)
                ctk.CTkLabel(e_core_cache_frame, text="Cache L3: " + self.get_l3_cache(core) + " Ways: " + self.get_l3_way(core)).pack(anchor="w", padx=5, pady=5)
                ctk.CTkLabel(e_core_cache_frame, text="Cache L4: " + self.get_l4_cache(core) + " Ways: " + self.get_l4_way(core)).pack(anchor="w", padx=5, pady=5)

            titulo_cpu_cache = ["Cache L1d: ", "Cache L1i: ", "Cache L2: ", "Cache L3: ", "Cache L4: "]
            global_cache_ref = [self.get_core_l1d_cache, self.get_core_l1i_cache, self.get_core_l2_cache]
            func_ref_way = [self.get_core_l1i_way, self.get_core_l1d_way, self.get_core_l2_way]
            cache_frame = LabelFrame(self.frame_cpu, text="CPU cache system", background='#212121', foreground="white")
            cache_frame.grid(row=0, column=1)
            if self.big_little: # big litlle is true
                rende_cache_perf_core()
                rende_cache_eco_cores()
            else:
                for cache_tit, cache_func, way_func in zip(titulo_cpu_cache, global_cache_ref, func_ref_way):
                    ctk.CTkLabel(cache_frame, text=cache_tit + cache_func(0) + " X" + str(self.core_num) + " Ways: " + way_func(0)).pack(anchor="w", padx=5, pady=5)
                ctk.CTkLabel(cache_frame, text="Cache L3: " + self.get_l3_cache(0) + " Ways: " + self.get_l3_way(0)).pack(anchor="w", padx=5, pady=5)
                ctk.CTkLabel(cache_frame, text="Cache L4: " + self.get_l4_cache(0) + " Ways: " + self.get_l4_way(0)).pack(anchor="w", padx=5, pady=5)

        def rende_cpufreq_info():
            def rende_perf_freq_core():
                p_core_freq_frame = LabelFrame(freq_frame, text="Performance cores frequency", background='#212121', foreground="white")
                p_core_freq_frame.pack(padx=5, pady=5)
                cpu_freq_info = get_core_freq(0)
                for key in cpu_freq_info.keys():
                    ctk.CTkLabel(p_core_freq_frame, text=key + ": " + cpu_freq_info[key]).pack(anchor="w", padx=5, pady=5)

            def rende_eco_freq_cores():
                e_core_freq_frame = LabelFrame(freq_frame, text="Eficiency cores frequency", background='#212121', foreground="white")
                e_core_freq_frame.pack(padx=5, pady=5)
                core = self.p_cores + self.e_cores - 1
                cpu_freq_info = get_core_freq(core)
                for key in cpu_freq_info.keys():
                    ctk.CTkLabel(e_core_freq_frame, text=key + ": " + cpu_freq_info[key]).pack(anchor="w", padx=5, pady=5)


            freq_frame = LabelFrame(self.frame_cpu, text="CPU freq system", background='#212121', foreground="white")
            freq_frame.grid(row=1, column=1)
            if self.big_little: # big litlle is true
                rende_perf_freq_core()
                rende_eco_freq_cores()
            else:
                cpu_freq_info = get_core_freq(0)
                for key in cpu_freq_info.keys():
                    ctk.CTkLabel(freq_frame, text=key + ": " + cpu_freq_info[key]).pack(anchor="w", padx=5, pady=5)

        def get_core_freq(core):
            freq_info = {}
            freq_title = ["Max freq", "Min freq", "Base freq"]
            freq_range = ["cpuinfo_max_freq", "cpuinfo_min_freq", "base_frequency"]
            for key, folder in zip(freq_title, freq_range):
                try:
                    with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/{folder}", "r") as freq:
                        freq_info[key] = str(int(freq.read().strip()) // 100) + " MHz"
                except:
                    freq_info[key] = "Unsupported"
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/cpuinfo_transition_latency", "r") as freq:
                    freq_info["translation latency"] = freq.read().strip() + " Ms"
            except:
                freq_info["translation latency"] = "Unsupported"

            return freq_info

        titulo_cpu_rotulos = ["CPU Name: ", "Vendor: ", "Architecture: "]
        titulo_cpu_rotulos2 = ["Model: ", "Family: ", "Stepping: ", "Bits: ", "Microcode: "]
        cpu_hash = ["brand_raw", "vendor_id_raw", "arch"]
        cpu_hash2 = ["model", "family", "stepping", "bits"]
        self.num_cores = int(self.thread_num) if self.hyper_state == 1 else int(self.core_num)
        self.e_cores, self.p_cores = self.cpu_is_big_little()
        isa = ""
        for feature in self.cpu_info["flags"]:
            isa += feature + ", "
        hyper_state = self.cpu_has_ht(str(self.cpu_info["flags"]))
        self.frame_cpuinfo_global = ctk.CTkScrollableFrame(self.cpu_info_tab, width=770, height=800)
        self.frame_cpuinfo_global.grid(row=3, column=0)
        self.frame_cpu = LabelFrame(self.frame_cpuinfo_global, text="CPU info", background='#212121', foreground="white")
        self.frame_cpu.pack(padx=5, pady=5, fill=ctk.BOTH, expand=1)
        self.frame_cpu_brand = LabelFrame(self.frame_cpu, text="CPU Brand", background='#212121', foreground="white")
        self.frame_cpu_brand.grid(row=0, column=0, padx=5, pady=5, sticky="nw", rowspan=10)
        for info, hash_cpu in zip(titulo_cpu_rotulos, cpu_hash):
            ctk.CTkLabel(self.frame_cpu_brand, text=info + self.cpu_info[hash_cpu]).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="Architecture extension: " + self.cpu_info["arch"] + "-" + self.get_architecture_extension(isa)).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="Cores: " + str(psutil.cpu_count(logical=False))).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="Threads: " + str(psutil.cpu_count())).pack(anchor="w", padx=5, pady=5)
        if hyper_state == 0:
            ctk.CTkLabel(self.frame_cpu_brand, text="Hyperthreading: Not supported").pack(anchor="w", padx=5, pady=5)
        elif hyper_state == 1:
            ctk.CTkLabel(self.frame_cpu_brand, text="Hyperthreading: Supported and enabled").pack(anchor="w", padx=5, pady=5)
        else:
            ctk.CTkLabel(self.frame_cpu_brand, text="Hyperthreading: Supported (disabled)").pack(anchor="w", padx=5, pady=5)
        self.rende_big_little(self.p_cores, self.e_cores)
        self.cpu_utilization = ctk.CTkLabel(self.frame_cpu_brand)
        self.cpu_utilization.pack(anchor="w", padx=5, pady=5)
        self.update_cpu_util()
        rende_cache_system()
        rende_cpufreq_info()
        for info, hash_cpu in zip(titulo_cpu_rotulos2, cpu_hash2):
            ctk.CTkLabel(self.frame_cpu_brand, text=info + str(self.cpu_info[hash_cpu])).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="CPU endian: " + get_cpu_endian()).pack(anchor="w", padx=5, pady=5)
        self.cpu_errata_frame = LabelFrame(self.frame_cpu, text="CPU bugs (Errata)", background='#212121', foreground="white")
        self.cpu_errata_frame.grid(padx=5, pady=5, column=1, row=2)
        #ctk.CTkLabel(self.cpu_errata_frame, text="jkdhfreh").pack(padx=5, pady=5)
        cpu_errata = get_cpu_erratas()
        for errata in cpu_errata.keys():
            ctk.CTkLabel(self.cpu_errata_frame, text=errata.replace("_", " ") + ": " + cpu_errata[errata], wraplength=300, justify="left").pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="ISA: " + isa, wraplength=400, justify="left").pack(anchor="w", padx=5, pady=5)
        rende_microcode()

    def update_cpu_util(self):
            cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            self.cpu_utilization.configure(text="CPU utilization: " + str(int(sum(cpu_util) / self.num_cores)) + "%")
            self.task = self.frame_cpu.after(1000, self.update_cpu_util)

    def get_core_l1d_cache(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index0/size", "r") as cache_1d_info:
                return cache_1d_info.read().strip() + "B"
        except:
            return "Unsupported"

    def get_core_l1i_cache(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index1/size", "r") as cache_1i_info:
                return cache_1i_info.read().strip() + "B"
        except:
            return "Unsupported"
    
    def get_core_l2_cache(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index2/size", "r") as cache_2_info:
                return cache_2_info.read().strip() + "B"
        except:
            return "Unsupported"
        
    # L3 is a global cache (I think)
    def get_l3_cache(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index3/size", "r") as cache_3_info:
                return cache_3_info.read().strip() + "B"
        except:
            return "unsupported"
    
    # poucos processadores tem cache L4 
    def get_l4_cache(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index4/size", "r") as cache_4_info:
                return cache_4_info.read().strip() + "B"
        except:
            return "unsupported"
        
    def get_core_l1d_way(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index0/ways_of_associativity", "r") as cache_1d_info:
                return cache_1d_info.read().strip() + " ways"
        except:
            return "Unsupported"

    def get_core_l1i_way(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index1/ways_of_associativity", "r") as cache_1i_info:
                return cache_1i_info.read().strip() + " ways"
        except:
            return "Unsupported"
    
    def get_core_l2_way(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index2/ways_of_associativity", "r") as cache_2_info:
                return cache_2_info.read().strip() + " ways"
        except:
            return "Unsupported"
        
    # L3 is a global cache (I think)
    def get_l3_way(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index3/ways_of_associativity", "r") as cache_3_info:
                return cache_3_info.read().strip() + " ways"
        except:
            return "unsupported"
    
    # poucos processadores tem cache L4 
    def get_l4_way(self, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cache/index4/ways_of_associativity", "r") as cache_4_info:
                return cache_4_info.read().strip() + " ways"
        except:
            return "unsupported"

    def cpu_is_big_little(self):
        self.big_little = False
        l_core = b_core = 0
        try:
            with open(f"/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq", "r") as fd:
                max_freq = int(fd.read().strip())
        except:
            print("err")
        for core in range(1, int(self.thread_num)):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/cpuinfo_max_freq", "r") as fd:
                    if int(fd.read().strip()) == max_freq:
                        b_core += 1
                    else:
                        l_core += 1
            except:
                pass
        b_core += 1
        if l_core:
            self.big_little = True
            try:
                with open("big_little.txt", "w") as fd:
                    fd.write(str(b_core) + " " + str(l_core))
            except:
                print("err")
        return l_core, b_core

    def rende_big_little(self, b_cores, l_cores):
        if b_cores == 0 or l_cores == 0:
            ctk.CTkLabel(self.frame_cpu_brand, text="Big-Little: False").pack(anchor="w", padx=5, pady=5)
            return
        ctk.CTkLabel(self.frame_cpu_brand, text="Big-Little: True").pack(anchor="w",padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text=f"Performance cores/threads: {b_cores}").pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text=f"Eficiency cores/threads: {l_cores}").pack(anchor="w", padx=5, pady=5)

    # lógica podre mas temos pena
    def p_or_e(self):
        if self.p_cores > 0:
            self.p_cores -= 1
            return "performance"
        elif self.e_cores > 0:
            self.e_cores -= 1
            return "eficiency"


    def rende_placa_mae_info(self):
        info = get_system_info()
        frame_mother_board = LabelFrame(self.frame_cpu, text="Motherboard info", background='#212121', foreground="white")
        frame_mother_board.grid(padx=5, pady=5, row=3, column=0)
        for key in info.keys():
            ctk.CTkLabel(frame_mother_board, text=key + ": " + info[key]).pack(anchor="w", padx=5)


    def rende_cpu_info(self):
         self.frame_cpu_info()
         self.rende_placa_mae_info()
     #    self.frame_core_info()

    def __init__(self) -> None:
         self.janela : ctk.CTk = ctk.CTk() # nome tempoprario
         self.janela.title("Kernel manager")
     #    self.janela.maxsize(1080, 1280)
         self.frame_atual = "CPU info"
         self.frame_anterior = "CPU info"
         self.init_title_menu()
         self.cpu_info()
         self.init_menu()
         self.rende_cpu_info()
         self.inicialize_objects()
         self.inicialize_pages()
         self.janela.mainloop()

    def inicialize_objects(self):
        self.error = event_error.io_error()
        self.system_module = system.system
        self.cpufreq_module = cpufreq.cpu_freq()
        self.cpuidle_module = cpuidle.cpu_idle()
        self.memory_module = memory.memory()
        self.io_module = io_manager.io_manager()
        self.battery_module = battery.battery()

    def inicialize_pages(self):
        self.system_module.rende_system_info(self.cpu_system_tab)
        self.cpufreq_module.rende_cpu_freq(menu=self.cpu_freq_tab, num_cores=self.thread_num)
        self.cpuidle_module.rende_cpu_idle(menu=self.cpu_idle_tab)
        self.memory_module.rende_memory(menu=self.cpu_menu_tab)
        self.io_module.rende_io(self.io_menu_tab)
        self.battery_module.rende_battery(self.battery_menu_tab)

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

    def verify_page(self):
        self.frame_atual = self.menu.get()

        if self.frame_anterior == "CPU frequency":
            self.cpufreq_module.cancel_task()
        elif self.frame_anterior == "Memory":
            self.memory_module.cancel_task()
        elif self.frame_anterior == "CPU info":
            self.cancel_task()
        
        if self.frame_atual == "CPU frequency":
            self.cpufreq_module.start_task()
        elif self.frame_atual == "Memory":
            self.memory_module.start_task()
        elif self.frame_atual == "CPU info":
            self.memory_module.start_task()


        self.frame_anterior = self.frame_atual
            
    def start_task(self):
        self.update_cpu_util()
    
    def cancel_task(self):
        self.frame_cpu.after_cancel(self.task)

    def init_menu(self):
       # self.menu = ctk.CTkTabview(master=self.janela, command=self.mudar_pagina)
        self.menu = ctk.CTkTabview(master=self.janela, command=self.verify_page)
        self.menu.pack(padx=5)
        self.cpu_info_tab = self.menu.add("CPU info")  # add tab at the end
        self.cpu_system_tab = self.menu.add("System info")  # add tab at the end
        self.cpu_freq_tab = self.menu.add("CPU frequency")  # add tab at the end
        self.cpu_idle_tab = self.menu.add("CPU idle")  # add tab at the end
        self.cpu_menu_tab = self.menu.add("Memory")  # add tab at the end
        self.io_menu_tab = self.menu.add("I/O")  # add tab at the end
        self.battery_menu_tab = self.menu.add("Battery")  # add tab at the end

        self.rende_cpu_info()

ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("dark")
main = janela_prin()

