import customtkinter as ctk
from tkinter import LabelFrame
from os import path, system, listdir
from CTkMessagebox import CTkMessagebox
from queue import Queue
from subprocess import check_output, PIPE, run

def rende_thp(frame_memory, messager : Queue):

    def get_thp_modes(file):
        try:
            with open(f"/sys/kernel/mm/transparent_hugepage/{file}", "r") as fd:
                modes = fd.read().strip()
                modes = modes.replace("[", '')
                modes = modes.replace("]", '')
                modes_list = modes.split()
                return modes_list
        except:
            return "err"
    
    def get_thp_mode(file):
        try:
            with open(f"/sys/kernel/mm/transparent_hugepage/{file}", "r") as fd:
                modes = fd.read().strip().split()
                default_mode = [mode for mode in modes if not mode.find("[")]
                default_mode = default_mode[0].replace("[", "")
                default_mode = default_mode.replace("]", "")
                return default_mode
        except:
            return "err"

    def verify_value_is_num(value: str):
        if not value.isdigit() or int(value) < 0:
            raise ValueError("The value needs to be positive integer not string")

    def set_thp_defrag_mode(mode):
        nonlocal thp_defrag_status
        if mode == thp_defrag_status:
            return
        result = run([f"echo {mode} > /sys/kernel/mm/transparent_hugepage/defrag"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        if result.stderr:
            modo_thp_defrag.set(thp_defrag_status)
            messager.put(f"Error memory thp: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} to {thp_defrag_status} in thp defrag mode\n{result.stderr}")
        else:
            messager.put(f"Memory thp: Success to set thp defrag mode from {thp_defrag_status} to {mode}, {result.stdout}")
            thp_defrag_status = mode

    def set_thp_mode(mode):
        nonlocal modo_thp_status
        if mode == modo_thp_status:
            return
        result = run([f"echo {mode} > /sys/kernel/mm/transparent_hugepage/enabled"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        if result.stderr:
            modo_thp.set(modo_thp_status)
            messager.put(f"Error memory thp: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} to {modo_thp_status} in thp mode\n{result.stderr}")
        else:
            messager.put(f"Memory thp: Success to set thp mode from {modo_thp_status} to {mode}, {result.stdout}")
            modo_thp_status = mode
        
    def set_thp_shm_mode(mode):
        nonlocal thp_shm_status
        if mode == thp_shm_status:
            return
        result = run([f"echo {mode} > /sys/kernel/mm/transparent_hugepage/shmem_enabled"], stderr=PIPE, text=True, shell=True)
        if result.stderr:
            modo_thp_shm.set(thp_shm_status)
            messager.put(f"Error memory thp: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} to {thp_shm_status} in thp shared mode\n{result.stderr}")
        else:
            messager.put(f"Memory thp: Success to set thp shared mode from {thp_shm_status} to {mode}, {result.stdout}")
            thp_shm_status = mode

    def get_thp_info():

        def get_thp_sized_mode(folder):
            try:
                with open(f"/sys/kernel/mm/transparent_hugepage/{folder}/enabled", "r") as fd_mode:
                    modes = fd_mode.read().strip().split()
                #    modes = modes.split()
                    print(modes)
                    default_mode = [mode for mode in modes if not mode.find("[")]
                    default_mode = default_mode[0].replace("[", "")
                    default_mode = default_mode.replace("]", "")
                    return default_mode
            except Exception as e:
                  messager.put(f"Error memory thp: error to open {folder} folder {e}")
                  return "err"

        def get_thp_sized_modes(folder):
            try:
                with open(f"/sys/kernel/mm/transparent_hugepage/{folder}/enabled", "r") as fd:
                    modes = fd.read().strip()
                    modes = modes.replace("[", '')
                    modes = modes.replace("]", '')
                    modes_list = modes.split()
                    return modes_list
            except Exception as e:
                messager.put(f"Error memory thp: error to open {folder} folder {e}")
                return "err"

        def set_thp(thp_mode, thp_file):
            if thp_size_mode_status[thp_file] == thp_mode:
                return
            result = run([f"echo {thp_mode} > /sys/kernel/mm/transparent_hugepage/{thp_file}/enabled"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
            if result.stderr:
                huge_page[thp_file] = thp_size_mode_status[thp_file]
                messager.put(f"Error memory thp: {result.stderr}")
                CTkMessagebox("Error", f"Error to set {thp_mode} in thp {thp_file} mode\n{result.stderr}")
            else:
                messager.put(f"Memory thp: Success to set {thp_file} mode from {thp_size_mode_status[thp_file]} to {thp_mode}, {result.stdout}")
                thp_size_mode_status[thp_file] = thp_mode


        thp_size_mode_status = {}
        huge_page = {}
        try:
            folders = listdir("/sys/kernel/mm/transparent_hugepage/")
            folders_num = len(folders)
            print(folders_num)
        except:
            folders = ""
            folders_num = 0
        print(folders)
        for folder, index in zip(folders, range(4, folders_num+2)):
            if path.isdir("/sys/kernel/mm/transparent_hugepage/" + folder) and folder != "khugepaged":
                    modes_thp = get_thp_sized_modes(folder)
                    if modes_thp != "err":
                        ctk.CTkLabel(frame_thp, text=folder).grid(row=index, column=0)
                        huge_page[folder] = ctk.CTkComboBox(frame_thp, values=modes_thp, state="readonly", command=lambda v=index, f=folder: set_thp(v, f))
                        thp_size_mode_status[folder] = get_thp_sized_mode(folder)
                        huge_page[folder].set(thp_size_mode_status[folder])
                        huge_page[folder].grid(pady=5, row=index, column=1)

    def get_thp_zero_page():
        try:
            with open("/sys/kernel/mm/transparent_hugepage/use_zero_page", "r") as fd:
                return fd.read().strip()
        except:
            return "0"

    def set_thp_zero_page(mode_zero_page):
        try:
            with open("/sys/kernel/mm/transparent_hugepage/use_zero_page", "w") as fd:
                fd.write(str(mode_zero_page))
            messager.put(f"Memory thp: Set Transparent Hugepage zero pages to {mode_zero_page}")
        except Exception as e:
            messager.put(f"Error memory thp: error to set Transparent Hugepage zero pages {e}")
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
                messager.put(f"Memory kthp: Transparent Hugepage defrag seted to {mode}")
            except Exception as e:
                if mode:
                    modo_kthp_defrag.deselect()
                else:
                    modo_kthp_defrag.select()
                messager.put(f"Error memory kthp: error to set Transparent Hugepage defrag to {mode}, {e}")
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        def get_khuge_info(folder):
            try:
                with open(f"/sys/kernel/mm/transparent_hugepage/khugepaged/{folder}", "r") as fd:
                    return fd.read().strip()
            except:
                return "-1"

        def set_kthp_info(mode, folder):
            try:
                verify_value_is_num(mode)
                with open(f"/sys/kernel/mm/transparent_hugepage/khugepaged/{folder}", "w") as fd:
                    fd.write(str(mode))
                messager.put(f"Memory kthp: Success {folder} seted to {mode}")
            except ValueError as e:
                messager.put(f"Error memory thp: Invalid value {mode} in feature {folder}")
                CTkMessagebox(title="value invalid", message=str(e), icon="cancel")
            except Exception as e:
                messager.put(f"Error memory thp: error to set Transparent Hugepage {folder} {e}")
                CTkMessagebox(title="Error", message="A one error ocurred to try to write value\n" + str(e), icon="cancel")

        frame_khugepaged = LabelFrame(frame_memory, text="Khugepaged", background='#212121', foreground="white", labelanchor="n")
        frame_khugepaged.grid(pady=5, column=1, row=3, sticky="nsew", padx=5, rowspan=1)
        folders = ["alloc_sleep_millisecs", "scan_sleep_millisecs", "pages_to_scan"]
        entry_khuge = list(range(3))

        ctk.CTkLabel(frame_khugepaged, text="Defrag").grid(row=0, column=0, padx=5, pady=5)
        modo_kthp_defrag = ctk.CTkSwitch(frame_khugepaged, text="Off/On", command=lambda: set_kthp_defrag(modo_kthp_defrag.get()))
        if get_kthp_defrag() == "1":
            modo_kthp_defrag.select()
        modo_kthp_defrag.grid(row=0, column=1, padx=5, pady=5)

        for folder, row in zip(folders, range(1, 3)):
            mode_kthp_status = get_khuge_info(folder)
            if mode_kthp_status != "-1":
                ctk.CTkLabel(frame_khugepaged, text=folder.replace("_", " ") + ":").grid(row=row, column=0, padx=5, pady=5)
                entry_khuge[row-1] = ctk.CTkEntry(frame_khugepaged, placeholder_text=mode_kthp_status)
                entry_khuge[row-1].grid(row=row, column=1, padx=5, pady=5)
                ctk.CTkButton(frame_khugepaged, text="Aplicar alteração", command=lambda f=folder, r=row-1: set_kthp_info(entry_khuge[r].get(), f)).grid(row=row, column=2, padx=5, pady=5)

    if not path.exists("/sys/kernel/mm/transparent_hugepage"):
        return

    frame_thp = LabelFrame(frame_memory, text="Transparent Huge Page", background='#212121', foreground="white", labelanchor="n")
    frame_thp.grid(pady=5, column=0, row=3, sticky="nsew", padx=5, rowspan=3)

    modos = get_thp_modes("enabled")
    modo_thp_status = get_thp_mode("enabled")
    ctk.CTkLabel(frame_thp, text="Transparent Huge Page mode").grid(row=0, column=0, padx=5, pady=5)
    modo_thp = ctk.CTkComboBox(frame_thp, values=modos, state="readonly", command=set_thp_mode)
    modo_thp.set(modo_thp_status)
    modo_thp.grid(row=0, column=1, padx=5, pady=5)
       # ctk.CTkButton(frame_thp, text="Alterar", command=set_thp_mode).grid(row=0, column=2, padx=5, pady=5)

    thp_defrag_status = get_thp_mode("defrag")
    ctk.CTkLabel(frame_thp, text="Defrag").grid(row=1, column=0, padx=5, pady=5)
    modo_thp_defrag = ctk.CTkComboBox(frame_thp, values=get_thp_modes("defrag"), state="readonly", command=set_thp_defrag_mode)
    modo_thp_defrag.set(thp_defrag_status)
    modo_thp_defrag.grid(row=1, column=1, padx=5, pady=5)
       # ctk.CTkButton(frame_thp, text="Alterar", command=set_thp_defrag_mode).grid(row=1, column=2, padx=5, pady=5)

    thp_shm_status = get_thp_mode("shmem_enabled")
    ctk.CTkLabel(frame_thp, text="Shared mem").grid(row=2, column=0, padx=5, pady=5)
    modo_thp_shm = ctk.CTkComboBox(frame_thp, values=get_thp_modes("shmem_enabled"), state="readonly", command=set_thp_shm_mode)
    modo_thp_shm.set(thp_shm_status)
    modo_thp_shm.grid(row=2, column=1, padx=5, pady=5)
     #   ctk.CTkButton(frame_thp, text="Alterar", command=set_thp_shm_mode).grid(row=2, column=2, padx=5, pady=5)
    
    ctk.CTkLabel(frame_thp, text="Zero page").grid(row=3, column=0, padx=5, pady=5)
    modo_thp_zero_page = ctk.CTkSwitch(frame_thp, text="Off/On", command=lambda: set_thp_zero_page(modo_thp_zero_page.get()))
    if get_thp_zero_page() == "1":
        modo_thp_zero_page.select()
    modo_thp_zero_page.grid(row=3, column=1, padx=5, pady=5)

    get_thp_info()
    rende_khugepaged()
