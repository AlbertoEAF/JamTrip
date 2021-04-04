import os
import argparse
import tkinter as tk
import tkinter.font
from tkinter.scrolledtext import ScrolledText
import time
from queue import SimpleQueue
import re

from process import Process

def jacktrip_connection_args(server_ip, server_mode, verbose=True):
    args = [".\jacktrip.exe"]    
    args += ["-S"] if server_mode else ["-C", server_ip]
    if verbose:
        args.append("-V")
    return args
    

class Q(SimpleQueue):

    def write(self, x):
        self.put(x)     

    def flush(self):
        pass     


class Settings:    
    def __init__(self, filepath):       
        self._filepath = filepath
        self.server_ip = None

        if os.path.exists(filepath):            
            self.load(filepath)            

    def load(self, filepath=None):
        with open(filepath or self._filepath) as infile:
            lines = infile.readlines()
            for line in lines:
                key, value = line.split(":")
                setattr(self, key, value.strip())

    def save(self, filepath=None):
        with open(filepath or self._filepath, "w") as out:
            out.write(f"server_ip: {self.server_ip}\n")



class JamTripApp:
    window = tk.Tk()
    window.title("JamTrip")
    
    frm_server_ip = tk.Frame()
    lbl_server_ip = tk.Label(master=frm_server_ip, text="Server IP")
    ent_server_ip = tk.Entry(master=frm_server_ip, width=15)
    btn_server_ip_save = tk.Button(master=frm_server_ip, text="Save")
    server_mode = tk.IntVar()
    btn_server_mode_checkbox = tk.Checkbutton(master=frm_server_ip, text="Server mode", var=server_mode)
    btn_server_connect = tk.Button(master=frm_server_ip, text="(Re)Connect!")

    frm_server_ip.pack(fill=tk.X)
    lbl_server_ip.pack(side=tk.LEFT)
    ent_server_ip.pack(side=tk.LEFT)
    btn_server_ip_save.pack(side=tk.LEFT)
    btn_server_connect.pack(side=tk.RIGHT)    
    btn_server_mode_checkbox.pack(side=tk.RIGHT)
    
    frm_output = tk.Frame()
    txt_output = ScrolledText()
    txt_output.insert(1.0, "### Welcome to JamTrip! ###\n\nNo JackTrip sessions started yet.\n\n")
    frm_output.pack(expand=True, fill=tk.BOTH)
    txt_output.pack()

    settings = Settings("settings.yaml")

    q = Q()
    
    @classmethod
    def setup(cls):
        if not os.path.exists("jacktrip.exe"):
            cls.txt_output.insert(tk.END, "\nERROR: jacktrip.exe not found in this folder! Download it first!")
        cls.ent_server_ip.insert(0, cls.settings.server_ip or "")
        cls.btn_server_connect.bind("<Button-1>", JamTripApp.connect)
        cls.btn_server_ip_save.bind("<Button-1>", JamTripApp.save_ip)

    @staticmethod
    def save_ip(event):
        cls = JamTripApp
        cls.settings.server_ip = JamTripApp.ent_server_ip.get()
        cls.settings.save()
        

    @staticmethod
    def connect(event):
        
        JamTripApp.txt_output.tag_config("msg", foreground="blue")
        print_msg = lambda msg: JamTripApp.txt_output.insert(tk.END, f"\n\n>>> {msg}\n\n", "msg")

        ip = JamTripApp.ent_server_ip.get()
        server_mode = JamTripApp.server_mode.get()

        if not ip and not server_mode:
            print_msg("Invalid IP address! Client mode requires an IP.")
            return
        elif not server_mode:
            print_msg(f"Starting client connection to server at IP <{ip}>...")

        # TODO: close previous!
        
        args = jacktrip_connection_args(ip, server_mode)
        print_msg(f"Starting jacktrip connection with args {args}")
        JamTripApp.connection_ps = Process(args, out = JamTripApp.q)
        JamTripApp.connection_ps.start()
            
    
    @classmethod
    def update(cls):        
        ps = getattr(cls, "connection_ps", None)        
        if ps:
            if not cls.q.empty():
                cls.txt_output.insert(tk.END, cls.q.get())
            else:
                pass
                # TODO: clear old connection
                #ps.join()
                #cls.connection_ps = None # clear connection

        cls.window.after(100, cls.update)

    @classmethod
    def start(cls):
        cls.update()
        cls.window.mainloop()


if __name__ == "__main__":    
    JamTripApp.setup()
    JamTripApp.start()
    print("done")
