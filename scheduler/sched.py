import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox

class sched:

    def set_sched_val(self, val, feature):
        print(val, feature)
        try:
            with open(f"/proc/sys/kernel/{feature}", "w") as fd:
                fd.write(str(val))
        except:
            CTkMessagebox(self.frame_sched, title="Write error", message=f"Unable to write to /proc/sys/kernel/{feature}", icon="cancel")
         #   print(f"Error: unable to write to /proc/sys/kernel/{feature}")
    
    def get_sched_val(self, feature):
        try:
            with open(f"/proc/sys/kernel/{feature}", "r") as fd:
                return int(fd.read().strip())
        except:
            print(f"Error: unable to read to /proc/sys/kernel/{feature}")
            return -1

    def rende_bolean_sched_widgets(self):
        self.frame_sched = LabelFrame(self.menu, text="Scheduling", background='#212121', foreground="white")
        self.frame_sched.grid(row=3, column=0, padx=5, pady=5)

        list_label_text = ["Sched statistics:", "Timer migration:", "Child runs first:", "sched autogroup enabled:", "Itmt enabled:"]
        list_folders = ["sched_schedstats", "timer_migration", "sched_child_runs_first", "sched_autogroup_enabled", "sched_itmt_enabled"]
        list_widgets_switch = list(range(5))

        index = 0
        for text, folder in zip(list_label_text, list_folders):
            sched_status = self.get_sched_val(folder)
            if sched_status == -1:
                del list_widgets_switch[index]
                continue
            ctk.CTkLabel(self.frame_sched, text=text).grid(row=self.row, column=0, padx=5, pady=5)
            list_widgets_switch[index] = ctk.CTkSwitch(self.frame_sched, text="Off/On", command=lambda idx=index, fd=folder: self.set_sched_val(list_widgets_switch[idx].get(), fd))
            list_widgets_switch[index].grid(row=self.row, column=1, padx=5, pady=5)
            if sched_status == 1:
                list_widgets_switch[index].select()
            self.row += 1
            index += 1
        print("sched:", list_widgets_switch)

    def rend_entry_sched_widgets(self):
        def threat_runtime_val():
            val = sched_runtime_us.get()
            try:
                if not val.isdigit() or int(val) > 950000 or int(val) < -1:
                    raise ValueError
                self.set_sched_val(val, "sched_rt_runtime_us")
            except ValueError:
                CTkMessagebox(self.frame_sched, title="Invalid value", message=f"Invalid value {val}\n necessary integer from -1 to 950000", icon="cancel")
            #    print(f"Error: invalid value {val}\n necessary integer from -1 at 950000")
        
        def threat_sched_val(value, folder):
            try:
                if not value.isdigit() or int(value) < 0:
                    raise ValueError
                self.set_sched_val(value, folder)
            except ValueError:
                CTkMessagebox(self.frame_sched, title="Invalid value", message=f"Invalid value {value}\n necessary positive integer", icon="cancel")
             #   print(f"Error: invalid value {value}\n necessary integer")

        # sched_energy_aware pesquisar no futuro
        list_folders = ["sched_latency_ns", "sched_min_granularity_ns", "sched_wakeup_granularity_ns", "sched_rt_period_us", "sched_migration_cost_ns", "sched_cfs_bandwidth_slice_us", "sched_deadline_period_max_us", "sched_deadline_period_min_us", "sched_rr_timeslice_ms", "sched_util_clamp_max", "sched_util_clamp_min", "sched_util_clamp_min_rt_default"]
        list_text = ["Latency ns:", "Min granularity ns:", "Wakeup granularity ns:", "Rt period us:", "Migration cost ns:", "CFS dlice us:", "Deadline max period:", "Deadline min period:", "Sched rr timeslice ms:", "Util clamp max:", "Util clamp min:", "Util clamp min RT:"]

        # sched_rt_runtime_us tem uns requesitos diferentes
        tmp_sched_runtine = self.get_sched_val("sched_rt_runtime_us")
        if tmp_sched_runtine != -1:
            ctk.CTkLabel(self.frame_sched, text="Sched runtime us:").grid(row=self.row, column=0, padx=5, pady=5)
            sched_runtime_us = ctk.CTkEntry(self.frame_sched, placeholder_text=tmp_sched_runtine)
            sched_runtime_us.grid(row=self.row, column=1, padx=5, pady=5)
            ctk.CTkButton(self.frame_sched, text="Aplicar alteração", command=threat_runtime_val).grid(row=self.row, column=2, padx=5, pady=5)
            self.row += 1
        del tmp_sched_runtine

        for text, folder in zip(list_text, list_folders):
            sched_status = self.get_sched_val(folder)
            if sched_status == -1:
                continue
            ctk.CTkLabel(self.frame_sched, text=text).grid(row=self.row, column=0, padx=5, pady=5)
            sched_entry_widget = ctk.CTkEntry(self.frame_sched, placeholder_text=sched_status)
            sched_entry_widget.grid(row=self.row, column=1, padx=5, pady=5)
            ctk.CTkButton(self.frame_sched, text="Aplicar alteração", command=lambda sched_val=sched_entry_widget, fd=folder: threat_sched_val(sched_val.get(), fd)).grid(row=self.row, column=2, padx=5, pady=5)
            self.row += 1

    def rende_sched(self, menu):
        self.menu = menu
        self.row = 0
        self.rende_bolean_sched_widgets()
        self.rend_entry_sched_widgets()
