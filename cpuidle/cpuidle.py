import customtkinter as ctk
from tkinter import LabelFrame

# retorna o governador atual do nucleo
def get_cpu_idle_governor():
    try:
        with open(f"/sys/devices/system/cpu/cpuidle/current_governor_ro", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

# retorna a lista de todos os governadores disponiveis no kernel
def get_cpu_idle_governors():
    try:
        with open("/sys/devices/system/cpu/cpuidle/available_governors", "r") as gov:
            ret = gov.read().split(" ")
            ret = [governor.strip() for governor in ret if governor.strip()]
            return ret
    except:
        return "err"

def set_cpu_idle_governor(governador):
    try:
        with open(f"/sys/devices/system/cpu/cpuidle/current_governor", "w") as gov:
            gov.write(governador)
    except:
        print("idbciusd")

def set_cpu_clocksource_mode(mode):
    try:
        with open("/sys/devices/system/clocksource/clocksource0/current_clocksource", "w") as gov:
            gov.write(mode)
    except:
        return "err"

def get_cpu_clocksource_modes():
    try:
        with open("/sys/devices/system/clocksource/clocksource0/available_clocksource", "r") as gov:
            ret = gov.read().split(" ")
            ret = [governor.strip() for governor in ret if governor.strip()]
            return ret
    except:
        return "err"

def get_cpu_clocksource_mode():
    try:
        with open("/sys/devices/system/clocksource/clocksource0/current_clocksource", "r") as gov:
            return gov.read().strip()
    except:
        return "err"

class cpu_idle:

    def muda_governador(self):
            print(self.governadores_idle.get())
            governador = self.governadores_idle.get()
            print(governador)
            if governador == get_cpu_idle_governor():
                return
            set_cpu_idle_governor(governador)

    def muda_modo(self):
        print(self.modos_clocksource.get())
        modo = self.modos_clocksource.get()
        print(modo)
        if modo == get_cpu_idle_governor():
            return
        set_cpu_idle_governor(modo)

    def cpu_clocksource_frame(self):
        self.cpu_clocksource_f = LabelFrame(master=self.frame_cpu_idle_glob, text="Clocksource", background='#212121', foreground="white")
        self.cpu_clocksource_f.pack(fill="both", expand=True, pady=20)
        ctk.CTkLabel(self.cpu_clocksource_f, text="O clocksource é responsável por manter uma contagem de tempo e gerenciar os ticks do kernel.", wraplength=700, justify="center").grid(column=1, row=0, columnspan=6)
        ctk.CTkLabel(self.cpu_clocksource_f, text="Clocksource mode: ").grid(column=0, row=2, pady=5, padx=5)
        self.modos_clocksource = ctk.CTkComboBox(self.cpu_clocksource_f, values=get_cpu_clocksource_modes())
        self.modos_clocksource.set(get_cpu_clocksource_mode())
        ok = ctk.CTkButton(self.cpu_clocksource_f, text="salvar alteração" , command=self.muda_modo)
        self.modos_clocksource.grid(column=1, row=2, padx=5, pady=5)
        ok.grid(column=2, row=2, padx=5, pady=5)

    def cpu_idle_frame(self):
        self.frame_cpu_idle = LabelFrame(self.frame_cpu_idle_glob, width=880, height=380, text="CPU Idle", background='#212121', foreground="white")
        self.frame_cpu_idle.pack(fill="both", expand=True)
        ctk.CTkLabel(self.frame_cpu_idle, text="CPU idle é um recurso de gerenciamento de energia que permite desabilitar partes da CPU que estão ociosas quando nenhum programa esta a ser executado ou em carga baixa para economizar energia.", wraplength=700, justify="center").grid(column=1, row=0, columnspan=6)
        ctk.CTkLabel(self.frame_cpu_idle, text="Governador idle: ").grid(column=0, row=2, pady=5, padx=5)
        self.governadores_idle = ctk.CTkComboBox(self.frame_cpu_idle, values=get_cpu_idle_governors())
        self.governadores_idle.set(get_cpu_idle_governor())
        ok = ctk.CTkButton(self.frame_cpu_idle, text="salvar alteração" , command=self.muda_governador)
        self.governadores_idle.grid(column=1, row=2, padx=5, pady=5)
        ok.grid(column=2, row=2, padx=5, pady=5)

    def rende_cpu_idle(self, menu):
        self.menu = menu
        self.frame_cpu_idle_glob = ctk.CTkScrollableFrame(self.menu, width=880, height=380)
        self.frame_cpu_idle_glob.grid(column=0, row=3, columnspan=2)
        self.cpu_idle_frame()
        self.cpu_clocksource_frame()