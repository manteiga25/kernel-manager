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
            #    modes = modes.split()
                print(modes)
                default_mode = [mode for mode in modes if not mode.find("[")]
                default_mode = default_mode[0].replace("[", "")
                default_mode = default_mode.replace("]", "")
                return default_mode
        except:
            return "err"

    def verify_value_is_num(value: str):
        if not value.isdigit():
            raise ValueError("The value needs to be integer not string")

    def set_thp_defrag_mode(mode):
        result = run([f"echo {mode} > /sys/kernel/mm/transparent_hugepage/defrag"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        if result.stderr:
            modo_thp_defrag.set(thp_defrag_status)
            messager.put(f"Error memory thp: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} in thp defrag mode\n{result.stderr}")
        else:
            thp_defrag_status = mode
            messager.put(f"Memory thp: {result.stdout}")

    def set_thp_mode(mode):
          #  mode = modo_thp.get()
    #    system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/enabled")
        result = run([f"echo {mode} > /sys/kernel/mm/transparent_hugepage/enabled"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        if result.stderr:
            messager.put(f"Error memory thp: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} in thp mode\n{result.stderr}")
        else:
            messager.put(f"Memory thp: {result.stdout}")
        
    def set_thp_shm_mode(mode):
           # mode = modo_thp_shm.get()
    #    system(f"echo {mode} > /sys/kernel/mm/transparent_hugepage/shmem_enabled")
        result = run([f"echo {mode} > /sys/kernel/mm/transparent_hugepage/shmem_defrag"], stderr=PIPE, text=True, shell=True)
        if result.stderr:
            messager.put(f"Error memory thp: {result.stderr}")
            CTkMessagebox("Error", f"Error to set {mode} in thp mode\n{result.stderr}")
        else:
            messager.put(f"Memory thp: {result.stdout}")

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
            print(thp_mode)
             #   state = huge_page[thp].get()
            print(thp_file)
         #   system(f"echo {thp_mode} > /sys/kernel/mm/transparent_hugepage/{thp_file}/enabled")
            result = run([f"echo {thp_mode} > /sys/kernel/mm/transparent_hugepage/{thp_file}/enabled"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
            if result.stderr:
                messager.put(f"Error memory thp: {result.stderr}")
                CTkMessagebox("Error", f"Error to set {thp_mode} in thp {thp_file} mode\n{result.stderr}")
            else:
                messager.put(f"Memory thp: {result.stdout}")


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
            if path.isdir("/sys/kernel/mm/transparent_hugepage/" + folder) and folder != "khugepaged":
                  #  print(folder)
                    #if path.exists()
                #try:
                #    with open(f"/sys/kernel/mm/transparent_hugepage/{folder}/enabled", "r") as huge_fd:
                   #     print("opened " + folder)
                       # estado = huge_fd.read().strip()
                    modes_thp = get_thp_sized_modes(folder)
                    if modes_thp != "err":
                        ctk.CTkLabel(frame_thp, text=folder).grid(row=index, column=0)
                        huge_page = ctk.CTkComboBox(frame_thp, values=modes_thp, state="readonly", command=lambda v=index, f=folder: set_thp(v, f))
                        mode = get_thp_sized_mode(folder)
                        huge_page.set(mode)
                            #huge_page_ok[folder] = ctk.CTkButton(frame_thp, text="Alterar", command=lambda f=folder: set_thp(f))
                        huge_page.grid(pady=5, row=index, column=1)
                        #huge_page_ok[folder].grid(pady=5, row=index, column=2)
              #  except Exception as e:
               #     messager.put(f"Error memory thp: error to open {folder} folder {e}")

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
            except Exception as e:
                messager.put(f"Error memory kthp: error to set Transparent Hugepage defrag {e}")
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
                verify_value_is_num()
                with open(f"/sys/kernel/mm/transparent_hugepage/khugepaged/{folder}", "w") as fd:
                    fd.write(str(mode))
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
            ctk.CTkLabel(frame_khugepaged, text=folder.replace("_", " ") + ":").grid(row=row, column=0, padx=5, pady=5)
            entry_khuge[row-1] = ctk.CTkEntry(frame_khugepaged, placeholder_text=get_khuge_info(folder))
            entry_khuge[row-1].grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkButton(frame_khugepaged, text="Aplicar alteração", command=lambda f=folder, r=row-1: set_kthp_info(entry_khuge[r].get(), folder)).grid(row=row, column=2, padx=5, pady=5)

    if not path.exists("/sys/kernel/mm/transparent_hugepage"):
        return

    frame_thp = LabelFrame(frame_memory, text="Transparent Huge Page", background='#212121', foreground="white", labelanchor="n")
    frame_thp.grid(pady=5, column=0, row=3, sticky="nsew", padx=5, rowspan=3)
    modos = get_thp_modes("enabled")
    modo = get_thp_mode("enabled")
    ctk.CTkLabel(frame_thp, text="Transparent Huge Page mode").grid(row=0, column=0, padx=5, pady=5)
    modo_thp = ctk.CTkComboBox(frame_thp, values=modos, state="readonly", command=set_thp_mode)
    modo_thp.set(modo)
    modo_thp.grid(row=0, column=1, padx=5, pady=5)
       # ctk.CTkButton(frame_thp, text="Alterar", command=set_thp_mode).grid(row=0, column=2, padx=5, pady=5)

    thp_defrag_status = get_thp_mode("defrag")
    ctk.CTkLabel(frame_thp, text="Defrag").grid(row=1, column=0, padx=5, pady=5)
    modo_thp_defrag = ctk.CTkComboBox(frame_thp, values=get_thp_modes("defrag"), state="readonly", command=set_thp_defrag_mode)
    modo_thp_defrag.set(thp_defrag_status)
    modo_thp_defrag.grid(row=1, column=1, padx=5, pady=5)
       # ctk.CTkButton(frame_thp, text="Alterar", command=set_thp_defrag_mode).grid(row=1, column=2, padx=5, pady=5)

    ctk.CTkLabel(frame_thp, text="Shared mem").grid(row=2, column=0, padx=5, pady=5)
    modo_thp_shm = ctk.CTkComboBox(frame_thp, values=get_thp_modes("shmem_enabled"), state="readonly", command=set_thp_shm_mode)
    modo_thp_shm.set(get_thp_mode("shmem_enabled"))
    modo_thp_shm.grid(row=2, column=1, padx=5, pady=5)
     #   ctk.CTkButton(frame_thp, text="Alterar", command=set_thp_shm_mode).grid(row=2, column=2, padx=5, pady=5)
    
    ctk.CTkLabel(frame_thp, text="Zero page").grid(row=3, column=0, padx=5, pady=5)
    modo_thp_zero_page = ctk.CTkSwitch(frame_thp, text="Off/On", command=lambda: set_thp_zero_page(modo_thp_zero_page.get()))
    if get_thp_zero_page() == "1":
        modo_thp_zero_page.select()
    modo_thp_zero_page.grid(row=3, column=1, padx=5, pady=5)

    get_thp_info()
    rende_khugepaged()