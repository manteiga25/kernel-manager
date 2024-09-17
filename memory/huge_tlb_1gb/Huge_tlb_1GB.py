import customtkinter as ctk
from tkinter import LabelFrame
from CTkMessagebox import CTkMessagebox
from queue import Queue

def verify_value_is_num(value: str):
        if not value.isdigit() or int(value) < 0:
            raise ValueError("The value needs to be integer not string and > 0")

def rende_huge_tlb(frame_memory, messager : Queue):

    def update_entry_value(folder, index_widget):
        value = get_1gb_huge(folder)
        entry_hp[index_widget].delete(0, "end")
        entry_hp[index_widget].insert(0, value)
        messager.put(f"Memory Huge TLB 1GB: kernel as update value of {folder} to {value}")

    def get_1gb_huge(folder):
            try:
                with open(f"/sys/kernel/mm/hugepages/hugepages-1048576kB/{folder}", "r") as fd:
                    return fd.read().strip()
            except:
                return "err"

    def set_1gb_huge(folder, idx):
        value = entry_hp[idx].get()
        try:
            verify_value_is_num(value)
            with open(f"/sys/kernel/mm/hugepages/hugepages-1048576kB/{folder}", "w") as fd:
                fd.write(value)
            messager.put(f"Memory Huge TLB 1GB: Success to update value of {folder} to {value}")
            entry_hp[idx].after(2000, lambda: update_entry_value(folder, idx))
        except ValueError as e:
            messager.put(f"Memory Huge TLB 1GB: Error {e}")
            CTkMessagebox(title="value invalid", message=e, icon="cancel")
        except Exception as e:
            messager.put(f"Memory Huge TLB 1GB: Error to update value of {folder} to {value}")
            CTkMessagebox(title="Error", message=f"A one error ocurred to try to write value\n{e}", icon="cancel")

    hugepage_1bg = LabelFrame(frame_memory, text="Hugepage 1gb", background='#212121', foreground="white", labelanchor="n")
    hugepage_1bg.grid(row=4, column=1, padx=5, pady=5)
    folders = ["nr_hugepages", "nr_overcommit_hugepages"]
    labels = ["Nr hugepages 1gb:", "overcommit_hugepages:"]
    entry_hp = list(range(2))

    for folder, label, row in zip(folders, labels, range(2)):
        ctk.CTkLabel(hugepage_1bg, text=label).grid(row=row, column=0, padx=5, pady=5)
        entry_hp[row] = ctk.CTkEntry(hugepage_1bg, placeholder_text=get_1gb_huge(folder))
        entry_hp[row].grid(row=row, column=1, padx=5, pady=5)
        ctk.CTkButton(hugepage_1bg, text="Aplicar alteração", command=lambda f=folder, index=row: set_1gb_huge(f, index)).grid(row=row, column=2, padx=5, pady=5)