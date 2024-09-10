from tkinter import LabelFrame
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from blinker import signal
from queue import Queue

def rende_cpu_driver_intel(frame_cpu_freq, messager : Queue):
    def get_cpu_driver_state_mode():
        try:
            with open("/sys/devices/system/cpu/intel_pstate/status", "r") as fd:
                return fd.read().strip()
        except Exception as e:
            messager.put(f"Error intel pstate: Error to get intel pstate mode {e}")
            print("hvgvc")
            return "active"
        
    def get_cpu_driver_no_turbo_mode():
        try:
            with open("/sys/devices/system/cpu/intel_pstate/no_turbo", "r") as fd:
                return int(fd.read().strip())
        except Exception as e:
            messager.put(f"Error intel pstate: Error to get turbo mode state {e}")
            print("hvgvc")

    def set_cpu_driver_no_turbo_mode(value):
        try:
            with open("/sys/devices/system/cpu/intel_pstate/no_turbo", "w") as fd:
                fd.write(str(value))
            print(f"Info intel pstate: Turbo mode changed to {value}")
            messager.put(f"Info intel pstate: Turbo mode changed to {value}")
        except Exception as e:
            messager.put(f"Error intel pstate: Error to set turbo mode {e}")
            CTkMessagebox(frame_intel_pstate, title="Error", message=f"Ocorreu um erro de escrita.\n{e}", icon="cancel")
        
    def get_cpu_driver_pct_max_val():
        try:
            with open("/sys/devices/system/cpu/intel_pstate/max_perf_pct", "r") as fd:
                return int(fd.read().strip())
        except Exception as e:
            messager.put(f"Error intel pstate: Error to get pct max value {e}")
            print("hvgvc")
        
    def get_cpu_driver_pct_min_val():
        try:
            with open("/sys/devices/system/cpu/intel_pstate/min_perf_pct", "r") as fd:
                return int(fd.read().strip())
        except Exception as e:
            messager.put(f"Error intel pstate: Error to get pct min value {e}")
            print("hvgvc")

    def get_cpu_driver_hwp_mode():
        try:
            with open("/sys/devices/system/cpu/intel_pstate/hwp_dynamic_boost", "r") as fd:
                return int(fd.read().strip())
        except Exception as e:
            messager.put(f"Error intel pstate: Error to get intel pstate dynamic boost {e}")
            print("hvgvc")

    def set_cpu_driver_hwp_mode(value):
        try:
            with open(f"/sys/devices/system/cpu/intel_pstate/hwp_dynamic_boost", "w") as fd:
                fd.write(str(value))
            messager.put(f"Info intel pstate: Dynamic boost mode changed to {value}.")
        except Exception as e:
            messager.put(f"Error intel pstate: Error to set intel pstate dynamic boost {e}.")
            CTkMessagebox(frame_intel_pstate, title="Error", message=f"Ocorreu um erro de escrita.\n{e}", icon="cancel")

    def set_cpu_driver_state_mode(value):
        nonlocal pstate_mode
        if pstate_mode == value: # evita gasto computacional elevado
            return
        try:
            with open("/sys/devices/system/cpu/intel_pstate/status", "w") as fd:
                fd.write(value)
            pstate_mode = value
            if value == "passive":
                label_hwp.grid_forget()
                hwp_dynamin_boost.grid_forget()
            elif value == "active":
                label_hwp.grid(row=4, column=0, padx=5, pady=5)
                hwp_dynamin_boost.grid(row=4, column=1, padx=5, pady=5)
            signal("change governor table").send()
            messager.put(f"Info intel pstate: intel pstate mode changed to {value}.")
        except Exception as e:
            messager.put(f"Error intel pstate: Error to set intel pstate mode {e}.")
            CTkMessagebox(frame_intel_pstate, title="Error", message=f"Ocorreu um erro de escrita.\n{e}", icon="cancel")

    def set_cpu_driver_pct_max_val(value):
        value = int(value)
        try:
            if value < min_pct_val:
                max_perf_pct_value.set(min_pct_val)
                value = min_pct_val
            with open("/sys/devices/system/cpu/intel_pstate/max_perf_pct", "w") as fd:
                fd.write(str(value))
            nonlocal max_pct_val
            max_pct_val = value
            label_max_pct.configure(text=str(value) + "%")
            messager.put(f"Info intel pstate: Max perf pct changed to {value}.")
        except Exception as e:
            messager.put(f"Error intel pstate: Error to set intel pstate max pct val {e}.")
            CTkMessagebox(frame_intel_pstate, title="Error", message=f"Ocorreu um erro de escrita.\n{e}", icon="cancel")

    def set_cpu_driver_pct_min_val(value):
        value = int(value)
        try:
            if value > max_pct_val:
                min_perf_pct_value.set(max_pct_val)
                value = max_pct_val
            with open("/sys/devices/system/cpu/intel_pstate/min_perf_pct", "w") as fd:
                fd.write(str(value))
            nonlocal min_pct_val
            min_pct_val = value
            label_min_pct.configure(text=str(value) + "%")
            messager.put(f"Info intel pstate: Min perf pct changed to {value}.")
        except Exception as e:
            messager.put(f"Error intel pstate: Error to set intel pstate min pct val {e}.")
            CTkMessagebox(frame_intel_pstate, title="Error", message=f"Ocorreu um erro de escrita.\n{e}", icon="cancel")

    pstate_mode = get_cpu_driver_state_mode()
    max_pct_val = get_cpu_driver_pct_max_val()
    min_pct_val = get_cpu_driver_pct_min_val()
    frame_intel_pstate = LabelFrame(frame_cpu_freq, text="Intel P-state", background='#212121', foreground="white")
    frame_intel_pstate.grid(column=0)
    ctk.CTkLabel(frame_intel_pstate, text="Intel P-state mode").grid(row=0, column=0, padx=5, pady=5)
    intel_pstate_mode = ctk.CTkComboBox(frame_intel_pstate, values=["active", "passive", "off"], state="readonly", command=set_cpu_driver_state_mode)
    intel_pstate_mode.set(pstate_mode)
    intel_pstate_mode.grid(row=0, column=1, padx=5, pady=5)
    ctk.CTkLabel(frame_intel_pstate, text="No turbo:").grid(row=1, column=0, padx=5, pady=5)
    no_turbo_mode = ctk.CTkSwitch(frame_intel_pstate, text="Off/On", command=lambda: set_cpu_driver_no_turbo_mode(no_turbo_mode.get()))
    if get_cpu_driver_no_turbo_mode():
        no_turbo_mode.select()
    no_turbo_mode.grid(row=1, column=1, padx=5, pady=5)
    ctk.CTkLabel(frame_intel_pstate, text="Max pct value:").grid(row=2, column=0, padx=5, pady=5)
    max_perf_pct_value = ctk.CTkSlider(frame_intel_pstate, from_=0, to=100, command=set_cpu_driver_pct_max_val)
    max_perf_pct_value.set(max_pct_val)
    max_perf_pct_value.grid(row=2, column=1, padx=5, pady=5)
    label_max_pct = ctk.CTkLabel(frame_intel_pstate, text=str(max_pct_val) + "%")
    label_max_pct.grid(row=2, column=2, padx=5, pady=5)
    ctk.CTkLabel(frame_intel_pstate, text="Min pct value:").grid(row=3, column=0, padx=5, pady=5)
    min_perf_pct_value = ctk.CTkSlider(frame_intel_pstate, from_=0, to=100, command=set_cpu_driver_pct_min_val)
    min_perf_pct_value.set(min_pct_val)
    min_perf_pct_value.grid(row=3, column=1, padx=5, pady=5)
    label_min_pct = ctk.CTkLabel(frame_intel_pstate, text=str(min_pct_val) + "%")
    label_min_pct.grid(row=3, column=2, padx=5, pady=5)
    label_hwp = ctk.CTkLabel(frame_intel_pstate, text="hwp dynamic boost:")
    hwp_dynamin_boost = ctk.CTkSwitch(frame_intel_pstate, text="Off/On", command=lambda: set_cpu_driver_hwp_mode(hwp_dynamin_boost.get()))
    if get_cpu_driver_hwp_mode():
        hwp_dynamin_boost.select()
    if pstate_mode == "active":
        label_hwp.grid(row=4, column=0, padx=5, pady=5)
        hwp_dynamin_boost.grid(row=4, column=1, padx=5, pady=5)