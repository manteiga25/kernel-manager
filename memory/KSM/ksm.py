import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def rende_ksm(frame_memory, messager):

    def get_ksm_status():
        try:
            with open("/sys/kernel/mm/ksm/run", "r") as fd:
                return fd.read().strip()
        except:
            return "0"

    def set_ksm_status(choice):
        try:
            with open("/sys/kernel/mm/ksm/run", "w") as fd:
               fd.write(choice)
        except Exception as e:
            messager.put(f"Memory ksm: Error to set ksm status to {choice}, {e}")
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
            messager.put(f"Memory ksm: Error to set ksm max cpu value to {value}, {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

    def get_zero_page_status():
        try:
            with open("/sys/kernel/mm/ksm/use_zero_pages", "r") as fd:
                return fd.read().strip()
        except:
            return "0"

    def set_zero_page():
        value = ksm_zero_page.get()
        try:
            with open("/sys/kernel/mm/ksm/use_zero_pages", "w") as fd:
                fd.write(value)
        except Exception as e:
            messager.put(f"Memory ksm: Error to set ksm zero page to {value}, {e}")
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
        except ValueError as e:
            messager.put(f"Memory ksm: Error {value} is invalis valuu, {e}")
        except Exception as e:
            messager.put(f"Memory ksm: Error to set ksm {folder} status to {value}, {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        # tratamento futuro para pages to scan, smart scan?
    entry_params = ["pages_to_scan", "sleep_millisecs", "stable_node_chains_prune_millisecs", "advisor_target_scan_time", "advisor_min_pages_to_scan", "adivsor_max_pages_to_scan"]
    entry_names = ["Pages to scan:", "sleep millisecs:", "Check pages metadata:", "Target scan time:", "Min pages to scan:", "Max pages to scan:"]

    ksm_status_var = ctk.StringVar(value=get_ksm_status())
    ksm_frame = LabelFrame(frame_memory, text="KSM", background='#212121', foreground="white", labelanchor="n")
    ksm_frame.grid(row=2, column=0, padx=5, pady=5)
    ctk.CTkLabel(ksm_frame, text="KSM: ").grid(row=0, column=0, padx=5, pady=5)
    ksm_button = ctk.CTkComboBox(ksm_frame, values=["0", "1", "2"], command=set_ksm_status, variable=ksm_status_var, state="readonly")
    ksm_button.grid(row=0, column=1, pady=5)
    ctk.CTkLabel(ksm_frame, text="KSM cpu usage:").grid(row=1, column=0)
    ksm_cpu_usage_slider = ctk.CTkSlider(ksm_frame, from_=0, to=90, command=set_ksm_max_cpu_usage)
    ksm_cpu_usage_slider.set(int(get_ksm_max_cpu_usage()))
    ksm_cpu_usage_slider.grid(row=1, column=1)
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