import cpuinfo as cpui
import psutil
import customtkinter as ctk
import os
from CTkMenuBar import *
from CTkMessagebox import CTkMessagebox
from tkinter import LabelFrame
from ctypes import CDLL, c_int32, c_char_p, c_bool, Structure, POINTER
from blinker import signal

class cache_struct(Structure):
    _fields_ = [("cache_l1i_size", c_int32),
              ("cache_l1i_assoc", c_int32),
              ("cache_l1i_line_size", c_int32),
              ("cache_l1i_instances", c_int32),

              ("cache_l1d_size", c_int32),
              ("cache_l1d_assoc", c_int32),
              ("cache_l1d_line_size", c_int32),
              ("cache_l1d_instances", c_int32),

              ("cache_l2_size", c_int32),
              ("cache_l2_assoc", c_int32),
              ("cache_l2_line_size", c_int32),
              ("cache_l2_instances", c_int32),

              ("cache_l3_size", c_int32),
              ("cache_l3_assoc", c_int32),
              ("cache_l3_line_size", c_int32),
              ("cache_l3_instances", c_int32),

              ("cache_l4_size", c_int32),
              ("cache_l4_assoc", c_int32),
              ("cache_l4_line_size", c_int32),
              ("cache_l4_instances", c_int32),
              ]

# Definir a OuterStruct em Python, que contém a InnerStruct
class cpu_info_struct(Structure):
    _fields_ = [("cpu_name", c_char_p),
                ("cpu_purpouse", c_char_p),
                ("fisical_cores", c_int32),
                ("logical_cores", c_int32),
                ("cpu_model", c_int32),
                ("cpu_family", c_int32),
                ("cpu_stepping", c_int32),
                ("cpu_vendor", c_char_p),
                ("cpu_codename", c_char_p),
                ("cache_info", cache_struct)]

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
                cpu_errata_val = errata_fd.read().strip()
                if cpu_errata_val == "Not affected":
                    continue
                info[folder] = cpu_errata_val
    except:
        pass
    return info

class cpuinfo:

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
        for id in range(self.clusters):
            self.core_num = self.struct[id].fisical_cores
            self.thread_num = self.struct[id].logical_cores
        self.hyper_state = self.cpu_has_ht(str(self.cpu_info["flags"]))

    def frame_cpu_info(self):

        def rende_microcode():
            microcode_info = get_cpu_microcode()
            for micro_info in microcode_info:
                ctk.CTkLabel(self.frame_cpu_brand, text=micro_info).pack(padx=5, pady=5, anchor="w")

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
     #   titulo_cpu_rotulos = ["CPU Name: ", "Vendor: ", "Architecture: "]
    #    titulo_cpu_rotulos2 = ["Model: ", "Family: ", "Stepping: ", "Bits: ", "Microcode: "]
     #   self.num_cores = int(self.thread_num) if self.hyper_state == 1 else int(self.core_num)
        self.num_cores = self.total_cores
        self.e_cores, self.p_cores = self.cpu_is_big_little()
        isa = ""
        for feature in self.cpu_info["flags"]:
            isa += feature + ", "
        hyper_state = self.cpu_has_ht(str(self.cpu_info["flags"]))
        self.frame_cpuinfo_global = ctk.CTkScrollableFrame(self.menu, width=770, height=800)
        self.frame_cpuinfo_global.grid(row=3, column=0)
        self.frame_cpu = LabelFrame(self.frame_cpuinfo_global, text="CPU info", background='#212121', foreground="white")
        self.frame_cpu.pack(padx=5, pady=5, fill=ctk.BOTH, expand=1)
        self.frame_cpu_brand = LabelFrame(self.frame_cpu, text="CPU Brand", background='#212121', foreground="white")
        self.frame_cpu_brand.grid(row=0, column=0, padx=5, pady=5, sticky="nw", rowspan=10)
        for info, hash_cpu in zip(titulo_cpu_rotulos, cpu_hash):
            ctk.CTkLabel(self.frame_cpu_brand, text=info + self.cpu_info[hash_cpu]).pack(anchor="w", padx=5, pady=5)
       # ctk.CTkLabel(self.frame_cpu_brand, text="Architecture extension: " + self.cpu_info["arch"] + "-" + self.get_architecture_extension(isa)).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="Cores: " + str(self.struct[0].fisical_cores)).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="Threads: " + str(self.struct[0].logical_cores)).pack(anchor="w", padx=5, pady=5)
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
        rende_microcode()
        self.cpu_errata_frame = LabelFrame(self.frame_cpu, text="CPU bugs (Errata)", background='#212121', foreground="white")
        self.cpu_errata_frame.grid(padx=5, pady=5, column=1, row=2)
        #ctk.CTkLabel(self.cpu_errata_frame, text="jkdhfreh").pack(padx=5, pady=5)
        cpu_errata = get_cpu_erratas()
        for errata in cpu_errata.keys():
            ctk.CTkLabel(self.cpu_errata_frame, text=errata.replace("_", " ") + ": " + cpu_errata[errata], wraplength=300, justify="left").pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(self.frame_cpu_brand, text="ISA: " + isa, wraplength=400, justify="left").pack(anchor="w", padx=5, pady=5)

    def update_cpu_util(self):
            cpu_util = psutil.cpu_percent(interval=None, percpu=True)
          #  self.cpu_utilization.configure(text="CPU utilization: " + str(int(sum(cpu_util) / self.num_cores)) + "%")
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

    def set_list_purpouse(self):
        purpouse_list = []
        for id in range(self.clusters):
            purpouse_list.append(self.struct[id].cpu_purpouse.decode("utf-8"))
        print(purpouse_list)
        return purpouse_list

    def init_library_cpuid(self):
        print(os.getcwd())
        lib_cpuid = CDLL("/opt/kernel_manager/lib_manager.so")
        lib_cpuid.cpu_init.restype = c_bool
        lib_cpuid.get_cpu_info.restype = POINTER(cpu_info_struct)
        lib_cpuid.total_cores_system.restype = c_int32
        lib_cpuid.clusters.restype = c_int32

        if lib_cpuid.cpu_init() == 1:
            print("Erro")
            return True

        self.struct = lib_cpuid.get_cpu_info()

        if not self.struct:
            print("Error null struct")
            return True

        self.total_cores = lib_cpuid.total_cores_system()
        self.clusters = lib_cpuid.clusters()
        print("total cores, ", self.total_cores)
        print("clusters, ", self.clusters)
        self.list_cores = {}
        for cluster in range(self.clusters):
            self.list_cores[self.struct[cluster].cpu_purpouse.decode("utf-8")] = self.struct[cluster].logical_cores

        print("cores in clusters: ", self.list_cores)

        return False

    def rende_cpu_info(self, menu):
         library = self.init_library_cpuid()
         if library:
             CTkMessagebox(title="Error", message="Error to inicialize library", icon="cancel")
             os._exit(1)
         self.set_list_purpouse()
         self.menu = menu
         self.cpu_info()
         self.frame_cpu_info()
         return self.total_cores, self.list_cores

    def start_task(self):
        self.update_cpu_util()
    
    def cancel_task(self):
        self.frame_cpu.after_cancel(self.task)