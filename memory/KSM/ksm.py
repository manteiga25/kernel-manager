import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue
from subprocess import run, PIPE

def rende_ksm(frame_memory, messager : Queue):

    def get_advisor_modes():
        try:
            with open("/sys/kernel/mm/ksm/advisor_mode", "r") as fd:
                modes = fd.read().strip()
                modes = modes.replace("[", '')
                modes = modes.replace("]", '')
                modes_list = modes.split()
                return modes_list
        except:
            return "err"

    def get_advisor_mode():
        try:
            with open("/sys/kernel/mm/ksm/advisor_mode", "r") as fd:
                modes = fd.read().strip().split()
                print(modes)
                default_mode = [mode for mode in modes if not mode.find("[")]
                default_mode = default_mode[0].replace("[", "")
                default_mode = default_mode.replace("]", "")
                return default_mode
        except:
            return "err"

    def get_ksm_status():
        try:
            with open("/sys/kernel/mm/ksm/run", "r") as fd:
                return fd.read().strip()
        except:
            return "-1"

    def set_ksm_status(choice):
        nonlocal ksm_status
        if ksm_status == choice:
            return
        try:
            with open("/sys/kernel/mm/ksm/run", "w") as fd:
               fd.write(choice)
            ksm_status = choice
        except Exception as e:
            ksm_button.set(ksm_status)
            messager.put(f"Memory ksm: Error to set ksm status to {choice}, {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

    def get_ksm_max_cpu_usage():
        try:
            with open("/sys/kernel/mm/ksm/advisor_max_cpu", "r") as fd:
                return int(fd.read().strip())
        except:
            return -1

    def set_ksm_max_cpu_usage(value):
        try:
            value = str(int(value))
            with open("/sys/kernel/mm/ksm/advisor_max_cpu", "w") as fd:
                label_cpu_ksm_usage.configure(text=value + "%")
                fd.write(value)
            max_cpu_usage_status = int(value)
        except Exception as e:
            label_cpu_ksm_usage.configure(text=str(max_cpu_usage_status) + "%")
            messager.put(f"Memory ksm: Error to set ksm max cpu value to {value}, {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

    def get_zero_page_status():
        try:
            with open("/sys/kernel/mm/ksm/use_zero_pages", "r") as fd:
                return fd.read().strip()
        except:
            return "-1"

    def set_zero_page():
        nonlocal ksm_zero_page_status
        value = ksm_zero_page.get()
        try:
            with open("/sys/kernel/mm/ksm/use_zero_pages", "w") as fd:
                fd.write(str(value))
            ksm_zero_page_status = value
        except Exception as e:
            if ksm_zero_page_status == 1:
                ksm_zero_page.select()
            else:
                ksm_zero_page.deselect()
            messager.put(f"Memory ksm: Error to set ksm zero page to {value}, {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

    def get_param_ksm(folder):
        try:
            with open(f"/sys/kernel/mm/ksm/{folder}", "r") as fd:
                return fd.read().strip()
        except:
            return "-1"

    def set_ksm_advisor_mode(mode):
        nonlocal ksm_advisor_status
        if mode == ksm_advisor_status:
            return
        result = run([f"echo {mode} > /sys/kernel/mm/ksm/advisor_mode"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        if result.stderr:
            ksm_advisor_mode.set(ksm_advisor_status)
            messager.put(f"Error memory ksm: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} to {ksm_advisor_status} in thp mode\n{result.stderr}")
        else:
            messager.put(f"Memory ksm: Success to set ksm mode from {ksm_advisor_status} to {mode}, {result.stdout}")
            ksm_advisor_status = mode

    def set_param_ksm(folder, value):
        try:
            if not value.isdigit() or int(value) < 0:
                raise ValueError("The parameter has been integer not string")
            with open(f"/sys/kernel/mm/ksm/{folder}", "w") as fd:
                fd.write(value)
            messager.put(f"Memory ksm: Sucess to set value {value} on folder {folder}")
        except ValueError as e:
            messager.put(f"Memory ksm: Error {value} is invalid value, {e}")
        except Exception as e:
            messager.put(f"Memory ksm: Error to set ksm {folder} status to {value}, {e}")
            CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        # tratamento futuro para pages to scan, smart scan?
    entry_params = ["pages_to_scan", "sleep_millisecs", "stable_node_chains_prune_millisecs", "advisor_target_scan_time", "advisor_min_pages_to_scan", "advisor_max_pages_to_scan"]
    entry_names = ["Pages to scan:", "sleep millisecs:", "Check pages metadata:", "Target scan time:", "Min pages to scan:", "Max pages to scan:"]

    ksm_status = get_ksm_status()
    if ksm_status == "-1": # fatal error
        return
    ksm_status_var = ctk.StringVar(value=ksm_status)
    ksm_frame = LabelFrame(frame_memory, text="KSM", background='#212121', foreground="white", labelanchor="n")
    ksm_frame.grid(row=2, column=0, padx=5, pady=5)
    ctk.CTkLabel(ksm_frame, text="KSM: ").grid(row=0, column=0, padx=5, pady=5)
    ksm_button = ctk.CTkComboBox(ksm_frame, values=["0", "1", "2"], command=set_ksm_status, variable=ksm_status_var, state="readonly")
    ksm_button.grid(row=0, column=1, pady=5)

    ksm_advisor_status = get_advisor_mode()
    if ksm_advisor_status != "err":
        ctk.CTkLabel(ksm_frame, text="KSM advisor mode: ").grid(row=1, column=0, padx=5, pady=5)
        ksm_advisor_mode = ctk.CTkComboBox(ksm_frame, values=get_advisor_modes(), command=set_ksm_advisor_mode, state="readonly")
        ksm_advisor_mode.set(ksm_advisor_status)
        ksm_advisor_mode.grid(row=1, column=1, padx=5, pady=5)

    max_cpu_usage_status = int(get_ksm_max_cpu_usage())
    if max_cpu_usage_status != -1:
        ctk.CTkLabel(ksm_frame, text="KSM cpu usage:").grid(row=2, column=0)
        ksm_cpu_usage_slider = ctk.CTkSlider(ksm_frame, from_=0, to=90, command=set_ksm_max_cpu_usage)
        ksm_cpu_usage_slider.set(max_cpu_usage_status)
        ksm_cpu_usage_slider.grid(row=2, column=1)
        label_cpu_ksm_usage = ctk.CTkLabel(ksm_frame, text=str(max_cpu_usage_status) + "%")
        label_cpu_ksm_usage.grid(row=2, column=2, sticky="w")

    ksm_zero_page_status = get_zero_page_status()
    if ksm_zero_page_status != "-1":
        ctk.CTkLabel(ksm_frame, text="Use zero page:").grid(row=3, column=0)
        ksm_zero_page = ctk.CTkSwitch(ksm_frame, text="off/on", command=set_zero_page)
        if ksm_zero_page_status == "1":
            ksm_zero_page.select()
        ksm_zero_page.grid(row=3, column=1)

    row = 3
    entry_param = list(range(6))
    for label, folder, index in zip(entry_names, entry_params, range(6)):
        ksm_feature_status = get_param_ksm(folder)
        if ksm_feature_status == "-1":
            continue
        row += 1
        ctk.CTkLabel(ksm_frame, text=label).grid(row=row, column=0, padx=5, pady=5)
        entry_param[index] = ctk.CTkEntry(ksm_frame, placeholder_text=ksm_feature_status)
        entry_param[index].grid(column=1, row=row, padx=5, pady=5)
        ctk.CTkButton(ksm_frame, text="Aplicar alterações", command=lambda f=folder, i=index: set_param_ksm(f, entry_param[i].get())).grid(column=2, row=row, padx=5, pady=5)
