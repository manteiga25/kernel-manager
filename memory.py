import customtkinter as ctk
import event_error
import psutil
from platform import uname
from os import listdir, stat, path, system
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox

class memory:

    def rende_thp(self):

        def get_thp_modes(file):
            try:
                with open(f"/sys/kernel/mm/transparent_hugepage/{file}", "r") as fd_mode:
                    modes = fd_mode.read()
                    modes = modes.replace("[", '')
                    modes = modes.replace("]", '')
                    modes_list = modes.split()
                    return modes_list
            except:
               return "err"
        
        def get_thp_mode(file):
            try:
                with open(f"/sys/kernel/mm/transparent_hugepage/{file}", "r") as fd_mode:
                    modes = fd_mode.read().split()
                    if '[always]' in modes:
                        return 'always'
                    elif '[madvise]' in modes:
                        return 'madvise'
                    elif '[never]' in modes:
                        return 'never'
                    elif '[inherit]' in modes:
                            return 'inherit'
                    else:
                        return "undefined" # ainda faltam mais modos
            except:
                        return "err"

        def set_thp_defrag_mode():
            mode = modo_thp_defrag.get()
            system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/defrag")

        def set_thp_mode():
            mode = modo_thp.get()
            system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/enabled")
        
        def set_thp_shm_mode():
            mode = modo_thp_shm.get()
            system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/shmem_enabled")

        def get_thp_info():

            def get_thp_mode(folder):
                try:
                    with open(f"/sys/kernel/mm/transparent_hugepage/{folder}/enabled", "r") as fd_mode:
                        modes = fd_mode.read().split()
                        if '[always]' in modes:
                            return 'always'
                        elif '[madvise]' in modes:
                            return 'madvise'
                        elif '[never]' in modes:
                            return 'never'
                        elif '[inherit]' in modes:
                            return 'inherit'
                        else:
                            return "undefined" # ainda faltam mais modos
                except:
                            return "err"

            def set_thp(thp):
                print(thp)
                state = huge_page[thp].get()
                print(state)
                system(f"echo {state} > /sys/kernel/mm/transparent_hugepage/{thp}/enabled")

            huge_page = {}
            huge_page_ok = {}
            try:
                folders = listdir("/sys/kernel/mm/transparent_hugepage/")
                folders_num = len(folders)
                print(folders_num)
            except:
                folders = ""
                folders_num = 0
            print(folders)
            for folder, index in zip(folders, range(3, folders_num+1)):
                #print(index)
                if path.isdir("/sys/kernel/mm/transparent_hugepage/" + folder):
                  #  print(folder)
                    #if path.exists()
                    try:
                        with open(f"/sys/kernel/mm/transparent_hugepage/{folder}/enabled", "r") as huge_fd:
                            print("opened " + folder)
                            estado = huge_fd.read().strip()
                            ctk.CTkLabel(self.frame_thp, text=folder).grid(row=index, column=0)
                            huge_page[folder] = ctk.CTkComboBox(self.frame_thp, values=self.modos)
                            mode = get_thp_mode(folder)
                            huge_page[folder].set(mode)
                            huge_page_ok[folder] = ctk.CTkButton(self.frame_thp, text="Alterar", command=lambda f=folder: set_thp(f))
                            huge_page[folder].grid(pady=5, row=index, column=1)
                            huge_page_ok[folder].grid(pady=5, row=index, column=2)
                    except:
                        print("erro " + folder)

        if not path.exists("/sys/kernel/mm/transparent_hugepage"):
            return

        self.frame_thp = LabelFrame(self.frame_memory, text="Transparent Huge Page", background='#212121', foreground="white", labelanchor="n")
        self.frame_thp.grid(pady=5, column=1, row=0, sticky="nsew", padx=5)
        self.modos = get_thp_modes("enabled")
        modo = get_thp_mode("enabled")
        ctk.CTkLabel(self.frame_thp, text="Transparent Huge Page mode").grid(row=0, column=0, padx=5, pady=5)
        modo_thp = ctk.CTkComboBox(self.frame_thp, values=self.modos)
        modo_thp.set(modo)
        modo_thp.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(self.frame_thp, text="Alterar", command=set_thp_mode).grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.frame_thp, text="Defrag").grid(row=1, column=0, padx=5, pady=5)
        modo_thp_defrag = ctk.CTkComboBox(self.frame_thp, values=get_thp_modes("defrag"))
        modo_thp_defrag.set(get_thp_mode("defrag"))
        modo_thp_defrag.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(self.frame_thp, text="Alterar", command=set_thp_defrag_mode).grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.frame_thp, text="Shared mem").grid(row=2, column=0, padx=5, pady=5)
        modo_thp_shm = ctk.CTkComboBox(self.frame_thp, values=get_thp_modes("shmem_enabled"))
        modo_thp_shm.set(get_thp_mode("shmem_enabled"))
        modo_thp_shm.grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkButton(self.frame_thp, text="Alterar", command=set_thp_shm_mode).grid(row=2, column=2, padx=5, pady=5)
        get_thp_info()

    def get_vm_info(self):
        info = {}
        perm = {}
        try:
            folders = listdir("/proc/sys/vm/")
        except:
            folders = ""
        for folder in folders:
            status = stat("/proc/sys/vm/" + folder)
            #print(status.st_mode)
            try:
                #print(folder)
                with open("/proc/sys/vm/" + folder, "r") as f:
               #     key = folder.replace("_", " ")
                   # print(key)
                    info[folder] = f.read().strip()
                    perm[folder] = status.st_mode
            except:
                print("arquivo" + folder + " " + str(status.st_mode))
        return info, perm

    def set_memory_info(self, mem):
        for value, folder in zip(mem.values(), mem.keys()):
            try:
                with open("/proc/sys/vm/" + folder, "w") as f:
                    print(folder, "change to, ", value)
                    f.write(value)
            except:
                self.error.escreve_erro(f"Error to set memory {folder}", str(Exception))

    def set_memory_param(self):
        change = {}
        for var, key in zip(self.entry_vars.keys(), self.vm_info.keys()):
            print(f"{str(var)} {self.vm_info[var]} != {self.entry_vars[var].get()}")
            tmp = self.entry_vars[var].get() # increase cache hit and less instruction executing
            if self.vm_info[var] != tmp:
            #    self.set_memory_info(var)
                change[var] = tmp
        if change:
            self.set_memory_info(change)

    def rende_vm_info(self):
        self.vm_info, file_perm = self.get_vm_info()
        self.entry_vars = {}
        self.vm_widget = {}
        frame_vm_info = LabelFrame(self.frame_memory, text="VM info", background='#212121', foreground="white", labelanchor="n")
        frame_vm_info.grid(column=0, row=1)
        for info, local in zip(self.vm_info.keys(), range(len(self.vm_info))):
            if file_perm[info] == 33188:
                ctk.CTkLabel(frame_vm_info, text=info.replace("_", " ") + " : ", justify="left").grid(padx=5, row=local, column=0)
                self.entry_var = ctk.StringVar()
                self.entry_var.set(self.vm_info[info])
                self.entry_vars[info] = self.entry_var
                #self.entry_vars[info] = vm_info[info]
                #ctk.CTkEntry(frame_vm_info, placeholder_text=vm_info[info], justify="left").grid(padx=5, row=local, column=1)
                self.vm_widget[info] = ctk.CTkEntry(frame_vm_info, textvariable=self.entry_var, placeholder_text=self.vm_info[info], justify="left").grid(padx=5, pady=5, row=local, column=1)
            else:
                ctk.CTkLabel(frame_vm_info, text=info.replace("_", " ") + " : ").grid(padx=5, pady=5, row=local, column=0)
                ctk.CTkLabel(frame_vm_info, text=self.vm_info[info] + " (read-only)").grid(padx=5, pady=5, row=local, column=1, sticky="w")

        ctk.CTkButton(frame_vm_info, text="Salvar alterações", command=self.set_memory_param).grid()

    def rende_memory_bar(self):
        def update_mem_info(): # código feito com preguiça
            mem_text = ["Disponível: ", "usado: "]
            aux = [1, 3]
            memory_info = psutil.virtual_memory()
            for i in range(2):
                mem[i].configure(text=mem_text[i] + str(round(memory_info[aux[i]] / 1024 / 1024 / 1024, 1)) + "GB")
            mem_bar.set(round(memory_info[2] / 100, 2))
            mem_bar.after(1000, update_mem_info)
        mem = list(range(2))
        frame_mem = ctk.CTkFrame(self.frame_memory, width=350, height=100)
        frame_mem.grid(row=0, column=1, columnspan=6)
     #   ctk.CTkLabel(self.frame_memory, text="Memory RAM size: " + str(round(psutil.virtual_memory()[0] / 1024 / 1024 / 1024, 1)) + "GB").grid(row=0, column=3, columnspan=2, padx=0, pady=5, sticky="w")
        ctk.CTkLabel(frame_mem, text="Memory RAM size: " + str(round(psutil.virtual_memory()[0] / 1024 / 1024 / 1024, 1)) + "GB").place(x=60, y=10)
        for i in range(2):
            mem[i] = ctk.CTkLabel(frame_mem)
       # mem[0].grid(row=1, column=2, columnspan=2, padx=5, sticky="ew", pady=5)
       # mem[1].grid(row=1, column=4, columnspan=2, padx=5, sticky="ew", pady=5)
        mem_bar = ctk.CTkProgressBar(frame_mem, orientation="horizontal", width=250, height=30)
        #mem_bar.grid(row=2, column=3, rowspan=2, columnspan=6, sticky="ew", padx=5, pady=5)
        mem_bar.place(x=10, y=60)
        mem[0].place(x=20, y=30)
        mem[1].place(x=160, y=30)

        update_mem_info()

    def memory_system(self):
        self.frame_memory = ctk.CTkScrollableFrame(self.menu, width=1280, height=380)
        self.frame_memory.grid(column=0, row=3, columnspan=6, sticky="ew")
        self.rende_memory_bar()

    def rende_zswap(self):
        if not path.exists("/sys/module/zswap"):
            pass
        
        def switch_zswap(folder):
            state = "N"
            if zswap_state.get():
                state = "Y"
            print(state)
            try:
                with open(f"/sys/module/zswap/parameters/{folder}", "w") as f:
                    f.write(state)
            except:
                print("err")
                return

        def get_zswap_state(folder):
            try:
                with open(f"/sys/module/zswap/parameters/{folder}", "r") as f:
                    value = f.read().strip()
                    return value == "Y"
            except:
                print("err")
                return "err"

        def get_pool_perc():
            try:
                with open("/sys/module/zswap/parameters/max_pool_percent", "r") as f:
                    return int(f.read().strip()) / 100
            except:
                print("err")
                return 0

        def switch_pool_value(event):
            value = str(int(float(pool.get()) * 100))
          #  try:
            with open("/sys/module/zswap/parameters/max_pool_percent", "w") as f:
                f.write(value)
            pool_perc.configure(text=value + "%")
    #        except:
     #           print("err")
      #          return 0

        def get_thre_perc():
            try:
                with open("/sys/module/zswap/parameters/accept_threshold_percent", "r") as f:
                    return int(f.read().strip()) / 100
            except:
                print("err")
                return 0

        def switch_thre_value(event):
            value = str(int(float(threshold.get()) * 100))
          #  try:
            with open("/sys/module/zswap/parameters/accept_threshold_percent", "w") as f:
                f.write(value)
            threshold_perc.configure(text=value + "%")
    #        except:
     #           print("err")
      #          return 0

        def get_zswap_compressor():
            try:
                with open("/sys/module/zswap/parameters/compressor", "r") as f:
                    return f.read().strip()
            except:
                print("err")
                return ""
            
        def set_zswap_algorithm():
            try:
                algoritmo = algoritmo_zswap.get()
                with open("/sys/module/zswap/parameters/compressor", "w") as f:
                    f.write(algoritmo)
            except:
                print("err")
                return ""
            
        def get_zpool_compressor():
            try:
                with open("/sys/module/zswap/parameters/zpool", "r") as f:
                    return f.read().strip()
            except:
                print("err")
                return ""
            
        def set_zpool_algorithm():
            try:
                algoritmo = algoritmo_zpool.get()
                with open("/sys/module/zswap/parameters/zpool", "w") as f:
                    f.write(algoritmo)
            except:
                print("err")
                return ""

        self.frame_zswap = LabelFrame(self.frame_memory, text="Zswap", background='#212121', foreground="white", labelanchor="n")
        self.frame_zswap.grid(row=1, column=1, columnspan=6, pady=5, padx=5)
        zswap_feature_bool_name = ["Zswap state", "shrinker", "exclusive loads", "same filled pages", "non same filled pages"]
        zswap_feature_bool_folder =  ["enabled", "shrinker_enabled", "exclusive_loads", "same_filled_pages_enabled", "non_same_filled_pages_enabled"]
        zswap_state = list(range(5))
        for name_index in range(5):
            ctk.CTkLabel(self.frame_zswap, text=zswap_feature_bool_name[name_index]).grid(row=name_index, column=0, pady=5)
            zswap_state[name_index] = ctk.CTkSwitch(self.frame_zswap, text="Off/On", onvalue=1, offvalue=0, command=lambda: switch_zswap(zswap_feature_bool_folder[name_index]))
            if get_zswap_state(zswap_feature_bool_folder[name_index]):
                zswap_state[name_index].select()
            else:
                zswap_state[name_index].deselect()
            zswap_state[name_index].grid(row=name_index, column=1, pady=5)
        ctk.CTkLabel(self.frame_zswap, text="Zpool percent").grid(row=5, column=0)
        pool = ctk.CTkSlider(self.frame_zswap, from_=0, to=1)
        pool_percent = get_pool_perc()
        pool.set(pool_percent)
        print(get_pool_perc())
        pool.bind("<B1-Motion>", switch_pool_value)
        pool.bind("<Button-1>", switch_pool_value)
        pool.grid(row=5, column=1)
        pool_perc = ctk.CTkLabel(self.frame_zswap, text=str(int(pool_percent * 100)) + "%")
        pool_perc.grid(row=5, column=2)

        ctk.CTkLabel(self.frame_zswap, text="Threshold percent").grid(row=6, column=0)
        threshold = ctk.CTkSlider(self.frame_zswap, from_=0, to=1)
        threshold_percentage = get_thre_perc()
        threshold.set(threshold_percentage)
        print(get_thre_perc())
        threshold.bind("<B1-Motion>", switch_thre_value)
        threshold.bind("<Button-1>", switch_thre_value)
        threshold.grid(row=6, column=1)
        threshold_perc = ctk.CTkLabel(self.frame_zswap, text=str(int(threshold_percentage * 100)) + "%")
        threshold_perc.grid(row=6, column=2)

        ctk.CTkLabel(self.frame_zswap, text="Zswap alghoritm").grid(row=7, column=0, padx=0, pady=5)
        algoritmo_zswap = ctk.CTkComboBox(self.frame_zswap, values=["lz4", "lz4hc", "lzo", "lzo-rle", "zstd", "deflate", "842"])
        algoritmo_zswap.set(get_zswap_compressor())
        algoritmo_zswap.grid(row=7, column=1)
        ctk.CTkButton(self.frame_zswap, text="Alterar", command=set_zswap_algorithm).grid(row=7, column=2)

        ctk.CTkLabel(self.frame_zswap, text="Zpool alghoritm").grid(row=8, column=0, padx=0, pady=5)
        algoritmo_zpool = ctk.CTkComboBox(self.frame_zswap, values=["zbud", "z3fold", "zsmalloc"])
        algoritmo_zpool.set(get_zpool_compressor())
        algoritmo_zpool.grid(row=8, column=1)
        ctk.CTkButton(self.frame_zswap, text="Alterar", command=set_zpool_algorithm).grid(row=8, column=2)

    def rende_zram(self):
        if not path.exists(f"/lib/modules/{uname().release}/kernel/drivers/block/zram"):
            pass

        def switch_zram():
            if zram_button.get():
                system("sudo modprobe zram")
                zram_button.configure(text="Desativar zram")
                zram_status.configure(text="Zram habilitado")
                create_zram()
            else:
                #system("sudo swapoff /dev/zram0")
                system("sudo echo 1 > /sys/block/zram0/reset")
                system("sudo rmmod zram")
                zram_button.configure(text="Ativar zram")
                zram_status.configure(text="Zram desabilitado")

        def create_zram():

            def change_slide_val(event):
                zram_s.configure(text=str(round(zram_size.get() / 1024 / 1024 / 1024, 1)) + " GB")

            def set_zram_size():
                zram_nsize = zram_size.get()
                print(round(zram_nsize / 1024 / 1024 / 1024, 1), " GB")
                try:
                    system("sudo echo 1 > /sys/block/zram0/reset")
                    with open("/sys/block/zram0/disksize", "w") as f:
                        f.write(str(zram_nsize))
                except:
                    zram_val = get_zram_size()
                    zram_s.configure(text=str(round(zram_val / 1024 / 1024 / 1024, 1)) + " GB")
                    zram_size.set(zram_val)
                    CTkMessagebox(title="Dispositivo ocupado", message="Não foi possivel aplicar parametro ao dispositivo Zram,\n Zram ocupado", icon="cancel")

            def get_zram_size():
                try:
                    with open("/sys/block/zram0/disksize", "r") as f:
                        return int(f.read())
                except:
                    print("e")
                    return 0

            ctk.CTkLabel(self.frame_zram, text="Tamanho do zram:").grid(row=1, column=0)
            zram_size = ctk.CTkSlider(self.frame_zram, from_=0, to=psutil.virtual_memory()[0] / 2)
            print(get_zram_size() / 1024 / 1024 / 1024)
            zram_size.set(get_zram_size())
            zram_size.bind('<Button-1>', change_slide_val)
            zram_size.bind("<B1-Motion>", change_slide_val)
            zram_size.grid(row=1, column=1, padx=5)
            zram_s = ctk.CTkLabel(self.frame_zram, text=str(round(get_zram_size() / 1024 / 1024 / 1024, 1)) + " GB")
            zram_s.grid(row=1, column=2)
            ctk.CTkButton(self.frame_zram, text="Criar dispositivo Zram", command=set_zram_size).grid(row=2, column=0, columnspan=2, pady=5)

        self.frame_zram = LabelFrame(self.frame_memory, text="ZRAM", background='#212121', foreground="white", labelanchor="n")
        self.frame_zram.grid(row=2, column=1, padx=5, pady=5)

        zram_status = ctk.CTkLabel(self.frame_zram, text="Zram desabilitado")
        zram_status.grid(row=0, column=0, padx=5, pady=5)
        zram_init = path.exists("/sys/devices/virtual/block/zram0")
        print(zram_init)
        zram_button = ctk.CTkSwitch(self.frame_zram, text="Ativar Zram", command=switch_zram)
        if zram_init:
            zram_button.select()
            zram_status.configure(text="Zram habilitado.")
            zram_button.configure(text="Desativar zram")
            create_zram()
        zram_button.grid(row=0, column=1)

    def memory_hotplug(self):
        if not path.exists("/sys/module/memory_hotplug/parameters"):
            pass

        def get_hotplug_mem_status():
            try:
                with open("/sys/module/memory_hotplug/parameters/auto_movable_numa_aware", "r") as fd:
                    return fd.read().strip()
            except:
                print("ejfv")
        
        def set_hotplug_mem_status():
            try:
                with open("/sys/module/memory_hotplug/parameters/auto_movable_numa_aware", "w") as fd:
                    if hotplug_button.get():
                        fd.write("Y")
                    else:
                        fd.write("N")
            except:
                print("ejfv")

        def get_hotplug_map_mem_status():
            try:
                with open("/sys/module/memory_hotplug/parameters/memmap_on_memory", "r") as fd:
                    return fd.read().strip()
            except:
                print("ejfv")
        
        def set_hotplug_map_mem_status():
            try:
                with open("/sys/module/memory_hotplug/parameters/memmap_on_memory", "w") as fd:
                    if hotplug_map_button.get():
                        fd.write("Y")
                    else:
                        fd.write("N")
            except:
                print("ejfv")

        def get_hotplug_ratio_status():
            try:
                with open("/sys/module/memory_hotplug/parameters/ratio", "r") as fd:
                    return int(fd.read().strip())
            except:
                print("ejfv")
                return 0
        
        def set_hotplug_ratio_status():
            new_ratio = hotplug_ratio_slider.get()
            try:
                with open("/sys/module/memory_hotplug/parameters/ratio", "w") as fd:
                    fd.write(new_ratio)
                    rotulo_hotplug_ratio.configure(text=str(new_ratio) + "MB")
            except:
                print("ejfv")

        def change_label_ratio(event):
            rotulo_hotplug_ratio.configure(text=hotplug_ratio_slider.get())

        hotplug_ram_frame = LabelFrame(self.frame_memory, text="Hotplug Ram", background='#212121', foreground="white", labelanchor="n")
        hotplug_ram_frame.grid(row=3, column=1, padx=5, pady=5)
        ctk.CTkLabel(hotplug_ram_frame, text="O Hotplug Ram é um mecanismo que permite mudar os modulos fisicos de RAM mesmo que o sistema esteja em execução.", justify="center", wraplength=400).grid(padx=5, pady=5, row=0, column=0, columnspan=3)
        ctk.CTkLabel(hotplug_ram_frame, text="Hotplug Ram:").grid(row=1, column=0, padx=5, pady=5)
        hotplug_button = ctk.CTkSwitch(hotplug_ram_frame, text="off/on", command=set_hotplug_mem_status)
        if get_hotplug_mem_status() == "Y":
            hotplug_button.select()
        hotplug_button.grid(row=1, column=1, pady=5)
        ctk.CTkLabel(hotplug_ram_frame, text="Memmap on memory:").grid(row=2, column=0, padx=5, pady=5)
        hotplug_map_button = ctk.CTkSwitch(hotplug_ram_frame, text="off/on", command=set_hotplug_map_mem_status)
        if get_hotplug_map_mem_status() == "Y":
            hotplug_map_button.select()
        hotplug_map_button.grid(row=2, column=1, pady=5)

        ratio_init = get_hotplug_ratio_status() * 0.20
        ctk.CTkLabel(hotplug_ram_frame, text="Memory ratio:").grid(row=3, column=0, padx=5, pady=5)
        hotplug_ratio_slider = ctk.CTkSlider(hotplug_ram_frame, from_=0, to=psutil.virtual_memory()[0] * 0.20)
        hotplug_ratio_slider.set(ratio_init)
        hotplug_ratio_slider.bind("<B1-Motion>", change_label_ratio)
        hotplug_ratio_slider.grid(row=3, column=1, pady=5)
        rotulo_hotplug_ratio = ctk.CTkLabel(hotplug_ratio_slider, text=str(ratio_init) + "MB")
        rotulo_hotplug_ratio.grid(row=3, column=2)
        ctk.CTkButton(hotplug_ram_frame, text="save ratio val", command=set_hotplug_ratio_status).grid(row=4, column=0, columnspan=2)

    def rende_memory(self, menu):
        self.get_vm_info()
        self.menu = menu
        self.error = event_error.io_error()
        self.memory_system()
        self.rende_vm_info()
        self.rende_thp()
        self.rende_zswap()
        self.rende_zram()
        self.memory_hotplug()