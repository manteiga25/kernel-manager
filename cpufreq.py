import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import LabelFrame
from psutil import cpu_percent
from os import path, listdir
import threading

# retorna o governador atual do nucleo
def get_cpu_governor(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_governor", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

# retorna a lista de todos os governadores disponiveis no kernel
def get_cpu_governors():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors", "r") as gov:
            ret = gov.read().strip().split(" ")
            print(ret)
            ret = [governor.strip() for governor in ret]
            return ret
    except:
        return "err"

def get_cpu_preference(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/energy_performance_preference", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

def get_cpu_preferences():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_available_preferences", "r") as gov:
            ret = gov.read().split(" ")
            ret = [governor.strip() for governor in ret if governor.strip()]
            return ret
    except:
        return "err"

def set_cpu_preference(num_core, governador):
    try:
        print(governador)
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/energy_performance_preference", "w") as gov:
            gov.write(governador)
    except Exception as e:
        CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

def get_cpu_current_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_cur_freq", "r") as gov:
            return gov.read().strip()
    except:
        return 0

def get_cpu_max_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_max_freq", "r") as gov:
            return gov.read().strip()
    except:
        return 0

def get_cpu_min_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_min_freq", "r") as gov:
            return gov.read().strip()
    except:
        return 0

def set_cpu_governor(num_core, governador):
    try:
        print(governador)
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_governor", "w") as gov:
            gov.write(governador)
    except Exception as e:
        CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

def muda_estado_core(num_core, state):
    print("core state = ", state)
   # try:
    with open(f"/sys/devices/system/cpu/cpu{num_core}/online", "w") as gov:
        gov.write(str(state))
    #except Exception as e:
     #   raise Exception()
      #  CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

def get_estado_core(num_core):
    if num_core == 0: # 1 thread tem de estar reservada para o funcionamento
        return 1
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/online", "r") as gov:
            print(num_core)
            ret = int(gov.read().strip())
            print(ret)
            return ret
        #    if ret == "1":
         #       print("yupii")
          #      return 1
           # else:
            #    return 0
    except:
        print("err")

def get_core_table_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_available_frequencies", "r") as gov:
            ret = gov.read().split(" ")
            ret = [freq.strip() for freq in ret if freq.strip()]
            return ret
    except:
        return "err"

def get_core_min_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_min_freq", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

def set_core_min_freq(num_core, freq):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_min_freq", "w") as gov:
            gov.write(freq)
    except Exception as e:
        CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

def get_core_max_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_max_freq", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

def set_core_max_freq(num_core, freq):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/scaling_max_freq", "w") as gov:
            gov.write(freq)
    except Exception as e:
        CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

class cpu_freq:

    # tentativa de otimização
    def get_min_cores_scaling_freq(self, num_cores):
        cores_min_freq = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/scaling_min_freq", "r") as fd:
                    cores_min_freq[core] = fd.read().strip()
            except:
                print("err")
        return cores_min_freq

    def get_max_cores_scaling_freq(self, num_cores):
        cores_max_freq = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/scaling_max_freq", "r") as fd:
                    cores_max_freq[core] = fd.read().strip()
            except:
                print("err")
        return cores_max_freq

    def get_min_cores_freq(self, num_cores):
        cores_min_freq = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/cpuinfo_min_freq", "r") as fd:
                    cores_min_freq[core] = int(fd.read().strip())
            except:
                print("err")
        return cores_min_freq

    def get_max_cores_freq(self, num_cores):
        cores_max_freq = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/cpuinfo_max_freq", "r") as fd:
                    cores_max_freq[core] = int(fd.read().strip())
            except:
                print("err")
        return cores_max_freq

    def get_list_cores_freq(self, num_cores):
        list_table_freq = []
        min_freq = self.get_min_cores_freq(num_cores)
        max_freq = self.get_max_cores_freq(num_cores)
        for max_f, min_f in zip(max_freq, min_freq):
            list_freqs = [str(min_f)]
            while min_f < max_f:
                min_f += 100000
                list_freqs.append(str(min_f))
             #   print(list_freqs)
            list_table_freq.append(list_freqs)
        print(list_table_freq)
        return list_table_freq

    def get_cores_freq_table(self, num_cores):
        cores_freq_table = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/scaling_available_frequencies", "r") as fd:
                    freqs = fd.read().split(" ")
                    freqs = [freq.strip() for freq in freqs if freq.strip()]
                    cores_freq_table[core] = freqs
            except:
                cores_freq_table[core] = ["0"]
        return cores_freq_table

    def get_cores_governor(self, num_cores):
        core_governor = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/scaling_governor", "r") as gov:
                    core_governor[core] = gov.read().strip()
            except:
                core_governor[core] = "err"
        return core_governor
    
    def get_cores_preference(self, num_core):
        core_preference = list(range(num_core))
        for core in range(num_core):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/energy_performance_preference", "r") as gov:
                    core_preference[core] = gov.read().strip()
            except:
                core_preference[core] = "err"
        return core_preference

    # alguns drivers, politicas, etc... podem mudar a frequencia maxima e minima do processador automaticamente mesmo que o utilizador tenha definid uma frequencia especifica
    def check_system_change_core_freq(self, core, file):
        print(core, file)
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/scaling_{file}_freq", "r") as fd:
                self.lista_max_freq_core[core].set(fd.read().strip())
        except:
            pass

    def muda_core_min_freq(self, core):
        min_freq = self.lista_min_freq_core[core].get()
        if int(min_freq) > int(self.lista_max_freq_core[core].get()):
            CTkMessagebox(title="Valor inválido", message="A Frequência mínima tem de ser menor que a frequência maxima.", icon="cancel")
            self.lista_min_freq_core[core].set(get_core_min_freq(core))
            return
        set_core_min_freq(core, min_freq)
        threading.Timer(2.0, self.check_system_change_core_freq, args=(core, "min",)).start()

    def muda_core_max_freq(self, core):
        max_freq = self.lista_max_freq_core[core].get()
        if int(max_freq) < int(self.lista_min_freq_core[core].get()):
            CTkMessagebox(title="Valor inválido", message="A Frequência maxima tem de ser maior que a frequência mínima.", icon="cancel")
            self.lista_max_freq_core[core].set(get_core_max_freq(core))
            return
        set_core_max_freq(core, max_freq)
        threading.Timer(2.0, self.check_system_change_core_freq, args=(core, "max",)).start()

    def get_bios_cpufreq(self, num_cores):
        bios_freq_state = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/bios_limit", "r") as fd:
                    bios_freq_state[core] = int(fd.read().strip())
            except:
                print("err")
                bios_freq_state[core] = 0
        return bios_freq_state
    
    def muda_bios_cpufreq(self, state, core):
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/cpufreq/bios_limit", "w") as fd:
                fd.write(str(state))
        except:
            self.lista_state_bios_cpufreq[core].select() if not state else self.lista_state_bios_cpufreq[core].deselect()
            CTkMessagebox(title="Erro", message="Não foi possível mudar o valor", icon="cancel")

    def get_bias_energy_state(self, num_cores):
        modes = {"0": "performance", "4": "balance-performance", "6": "normal", "8": "balance-power", "15": "power"}
        bias_energy_state = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open(f"/sys/devices/system/cpu/cpu{core}/power/energy_perf_bias", "r") as fd:
                    val = fd.read().strip()
                    print(val)
                    bias_energy_state[core] = modes[val]
            except:
                print(modes)
                bias_energy_state[core] = "unknown"
        return bias_energy_state
    
    def muda_bias_energy(self, state, core):
        modes = {"performance": 0, "balance-performance": 4, "normal": 6, "balance-power": 8, "power": 15}
        try:
            with open(f"/sys/devices/system/cpu/cpu{core}/power/energy_perf_bias", "w") as fd:
                fd.write(str(modes[state]))
        except:
        #    self.lista_energy_bias[core].select() if not state else self.lista_state_bios_cpufreq[core].deselect()
            CTkMessagebox(title="Erro", message="Não foi possível mudar o valor\n" + str(Exception), icon="cancel")

    def muda_governador(self, governor, core):
            print(core)
            print(self.lista_governadores[core].get())
           # governador = self.lista_governadores[core].get()
          #  governador = event.widget.get()
            #print(governador)
            if governor == get_cpu_governor(core):
                return
            set_cpu_governor(core, governor)

    def muda_preferencia(self, core):
            print(core)
            print(self.lista_energy_state[core].get())
            governador = self.lista_energy_state[core].get()
          #  governador = event.widget.get()
            print(governador)
            if governador == get_cpu_preference(core):
                return
            set_cpu_preference(core, governador)

    def muda_state_core(self, core, state):
        try:
            muda_estado_core(core, state)
            self.estado_core[core] = state
        except Exception as e:
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")
            if self.estado_core[core]:
                self.lista_state_core[core].select()
            else:
                self.lista_state_core[core].deselect()
            return
        
       # if state:
        self.state_core[core].configure(text="Enabled" if self.estado_core[core] else "Disabled")
        self.lista_max_freq_core_button[core].configure(state="normal" if self.estado_core[core] else "disabled")
        self.lista_min_freq_core_button[core].configure(state="normal" if self.estado_core[core] else "disabled")
        self.lista_ok[core].configure(state="normal" if self.estado_core[core] else "disabled")
        self.lista_ok_preference[core].configure(state="normal" if self.estado_core[core] else "disabled")
        if self.bios_cpu:
            self.lista_state_bios_cpufreq[core].configure(state="normal" if self.estado_core[core] else "disabled")
#        else:
 #           self.state_core[core].configure(text="Disabled")

    def get_adv_sched_val(self, sched, folders):
        #folders = listdir(f"/sys/devices/system/cpu/cpufreq/{sched}")
        num_folders = len(folders)
        list_folders = list(range(num_folders))
        for folder in range(num_folders):
            try:
                with open(f"/sys/devices/system/cpu/cpufreq/{sched}/{folders[folder]}", "r") as fd:
                    list_folders[folder] = fd.read().strip()
            except:
                list_folders[folder] = "err"
        return list_folders

    def set_adv_sched_param(self, core, sched, folder, val_idx):
        try:
            with open(f"/sys/devices/system/cpu/cpufreq/{sched}/{folder}", "w") as fd:
                fd.write(str(val_idx))
        except:
            print(val_idx, "err")

    def rende_advanced_sched_params(self, core, sched):
        self.win_sched_adv = ctk.CTkToplevel(self.menu)
        self.win_sched_adv.title(f"Advanced Scheduling Parameters - {sched} - {core}")
        ctk.CTkLabel(self.win_sched_adv, text=f"{sched} Advanced Sched for {core} - Generic mode").grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        try:
            folders = listdir(f"/sys/devices/system/cpu/cpufreq/{sched}")
        except FileNotFoundError:
            self.win_sched_adv.destroy()
            CTkMessagebox(title="No params avalable", message="The current governor don´t have params to configure", icon="info")
            return
        num_folders = len(folders)
        list_sched_params = list(range(num_folders))
        list_sched_params_button = list(range(num_folders))
        list_sched_values = self.get_adv_sched_val(sched, folders)
        for folder in range(num_folders):
            if list_sched_values[folder] == "err":
                continue
            folder_param = folders[folder]
            ctk.CTkLabel(self.win_sched_adv, text=folder_param.replace("_", " ") + ":").grid(row=folder+1, column=0, padx=5, pady=5)
            list_sched_params[folder] = ctk.CTkEntry(self.win_sched_adv, placeholder_text=list_sched_values[folder])
            list_sched_params[folder].grid(row=folder+1, column=1, padx=5, pady=5)
            list_sched_params_button[folder] = ctk.CTkButton(self.win_sched_adv, text="Aplicar", command=lambda c=core, idx=folder: self.set_adv_sched_param(c, sched, folders[idx], list_sched_params[idx].get()))
            list_sched_params_button[folder].grid(row=folder+1, column=2, padx=5, pady=5)

    def cpu_freq_frame(self):
        num_cores = int(self.num_cores)
    #    print(self.get_list_cores_freq(num_cores))
        freq_table = self.get_list_cores_freq(num_cores)
        cores_min_freq = self.get_min_cores_scaling_freq(num_cores)
        cores_max_freq = self.get_max_cores_scaling_freq(num_cores)
        cores_freq_table = self.get_cores_freq_table(num_cores)
        cpu_governors = get_cpu_governors()
        cpu_preferences = get_cpu_preferences()
        core_governor = self.get_cores_governor(num_cores)
        core_preferences = self.get_cores_preference(num_cores)
        print(cores_freq_table)
        self.frame_cpu_freq = ctk.CTkScrollableFrame(self.menu, width=980, height=380)
        self.frame_cpu_freq.grid(column=0, row=3, columnspan=2)
        self.label_current_freq = list(range(num_cores))
        self.lista_governadores = list(range(num_cores))
        self.lista_ok = list(range(num_cores))
        self.lista_core_utilization = list(range(num_cores))
        self.lista_energy_state = list(range(num_cores))
        self.lista_state_core = list(range(num_cores))
        self.lista_ok_preference = list(range(num_cores))
        self.estado_core = list(range(num_cores))
        self.state_core = list(range(num_cores))
        self.lista_min_freq_core = list(range(num_cores))
        self.lista_max_freq_core = list(range(num_cores))
        self.lista_min_freq_core_button = list(range(num_cores))
        self.lista_max_freq_core_button = list(range(num_cores))
        self.bios_cpu = False
        self.energy_bias = False
        event = 0
        if path.exists("/sys/devices/system/cpu/cpu0/cpufreq/bios_limit"):
            self.bios_cpu = True
            lista_bios_cpufreq_init_state = self.get_bios_cpufreq(num_cores)
            self.lista_state_bios_cpufreq = list(range(num_cores))
        if path.exists("/sys/devices/system/cpu/cpu0/power/energy_perf_bias"):
            self.energy_bias = True
            lista_bias_energy_init_state = self.get_bias_energy_state(num_cores)
            self.lista_energy_bias = list(range(num_cores))
        for core in range(num_cores):
            print("core ", freq_table[core])
            self.estado_core[core] = get_estado_core(core)
            frame_core = LabelFrame(self.frame_cpu_freq, text="core " + str(core), background='#212121', foreground="white")
            frame_core.grid(row=core // 2, column=core % 2, padx=10)
            self.state_core[core] = ctk.CTkLabel(frame_core, text="Enabled" if self.estado_core[core] else "Disabled")
            self.state_core[core].grid(column=0, row=1, padx=5)
            self.lista_state_core[core] = ctk.CTkSwitch(frame_core, text="Off/On", onvalue=1, offvalue=0, command=lambda c=core: self.muda_state_core(c, self.lista_state_core[c].get()))
            if self.estado_core[core]:
                self.lista_state_core[core].select()
            else:
                self.lista_state_core[core].deselect()
            self.lista_state_core[core].grid(column=1, row=1, padx=5)

            if self.big_little:
                if self.b_cores > 0:
                    self.b_cores -= 1
                    ctk.CTkLabel(frame_core, text="Core Type: Performance").grid(row=2, column=0 ,padx=5, pady=5)
                else:
                    ctk.CTkLabel(frame_core, text="Core Type: Eficiency").grid(row=2, column=0, padx=5, pady=5)

           # print(self.lista_state_core[core].get())
            #print(get_estado_core(core))
            self.lista_core_utilization[core] = ctk.CTkLabel(frame_core)
            self.lista_core_utilization[core].grid(column=0, row=3, columnspan=1, padx=5)
            self.label_current_freq[core] = ctk.CTkLabel(frame_core)
            self.label_current_freq[core].grid(column=0, row=4, columnspan=2, sticky="w", padx=5)

            ctk.CTkLabel(frame_core, text="Max freq:").grid(column=0, row=5, pady=5)
            self.lista_max_freq_core[core] = ctk.CTkComboBox(frame_core, values=freq_table[core], state="readonly")
            self.lista_max_freq_core[core].set(cores_max_freq[core])
            self.lista_max_freq_core_button[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_core_max_freq(c), state="normal" if self.estado_core[core] else "disabled")
            self.lista_max_freq_core[core].grid(column=1, row=5, padx=10, pady=5)
            self.lista_max_freq_core_button[core].grid(column=2, row=5, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Min freq:").grid(column=0, row=6, pady=5)
            self.lista_min_freq_core[core] = ctk.CTkComboBox(frame_core, values=freq_table[core], state="readonly")
            self.lista_min_freq_core[core].set(cores_min_freq[core])
            self.lista_min_freq_core_button[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_core_min_freq(c), state="normal" if self.estado_core[core] else "disabled")
            self.lista_min_freq_core[core].grid(column=1, row=6, padx=10, pady=5)
            self.lista_min_freq_core_button[core].grid(column=2, row=6, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Governador:").grid(column=0, row=7, pady=5)
            self.lista_governadores[core] = ctk.CTkComboBox(frame_core, values=cpu_governors, state="readonly", command=lambda gov=event, c=core: self.muda_governador(gov, c))
            self.lista_governadores[core].set(core_governor[core])
            self.lista_ok[core] = ctk.CTkButton(frame_core, text="Advances sched params" , command=lambda c=core: self.rende_advanced_sched_params(c, self.lista_governadores[c].get()), state="normal" if self.estado_core[core] else "disabled")
         #   self.lista_governadores[core].bind("<ComboboxSelected>", lambda event: self.muda_governador(event, core))
            self.lista_governadores[core].grid(column=1, row=7, padx=10, pady=5)
            self.lista_ok[core].grid(column=2, row=7, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Preference:").grid(column=0, row=8, pady=5)
            self.lista_energy_state[core] = ctk.CTkComboBox(frame_core, values=cpu_preferences, state="readonly")
            self.lista_energy_state[core].set(core_preferences[core])
            self.lista_ok_preference[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_preferencia(c), state="normal" if self.estado_core[core] else "disabled")
            self.lista_energy_state[core].grid(column=1, row=8, padx=10, pady=5)
            self.lista_ok_preference[core].grid(column=2, row=8, padx=10, pady=5)

            if self.bios_cpu:
                ctk.CTkLabel(frame_core, text="Bios limiter freq:").grid(column=0, row=9, padx=10, pady=5)
                self.lista_state_bios_cpufreq[core] = ctk.CTkSwitch(frame_core, text="Off/On", onvalue=1, offvalue=0, state="normal" if self.estado_core[core] else "disabled", command=lambda c=core: self.muda_bios_cpufreq(self.lista_state_bios_cpufreq[c].get(), c))
                self.lista_state_bios_cpufreq[core].select() if lista_bios_cpufreq_init_state[core] else self.lista_state_bios_cpufreq[core].deselect()
                #.set(lista_bios_cpufreq_init_state[core])
                self.lista_state_bios_cpufreq[core].grid(column=1, row=9, padx=10, pady=5)
            
            if self.energy_bias:
                ctk.CTkLabel(frame_core, text="Bias energy:").grid(column=0, row=10, padx=10, pady=5)
                self.lista_energy_bias[core] = ctk.CTkComboBox(frame_core, values=["performance", "balance-performance", "normal", "balance-power", "power"], state="readonly")
                self.lista_energy_bias[core].set(lista_bias_energy_init_state[core])
                #.set(lista_bios_cpufreq_init_state[core])
                self.lista_energy_bias[core].grid(column=1, row=10, padx=10, pady=5)
                ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_bias_energy(self.lista_energy_bias[c].get(), c), state="normal" if self.estado_core[core] else "disabled").grid(column=2, row=10, padx=10, pady=5)

        self.lista_state_core[0].configure(state="disabled") # o kernel não permite modificar o estado desse nucleo para o funcionamento do sistema
       # self.update_current_freq_label()

    def update_current_freq_label(self):
        core_util = cpu_percent(interval=None, percpu=True)
        #cores_min_freq = self.get_min_cores_scaling_freq(int(self.num_cores))
        #cores_max_freq = self.get_max_cores_scaling_freq(int(self.num_cores))
        for index in range(int(self.num_cores)):
#            print(index)
            if self.estado_core[index]:
                self.label_current_freq[index].configure(text="Current freq: " + str(round(int(get_cpu_current_freq(index)) / 1000)) + " MHz")
                try:
                    self.lista_core_utilization[index].configure(text="Utilization: " + str(int(core_util[index])) + "%")
                   # self.lista_min_freq_core[index].set(cores_min_freq[index])
                    #self.lista_max_freq_core[index].set(cores_max_freq[index])
                except:
                    print("idk")
                #self.tarefa = self.label_current_freq[index].after(1000, lambda: self.update_current_freq_label(index))
            else:
                self.lista_core_utilization[index].configure(text="Utilization: 0 %")
                self.label_current_freq[index].configure(text="Current freq: Disabled")
               # self.tarefa = self.label_current_freq[index].after(1000, self.update_current_freq_label(index))
        self.state_task = self.frame_cpu_freq.after(1000, self.update_current_freq_label)

    def cpu_driver_frame(self):
        if path.exists("/sys/devices/system/cpu/intel_pstate/"):
            self.cpu_driver_state = "intel_pstate"
            self.rende_cpu_driver_intel()
        elif path.exists("/sys/devices/system/cpu/amd_pstate/"):
            self.cpu_driver_state = "amd_pstate"
            self.rende_cpu_driver_amd()

    def get_cpu_driver_state_mode(self):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/status", "r") as fd:
                return fd.read().strip()
        except:
            print("hvgvc")

    def set_cpu_driver_state_mode(self, value):
        if self.pstate_mode == value: # evita gasto computacional elevado
            return
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/status", "w") as fd:
                fd.write(value)
            self.pstate_mode = value
            if value == "passive":
                self.label_hwp.grid_forget()
                self.hwp_dynamin_boost.grid_forget()
            elif value == "active":
                self.label_hwp.grid(row=4, column=0, padx=5, pady=5)
                self.hwp_dynamin_boost.grid(row=4, column=1, padx=5, pady=5)
            self.restart_governors()
        except:
            print("hvgvc")
    
    def get_cpu_driver_no_turbo_mode(self):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/no_turbo", "r") as fd:
                return int(fd.read().strip())
        except:
            print("hvgvc")

    def set_cpu_driver_no_turbo_mode(self, value):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/no_turbo", "w") as fd:
                fd.write(str(value))
        except:
            print("hvgvc")
    
    def get_cpu_driver_pct_max_val(self):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/max_perf_pct", "r") as fd:
                return int(fd.read().strip())
        except:
            print("hvgvc")

    def set_cpu_driver_pct_max_val(self, value):
        value = int(value)
        try:
            if value < self.min_pct_val:
                self.max_perf_pct_value.set(self.min_pct_val)
                value = self.min_pct_val
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/max_perf_pct", "w") as fd:
                fd.write(str(value))
            self.max_pct_val = value
            self.label_max_pct.configure(text=str(value) + "%")
        except:
            print("hvgvc")
    
    def get_cpu_driver_pct_min_val(self):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/min_perf_pct", "r") as fd:
                return int(fd.read().strip())
        except:
            print("hvgvc")

    def set_cpu_driver_pct_min_val(self, value):
        value = int(value)
        print(value)
        try:
            if value > self.max_pct_val:
                self.min_perf_pct_value.set(self.max_pct_val)
                value = self.max_pct_val
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/min_perf_pct", "w") as fd:
                fd.write(str(value))
            self.min_pct_val = value
            self.label_min_pct.configure(text=str(value) + "%")
        except:
            print("hvgvc")

    def get_cpu_driver_hwp_mode(self):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/hwp_dynamic_boost", "r") as fd:
                return int(fd.read().strip())
        except:
            print("hvgvc")

    def set_cpu_driver_hwp_mode(self, value):
        try:
            with open(f"/sys/devices/system/cpu/{self.cpu_driver_state}/hwp_dynamic_boost", "w") as fd:
                fd.write(str(value))
        except:
            print("hvgvc")

    def rende_cpu_driver_intel(self):
        self.pstate_mode = self.get_cpu_driver_state_mode()
        self.max_pct_val = self.get_cpu_driver_pct_max_val()
        self.min_pct_val = self.get_cpu_driver_pct_min_val()
        frame_intel_pstate = LabelFrame(self.frame_cpu_freq, text="Intel P-state", background='#212121', foreground="white")
        frame_intel_pstate.grid(column=0)
        ctk.CTkLabel(frame_intel_pstate, text="Intel P-state mode").grid(row=0, column=0, padx=5, pady=5)
        self.intel_pstate_mode = ctk.CTkComboBox(frame_intel_pstate, values=["active", "passive", "off"], state="readonly", command=self.set_cpu_driver_state_mode)
        self.intel_pstate_mode.set(self.pstate_mode)
        self.intel_pstate_mode.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_intel_pstate, text="No turbo:").grid(row=1, column=0, padx=5, pady=5)
        self.no_turbo_mode = ctk.CTkSwitch(frame_intel_pstate, text="Off/On", command=lambda: self.set_cpu_driver_no_turbo_mode(self.no_turbo_mode.get()))
        if self.get_cpu_driver_no_turbo_mode():
            self.no_turbo_mode.select()
        self.no_turbo_mode.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_intel_pstate, text="Max pct value:").grid(row=2, column=0, padx=5, pady=5)
        self.max_perf_pct_value = ctk.CTkSlider(frame_intel_pstate, from_=0, to=100, command=self.set_cpu_driver_pct_max_val)
        self.max_perf_pct_value.set(self.max_pct_val)
        self.max_perf_pct_value.grid(row=2, column=1, padx=5, pady=5)
        self.label_max_pct = ctk.CTkLabel(frame_intel_pstate, text=str(self.max_pct_val) + "%")
        self.label_max_pct.grid(row=2, column=2, padx=5, pady=5)
        ctk.CTkLabel(frame_intel_pstate, text="Min pct value:").grid(row=3, column=0, padx=5, pady=5)
        self.min_perf_pct_value = ctk.CTkSlider(frame_intel_pstate, from_=0, to=100, command=self.set_cpu_driver_pct_min_val)
        self.min_perf_pct_value.set(self.min_pct_val)
        self.min_perf_pct_value.grid(row=3, column=1, padx=5, pady=5)
        self.label_min_pct = ctk.CTkLabel(frame_intel_pstate, text=str(self.min_pct_val) + "%")
        self.label_min_pct.grid(row=3, column=2, padx=5, pady=5)
        self.label_hwp = ctk.CTkLabel(frame_intel_pstate, text="hwp dynamic boost:")
        self.hwp_dynamin_boost = ctk.CTkSwitch(frame_intel_pstate, text="Off/On", command=lambda: self.set_cpu_driver_hwp_mode(self.hwp_dynamin_boost.get()))
        if self.get_cpu_driver_hwp_mode():
            self.hwp_dynamin_boost.select()
        if self.pstate_mode == "active":
            self.label_hwp.grid(row=4, column=0, padx=5, pady=5)
            self.hwp_dynamin_boost.grid(row=4, column=1, padx=5, pady=5)

    def rende_cpu_driver_amd(self):

        self.pstate_mode = self.get_cpu_driver_state_mode()
        self.max_pct_val = self.get_cpu_driver_pct_max_val()
        self.min_pct_val = self.get_cpu_driver_pct_min_val()
        frame_amd_pstate = LabelFrame(self.frame_cpu_freq, text="amd P-state", background='#212121', foreground="white")
        frame_amd_pstate.grid(column=0)
        ctk.CTkLabel(frame_amd_pstate, text="Amd P-state mode").grid(row=0, column=0, padx=5, pady=5)
        self.amd_pstate_mode = ctk.CTkComboBox(frame_amd_pstate, values=["active", "passive", "guided", "disable"], state="readonly", command=self.set_cpu_driver_state_mode)
        self.amd_pstate_mode.set(self.pstate_mode)
        self.amd_pstate_mode.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_amd_pstate, text="Highest perf:").grid(row=1, column=0, padx=5, pady=5)
        self.highest_perf = ctk.CTkEntry(frame_amd_pstate, placeholder_text="incomplete")

    # necessary if the user switch cpu driver
    def restart_governors(self):
        cores = int(self.num_cores)
        cpu_governors = get_cpu_governors()
        core_governor = self.get_cores_governor(cores)
        for core in range(cores):
            self.lista_governadores[core].configure(values=cpu_governors)
            self.lista_governadores[core].set(core_governor[core])

    def start_task(self):
        self.update_current_freq_label()

    def cancel_task(self):
        print(self.state_task)
        print("h")
        self.frame_cpu_freq.after_cancel(self.state_task)
      #  self.menu.destroy()
     #   del self.menu
    #    print(self.menu)

    def check_system_is_big_little(self):
        self.big_little = False
        try:
            with open("big_little.txt", "r") as fd:
                info_b_l = fd.read().strip().split(" ")
                self.big_little = True
        except:
            return 0, 0
        return int(info_b_l[0]), int(info_b_l[1]) 

    def rende_cpu_freq(self, menu, num_cores):
        self.b_cores, self.l_cores = self.check_system_is_big_little()
        self.state_task = None
        self.num_cores = num_cores
        self.menu = menu
        self.cpu_freq_frame()
        self.cpu_driver_frame()
