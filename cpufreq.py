import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import LabelFrame
from psutil import cpu_percent

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
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/min_freq?", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

def set_core_min_freq(num_core, freq):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/min_freq?", "w") as gov:
            gov.write(freq)
    except:
        return "err"

def get_core_max_freq(num_core):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/max_freq?", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

def set_core_max_freq(num_core, freq):
    try:
        with open(f"/sys/devices/system/cpu/cpu{num_core}/cpufreq/max_freq?", "w") as gov:
            gov.write(freq)
    except:
        return "err"

class cpu_freq:

    # tentativa de otimização
    def get_min_cores_freq(num_cores):
        pass

    def muda_core_min_freq(self, core):
        min_freq = self.lista_min_freq_core[core]
        if min_freq > self.lista_max_freq_core[core]:
            CTkMessagebox(title="Valor inválido", message="A Frequência mínima tem de ser menor que a frequência maxima.", icon="cancel")
            self.lista_min_freq_core[core].set(get_core_min_freq(core))
            return
        set_core_min_freq(core, min_freq)

    def muda_core_max_freq(self, core):
        max_freq = self.lista_max_freq_core[core]
        if max_freq < self.lista_min_freq_core[core]:
            CTkMessagebox(title="Valor inválido", message="A Frequência maxima tem de ser maior que a frequência mínima.", icon="cancel")
            self.lista_max_freq_core[core].set(get_core_max_freq(core))
            return
        set_core_min_freq(core, max_freq)

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
#        else:
 #           self.state_core[core].configure(text="Disabled")
        
        muda_estado_core(core, state)

    def cpu_freq_frame(self):
        self.frame_cpu_freq = ctk.CTkScrollableFrame(self.menu, width=880, height=380)
        self.frame_cpu_freq.grid(column=0, row=3, columnspan=2)
        self.label_current_freq = list(range(int(self.num_cores)))
        self.lista_governadores = list(range(int(self.num_cores)))
        self.lista_ok = list(range(int(self.num_cores)))
        self.lista_core_utilization = list(range(int(self.num_cores)))
        self.lista_energy_state = list(range(int(self.num_cores)))
        self.lista_state_core = list(range(int(self.num_cores)))
        self.lista_ok_preference = list(range(int(self.num_cores)))
        self.estado_core = list(range(int(self.num_cores)))
        self.state_core = list(range(int(self.num_cores)))
        self.lista_min_freq_core = list(range(int(self.num_cores)))
        self.lista_max_freq_core = list(range(int(self.num_cores)))
        self.lista_min_freq_core_button = list(range(int(self.num_cores)))
        self.lista_max_freq_core_button = list(range(int(self.num_cores)))
        for core in range(int(self.num_cores)):
            self.estado_core[core] = get_estado_core(core)
            frame_core = LabelFrame(self.frame_cpu_freq, text="core " + str(core), background='#212121', foreground="white")
            frame_core.grid(row=core // 2, column=core % 2, padx=10)
            self.state_core[core] = ctk.CTkLabel(frame_core, text="Enabled" if self.estado_core[core] else "Disabled")
            self.state_core[core].grid(column=0, row=1)
            self.lista_state_core[core] = ctk.CTkSwitch(frame_core, text="Off/On", onvalue=1, offvalue=0, command=lambda c=core: self.muda_state_core(c, self.lista_state_core[c].get()))
            if self.estado_core[core]:
                self.lista_state_core[core].select()
            else:
                self.lista_state_core[core].deselect()
            self.lista_state_core[core].grid(column=1, row=1)
           # print(self.lista_state_core[core].get())
            #print(get_estado_core(core))
            self.lista_core_utilization[core] = ctk.CTkLabel(frame_core)
            self.lista_core_utilization[core].grid(column=0, row=2, columnspan=1, padx=5)
            self.label_current_freq[core] = ctk.CTkLabel(frame_core)
            self.label_current_freq[core].grid(column=0, row=3, columnspan=2, sticky="w", padx=5)

            ctk.CTkLabel(frame_core, text="Max freq: ").grid(column=0, row=4, pady=5)
            self.lista_max_freq_core[core] = ctk.CTkComboBox(frame_core, values=get_core_table_freq(core))
            self.lista_max_freq_core[core].set(get_core_max_freq(core))
            self.lista_max_freq_core_button[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_core_max_freq(c))
            self.lista_max_freq_core[core].grid(column=1, row=4, padx=10, pady=5)
            self.lista_max_freq_core_button[core].grid(column=2, row=4, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Min freq: ").grid(column=0, row=5, pady=5)
            self.lista_min_freq_core[core] = ctk.CTkComboBox(frame_core, values=get_core_table_freq(core))
            self.lista_min_freq_core[core].set(get_core_min_freq(core))
            self.lista_min_freq_core_button[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_core_min_freq(c))
            self.lista_min_freq_core[core].grid(column=1, row=5, padx=10, pady=5)
            self.lista_min_freq_core_button[core].grid(column=2, row=5, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Governador: ").grid(column=0, row=6, pady=5)
            self.lista_governadores[core] = ctk.CTkComboBox(frame_core, values=get_cpu_governors())
            self.lista_governadores[core].set(get_cpu_governor(core))
            self.lista_ok[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_governador(c))
         #   self.lista_governadores[core].bind("<ComboboxSelected>", lambda event: self.muda_governador(event, core))
            self.lista_governadores[core].grid(column=1, row=6, padx=10, pady=5)
            self.lista_ok[core].grid(column=2, row=6, padx=10, pady=5)

            ctk.CTkLabel(frame_core, text="Preference: ").grid(column=0, row=7, pady=5)
            self.lista_energy_state[core] = ctk.CTkComboBox(frame_core, values=get_cpu_preferences())
            self.lista_energy_state[core].set(get_cpu_preference(core))
            self.lista_ok_preference[core] = ctk.CTkButton(frame_core, text="salvar alteração" , command=lambda c=core: self.muda_preferencia(c))
            self.lista_energy_state[core].grid(column=1, row=7, padx=10, pady=5)
            self.lista_ok_preference[core].grid(column=2, row=7, padx=10, pady=5)
        self.lista_state_core[0].configure(state="disabled") # o kernel não permite modificar o estado desse nucleo para o funcionamento do sistema
        self.update_current_freq_label()

    def update_current_freq_label(self):
        core_util = cpu_percent(interval=None, percpu=True)
        for index in range(int(self.num_cores)):
          #  print(index)
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
        self.frame_cpu_freq.after(1000, self.update_current_freq_label)

    def cancel_task(self):
        print(self.tarefa)
        self.label_current_freq.after_cancel(self.tarefa)

    def rende_cpu_freq(self, menu, num_cores):
        self.num_cores = num_cores
        self.menu = menu
        self.cpu_freq_frame()
