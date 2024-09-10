import customtkinter as ctk
from os import listdir, path
from tkinter import LabelFrame
from os import system
from CTkMessagebox import CTkMessagebox

class io_manager:

    def get_adv_sched_val(self, device):
        folders = listdir(f"/sys/block/{device}/queue/iosched")
        num_folders = len(folders)
        list_folders = list(range(num_folders))
        for folder in range(num_folders):
            try:
                with open(f"/sys/block/{device}/queue/iosched/{folders[folder]}", "r") as fd:
                    list_folders[folder] = fd.read().strip()
            except:
                list_folders[folder] = "err"
        return list_folders

    def set_adv_sched_param(self, device, sched, folder, val_idx):
        try:
            with open(f"/sys/block/{device}/queue/iosched/{folder}", "w") as fd:
                fd.write(str(val_idx))
        except:
            print(val_idx, "err")

    def rende_deadline_adv_sched(self, device):
        ctk.CTkLabel(self.win_sched_adv, text=f"Deadline Advanced Sched for {device}").grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        folders = listdir(f"/sys/block/{device}/queue/deadline")
        num_folders = len(folders)
        list_sched_params = list(range(num_folders))
        list_sched_params_button = list(range(num_folders))
        list_sched_values = self.get_adv_sched_val(device, sched="deadline")
        for folder in range(num_folders):
            if list_sched_values[folder] == "err":
                continue
            folder_param = folders[folder]
            ctk.CTkLabel(self.win_sched_adv, text=folder_param.replace("_", " ") + ":").grid(row=folder+1, column=0, padx=5, pady=5)
            if folder_param != "front_merges":
                list_sched_params[folder] = ctk.CTkEntry(self.win_sched_adv, placeholder_text=list_sched_values[folder])
                list_sched_params[folder].grid(row=folder+1, column=1, padx=5, pady=5)
                list_sched_params_button[folder] = ctk.CTkButton(self.win_sched_adv, command=lambda dev=device, idx=folder: self.set_adv_sched_param(dev, "deadline", folders[idx], list_sched_params[idx].get()))
                list_sched_params_button[folder].grid(row=folder+1, column=2, padx=5, pady=5)
            else:
                list_sched_params[folder] = ctk.CTkSwitch(self.win_sched_adv, text="off/on", command=lambda dev=device, idx=folder: self.set_adv_sched_param(dev, "deadline", folders[idx], list_sched_params[idx].get()))
                if list_sched_values[folder] == "1":
                    list_sched_params[folder].selected()
                list_sched_params[folder].grid(row=folder+1, column=1, padx=5, pady=5)

    def rende_cfq_adv_sched(self, device):
        ctk.CTkLabel(self.win_sched_adv, text=f"CFQ Advanced Sched for {device}").grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        folders = listdir(f"/sys/block/{device}/queue/cfq")
        num_folders = len(folders)
        list_sched_params = list(range(num_folders))
        list_sched_params_button = list(range(num_folders))
        list_sched_values = self.get_adv_sched_val(device, sched="cfq")
        for folder in range(num_folders):
            if list_sched_values[folder] == "err":
                continue
            folder_param = folders[folder]
            ctk.CTkLabel(self.win_sched_adv, text=folder_param.replace("_", " ") + ":").grid(row=folder+1, column=0, padx=5, pady=5)
            if folder_param != "slice_idle" or folder_param != "group_idle":
                list_sched_params[folder] = ctk.CTkEntry(self.win_sched_adv, placeholder_text=list_sched_values[folder])
                list_sched_params[folder].grid(row=folder+1, column=1, padx=5, pady=5)
                list_sched_params_button[folder] = ctk.CTkButton(self.win_sched_adv, command=lambda dev=device, idx=folder: self.set_adv_sched_param(dev, "cfq", folders[idx], list_sched_params[idx].get()))
                list_sched_params_button[folder].grid(row=folder+1, column=2, padx=5, pady=5)
            else:
                list_sched_params[folder] = ctk.CTkSwitch(self.win_sched_adv, text="off/on", command=lambda dev=device, idx=folder: self.set_adv_sched_param(dev, "cfq", folders[idx], list_sched_params[idx].get()))
                if list_sched_values[folder] == "1":
                    list_sched_params[folder].selected()
                list_sched_params[folder].grid(row=folder+1, column=1, padx=5, pady=5)

    def rende_adv_sched_generic(self, device, sched):
        ctk.CTkLabel(self.win_sched_adv, text=f"{sched} Advanced Sched for {device} - Generic mode").grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        try:
        #    folders = listdir(f"/sys/block/{device}/queue/{sched}")
            folders = listdir(f"/sys/block/{device}/queue/iosched")
        except FileNotFoundError:
            self.win_sched_adv.destroy()
            CTkMessagebox(title="No params avalable", message="The current governor don´t have params to configure", icon="info")
            return
        num_folders = len(folders)
        list_sched_params = list(range(num_folders))
        list_sched_params_button = list(range(num_folders))
        list_sched_values = self.get_adv_sched_val(device)
        for folder in range(num_folders):
            if list_sched_values[folder] == "err":
                continue
            folder_param = folders[folder]
            ctk.CTkLabel(self.win_sched_adv, text=folder_param.replace("_", " ") + ":").grid(row=folder+1, column=0, padx=5, pady=5)
            list_sched_params[folder] = ctk.CTkEntry(self.win_sched_adv, placeholder_text=list_sched_values[folder])
            list_sched_params[folder].grid(row=folder+1, column=1, padx=5, pady=5)
            list_sched_params_button[folder] = ctk.CTkButton(self.win_sched_adv, text="Aplicar alteração", command=lambda dev=device, idx=folder: self.set_adv_sched_param(dev, sched, folders[idx], list_sched_params[idx].get()))
            list_sched_params_button[folder].grid(row=folder+1, column=2, padx=5, pady=5)

    def rende_advanced_sched_params(self, device, sched):
        self.win_sched_adv = ctk.CTkToplevel(self.menu)
        self.win_sched_adv.title(f"Advanced Scheduling Parameters - {sched} - {device}")
        if sched == "cfq":
            self.rende_cfq_adv_sched(device)
        elif sched == "deadline":
            self.rende_deadline_adv_sched(device)
        else:
            self.rende_adv_sched_generic(device, sched)


    def get_static_io_devices(self):
        try:
            devices_dr = listdir("/sys/block/")
            devices = [device for device in devices_dr if path.isdir(f"/sys/block/{device}") and device.find("zram") and device.find("loop")] # permita todos os blocos menos o zram
            return devices
        except:
            return "err"
    
    def get_special_io_devices(self):
        try:
            devices_dr = listdir("/sys/block/")
            devices = [device for device in devices_dr if path.isdir(f"/sys/block/{device}") and not device.find("loop")] # permita todos os blocos menos o zram
            return devices
        except:
            return "err"

    def get_device_schedulers(self, device):
        try:
            with open(f"/sys/block/{device}/queue/scheduler", "r") as fd:
                schedulers = fd.read().strip()
                schedulers = schedulers.replace("[", '')
                schedulers = schedulers.replace("]", '')
                schedulers_list = schedulers.split()
                return schedulers_list
        except:
            return "err"
    
    def get_device_scheduler(self, device):
        try:
            with open(f"/sys/block/{device}/queue/scheduler", "r") as fd:
                schedulers = fd.read().strip()
                schedulers = schedulers.split()
                print(schedulers)
                default_sched = [scheduler for scheduler in schedulers if not scheduler.find("[")]
                default_sched = default_sched[0].replace("[", "")
                default_sched = default_sched.replace("]", "")
                return default_sched
        except:
            return "err"

    def set_device_scheduler(self, device, sched):
        print(device, sched)
        system(f"echo {sched} > /sys/block/{device}/queue/scheduler")

    def get_io_state(self, device, folder):
        try:
            with open(f"/sys/block/{device}/queue/{folder}", "r") as fd:
                return fd.read().strip()
        except:
            return "1"

    def set_io_state(self, device, folder, value):
        print(device, folder, value)
        try:
            with open(f"/sys/block/{device}/queue/{folder}", "w") as fd:
                fd.write(str(value))
        except:
            print(Exception)

    def combobox_treat_val(self, val, folder, device):
        self.set_io_state(device, folder, val[0])

    def rende_io_devices(self):
        self.io_devices = self.get_static_io_devices()
        special_devices = self.get_special_io_devices()
       # devices.extend(special_devices)
        devices = list(self.io_devices)
        devices.extend(special_devices)
        devices_len = len(devices)
        scheduler_box = list(range(devices_len))
        list_io_stat = list(range(devices_len))
        list_random_io = list(range(devices_len))
        list_rotational_io = list(range(devices_len))
        list_nomerges_io = list(range(devices_len))
        list_rq_affinity_io = list(range(devices_len))
        list_max_sector_io = list(range(devices_len))
        self.number_sector_selected = list(range(devices_len))
        self.list_ahead_io = list(range(devices_len))
        self.number_ahead_selected = list(range(devices_len))
        list_entry_nr_request = list(range(devices_len))
        device_frame = list(range(devices_len))
      #  list_bolean_io_folders = ["iostats", "add_random", "rotational"]
       # list_bolean_io_labels = ["io statistics:", "randomize io:", "rotational device:"]
    #    devices_list = {} # lista auxiliar para adição e remoção de frames


        #list_io_boelans = list(range(3 * devices_len))
        for device_idx, device in zip(range(devices_len), devices):
            device_frame[device_idx] = LabelFrame(self.frame_global_io, text=device, background='#212121', foreground="white", labelanchor="n")
            device_frame[device_idx].grid(row=device_idx // 2, column=device_idx % 2, padx=5, pady=5)

            # scheduler
            ctk.CTkLabel(device_frame[device_idx], text="scheduler:").grid(row=0, column=0, padx=5, pady=5)
            scheduler_box[device_idx] = ctk.CTkComboBox(device_frame[device_idx], state="readonly", values=self.get_device_schedulers(device), command=lambda idx=device_idx, dev=device: self.set_device_scheduler(dev, idx))
            scheduler_box[device_idx].set(self.get_device_scheduler(device))
            scheduler_box[device_idx].grid(row=0, column=1, padx=5, pady=5)
           # ctk.CTkButton(device_frame, text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_device_scheduler(dev, scheduler_box[idx].get())).grid(row=0, column=2)
            ctk.CTkButton(device_frame[device_idx], text="Advanced scheduler parameters", command=lambda idx=device_idx, dev=device: self.rende_advanced_sched_params(dev, scheduler_box[idx].get())).grid(row=0, column=2, padx=5, pady=5)

         #   """"""
          #  
      #      for folder, label, row in zip(list_bolean_io_folders, list_bolean_io_labels, range(3)):
       #         ctk.CTkLabel(device_frame, text=label).grid(row=row+1, column=0, padx=5, pady=5)
        #        list_io_boelans[row] = ctk.CTkSwitch(device_frame, text="off/on", command=lambda idx2=row * devices_len, dev=device, fd=folder: self.set_io_state(dev, fd, list_io_boelans[idx2].get(), idx2))
         #       if self.get_io_state(device, folder) == "1":
          #          list_io_boelans[row].select()
           #     list_io_boelans[row].grid(row=row+1, column=1, padx=5, pady=5)
         #   """""""

            # io stat
            ctk.CTkLabel(device_frame[device_idx], text="io statistics:").grid(row=1, column=0, padx=5, pady=5)
            list_io_stat[device_idx] = ctk.CTkSwitch(device_frame[device_idx], text="off/on", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "iostats", list_io_stat[idx].get()))
            if self.get_io_state(device, "iostats") == "1":
                list_io_stat[device_idx].select()
            list_io_stat[device_idx].grid(row=1, column=1, padx=5, pady=5)

            # random io
            ctk.CTkLabel(device_frame[device_idx], text="randomize io:").grid(row=2, column=0, padx=5, pady=5)
            list_random_io[device_idx] = ctk.CTkSwitch(device_frame[device_idx], text="off/on", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "add_random", list_random_io[idx].get()))
            if self.get_io_state(device, "add_random") == "1":
                list_random_io[device_idx].select()
            list_random_io[device_idx].grid(row=2, column=1, padx=5, pady=5)

            # rotation device
            ctk.CTkLabel(device_frame[device_idx], text="rotational device:").grid(row=3, column=0, padx=5, pady=5)
            list_rotational_io[device_idx] = ctk.CTkSwitch(device_frame[device_idx], text="off/on", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "rotational", list_rotational_io[idx].get()))
            if self.get_io_state(device, "rotational") == "1":
                list_rotational_io[device_idx].select()
            list_rotational_io[device_idx].grid(row=3, column=1, padx=5, pady=5)

            # nomerges
            nomerge_value = ["0 (enabled)", "1 (partial disabled)", "2 (full disabled)"]
            ctk.CTkLabel(device_frame[device_idx], text="nomerges:").grid(row=4, column=0, padx=5, pady=5)
            list_nomerges_io[device_idx] = ctk.CTkComboBox(device_frame[device_idx], values=nomerge_value, state="readonly")
          #  list_nomerges_io[device_idx] = ctk.CTkComboBox(device_frame, values=nomerge_value, command=lambda idx=device_idx, dev=device: print(idx[0]))
        #    if self.get_io_state(device, "nomerges") == "1":
            list_nomerges_io[device_idx].set(nomerge_value[int(self.get_io_state(device, "nomerges"))])
            list_nomerges_io[device_idx].grid(row=4, column=1, padx=5, pady=5)
            ctk.CTkButton(device_frame[device_idx], text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "nomerges", list_nomerges_io[idx].get()[0])).grid(row=4, column=2, padx=5, pady=5)

            # rq affinity
            re_affinity_value = ["0", "1", "2"] # por mudar
            ctk.CTkLabel(device_frame[device_idx], text="rq affinity:").grid(row=5, column=0, padx=5, pady=5)
            list_rq_affinity_io[device_idx] = ctk.CTkComboBox(device_frame[device_idx], values=re_affinity_value, state="readonly")
          #  list_nomerges_io[device_idx] = ctk.CTkComboBox(device_frame, values=nomerge_value, command=lambda idx=device_idx, dev=device: print(idx[0]))
        #    if self.get_io_state(device, "nomerges") == "1":
            list_rq_affinity_io[device_idx].set(nomerge_value[int(self.get_io_state(device, "rq_affinity"))])
            list_rq_affinity_io[device_idx].grid(row=5, column=1, padx=5, pady=5)
            ctk.CTkButton(device_frame[device_idx], text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "rq_affinity", list_rq_affinity_io[idx].get()[0])).grid(row=5, column=2, padx=5, pady=5)

            def treat_read_block_val(index, value, device, widget):
                print(index, str(value), device, widget)
                self.number_sector_selected[index].configure(text=str(int(value)) + " KB")
                self.set_io_state(device, "max_sectors_kb", value)

            # max_sector_size
            logical_blk_size = int(self.get_io_state(device, "logical_block_size"))
            ctk.CTkLabel(device_frame[device_idx], text="max sector size:").grid(row=6, column=0, padx=5, pady=5)
            self.number_sector_selected[device_idx] = ctk.CTkLabel(device_frame[device_idx], text=self.get_io_state(device, "max_hw_sectors_kb") + " KB")
            list_max_sector_io[device_idx] = ctk.CTkSlider(device_frame[device_idx], from_=1, to=int(self.get_io_state(device, "max_hw_sectors_kb")), number_of_steps=logical_blk_size, command=lambda widget=device_idx, val=device_idx, dev=device: treat_read_block_val(val, int(widget), dev, self.number_sector_selected[device_idx]))
            print(device, int(self.get_io_state(device, "max_sectors_kb")) * 1000)
            list_max_sector_io[device_idx].set(int(int(self.get_io_state(device, "max_sectors_kb"))))
            list_max_sector_io[device_idx].grid(row=6, column=1, padx=5, pady=5)
            self.number_sector_selected[device_idx].grid(row=6, column=2, padx=5, pady=5)

            #
            def treat_read_ahead_val(index, value, device, widget):
                print(index, str(value), device, widget)
                self.number_ahead_selected[index].configure(text=str(int(value)) + " kb")
                self.set_io_state(device, "read_ahead_kb", value)

            read_ahead_size = int(self.get_io_state(device, "read_ahead_kb"))
            ctk.CTkLabel(device_frame[device_idx], text="read ahead").grid(row=7, column=0, padx=5, pady=5)
            self.number_ahead_selected[device_idx] = ctk.CTkLabel(device_frame[device_idx], text=str(read_ahead_size) + " kb", justify="left")
          #  list_max_sector_io[device_idx] = ctk.CTkSlider(device_frame, from_=logical_blk_size, to=int(self.get_io_state(device, "max_hw_sectors_kb")) * 1000, number_of_steps=logical_blk_size, command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "max_sectors_kb", list_max_sector_io[idx].get()))
            self.list_ahead_io[device_idx] = ctk.CTkSlider(device_frame[device_idx], from_=64, to=71296, number_of_steps=64, command=lambda widget=device_idx, val=device_idx, dev=device: treat_read_ahead_val(val, int(widget), dev, self.number_ahead_selected[device_idx])) # wtf
            print(device, read_ahead_size)
            self.list_ahead_io[device_idx].set(read_ahead_size)
            self.list_ahead_io[device_idx].grid(row=7, column=1, padx=5, pady=5)
            self.number_ahead_selected[device_idx].grid(row=7, column=2, padx=5, pady=5)

            # nr_request
            ctk.CTkLabel(device_frame[device_idx], text="Nr request:").grid(row=8, column=0, padx=5, pady=5)
            list_entry_nr_request[device_idx] = ctk.CTkEntry(device_frame[device_idx], placeholder_text=self.get_io_state(device, "nr_requests"))
            list_entry_nr_request[device_idx].grid(row=8, column=1, padx=5, pady=5)
            ctk.CTkButton(device_frame[device_idx], text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "nr_requests", list_entry_nr_request[idx].get())).grid(row=8, column=2, padx=5, pady=5)

          #  devices_list[device] = device_idx
     #   self.check_system_devices()

        

    def check_system_devices(self):
        devices = self.get_static_io_devices()
        print(devices, self.io_devices)
        if self.io_devices != devices:
            print("mudou")
            for w in self.frame_global_io.winfo_children():
                w.destroy()
            self.rende_io_devices()
        else:
            print("nothing")
            self.task = self.frame_global_io.after(1000, self.check_system_devices)
                


    def rende_io_loop_devices(self):
        self.frame_loop_devices = ctk.CTkFrame(self.frame_global_io)
        self.frame_loop_devices.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.loop_devices = self.get_special_io_devices()
        devices_len = len(self.loop_devices)

        scheduler_box = list(range(devices_len))
        list_io_stat = list(range(devices_len))
        list_random_io = list(range(devices_len))
        list_rotational_io = list(range(devices_len))
        list_nomerges_io = list(range(devices_len))
        list_rq_affinity_io = list(range(devices_len))
        list_max_sector_io = list(range(devices_len))
        self.number_sector_selected = list(range(devices_len))
        self.list_ahead_io = list(range(devices_len))
        self.number_ahead_selected = list(range(devices_len))
        list_entry_nr_request = list(range(devices_len))

        for device, device_idx in zip(self.loop_devices, range(devices_len)):
            frame_loop = LabelFrame(self.frame_loop_devices, text=device, background='#212121', foreground="white", labelanchor="n")
            frame_loop.grid(row=device_idx // 2, column=device_idx % 2, padx=5, pady=5)

            ctk.CTkLabel(frame_loop, text="scheduler:").grid(row=0, column=0, padx=5, pady=5)
            scheduler_box[device_idx] = ctk.CTkComboBox(frame_loop, state="readonly", values=self.get_device_schedulers(device), command=lambda idx=device_idx, dev=device: self.set_device_scheduler(dev, idx))
            scheduler_box[device_idx].set(self.get_device_scheduler(device))
            scheduler_box[device_idx].grid(row=0, column=1, padx=5, pady=5)
           # ctk.CTkButton(device_frame, text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_device_scheduler(dev, scheduler_box[idx].get())).grid(row=0, column=2)
            ctk.CTkButton(frame_loop, text="Advanced scheduler parameters", command=lambda idx=device_idx, dev=device: self.rende_advanced_sched_params(dev, scheduler_box[idx].get())).grid(row=0, column=2, padx=5, pady=5)

         #   """"""
          #  
      #      for folder, label, row in zip(list_bolean_io_folders, list_bolean_io_labels, range(3)):
       #         ctk.CTkLabel(device_frame, text=label).grid(row=row+1, column=0, padx=5, pady=5)
        #        list_io_boelans[row] = ctk.CTkSwitch(device_frame, text="off/on", command=lambda idx2=row * devices_len, dev=device, fd=folder: self.set_io_state(dev, fd, list_io_boelans[idx2].get(), idx2))
         #       if self.get_io_state(device, folder) == "1":
          #          list_io_boelans[row].select()
           #     list_io_boelans[row].grid(row=row+1, column=1, padx=5, pady=5)
         #   """""""

            # io stat
            ctk.CTkLabel(frame_loop, text="io statistics:").grid(row=1, column=0, padx=5, pady=5)
            list_io_stat[device_idx] = ctk.CTkSwitch(frame_loop, text="off/on", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "iostats", list_io_stat[idx].get()))
            if self.get_io_state(device, "iostats") == "1":
                list_io_stat[device_idx].select()
            list_io_stat[device_idx].grid(row=1, column=1, padx=5, pady=5)

            # random io
            ctk.CTkLabel(frame_loop, text="randomize io:").grid(row=2, column=0, padx=5, pady=5)
            list_random_io[device_idx] = ctk.CTkSwitch(frame_loop, text="off/on", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "add_random", list_random_io[idx].get()))
            if self.get_io_state(device, "add_random") == "1":
                list_random_io[device_idx].select()
            list_random_io[device_idx].grid(row=2, column=1, padx=5, pady=5)

            # rotation device
            ctk.CTkLabel(frame_loop, text="rotational device:").grid(row=3, column=0, padx=5, pady=5)
            list_rotational_io[device_idx] = ctk.CTkSwitch(frame_loop, text="off/on", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "rotational", list_rotational_io[idx].get()))
            if self.get_io_state(device, "rotational") == "1":
                list_rotational_io[device_idx].select()
            list_rotational_io[device_idx].grid(row=3, column=1, padx=5, pady=5)

            # nomerges
            nomerge_value = ["0 (enabled)", "1 (partial disabled)", "2 (full disabled)"]
            ctk.CTkLabel(frame_loop, text="nomerges:").grid(row=4, column=0, padx=5, pady=5)
            list_nomerges_io[device_idx] = ctk.CTkComboBox(frame_loop, values=nomerge_value, state="readonly")
          #  list_nomerges_io[device_idx] = ctk.CTkComboBox(device_frame, values=nomerge_value, command=lambda idx=device_idx, dev=device: print(idx[0]))
        #    if self.get_io_state(device, "nomerges") == "1":
            list_nomerges_io[device_idx].set(nomerge_value[int(self.get_io_state(device, "nomerges"))])
            list_nomerges_io[device_idx].grid(row=4, column=1, padx=5, pady=5)
            ctk.CTkButton(frame_loop, text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "nomerges", list_nomerges_io[idx].get()[0])).grid(row=4, column=2, padx=5, pady=5)

            # rq affinity
            re_affinity_value = ["0", "1", "2"] # por mudar
            ctk.CTkLabel(frame_loop, text="rq affinity:").grid(row=5, column=0, padx=5, pady=5)
            list_rq_affinity_io[device_idx] = ctk.CTkComboBox(frame_loop, values=re_affinity_value, state="readonly")
          #  list_nomerges_io[device_idx] = ctk.CTkComboBox(device_frame, values=nomerge_value, command=lambda idx=device_idx, dev=device: print(idx[0]))
        #    if self.get_io_state(device, "nomerges") == "1":
            list_rq_affinity_io[device_idx].set(nomerge_value[int(self.get_io_state(device, "rq_affinity"))])
            list_rq_affinity_io[device_idx].grid(row=5, column=1, padx=5, pady=5)
            ctk.CTkButton(frame_loop, text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "rq_affinity", list_rq_affinity_io[idx].get()[0])).grid(row=5, column=2, padx=5, pady=5)

            def treat_read_block_val(index, value, device, widget):
                print(index, str(value), device, widget)
                self.number_sector_selected[index].configure(text=str(int(value)) + " KB")
                self.set_io_state(device, "max_sectors_kb", value)

            # max_sector_size
            logical_blk_size = int(self.get_io_state(device, "logical_block_size"))
            ctk.CTkLabel(frame_loop, text="max sector size:").grid(row=6, column=0, padx=5, pady=5)
            self.number_sector_selected[device_idx] = ctk.CTkLabel(frame_loop, text=self.get_io_state(device, "max_hw_sectors_kb") + " KB")
            list_max_sector_io[device_idx] = ctk.CTkSlider(frame_loop, from_=1, to=int(self.get_io_state(device, "max_hw_sectors_kb")), number_of_steps=logical_blk_size, command=lambda widget=device_idx, val=device_idx, dev=device: treat_read_block_val(val, int(widget), dev, self.number_sector_selected[device_idx]))
            print(device, int(self.get_io_state(device, "max_sectors_kb")) * 1000)
            list_max_sector_io[device_idx].set(int(int(self.get_io_state(device, "max_sectors_kb"))))
            list_max_sector_io[device_idx].grid(row=6, column=1, padx=5, pady=5)
            self.number_sector_selected[device_idx].grid(row=6, column=2, padx=5, pady=5)

            #
            def treat_read_ahead_val(index, value, device, widget):
                print(index, str(value), device, widget)
                self.number_ahead_selected[index].configure(text=str(int(value)) + " kb")
                self.set_io_state(device, "read_ahead_kb", value)

            read_ahead_size = int(self.get_io_state(device, "read_ahead_kb"))
            ctk.CTkLabel(frame_loop, text="read ahead").grid(row=7, column=0, padx=5, pady=5)
            self.number_ahead_selected[device_idx] = ctk.CTkLabel(frame_loop, text=str(read_ahead_size) + " kb", justify="left")
          #  list_max_sector_io[device_idx] = ctk.CTkSlider(device_frame, from_=logical_blk_size, to=int(self.get_io_state(device, "max_hw_sectors_kb")) * 1000, number_of_steps=logical_blk_size, command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "max_sectors_kb", list_max_sector_io[idx].get()))
            self.list_ahead_io[device_idx] = ctk.CTkSlider(frame_loop, from_=64, to=71296, number_of_steps=64, command=lambda widget=device_idx, val=device_idx, dev=device: treat_read_ahead_val(val, int(widget), dev, self.number_ahead_selected[device_idx])) # wtf
            print(device, read_ahead_size)
            self.list_ahead_io[device_idx].set(read_ahead_size)
            self.list_ahead_io[device_idx].grid(row=7, column=1, padx=5, pady=5)
            self.number_ahead_selected[device_idx].grid(row=7, column=2, padx=5, pady=5)

            # nr_request
            ctk.CTkLabel(frame_loop, text="Nr request:").grid(row=8, column=0, padx=5, pady=5)
            list_entry_nr_request[device_idx] = ctk.CTkEntry(frame_loop, placeholder_text=self.get_io_state(device, "nr_requests"))
            list_entry_nr_request[device_idx].grid(row=8, column=1, padx=5, pady=5)
            ctk.CTkButton(frame_loop, text="Aplicar alteração", command=lambda idx=device_idx, dev=device: self.set_io_state(dev, "nr_requests", list_entry_nr_request[idx].get())).grid(row=8, column=2, padx=5, pady=5)

    def start_task(self):
        self.check_system_devices()

    def cancel_task(self):
        self.frame_global_io.after_cancel(self.task)

    def rende_io(self, menu):
        self.task = None
        self.menu = menu
        self.frame_global_io = ctk.CTkScrollableFrame(self.menu, width=1080, height=400)
        self.frame_global_io.pack(padx=5, pady=5, expand=True, fill="both")
        self.rende_io_devices()
    #    self.rende_io_loop_devices()