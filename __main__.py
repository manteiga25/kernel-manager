import customtkinter as ctk
import manager
import cpufreq
import cpuidle
import system
import event_error
import memory
import io_manager
import battery
import sched
import network
from threading import Thread
from CTkMenuBar import *
from blinker import signal
from os import listdir
from queue import Queue

def check_number_of_cores_files():
    folders = listdir("/sys/devices/system/cpu/")
    num_folder_cores = 0
    for folder in folders:
        if len(folder) > 3:
            if folder.find("cpu") == 0 and folder[3].isdigit(): # if folder as cpu core folder increment counter
                num_folder_cores += 1
    return num_folder_cores

class main_window:
    def __init__(self) -> None:
        self.window : ctk.CTk = ctk.CTk()
        self.window.title("Kernel manager")
        self.window.resizable(False, False)
        self.frame_atual = "CPU info"
        self.frame_anterior = "CPU info"
        self.init_title_menu()
        self.init_menu()
        self.inicialize_objects()
        self.inicialize_pages()
        self.window.mainloop()

    def inicialize_objects(self):
        self.kernel_threads = check_number_of_cores_files()
        self.error = event_error.io_error()
        self.messager = Queue()
        self.cpuinfo_module = manager.cpuinfo()
        self.system_module = system.system()
        self.cpufreq_module = cpufreq.cpu_freq()
        self.cpuidle_module = cpuidle.cpu_idle()
        self.memory_module = memory.memory()
        self.io_module = io_manager.io_manager()
        self.battery_module = battery.battery()
        self.sched_module = sched.sched()
        self.network_module = network.network()

    def inicialize_pages(self):
        threads, purpouse = self.cpuinfo_module.rende_cpu_info(self.cpu_info_tab, self.error) # necessary for cpu freq
        print("threads: ", threads)
        Thread(target=self.system_module.rende_system_info, args=(self.cpu_system_tab,), daemon=False).start()
        Thread(target=self.cpufreq_module.rende_cpu_freq, args=(self.cpu_freq_tab, self.kernel_threads, purpouse, self.messager,), daemon=False).start()
       # signal("cpu_freq").connect(self.cpufreq_module.rende_cpu_freq(self.cpu_freq_tab))
        Thread(target=self.cpuidle_module.rende_cpu_idle, args=(self.cpu_idle_tab,), daemon=False).start()
        Thread(target=self.memory_module.rende_memory, args=(self.memory_menu_tab,), daemon=False).start()
        Thread(target=self.io_module.rende_io, args=(self.io_menu_tab,), daemon=False).start()
        Thread(target=self.battery_module.rende_battery, args=(self.battery_menu_tab,), daemon=False).start()
        Thread(target=self.sched_module.rende_sched, args=(self.sched_menu_tab,), daemon=False).start()
        Thread(target=self.network_module.rende_network, args=(self.network_menu_tab,), daemon=False).start()

    def init_log_window(self):
        self.janela_reg = ctk.CTkToplevel(self.window)
        self.janela_reg.title("Log")
        self.janela_reg.maxsize(600, 200)
        self.janela_reg.protocol("WM_DELETE_WINDOW", self.hide_log_window)
        self.janela_reg.withdraw()
   #     frame = ctk.CTkScrollableFrame(self.janela_reg)
    #    frame.pack(fill="both", expand=True)
        self.textbox = ctk.CTkTextbox(self.janela_reg, wrap="word", width=600, height=200)
        self.textbox.configure(state="disabled")
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

    def write_log_window(self):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", self.messager.get())
        self.textbox.configure(state="disabled")

    def show_log_window(self):
        self.janela_reg.deiconify()

    def hide_log_window(self):
        self.janela_reg.withdraw()

    def ver_registo(self):
        conteudo = self.error.le_registro()
        janela_reg = ctk.CTkToplevel(self.window)
        janela_reg.title("errors")
        frame = ctk.CTkFrame(janela_reg)
        frame.pack(fill="both", expand=True)
        self.textbox = ctk.CTkTextbox(frame, wrap="word", width=600, height=200)
        self.textbox.insert("0.0", conteudo)
        self.textbox.configure(state="disabled")
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

    def init_title_menu(self):
        title_menu = CTkMenuBar(self.window)
        menu_file = title_menu.add_cascade("Debug")
        dropdown1 = CustomDropdownMenu(widget=menu_file)
        dropdown1.add_option(option="Open", command=self.show_log_window)
        dropdown1.add_separator()

    def verify_page(self):
        self.frame_atual = self.menu.get()

        if self.frame_anterior == "CPU info":
            self.cpuinfo_module.cancel_task()
        elif self.frame_anterior == "CPU frequency":
            self.cpufreq_module.cancel_task()
        elif self.frame_anterior == "Memory":
            self.memory_module.cancel_task()
        elif self.frame_anterior == "Battery":
            self.battery_module.cancel_task()
        elif self.frame_anterior == "I/O":
            self.io_module.cancel_task()

        if self.frame_atual == "CPU info":
            self.cpuinfo_module.start_task()
        elif self.frame_atual == "CPU frequency":
            self.cpufreq_module.start_task()
        elif self.frame_atual == "Memory":
            self.memory_module.start_task()
        elif self.frame_atual == "Battery":
            self.battery_module.start_task()
        elif self.frame_atual == "I/O":
            self.io_module.start_task()


        self.frame_anterior = self.frame_atual

    def init_menu(self):
        self.menu = ctk.CTkTabview(master=self.window, command=self.verify_page)
        self.menu.pack(padx=5, expand=True, fill="both")
        self.cpu_info_tab = self.menu.add("CPU info")  # add tab at the end
        self.cpu_system_tab = self.menu.add("System info")  # add tab at the end
        self.cpu_freq_tab = self.menu.add("CPU frequency")  # add tab at the end
        self.cpu_idle_tab = self.menu.add("CPU idle")  # add tab at the end
        self.memory_menu_tab = self.menu.add("Memory")  # add tab at the end
        self.io_menu_tab = self.menu.add("I/O")  # add tab at the end
        self.battery_menu_tab = self.menu.add("Battery")  # add tab at the end
        self.sched_menu_tab = self.menu.add("Sched")  # add tab at the end
        self.network_menu_tab = self.menu.add("Network")

if __name__ == "__main__":
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    ctk.set_appearance_mode("dark")
    main = main_window()