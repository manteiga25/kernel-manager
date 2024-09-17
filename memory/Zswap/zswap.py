import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def rende_zswap(frame_memory, messager : Queue):
    def switch_zswap(folder, index):
        state = zswap_state[index].get()
        if state == zswap_value_state[index]:
            return
        try:
            with open(f"/sys/module/zswap/parameters/{folder}", "w") as f:
                f.write(state)
            messager.put(f"Memory zswap: Success to change state of {folder} from {zswap_value_state[index]} to {state}")
            zswap_value_state[index] = state
        except Exception as e:
            if zswap_value_state[index] == "Y":
                zswap_state[index].select()
            else:
                zswap_state[index].deselect()
            messager.put(f"Memory zswap: Error to change state of {folder} from {zswap_value_state[index]} to {state}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_zswap_state(folder):
        try:
            with open(f"/sys/module/zswap/parameters/{folder}", "r") as f:
                return f.read().strip()
        except:
            return "e"

    def get_pool_perc():
        try:
            with open("/sys/module/zswap/parameters/max_pool_percent", "r") as f:
                return int(f.read().strip())
        except:
            return -1

    def switch_pool_value(value):
        nonlocal pool_percent
       # value = str(int(float(pool.get()) * 100))
        if pool_percent == value:
            return
        try:
            with open("/sys/module/zswap/parameters/max_pool_percent", "w") as f:
                f.write(value)
            pool_perc.configure(text=value + "%")
            pool_percent = value
        except Exception as e:
            pool.set(pool_percent)
            pool_perc.configure(text=pool_percent + "%")
            messager.put(f"Memory Zswap: Error to  change pool value from {pool_percent} to {value}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_thre_perc():
        try:
            with open("/sys/module/zswap/parameters/accept_threshold_percent", "r") as f:
                return int(f.read().strip())
        except:
            return -1

    def switch_thre_value(value):
        nonlocal threshold_percentage
        if threshold_percentage == value:
            return
    #    value = str(int(float(threshold.get()) * 100))
        try:
            with open("/sys/module/zswap/parameters/accept_threshold_percent", "w") as f:
                f.write(str(value))
            threshold_perc.configure(text=value + "%")
            threshold_percentage = value
        except Exception as e:
            threshold_perc.configure(text=threshold_percentage + "%")
            threshold.set(threshold_percentage)
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_zswap_compressor():
        try:
            with open("/sys/module/zswap/parameters/compressor", "r") as f:
                return f.read().strip()
        except:
            return "err"

    def set_zswap_algorithm(algoritmo):
        nonlocal zswap_compressor_status
        if algoritmo == zswap_compressor_status:
            return
        try:
          #  algoritmo = algoritmo_zswap.get()
            with open("/sys/module/zswap/parameters/compressor", "w") as f:
                f.write(algoritmo)
            messager.put(f"Memory zswap: Success to change zswap compressor from {zswap_compressor_status} to {algoritmo}")
            zswap_compressor_status = algoritmo
        except Exception as e:
            algoritmo_zswap.set(zswap_compressor_status)
            messager.put(f"Memory zswap: Error to change zswap compressor from {zswap_compressor_status} to {algoritmo}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    def get_zpool_compressor():
        try:
            with open("/sys/module/zswap/parameters/zpool", "r") as f:
                return f.read().strip()
        except:
            return "err"

    def set_zpool_algorithm(algoritmo):
        nonlocal zpool_algorithm_status
        if algoritmo == zpool_algorithm_status:
            return
        try:
       #     algoritmo = algoritmo_zpool.get()
            with open("/sys/module/zswap/parameters/zpool", "w") as f:
                f.write(algoritmo)
            messager.put(f"Memory zswap: Success to change zpool algorithm from {zpool_algorithm_status} to {algoritmo}")
            zpool_algorithm_status = algoritmo
        except Exception as e:
            algoritmo_zpool.set(zpool_algorithm_status)
            messager.put(f"Memory zswap: Error to change zpool algorithm from {zpool_algorithm_status} to {algoritmo}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    frame_zswap = LabelFrame(frame_memory, text="Zswap", background='#212121', foreground="white", labelanchor="n")
    frame_zswap.grid(row=2, column=1, columnspan=6, pady=5, padx=5)
    zswap_feature_bool_name = ["Zswap state", "shrinker", "exclusive loads", "same filled pages", "non same filled pages"]
    zswap_feature_bool_folder =  ["enabled", "shrinker_enabled", "exclusive_loads", "same_filled_pages_enabled", "non_same_filled_pages_enabled"]
    zswap_state = list(range(5))
    zswap_value_state = list(range(5))
    for name_index in range(5):
        zswap_value_state[name_index] = get_zswap_state(zswap_feature_bool_folder[name_index])
        if zswap_value_state[name_index] == "e":
            continue
        ctk.CTkLabel(frame_zswap, text=zswap_feature_bool_name[name_index]).grid(row=name_index, column=0, pady=5)
        zswap_state[name_index] = ctk.CTkSwitch(frame_zswap, text="Off/On", onvalue="Y", offvalue="N", command=lambda index=name_index: switch_zswap(zswap_feature_bool_folder[index], index))
        if zswap_value_state[name_index] == "Y":
            zswap_state[name_index].select()
        else:
            zswap_state[name_index].deselect()
        zswap_state[name_index].grid(row=name_index, column=1, pady=5, padx=5)

    pool_percent = get_pool_perc()
    if pool_percent != -1:
        ctk.CTkLabel(frame_zswap, text="Zpool percent").grid(row=5, column=0)
        pool = ctk.CTkSlider(frame_zswap, from_=0, to=50, command=switch_pool_value)
        pool.set(pool_percent)
    #  pool.bind("<B1-Motion>", switch_pool_value)
    # pool.bind("<Button-1>", switch_pool_value)
        pool.grid(row=5, column=1)
        pool_perc = ctk.CTkLabel(frame_zswap, text=str(pool_percent) + "%")
        pool_perc.grid(row=5, column=2)

    threshold_percentage = get_thre_perc()
    if threshold_percentage != -1:
        ctk.CTkLabel(frame_zswap, text="Threshold percent").grid(row=6, column=0)
        threshold = ctk.CTkSlider(frame_zswap, from_=0, to=100, command=switch_thre_value)
        threshold.set(threshold_percentage)
    #    print(get_thre_perc())
    #   threshold.bind("<B1-Motion>", switch_thre_value)
    #  threshold.bind("<Button-1>", switch_thre_value)
        threshold.grid(row=6, column=1)
        threshold_perc = ctk.CTkLabel(frame_zswap, text=str(threshold_percentage) + "%")
        threshold_perc.grid(row=6, column=2)

    zswap_compressor_status = get_zswap_compressor()
    if zswap_compressor_status != "err":
        ctk.CTkLabel(frame_zswap, text="Zswap alghoritm").grid(row=7, column=0, padx=0, pady=5)
        algoritmo_zswap = ctk.CTkComboBox(frame_zswap, values=["lz4", "lz4hc", "lzo", "lzo-rle", "zstd", "deflate", "842"], state="readonly")
        algoritmo_zswap.set(zswap_compressor_status)
        algoritmo_zswap.grid(row=7, column=1)
        ctk.CTkButton(frame_zswap, text="Alterar", command=set_zswap_algorithm).grid(row=7, column=2)

    zpool_algorithm_status = get_zpool_compressor()
    if zpool_algorithm_status != "err":
        ctk.CTkLabel(frame_zswap, text="Zpool alghoritm").grid(row=8, column=0, padx=0, pady=5)
        algoritmo_zpool = ctk.CTkComboBox(frame_zswap, values=["zbud", "z3fold", "zsmalloc"], state="readonly")
        algoritmo_zpool.set(zpool_algorithm_status)
        algoritmo_zpool.grid(row=8, column=1)
        ctk.CTkButton(frame_zswap, text="Alterar", command=set_zpool_algorithm).grid(row=8, column=2)