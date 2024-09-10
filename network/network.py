import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox

class network:

    def set_ipv4_val(self, val, folder):
        try:
            with open(f"/proc/sys/net/ipv4/{folder}", "w") as fd:
                fd.write(val)
        except:
            print("error")

    def get_ipv4_value(self, folder):
        try:
            with open(f"/proc/sys/net/ipv4/{folder}", "r") as fd:
                return fd.read().strip()
        except:
            return "err"

    def rende_ipv4_switch(self):
        list_ipv4_switch_folders = ["tcp_tw_reuse", "tcp_tw_recycle", "ip_forward", "icmp_echo_ignore_all", "accept_redirects", "accept_source_route"]
        list_ipv4_switch_text = ["tcp tw reuse:", "tcp tw recycle:", "IP forward:", "Ignore ICMP packs:", "Acept ICMP redierect pack:", "Acept source routing:"]
        list_ipv4_switch = list(range(6))
        index = 0
        for ipv4_feature, ipv4_text in zip(list_ipv4_switch_folders, list_ipv4_switch_text):
            ipv4_value = self.get_ipv4_value(ipv4_feature)
            if ipv4_value == "err":
                del list_ipv4_switch[index]
                continue
            ctk.CTkLabel(self.ipv4_frame, text=ipv4_text).grid(row=self.ipv4_row, column=0, padx=5, pady=5)
            list_ipv4_switch[index] = ctk.CTkSwitch(self.ipv4_frame, text="Off/On", command=lambda idx=index, fd=ipv4_feature: self.set_ipv4_val(list_ipv4_switch[idx].get(), fd))
            list_ipv4_switch[index].grid(row=self.ipv4_row, column=1, padx=5, pady=5)
            if ipv4_value == 1:
                list_ipv4_switch[index].select()
            self.ipv4_row += 1
            index += 1

    def rende_ipv4_entry(self):
        def threat_ipv4_val(value, folder):
            try:
                if not value.isdigit() or int(value) < 0:
                    raise ValueError
                self.set_ipv4_val(value, folder)
            except ValueError:
                CTkMessagebox(self.ipv4_frame, title="Invalid value", message=f"Invalid value {value}\n necessary positive integer", icon="cancel")

        list_ipv4_folders = ["tcp_syn_retries", "tcp_synack_retries", "tcp_fin_timeout", "tcp_keepalive_time", "tcp_keepalive_probes", "tcp_keepalive_intvl", "tcp_max_syn_backlog", "tcp_rmem", "tcp_wmem"]
        list_ipv4_text = list_ipv4_folders

        for text, folder in zip(list_ipv4_text, list_ipv4_folders):
            ipv4_val = self.get_ipv4_value(folder)
            if ipv4_val == "err":
                continue
            ctk.CTkLabel(self.ipv4_frame, text=text).grid(row=self.ipv4_row, column=0, padx=5, pady=5)
            ipv4_entry_widget = ctk.CTkEntry(self.ipv4_frame, placeholder_text=ipv4_val)
            ipv4_entry_widget.grid(row=self.ipv4_row, column=1, padx=5, pady=5)
            ctk.CTkButton(self.ipv4_frame, text="Aplicar alteração", command=lambda ipv4_value=ipv4_entry_widget, fd=folder: threat_ipv4_val(ipv4_value.get(), fd)).grid(row=self.ipv4_row, column=2, padx=5, pady=5)
            self.ipv4_row += 1

    def rende_ipv4_frame(self):
        self.ipv4_frame = LabelFrame(self.frame_network_global, text="IPv4", background='#212121', foreground="white")
        self.ipv4_frame.grid(column=0, row=0, padx=5, pady=5)
        self.ipv4_row = 0
        self.rende_ipv4_switch()
        self.rende_ipv4_entry()

    def set_ipv6_val(self, val, folder):
        try:
            with open(f"/proc/sys/net/ipv6/{folder}", "w") as fd:
                fd.write(val)
        except:
            print("error")

    def get_ipv6_value(self, folder):
        try:
            with open(f"/proc/sys/net/ipv6/{folder}", "r") as fd:
                return fd.read().strip()
        except:
            return "err"

    def rende_ipv6_switch(self):
        list_ipv6_switch_folders = ["conf/all/forwarding", "conf/all/autoconf", "conf/all/accept_ra", "conf/all/accept_ra_defrtr" "icmp/echo_ignore_all", "conf/all/accept_redirects", "conf/all/log_martians"]
        list_ipv6_switch_text = ["forwarding:", "autoconfig:", "Accept ra:", "Accept ra defrtr:", "ICMP ignore all:", "Accept redirects:", "log martians:"]
        list_ipv6_switch = list(range(6))
        index = 0
        for ipv6_feature, ipv6_text in zip(list_ipv6_switch_folders, list_ipv6_switch_text):
            ipv6_value = self.get_ipv6_value(ipv6_feature)
            if ipv6_value == "err":
                del list_ipv6_switch[index]
                continue
            ctk.CTkLabel(self.ipv6_frame, text=ipv6_text).grid(row=self.ipv6_row, column=0, padx=5, pady=5)
            list_ipv6_switch[index] = ctk.CTkSwitch(self.ipv6_frame, text="Off/On", command=lambda idx=index, fd=ipv6_feature: self.set_ipv6_val(list_ipv6_switch[idx].get(), fd))
            list_ipv6_switch[index].grid(row=self.ipv6_row, column=1, padx=5, pady=5)
            if ipv6_value == 1:
                list_ipv6_switch[index].select()
            self.ipv6_row += 1
            index += 1

    def rende_ipv6_entry(self):
        def threat_ipv6_val(value, folder):
            try:
                if not value.isdigit() or int(value) < 0:
                    raise ValueError
                self.set_ipv6_val(value, folder)
            except ValueError:
                CTkMessagebox(self.ipv6_frame, title="Invalid value", message=f"Invalid value {value}\n necessary positive integer", icon="cancel")

        list_ipv6_folders = ["tcp_syn_retries", "tcp_synack_retries", "tcp_fin_timeout", "tcp_keepalive_time", "tcp_keepalive_probes", "tcp_keepalive_intvl", "tcp_max_syn_backlog", "tcp_rmem", "tcp_wmem", "conf/all/router_solicitations", "route/max_size", "route/gc_thresh1", "route/gc_thresh2", "route/gc_thresh3"]
        list_ipv6_text = list_ipv6_folders

        for text, folder in zip(list_ipv6_text, list_ipv6_folders):
            ipv6_val = self.get_ipv6_value(folder)
            if ipv6_val == "err":
                continue
            ctk.CTkLabel(self.ipv6_frame, text=text).grid(row=self.ipv6_row, column=0, padx=5, pady=5)
            ipv6_entry_widget = ctk.CTkEntry(self.ipv6_frame, placeholder_text=ipv6_val)
            ipv6_entry_widget.grid(row=self.ipv6_row, column=1, padx=5, pady=5)
            ctk.CTkButton(self.ipv6_frame, text="Aplicar alteração", command=lambda ipv6_value=ipv6_entry_widget, fd=folder: threat_ipv6_val(ipv6_value.get(), fd)).grid(row=self.ipv6_row, column=2, padx=5, pady=5)
            self.ipv6_row += 1

    def rende_ipv6_frame(self):
        print("ipv6")
        self.ipv6_frame = LabelFrame(self.frame_network_global, text="IPv6", background='#212121', foreground="white")
        self.ipv6_frame.grid(column=1, row=0, padx=5, pady=5)
        self.ipv6_row = 0
        self.rende_ipv6_switch()
        self.rende_ipv6_entry()

    def rende_network(self, menu):
        self.menu = menu
        self.frame_network_global = ctk.CTkScrollableFrame(self.menu)
        self.frame_network_global.pack(padx=5, pady=5, fill="both", expand=True)
        self.rende_ipv4_frame()
        self.rende_ipv6_frame()