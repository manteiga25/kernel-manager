import customtkinter as ctk
import event_error
import psutil
from platform import uname
from os import listdir, stat, path, system
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
#import CTkTable

class memory:

    def verify_value_is_num(self, value: str):
        if not value.isdigit():
            raise ValueError("The value needs to be integer not string")

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

        def set_thp_defrag_mode(mode):
         #   mode = modo_thp_defrag.get()
            system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/defrag")

        def set_thp_mode(mode):
          #  mode = modo_thp.get()
            system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/enabled")
        
        def set_thp_shm_mode(mode):
           # mode = modo_thp_shm.get()
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

            def set_thp(thp_mode, thp_file):
                print(thp_mode)
             #   state = huge_page[thp].get()
                print(thp_file)
                system(f"echo {thp_mode} > /sys/kernel/mm/transparent_hugepage/{thp_file}/enabled")

          #  huge_page = {}
           # huge_page_ok = {}
            try:
                folders = listdir("/sys/kernel/mm/transparent_hugepage/")
                folders_num = len(folders)
                print(folders_num)
            except:
                folders = ""
                folders_num = 0
            print(folders)
            for folder, index in zip(folders, range(4, folders_num+2)):
                #print(index)
                if path.isdir("/sys/kernel/mm/transparent_hugepage/" + folder):
                  #  print(folder)
                    #if path.exists()
                    try:
                        with open(f"/sys/kernel/mm/transparent_hugepage/{folder}/enabled", "r") as huge_fd:
                            print("opened " + folder)
                            estado = huge_fd.read().strip()
                            ctk.CTkLabel(self.frame_thp, text=folder).grid(row=index, column=0)
                            huge_page = ctk.CTkComboBox(self.frame_thp, values=self.modos, state="readonly", command=lambda v=index, f=folder: set_thp(v, f))
                            mode = get_thp_mode(folder)
                            huge_page.set(mode)
                            #huge_page_ok[folder] = ctk.CTkButton(self.frame_thp, text="Alterar", command=lambda f=folder: set_thp(f))
                            huge_page.grid(pady=5, row=index, column=1)
                            #huge_page_ok[folder].grid(pady=5, row=index, column=2)
                    except:
                        print("erro " + folder)

        def get_thp_zero_page():
            try:
                with open("/sys/kernel/mm/transparent_hugepage/use_zero_page", "r") as fd:
                    return fd.read().strip()
            except:
                print("dhbfuwegbfuwedfywefyheyuweyugwefegbfebfqegfwqg")
                return "0"

        def set_thp_zero_page(mode_zero_page):
            try:
                with open("/sys/kernel/mm/transparent_hugepage/use_zero_page", "w") as fd:
                    fd.write(str(mode_zero_page))
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def rende_khugepaged():
            def get_kthp_defrag():
                try:
                    with open("/sys/kernel/mm/transparent_hugepage/khugepaged/defrag", "r") as fd:
                        return fd.read().strip()
                except:
                    print("dhbfuwegbfuwedfywefyheyuweyugwefegbfebfqegfwqg")
                    return "0"

            def set_kthp_defrag(mode):
                try:
                    with open("/sys/kernel/mm/transparent_hugepage/khugepaged/defrag", "w") as fd:
                        fd.write(str(mode))
                except Exception as e:
                    CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

            def get_khuge_info(folder):
                try:
                    with open(f"/sys/kernel/mm/transparent_hugepage/khugepaged/{folder}", "r") as fd:
                        return fd.read().strip()
                except:
                    print("dhbfuwegbfuwedfywefyheyuweyugwefegbfebfqegfwqg")
                    return "0"
            
            def set_kthp_info(mode, folder):
                try:
                    self.verify_value_is_num()
                    with open(f"/sys/kernel/mm/transparent_hugepage/khugepaged/{folder}", "w") as fd:
                        fd.write(str(mode))
                except ValueError as e:
                    CTkMessagebox(title="value invalid", message=str(e), icon="cancel")
                except Exception as e:
                    CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

            frame_khugepaged = LabelFrame(self.frame_memory, text="Khugepaged", background='#212121', foreground="white", labelanchor="n")
            frame_khugepaged.grid(pady=5, column=1, row=3, sticky="nsew", padx=5, rowspan=1)
            folders = ["alloc_sleep_millisecs", "scan_sleep_millisecs", "pages_to_scan"]
            entry_khuge = list(range(3))

            ctk.CTkLabel(frame_khugepaged, text="Defrag").grid(row=0, column=0, padx=5, pady=5)
            modo_kthp_defrag = ctk.CTkSwitch(frame_khugepaged, text="Off/On", command=lambda: set_kthp_defrag(modo_kthp_defrag.get()))
            if get_kthp_defrag() == "1":
                modo_kthp_defrag.select()
            modo_kthp_defrag.grid(row=0, column=1, padx=5, pady=5)

            for folder, row in zip(folders, range(1, 3)):
                ctk.CTkLabel(frame_khugepaged, text=folder.replace("_", " ") + ":").grid(row=row, column=0, padx=5, pady=5)
                entry_khuge[row-1] = ctk.CTkEntry(frame_khugepaged, placeholder_text=get_khuge_info(folder))
                entry_khuge[row-1].grid(row=row, column=1, padx=5, pady=5)
                ctk.CTkButton(frame_khugepaged, text="Aplicar alteração", command=lambda f=folder, r=row-1: set_kthp_info(entry_khuge[r].get(), folder)).grid(row=row, column=2, padx=5, pady=5)

        if not path.exists("/sys/kernel/mm/transparent_hugepage"):
            return

        self.frame_thp = LabelFrame(self.frame_memory, text="Transparent Huge Page", background='#212121', foreground="white", labelanchor="n")
        self.frame_thp.grid(pady=5, column=0, row=3, sticky="nsew", padx=5, rowspan=3)
        self.modos = get_thp_modes("enabled")
        modo = get_thp_mode("enabled")
        ctk.CTkLabel(self.frame_thp, text="Transparent Huge Page mode").grid(row=0, column=0, padx=5, pady=5)
        modo_thp = ctk.CTkComboBox(self.frame_thp, values=self.modos, state="readonly", command=set_thp_mode)
        modo_thp.set(modo)
        modo_thp.grid(row=0, column=1, padx=5, pady=5)
       # ctk.CTkButton(self.frame_thp, text="Alterar", command=set_thp_mode).grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.frame_thp, text="Defrag").grid(row=1, column=0, padx=5, pady=5)
        modo_thp_defrag = ctk.CTkComboBox(self.frame_thp, values=get_thp_modes("defrag"), state="readonly", command=set_thp_defrag_mode)
        modo_thp_defrag.set(get_thp_mode("defrag"))
        modo_thp_defrag.grid(row=1, column=1, padx=5, pady=5)
       # ctk.CTkButton(self.frame_thp, text="Alterar", command=set_thp_defrag_mode).grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.frame_thp, text="Shared mem").grid(row=2, column=0, padx=5, pady=5)
        modo_thp_shm = ctk.CTkComboBox(self.frame_thp, values=get_thp_modes("shmem_enabled"), state="readonly", command=set_thp_shm_mode)
        modo_thp_shm.set(get_thp_mode("shmem_enabled"))
        modo_thp_shm.grid(row=2, column=1, padx=5, pady=5)
     #   ctk.CTkButton(self.frame_thp, text="Alterar", command=set_thp_shm_mode).grid(row=2, column=2, padx=5, pady=5)
        
        ctk.CTkLabel(self.frame_thp, text="Zero page").grid(row=3, column=0, padx=5, pady=5)
        modo_thp_zero_page = ctk.CTkSwitch(self.frame_thp, text="Off/On", command=lambda: set_thp_zero_page(modo_thp_zero_page.get()))
        if get_thp_zero_page() == "1":
            modo_thp_zero_page.select()
        modo_thp_zero_page.grid(row=3, column=1, padx=5, pady=5)

        get_thp_info()
        rende_khugepaged()

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
            except Exception as e:
                self.error.escreve_erro(f"Error to set memory {folder}", str(e))
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

    def set_memory_param(self):
        change = {}
        try:
            for var, key in zip(self.entry_vars.keys(), self.vm_info.keys()):
                print(f"{str(var)} {self.vm_info[var]} != {self.entry_vars[var].get()}")
                tmp = self.entry_vars[var].get() # increase cache hit and less instruction executing
                self.verify_value_is_num(tmp)
                if self.vm_info[var] != tmp:
                #    self.set_memory_info(var)
                    change[var] = tmp
        except ValueError as e:
            CTkMessagebox(title="value invalid", message=str(e), icon="cancel")
        if change:
            self.set_memory_info(change)

    def rende_vm_info(self):
        self.vm_info, file_perm = self.get_vm_info()
        self.entry_vars = {}
        self.vm_widget = {}
        frame_vm_info = LabelFrame(self.frame_memory, text="VM info", background='#212121', foreground="white", labelanchor="n")
        frame_vm_info.grid(column=0, row=1, columnspan=6)
    #    frame_vm_info.grid(column=0, row=1)
        for info, local in zip(self.vm_info.keys(), range(len(self.vm_info))):
          #  row = local // 3
           # col = (local % 3) * 3
            if file_perm[info] == 33188:
                row = local // 3
                col = (local % 3) * 3
                ctk.CTkLabel(frame_vm_info, text=info.replace("_", " ") + " : ", justify="left").grid(padx=5, row=row, column=col)
                self.entry_var = ctk.StringVar()
                self.entry_var.set(self.vm_info[info])
                self.entry_vars[info] = self.entry_var
                #self.entry_vars[info] = vm_info[info]
                #ctk.CTkEntry(frame_vm_info, placeholder_text=vm_info[info], justify="left").grid(padx=5, row=local, column=1)
              #  self.vm_widget[info] = ctk.CTkEntry(frame_vm_info, textvariable=self.entry_var, placeholder_text=self.vm_info[info], justify="left").grid(padx=5, pady=5, row=local, column=1)
                self.vm_widget[info] = ctk.CTkEntry(frame_vm_info, textvariable=self.entry_var, justify="left").grid(padx=5, pady=5, row=row, column=col+1)
                col += 3
       #     else:
        #        ctk.CTkLabel(frame_vm_info, text=info.replace("_", " ") + " : ").grid(padx=5, pady=5, row=row, column=col)
         #       ctk.CTkLabel(frame_vm_info, text=self.vm_info[info] + " (read-only)").grid(padx=5, pady=5, row=row, column=col+1, sticky="w")

        ctk.CTkButton(frame_vm_info, text="Salvar alterações", width=200, height=40, command=self.set_memory_param).grid(columnspan=6, pady=5, column=1)

    def update_mem_info(self): # código feito com preguiça
            mem_text = ["Disponível: ", "usado: "]
            aux = [1, 3]
            memory_info = psutil.virtual_memory()
            for i in range(2):
                self.mem[i].configure(text=mem_text[i] + str(round(memory_info[aux[i]] / 1024 / 1024 / 1024, 1)) + "GB")
            self.mem_bar.set(round(memory_info[2] / 100, 2))
            self.task = self.mem_bar.after(1000, self.update_mem_info)

    def rende_memory_bar(self):
        self.mem = list(range(2))
        frame_mem = ctk.CTkFrame(self.frame_memory, width=350, height=100)
        frame_mem.grid(row=0, column=0, columnspan=2)
        self.mem_ram_pc = psutil.virtual_memory()[0]
     #   ctk.CTkLabel(self.frame_memory, text="Memory RAM size: " + str(round(psutil.virtual_memory()[0] / 1024 / 1024 / 1024, 1)) + "GB").grid(row=0, column=3, columnspan=2, padx=0, pady=5, sticky="w")
        ctk.CTkLabel(frame_mem, text="Memory RAM size: " + str(round(self.mem_ram_pc / 1024 / 1024 / 1024, 1)) + "GB").place(x=60, y=10)
        for i in range(2):
            self.mem[i] = ctk.CTkLabel(frame_mem)
       # mem[0].grid(row=1, column=2, columnspan=2, padx=5, sticky="ew", pady=5)
       # mem[1].grid(row=1, column=4, columnspan=2, padx=5, sticky="ew", pady=5)
        self.mem_bar = ctk.CTkProgressBar(frame_mem, orientation="horizontal", width=250, height=30)
        #mem_bar.grid(row=2, column=3, rowspan=2, columnspan=6, sticky="ew", padx=5, pady=5)
        self.mem_bar.place(x=10, y=60)
        self.mem[0].place(x=20, y=30)
        self.mem[1].place(x=160, y=30)

        self.update_mem_info()

    def start_task(self):
        self.update_mem_info()

    def cancel_task(self):
        self.mem_bar.after_cancel(self.task)

    def memory_system(self):
        self.frame_memory = ctk.CTkScrollableFrame(self.menu, width=1080, height=800)
        self.frame_memory.grid(column=0, row=3, columnspan=6, sticky="ew")
        self.rende_memory_bar()

    def rende_hugepage_1gb(self):
        def get_1gb_huge(folder):
            try:
                with open(f"/sys/kernel/mm/hugepages/hugepages-1048576kB/{folder}", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"

        def set_1gb_huge(folder, idx):
            value = entry_hp[idx].get()
            try:
                self.verify_value_is_num(value)
                with open(f"/sys/kernel/mm/hugepages/hugepages-1048576kB/{folder}", "w") as fd:
                    fd.write(value)
            except ValueError as e:
                CTkMessagebox(title="value invalid", message=str(e), icon="cancel")
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        if round(self.mem_ram_pc / 1024 / 1024 / 1024, 1) < 30.0:
            return

        hugepage_1bg = LabelFrame(self.frame_memory, text="Hugepage 1gb", background='#212121', foreground="white", labelanchor="n")
        hugepage_1bg.grid(row=4, column=1, padx=5, pady=5)
        folders = ["nr_hugepages", "nr_overcommit_hugepages"]
        labels = ["Nr hugepages 1gb:", "overcommit_hugepages:"]
        entry_hp = list(range(2))

        for folder, label, row in zip(folders, labels, range(2)):
            ctk.CTkLabel(hugepage_1bg, text=label).grid(row=row, column=0, padx=5, pady=5)
            entry_hp[row] = ctk.CTkEntry(hugepage_1bg, placeholder_text=get_1gb_huge(folder))
            entry_hp[row].grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkButton(hugepage_1bg, text="Aplicar alteração", command=lambda f=folder, index=row: set_1gb_huge(f, index)).grid(row=row, column=2, padx=5, pady=5)

    def rende_zswap(self):
        if not path.exists("/sys/module/zswap"):
            return
        
        def switch_zswap(folder, index):
            state = "N"
            if zswap_state[index].get():
                state = "Y"
            print(state)
            try:
                with open(f"/sys/module/zswap/parameters/{folder}", "w") as f:
                    f.write(state)
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

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
            try:
                with open("/sys/module/zswap/parameters/max_pool_percent", "w") as f:
                    f.write(value)
                pool_perc.configure(text=value + "%")
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_thre_perc():
            try:
                with open("/sys/module/zswap/parameters/accept_threshold_percent", "r") as f:
                    return int(f.read().strip()) / 100
            except:
                print("err")
                return 0

        def switch_thre_value(event):
            value = str(int(float(threshold.get()) * 100))
            try:
                with open("/sys/module/zswap/parameters/accept_threshold_percent", "w") as f:
                    f.write(value)
                threshold_perc.configure(text=value + "%")
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

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
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")
            
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
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        self.frame_zswap = LabelFrame(self.frame_memory, text="Zswap", background='#212121', foreground="white", labelanchor="n")
        self.frame_zswap.grid(row=2, column=1, columnspan=6, pady=5, padx=5)
        zswap_feature_bool_name = ["Zswap state", "shrinker", "exclusive loads", "same filled pages", "non same filled pages"]
        zswap_feature_bool_folder =  ["enabled", "shrinker_enabled", "exclusive_loads", "same_filled_pages_enabled", "non_same_filled_pages_enabled"]
        zswap_state = list(range(5))
        for name_index in range(5):
            ctk.CTkLabel(self.frame_zswap, text=zswap_feature_bool_name[name_index]).grid(row=name_index, column=0, pady=5)
            zswap_state[name_index] = ctk.CTkSwitch(self.frame_zswap, text="Off/On", onvalue=1, offvalue=0, command=lambda index=name_index: switch_zswap(zswap_feature_bool_folder[index], index))
            if get_zswap_state(zswap_feature_bool_folder[name_index]) == "Y":
                zswap_state[name_index].select()
            else:
                zswap_state[name_index].deselect()
            zswap_state[name_index].grid(row=name_index, column=1, pady=5, padx=5)
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
        algoritmo_zswap = ctk.CTkComboBox(self.frame_zswap, values=["lz4", "lz4hc", "lzo", "lzo-rle", "zstd", "deflate", "842"], state="readonly")
        algoritmo_zswap.set(get_zswap_compressor())
        algoritmo_zswap.grid(row=7, column=1)
        ctk.CTkButton(self.frame_zswap, text="Alterar", command=set_zswap_algorithm).grid(row=7, column=2)

        ctk.CTkLabel(self.frame_zswap, text="Zpool alghoritm").grid(row=8, column=0, padx=0, pady=5)
        algoritmo_zpool = ctk.CTkComboBox(self.frame_zswap, values=["zbud", "z3fold", "zsmalloc"], state="readonly")
        algoritmo_zpool.set(get_zpool_compressor())
        algoritmo_zpool.grid(row=8, column=1)
        ctk.CTkButton(self.frame_zswap, text="Alterar", command=set_zpool_algorithm).grid(row=8, column=2)

    def rende_zram(self):
        if not path.exists(f"/lib/modules/{uname().release}/kernel/drivers/block/zram"):
            return

        def switch_zram():
            if zram_button.get():
                system("sudo modprobe zram")
                zram_button.configure(text="Desativar zram")
                zram_status.configure(text="Zram habilitado")
                self.create_zram()
            else:
                if self.zram_used:
                    self.zram_used = False
                    system("sudo swapoff /dev/zram0")
                    system("sudo echo 1 > /sys/block/zram0/reset")
                system("sudo rmmod zram")
                for widget in self.frame_zram.winfo_children():
                    widget.destroy()
                self.frame_zram.destroy()
                self.rende_zram()
            #    zram_button.configure(text="Ativar zram")
             #   zram_status.configure(text="Zram desabilitado")

        self.frame_zram = LabelFrame(self.frame_memory, text="ZRAM", background='#212121', foreground="white", labelanchor="n")
        self.frame_zram.grid(row=6, column=1, rowspan=2, padx=5, pady=5)

        zram_status = ctk.CTkLabel(self.frame_zram, text="Zram desabilitado")
        zram_status.grid(row=0, column=0, padx=5, pady=5)
        zram_init = path.exists("/sys/devices/virtual/block/zram0")
        print(zram_init)
        zram_button = ctk.CTkSwitch(self.frame_zram, text="Ativar Zram", command=switch_zram)
        self.zram_used = False
        if zram_init:
            zram_button.select()
            zram_status.configure(text="Zram habilitado.")
            zram_button.configure(text="Desativar zram")
            self.create_zram()
        zram_button.grid(row=0, column=1)

    def create_zram(self):
        def get_zram_algorithm():
                try:
                    with open("/sys/block/zram0/comp_algorithm", "r") as fd:
                        return fd.read().strip()
                except:
                    return "err"

        def set_zram_algorithm(value):
            print(self.zram_used)
            if self.zram_used:
                system("sudo swapoff /dev/zram0")
                system("sudo echo 1 > /sys/block/zram0/reset")
            system(f"echo {value} > /sys/block/zram0/comp_algorithm")
            if self.zram_used:
                system(f"swapon --priority {self.zram_priority.get()} /dev/zram0")

        def change_slide_val(event):
            zram_s.configure(text=str(round(zram_size.get() / 1024 / 1024 / 1024, 1)) + " GB")

        def set_zram_size(prio):
            zram_nsize = zram_size.get()
            print(round(zram_nsize / 1024 / 1024 / 1024, 1), " GB")
            try:
                if self.zram_used:
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
        
        
        self.zram_priority = ctk.StringVar(value=get_zram_disk_prio())
        ctk.CTkLabel(self.frame_zram, text="Tamanho do zram:").grid(row=1, column=0, padx=5, pady=5)
        zram_size = ctk.CTkSlider(self.frame_zram, from_=0, to=self.mem_ram_pc / 2)
        print(get_zram_size() / 1024 / 1024 / 1024)
        zram_size.set(get_zram_size())
        zram_size.bind('<Button-1>', change_slide_val)
        zram_size.bind("<B1-Motion>", change_slide_val)
        zram_size.grid(row=1, column=1, padx=5, pady=5)
        zram_disp_size = get_zram_size()
        self.zram_used = True if zram_disp_size else False
        zram_s = ctk.CTkLabel(self.frame_zram, text=str(round(zram_disp_size / 1024 / 1024 / 1024, 1)) + " GB")
        zram_s.grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkLabel(self.frame_zram, text="Zram disk priority:").grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkEntry(self.frame_zram, textvariable=self.zram_priority).grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame_zram, text="Zram algorithm:").grid(row=3, column=0, padx=5, pady=5)
        zram_comp_wid = ctk.CTkComboBox(self.frame_zram, state="readonly", values=get_zram_algorithms(), command=set_zram_algorithm)
        zram_comp_wid.set(get_zram_algorithm())
        zram_comp_wid.grid(row=3, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame_zram, text="max comp streams:").grid(row=4, column=0, padx=5, pady=5)
        zram_max_comp_entry = ctk.CTkEntry(self.frame_zram, placeholder_text=get_zram_max_comp())
        zram_max_comp_entry.grid(row=4, column=1, padx=5, pady=5)
        ctk.CTkButton(self.frame_zram, text="Aplicar alteração", command=set_zram_max_comp).grid(row=4, column=2, padx=5, pady=5)
        ctk.CTkButton(self.frame_zram, text="Criar dispositivo Zram", command=lambda: set_zram_size(self.zram_priority.get())).grid(row=5, column=0, columnspan=3, pady=5, padx=5)

    def memory_hotplug(self):
        if not path.exists("/sys/module/memory_hotplug/parameters"):
            return

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
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

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
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_hotplug_ratio_status():
            try:
                with open("/sys/module/memory_hotplug/parameters/ratio", "r") as fd:
                    return int(fd.read().strip())
            except:
                print("ejfv")
                return 0
        
        def set_hotplug_ratio_status():
            ref_max_val = int((self.mem_ram_pc / 1024 / 1024) * 0.2)
            try:
                new_ratio = int(hotplug_ratio_slider.get())
                if new_ratio > ref_max_val:
                    raise
                with open("/sys/module/memory_hotplug/parameters/ratio", "w") as fd:
                    fd.write(str(new_ratio))
                #    rotulo_hotplug_ratio.configure(text=str(new_ratio) + "MB")
            except:
      #          rotulo_hotplug_ratio.configure(text=str(get_hotplug_ratio_status()) + "MB")
                CTkMessagebox(title="valor invalido", message=f"só é permitido valores inteiros entre 0 e {ref_max_val}.")
                print("ejfv")

    #    def change_label_ratio(event):
     #       rotulo_hotplug_ratio.configure(text=str(int(hotplug_ratio_slider.get())) + "MB")

        hotplug_ram_frame = LabelFrame(self.frame_memory, text="Hotplug Ram", background='#212121', foreground="white", labelanchor="n")
        hotplug_ram_frame.grid(row=5, column=1, padx=5, pady=5)
        ctk.CTkLabel(hotplug_ram_frame, text="O Hotplug Ram é um mecanismo que permite mudar os modulos fisicos de RAM mesmo que o sistema esteja em execução.", justify="center", wraplength=400).grid(padx=5, pady=5, row=0, column=0, columnspan=4)
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
        hotplug_ratio_slider = ctk.CTkEntry(hotplug_ram_frame, placeholder_text=ratio_init)
     #   hotplug_ratio_slider.set(ratio_init)
       # hotplug_ratio_slider.bind("<B1-Motion>", change_label_ratio)
      #  hotplug_ratio_slider.bind("<Button-1>", change_label_ratio)
        hotplug_ratio_slider.grid(row=3, column=1, rowspan=2, pady=5)
      #  rotulo_hotplug_ratio = ctk.CTkLabel(hotplug_ratio_slider, text=str(ratio_init) + "MB")
       # rotulo_hotplug_ratio.grid(row=3, column=2)
        ctk.CTkButton(hotplug_ram_frame, text="save ratio val", command=set_hotplug_ratio_status).grid(row=3, column=3, padx=5)

    def rende_ksm(self):
        if not path.exists("/sys/kernel/mm/ksm"):
        #    ctk.CTkFrame(self.frame_memory, height=300, width=450).grid(row=2, column=0, padx=5, pady=5)
         #   f.grid(row=2, column=0, padx=5, pady=5)
            return

        def get_ksm_status():
            try:
                with open("/sys/kernel/mm/ksm/run", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"
            
        def set_ksm_status(choice):
            try:
                with open("/sys/kernel/mm/ksm/run", "w") as fd:
                   # fd.write(ksm_button.get())
                   fd.write(choice)
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_ksm_max_cpu_usage():
           # try:
            with open("/sys/kernel/mm/ksm/advisor_max_cpu", "r") as fd:
                return int(fd.read().strip())
            #except:
             #   print("err efvtrt")
              #  return 0
            
        def set_ksm_max_cpu_usage(value):
            try:
                value = str(int(value))
                with open("/sys/kernel/mm/ksm/advisor_max_cpu", "w") as fd:
                    label_cpu_ksm_usage.configure(text=value + "%")
                    fd.write(value)
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_zero_page_status():
            try:
                with open("/sys/kernel/mm/ksm/use_zero_pages", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"

        def set_zero_page():
            try:
                with open("/sys/kernel/mm/ksm/use_zero_pages", "w") as fd:
                    fd.write(ksm_zero_page.get())
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_param_ksm(folder):
            try:
                with open(f"/sys/kernel/mm/ksm/{folder}", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"

        def set_param_ksm(folder, value):
            try:
                if not value.isdigit():
                    raise ValueError("The parameter has been integer not string")
                with open(f"/sys/kernel/mm/ksm/{folder}", "w") as fd:
                    fd.write(value)
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        # tratamento futuro para pages to scan, smart scan?
        entry_params = ["pages_to_scan", "sleep_millisecs", "stable_node_chains_prune_millisecs", "advisor_target_scan_time", "advisor_min_pages_to_scan", "adivsor_max_pages_to_scan"]
        entry_names = ["Pages to scan:", "sleep millisecs:", "Check pages metadata:", "Target scan time:", "Min pages to scan:", "Max pages to scan:"]

        ksm_status_var = ctk.StringVar(value=get_ksm_status())
        ksm_frame = LabelFrame(self.frame_memory, text="KSM", background='#212121', foreground="white", labelanchor="n")
        ksm_frame.grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkLabel(ksm_frame, text="KSM: ").grid(row=0, column=0, padx=5, pady=5)
        ksm_button = ctk.CTkComboBox(ksm_frame, values=["0", "1", "2"], command=set_ksm_status, variable=ksm_status_var, state="readonly")
        #ksm_button.set(get_ksm_status())
        ksm_button.grid(row=0, column=1, pady=5)
        ctk.CTkLabel(ksm_frame, text="KSM cpu usage:").grid(row=1, column=0)
        ksm_cpu_usage_slider = ctk.CTkSlider(ksm_frame, from_=0, to=90, command=set_ksm_max_cpu_usage)
        ksm_cpu_usage_slider.set(int(get_ksm_max_cpu_usage()))
        ksm_cpu_usage_slider.grid(row=1, column=1)
     #   ctk.CTkButton(ksm_frame, text="Alterar", command=set_ksm_max_cpu_usage).grid(row=1, column=2)
        label_cpu_ksm_usage = ctk.CTkLabel(ksm_frame, text=str(get_ksm_max_cpu_usage()) + "%")
        label_cpu_ksm_usage.grid(row=1, column=2, sticky="w")

        ctk.CTkLabel(ksm_frame, text="Use zero page:").grid(row=2, column=0)
        ksm_zero_page = ctk.CTkSwitch(ksm_frame, text="off/on", command=set_zero_page)
        if get_zero_page_status() == "1":
            ksm_zero_page.select()
        ksm_zero_page.grid(row=2, column=1)

        row = 2
        entry_param = list(range(6))
        for label, folder, index in zip(entry_names, entry_params, range(6)):
            row += 1
            ctk.CTkLabel(ksm_frame, text=label).grid(row=row, column=0, padx=5, pady=5)
            entry_param[index] = ctk.CTkEntry(ksm_frame, placeholder_text=get_param_ksm(folder))
            entry_param[index].grid(column=1, row=row, padx=5, pady=5)
            ctk.CTkButton(ksm_frame, text="Aplicar alterações", command=lambda i=index: set_param_ksm(folder, entry_param[i].get())).grid(column=2, row=row, padx=5, pady=5)

    def rende_uksm(self):
        if not path.exists("/sys/kernel/mm/uksm"):
            return

        def get_uksm_status():
            try:
                with open("/sys/kernel/mm/uksm/run", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"
                
        def set_uksm_status(choice):
            try:
                with open("/sys/kernel/mm/uksm/run", "w") as fd:
                # fd.write(ksm_button.get())
                    fd.write(choice)
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_uksm_max_cpu_usage():
            try:
                with open("/sys/kernel/mm/uksm/advisor_max_cpu", "r") as fd:
                    return int(fd.read().strip())
            except:
                return 0
                
        def set_uksm_max_cpu_usage():
            try:
                with open("/sys/kernel/mm/uksm/advisor_max_cpu", "w") as fd:
                    fd.write(str(uksm_cpu_usage_slider.get()))
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_zero_page_status():
            try:
                with open("/sys/kernel/mm/uksm/use_zero_pages", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"
                
        def set_zero_page():
            try:
                with open("/sys/kernel/mm/uksm/use_zero_pages", "w") as fd:
                    fd.write(uksm_zero_page.get())
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_param_uksm(folder):
            try:
                with open(f"/sys/kernel/mm/uksm/{folder}", "r") as fd:
                    return fd.read().strip()
            except:
                return "0"

        def set_param_uksm(folder, value):
            try:
                if not value.isdigit():
                    raise ValueError("The parameter has been integer not string")
                with open(f"/sys/kernel/mm/uksm/{folder}", "w") as fd:
                    fd.write(value)
            except Exception as e:
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        # tratamento futuro para pages to scan, smart scan?
        entry_params = ["pages_to_scan", "sleep_millisecs", "stable_node_chains_prune_millisecs", "advisor_target_scan_time", "advisor_min_pages_to_scan", "adivsor_max_pages_to_scan"]
        entry_names = ["Pages to scan:", "sleep millisecs:", "Check pages metadata:", "Target scan time:", "Min pages to scan:", "Max pages to scan:"]

        uksm_status_var = ctk.StringVar(value=get_uksm_status())
        uksm_frame = LabelFrame(self.frame_memory, text="UKSM", background='#212121', foreground="white", labelanchor="n")
        uksm_frame.grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkLabel(uksm_frame, text="UKSM: ").grid(row=0, column=0, padx=5, pady=5)
        uksm_button = ctk.CTkComboBox(uksm_frame, values=["0", "1", "2"], command=set_uksm_status, variable=uksm_status_var, state="readonly")
        #uksm_button.set(get_ksm_status())
        uksm_button.grid(row=0, column=1, pady=5)
        ctk.CTkLabel(uksm_frame, text="UKSM cpu usage:").grid(row=1, column=0)
        uksm_cpu_usage_slider = ctk.CTkSlider(uksm_frame, from_=0, to=90)
        uksm_cpu_usage_slider.set(get_uksm_max_cpu_usage())
        uksm_cpu_usage_slider.grid(row=1, column=1)
        ctk.CTkButton(uksm_frame, text="Alterar", command=set_uksm_max_cpu_usage).grid(row=1, column=2)

        ctk.CTkLabel(uksm_frame, text="Use zero page:").grid(row=2, column=0)
        uksm_zero_page = ctk.CTkSwitch(uksm_frame, text="off/on", command=set_zero_page)
        if get_zero_page_status() == "1":
            uksm_zero_page.select()
        uksm_zero_page.grid(row=2, column=1)

        row = 2
        entry_param = list(range(6))
        for label, folder, index in zip(entry_names, entry_params, range(6)):
            row += 1
            ctk.CTkLabel(uksm_frame, text=label).grid(column=0, row=row)
            entry_param[index] = ctk.CTkEntry(uksm_frame, placeholder_text=lambda: get_param_uksm(folder))
            entry_param[index].grid(column=1, row=row)
            ctk.CTkButton(uksm_frame, text="Aplicar alterações", command=lambda i=index: set_param_uksm(folder, entry_param[i].get())).grid(column=2, row=row)

    def rende_swap_area(self):
        def get_swap_disks():
            swaps_files = []
            try:
                with open("/proc/swaps", "r") as fd:
                    for swap_text in fd:
                        if not swap_text.find("Filename"):
                            continue
                        print(swap_text)
                        swap_ar = swap_text.split()
                        print(swap_ar)
                        swaps_files.append(swap_ar[0])
                        print(swaps_files)
            except:
                pass
            return swaps_files

        def disable_swap(swap, b_swap, l_swap):
            system(f"sudo swapoff {swap}")
            b_swap.forget()
            l_swap.forget()

        swap_area_frame = LabelFrame(self.frame_memory, text="Swap area", background='#212121', foreground="white", labelanchor="n")
        swap_area_frame.grid(row=9, column=1, padx=5, pady=5)
     #   swaps = get_swap_disks()
        ctk.CTkLabel(swap_area_frame, text="Swap name").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(swap_area_frame, text="Swap button").grid(row=0, column=1, padx=5, pady=5)
       # ctk.CTkLabel(swap_area_frame, text="Swap size").grid(row=0, column=2, padx=5, pady=5)
        row = 1
        for swap in get_swap_disks():
            label_swap = ctk.CTkLabel(swap_area_frame, text=swap)
            label_swap.grid(row=row, column=0, padx=5, pady=5)
            self.buton_swap = ctk.CTkButton(swap_area_frame, text="Disable Swap", command=lambda swap_file=swap, bt_swap=self.buton_swap, l_swap=label_swap: disable_swap(swap_file, bt_swap, l_swap))
            self.buton_swap.grid(row=row, column=1, padx=5, pady=5)
            row += 1

    def rende_memory(self, menu):
        self.task = None
        self.menu = menu
        self.error = event_error.io_error()
        self.memory_system()
        self.rende_vm_info()
        self.rende_hugepage_1gb()
        self.rende_thp()
        self.rende_zswap()
        self.rende_zram()
        self.rende_ksm()
        self.rende_uksm()
        self.memory_hotplug()
   #     self.rende_swap_area()
