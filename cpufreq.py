import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import LabelFrame
from psutil import cpu_percent
from os import path

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
            ret = gov.read().split(" ")
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
    except:
        return "err"

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
    except:
        return "err"

def muda_estado_core(num_core, state):
    print("core state = ", state)
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/online", "w") as gov:
            gov.write(str(state))
    except:
        print("err")

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
    except:
        return "err"

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
    except:
        return "err"

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

    def get_cores_governor(self, num_core):
        core_governor = list(range(num_core))
        for core in range(num_core):
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

    def muda_core_min_freq(self, core):
        min_freq = self.lista_min_freq_core[core].get()
        if int(min_freq) > int(self.lista_max_freq_core[core].get()):
            CTkMessagebox(title="Valor inválido", message="A Frequência mínima tem de ser menor que a frequência maxima.", icon="cancel")
            self.lista_min_freq_core[core].set(get_core_min_freq(core))
            return
        set_core_min_freq(core, min_freq)

    def muda_core_max_freq(self, core):
        max_freq = self.lista_max_freq_core[core].get()
        if int(max_freq) < int(self.lista_min_freq_core[core].get()):
            CTkMessagebox(title="Valor inválido", message="A Frequência maxima tem de ser maior que a frequência mínima.", icon="cancel")
            self.lista_max_freq_core[core].set(get_core_max_freq(core))
            return
        set_core_min_freq(core, max_freq)

    def get_bios_cpufreq(self, num_cores):
        bios_freq_state = list(range(num_cores))
        for core in range(num_cores):
            try:
                with open("/sys/devices/system/cpu/cpu0/cpufreq/bios_limit", "r") as fd:
                    bios_freq_state[core] = int(fd.read().strip())
            except:
                print("err")
                bios_freq_state[core] = 0
        return bios_freq_state
    
    def muda_bios_cpufreq(self, state, core):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/bios_limit", "w") as fd:
                fd.write(str(state))
        except:
            self.lista_state_bios_cpufreq[core].select() if not state else self.lista_state_bios_cpufreq[core].deselect()
            CTkMessagebox(title="Erro", message="Não foi possível mudar o valor", icon="cancel")

    def muda_governador(self, core):
            print(core)
            print(self.lista_governadores[core].get())
            governador = self.lista_governadores[core].get()
          #  governador = event.widget.get()
            print(governador)
            if governador == get_cpu_governor(core):
                return
            set_cpu_governor(core, governador)

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
        self.estado_core[core] = state
        print(state)
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
        
        muda_estado_core(core, state)
        

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
        if path.exists("/sys/devices/system/cpu/cpu0/cpufreq/bios_limit"):
            self.bios_cpu = True
            lista_bios_cpufreq_init_state = self.get_bios_cpufreq(num_cores)
            self.lista_state_bios_cpufreq = list(range(num_cores))
        for core in range(num_cores):
            print("xore ", freq_table[core])
            self.estado_core[core] = get_estado_core(core)
            frame_core = LabelFrame(self.frame_cpu_freq, text="core " + str(core), background='#212121', foreground="white")
            frame_core.grid(row=core // 2, column=core % 2, padx=5)
            self.state_core[core] = ctk.CTkLabel(frame_core, text="Enabled" if self.estado_core[core] else "Disabled")
            self.state_core[core].grid(column=0, row=1)
            self.lista_state_core[core] = ctk.CTkSwitch(frame_core, text="Off/On", onvalue=1, offvalue=0, command=lambda c=core: self.muda_state_core(c, self.lista_state_core[c].get()))
            if self.estado_core[core]:
                self.lista_state_core[core].select()
            else:
                self.lista_state_core[core].deselect()
            self.lista_state_core[core].grid(column=1, row=1)

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

            ctk.CTkLabel(frame_core, text="Max freq: ").grid(column=0, row=5, pady=5)
            self.lista_max_freq_core[core] = ctk.CTkComboBox(frame_core, values=freq_table[core], state="readonly")
            self.lista_max_freq_core[core].set(cores_max_freq[core])
            self.lista_max_freq_core_button[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_core_max_freq(c), state="normal" if self.estado_core[core] else "disabled")
            self.lista_max_freq_core[core].grid(column=1, row=5, padx=10, pady=5)
            self.lista_max_freq_core_button[core].grid(column=2, row=5, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Min freq: ").grid(column=0, row=6, pady=5)
            self.lista_min_freq_core[core] = ctk.CTkComboBox(frame_core, values=freq_table[core], state="readonly")
            self.lista_min_freq_core[core].set(cores_min_freq[core])
            self.lista_min_freq_core_button[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_core_min_freq(c), state="normal" if self.estado_core[core] else "disabled")
            self.lista_min_freq_core[core].grid(column=1, row=6, padx=10, pady=5)
            self.lista_min_freq_core_button[core].grid(column=2, row=6, padx=10, pady=5)
            print(cpu_governors)
            ctk.CTkLabel(frame_core, text="Governador: ").grid(column=0, row=7, pady=5)
            self.lista_governadores[core] = ctk.CTkComboBox(frame_core, values=cpu_governors, state="readonly")
            self.lista_governadores[core].set(core_governor[core])
            self.lista_ok[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_governador(c), state="normal" if self.estado_core[core] else "disabled")
         #   self.lista_governadores[core].bind("<ComboboxSelected>", lambda event: self.muda_governador(event, core))
            self.lista_governadores[core].grid(column=1, row=7, padx=10, pady=5)
            self.lista_ok[core].grid(column=2, row=7, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Preference: ").grid(column=0, row=8, pady=5)
            self.lista_energy_state[core] = ctk.CTkComboBox(frame_core, values=cpu_preferences, state="readonly")
            self.lista_energy_state[core].set(core_preferences[core])
            self.lista_ok_preference[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_preferencia(c), state="normal" if self.estado_core[core] else "disabled")
            self.lista_energy_state[core].grid(column=1, row=8, padx=10, pady=5)
            self.lista_ok_preference[core].grid(column=2, row=8, padx=10, pady=5)

            if self.bios_cpu:
                ctk.CTkLabel(frame_core, text="Bios limiter freq").grid(column=0, row=9, padx=10, pady=5)
                self.lista_state_bios_cpufreq[core] = ctk.CTkSwitch(frame_core, text="Off/On", onvalue=1, offvalue=0, state="normal" if self.estado_core[core] else "disabled", command=lambda c=core: self.muda_bios_cpufreq(self.lista_state_bios_cpufreq[c].get(), c))
                self.lista_state_bios_cpufreq[core].select() if lista_bios_cpufreq_init_state[core] else self.lista_state_bios_cpufreq[core].deselect()
                #.set(lista_bios_cpufreq_init_state[core])
                self.lista_state_bios_cpufreq[core].grid(column=1, row=9, padx=10, pady=5)

        self.lista_state_core[0].configure(state="disabled") # o kernel não permite modificar o estado desse nucleo para o funcionamento do sistema
       # self.update_current_freq_label()

    def update_current_freq_label(self):
        core_util = cpu_percent(interval=None, percpu=True)
        for index in range(int(self.num_cores)):
            print(index)
            if self.estado_core[index]:
                self.label_current_freq[index].configure(text="Current freq: " + str(round(int(get_cpu_current_freq(index)) / 1000)) + " MHz")
                try:
                    self.lista_core_utilization[index].configure(text="Utilization: " + str(int(core_util[index])) + "%")
                except:
                    print("idk")
                #self.tarefa = self.label_current_freq[index].after(1000, lambda: self.update_current_freq_label(index))
            else:
                self.lista_core_utilization[index].configure(text="Utilization: 0 %")
                self.label_current_freq[index].configure(text="Current freq: Disabled")
               # self.tarefa = self.label_current_freq[index].after(1000, self.update_current_freq_label(index))
        self.state_task = self.frame_cpu_freq.after(1000, self.update_current_freq_label)

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
