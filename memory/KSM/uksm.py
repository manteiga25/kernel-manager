import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from queue import Queue
from tkinter import LabelFrame
from subprocess import run, PIPE

def rende_uksm(frame_memory, messager : Queue):

    def get_advisor_mode():
        try:
            with open("/sys/kernel/mm/uksm/advisor_mode", "r") as fd:
                modes = fd.read().strip().split()
                default_mode = [mode for mode in modes if not mode.find("[")]
                default_mode = default_mode[0].replace("[", "")
                default_mode = default_mode.replace("]", "")
                return default_mode
        except:
            return "err"

    def get_uksm_status():
            try:
                with open("/sys/kernel/mm/uksm/run", "r") as fd:
                    return fd.read().strip()
            except:
                return "-1"
                
    def set_uksm_status(choice):
        nonlocal uksm_status
        choice = choice[0]
        if uksm_status == choice:
            return
        try:
            with open("/sys/kernel/mm/uksm/run", "w") as fd:
                fd.write(choice)
            messager.put(f"Memory uksm: Success to set uksm status from {uksm_status} to {choice}")
            uksm_status = choice
        except Exception as e:
            uksm_button.set(uksm_status)
            messager.put(f"Memory uksm: Error to set uksm status from {uksm_status} to {choice}, {e}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_uksm_max_cpu_usage():
        try:
            with open("/sys/kernel/mm/uksm/advisor_max_cpu", "r") as fd:
                return int(fd.read().strip())
        except:
            return -1
                
    def set_uksm_max_cpu_usage(value):
        nonlocal max_cpu_usage
        try:
            if value == max_cpu_usage:
                return
            with open("/sys/kernel/mm/uksm/advisor_max_cpu", "w") as fd:
                label_cpu_uksm_usage.configure(text=value + "%")
                fd.write(str(value))
            max_cpu_usage = value
        except Exception as e:
            uksm_cpu_usage_slider.set(max_cpu_usage)
            label_cpu_uksm_usage.configure(text=str(max_cpu_usage) + "%")
            messager.put(f"Memory uksm: Error to set uksm max cpu value to {value}, {e}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_uksm_bolean_status(file):
        try:
            with open(f"/sys/kernel/mm/uksm/{file}", "r") as fd:
                return fd.read().strip()
        except:
            return "-1"

    def set_uksm_bolean_status(feature, index):
        nonlocal uksm_switch_feature_status
        value = uksm_switch_widget[index].get()
        try:
            with open(f"/sys/kernel/mm/uksm/{feature}", "w") as fd:
                fd.write(str(value))
            messager.put(f"Memory uksm: Success to set uksm {feature} to {value}")
            uksm_switch_feature_status[idx] = value
        except Exception as e:
            if uksm_switch_feature_status[idx] == 1:
                uksm_switch_widget[idx].select()
            else:
                uksm_switch_feature_status[idx].deselect()
            messager.put(f"Memory uksm: Error to set {feature} to {value}, {e}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_param_uksm(folder):
        try:
            with open(f"/sys/kernel/mm/uksm/{folder}", "r") as fd:
                return fd.read().strip()
        except:
            return "-1"

    def set_param_uksm(folder, value):
        try:
            if not value.isdigit():
                raise ValueError("The parameter has been integer not string")
            with open(f"/sys/kernel/mm/uksm/{folder}", "w") as fd:
                fd.write(value)
            messager.put(f"Memory uksm: Sucess to set value {value} on folder {folder}")
        except ValueError as e:
            messager.put(f"Memory uksm: Error {value} is invalid value, {e}")
        except Exception as e:
            messager.put(f"Memory uksm: Error to set uksm {folder} status to {value}, {e}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def set_uksm_advisor_mode(mode):
        nonlocal uksm_advisor_status
        if mode == uksm_advisor_status:
            return
        result = run([f"echo {mode} > /sys/kernel/mm/uksm/advisor_mode"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        if result.stderr:
            uksm_advisor_mode.set(uksm_advisor_status)
            messager.put(f"Error memory uksm: {result.stderr}")
            CTkMessagebox("Error", message=f"Error to set {mode} to {uksm_advisor_status} in uksm advisor mode\n{result.stderr}")
        else:
            messager.put(f"Memory uksm: Success to set uksm mode from {uksm_advisor_status} to {mode}, {result.stdout}")
            uksm_advisor_status = mode

    entry_params = ["pages_to_scan", "sleep_millisecs", "stable_node_chains_prune_millisecs", "advisor_target_scan_time", "advisor_min_pages_to_scan", "adivsor_max_pages_to_scan"]
    entry_names = ["Pages to scan:", "sleep millisecs:", "Check pages metadata:", "Target scan time:", "Min pages to scan:", "Max pages to scan:"]

    switch_params = ["merge_across_nodes", "use_zero_pages", "smart_scan"]
    switch_names = ["Merge across nodes:", "Use zero page:", "Smart scan:"]

    uksm_status = get_uksm_status()
    if uksm_status == "-1": # fatal error
        return
    uksm_status_var = ctk.StringVar(value=uksm_status)
    uksm_frame = LabelFrame(frame_memory, text="UKSM", background='#212121', foreground="white", labelanchor="n")
    uksm_frame.grid(row=2, column=0, padx=5, pady=5)
    ctk.CTkLabel(uksm_frame, text="UKSM: ").grid(row=0, column=0, padx=5, pady=5)
    uksm_button = ctk.CTkComboBox(uksm_frame, values=["0 (off)", "1 (on)", "2 (off unmerge pages)"], command=set_uksm_status, variable=uksm_status_var, state="readonly")
    uksm_button.grid(row=0, column=1, pady=5)

    uksm_advisor_status = get_advisor_mode()
    if uksm_advisor_status != "err":
        ctk.CTkLabel(uksm_frame, text="UKSM advisor mode: ").grid(row=1, column=0, padx=5, pady=5)
        uksm_advisor_mode = ctk.CTkComboBox(uksm_frame, values=["none", "scan-time"], command=set_uksm_advisor_mode, state="readonly")
        uksm_advisor_mode.set(uksm_advisor_status)
        uksm_advisor_mode.grid(row=1, column=1, padx=5, pady=5)

    max_cpu_usage = get_uksm_max_cpu_usage()
    if  max_cpu_usage != -1:
        ctk.CTkLabel(uksm_frame, text="UKSM cpu usage:").grid(row=2, column=0)
        uksm_cpu_usage_slider = ctk.CTkSlider(uksm_frame, from_=0, to=90, command=set_uksm_max_cpu_usage)
        uksm_cpu_usage_slider.set(max_cpu_usage)
        uksm_cpu_usage_slider.grid(row=2, column=1)
        label_cpu_uksm_usage = ctk.CTkLabel(uksm_frame, text=str(max_cpu_usage) + "%")
        label_cpu_uksm_usage.grid(row=2, column=2, sticky="w")

    row = 3
    uksm_switch_feature_status = list(range(3))
    uksm_switch_widget = list(range(3))
    for label, feature, idx in zip(switch_names, switch_params, range(3)):
        uksm_switch_feature_status[idx] = get_uksm_bolean_status(feature)
        if uksm_switch_feature_status[idx] == "-1":
            continue
        ctk.CTkLabel(uksm_frame, text=label).grid(column=0, row=row)
        uksm_switch_widget[idx] = ctk.CTkSwitch(uksm_frame, text="off/on", command=lambda f=feature, index=idx: set_uksm_bolean_status(f, index))
        if uksm_switch_feature_status[idx] == "1":
            uksm_switch_widget[idx].select()
        uksm_switch_widget[idx].grid(row=row, column=1)
        row += 1

    entry_param = list(range(6))
    for label, folder, index in zip(entry_names, entry_params, range(6)):
        uksm_feature_status = get_param_uksm(folder)
        if uksm_feature_status == "-1":
            continue
        row += 1
        ctk.CTkLabel(uksm_frame, text=label).grid(column=0, row=row)
        entry_param[index] = ctk.CTkEntry(uksm_frame, placeholder_text=uksm_feature_status)
        entry_param[index].grid(column=1, row=row)
        ctk.CTkButton(uksm_frame, text="Aplicar alterações", command=lambda i=index: set_param_uksm(folder, entry_param[i].get())).grid(column=2, row=row)
