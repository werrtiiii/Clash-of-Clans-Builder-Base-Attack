import cv2
import pyautogui as pa
import time
import win32gui
import ctypes
import win32ui
import win32con
import numpy as np
import subprocess
import tkinter as tk
from tkinter import ttk
import sys
import threading
import queue

# 从 script_core 导入所需要的函数
from script_core import (
    get_connected_devices, change_xy, tap, swipe, long_press,
    tapking, tapsend, attack1, auto_night_attack,getxy
)

class GameAutomationApp:
    def __init__(self):
        self.running = False
        self.thread = None
        self.status_queue = queue.Queue()
        
        self.adb_path = r'.\platform-tools\adb.exe'
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("部落冲突自动挂机配置 v1.0")
        self.root.geometry("1060x720")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 参数变量
        self.winstar_var = tk.IntVar(value=0)
        self.jineng_var = tk.IntVar(value=1)
        self.num = 9999
        self.count1 = 4

        style = ttk.Style()
        style.configure('TLabel', padding=6, font=('微软雅黑', 10))
        style.configure('TButton', font=('微软雅黑', 10))
        style.configure('Small.TLabel', font=('微软雅黑', 8), foreground='gray')

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)

        # 配置参数区域
        config_frame = ttk.LabelFrame(main_frame, text="配置参数", padding=10)
        config_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        ttk.Label(config_frame, text="挂机次数：").grid(row=0, column=0, sticky='w', pady=3)
        self.num_entry = ttk.Entry(config_frame, width=15)
        self.num_entry.insert(0, "9999")
        self.num_entry.grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(config_frame, text="（挂机进攻次数）", style='Small.TLabel').grid(row=0, column=2, sticky='w')

        ttk.Label(config_frame, text="收集间隔：").grid(row=1, column=0, sticky='w', pady=3)
        self.count1_entry = ttk.Entry(config_frame, width=15)
        self.count1_entry.insert(0, "4")
        self.count1_entry.grid(row=1, column=1, padx=5, sticky='w')
        ttk.Label(config_frame, text="（每几次进攻收集一次圣水车）", style='Small.TLabel').grid(row=1, column=2, sticky='w')

        # 设备选择
        ttk.Label(config_frame, text="设备选择：").grid(row=2, column=0, sticky='w', pady=3)
        self.device_var = tk.StringVar()
        self.device_combobox = ttk.Combobox(config_frame, textvariable=self.device_var, state="readonly", width=20)
        devices = get_connected_devices(self.adb_path)
        self.device_combobox['values'] = devices
        if devices:
            self.device_combobox.current(0)
        self.device_combobox.grid(row=2, column=1, padx=5, sticky='w')
        ttk.Button(config_frame, text="刷新设备", command=self.refresh_devices).grid(row=2, column=2, padx=5)

        # 功能选项区域
        option_frame = ttk.LabelFrame(main_frame, text="功能选项", padding=10)
        option_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=10)

        ttk.Checkbutton(option_frame, text="胜利之星检测", variable=self.winstar_var).grid(row=0, column=0, sticky='w', pady=3)
        ttk.Label(option_frame, text="（有胜利之星奖励必须打开，没有就关闭提高效率）", style='Small.TLabel').grid(row=0, column=1, sticky='w')
        ttk.Checkbutton(option_frame, text="立即释放女巫技能", variable=self.jineng_var).grid(row=1, column=0, sticky='w', pady=3)
        ttk.Label(option_frame, text="（可能影响蝙蝠存活率）", style='Small.TLabel').grid(row=1, column=1, sticky='w')
                 
        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="运行状态", padding=10)
        status_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=10)
        self.status_text = tk.Text(status_frame, height=5, width=70, wrap=tk.WORD)
        self.status_text.pack(fill='both', expand=True)
        self.status_text.insert(tk.END, "准备就绪，点击「开始挂机」按钮开始运行...\n")
        self.status_text.config(state=tk.DISABLED)
        
        # 操作按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, pady=15)
        self.start_button = ttk.Button(btn_frame, text="开始挂机", command=self.start_script, width=15)
        self.start_button.pack(side='left', padx=10)
        self.stop_button = ttk.Button(btn_frame, text="停止挂机", command=self.stop_script, width=15, state=tk.DISABLED)
        self.stop_button.pack(side='left', padx=10)
        ttk.Button(btn_frame, text="退出程序", command=self.on_close, width=15).pack(side='left', padx=10)
        
        self.root.after(100, self.check_status_queue)

    def refresh_devices(self):
        """刷新设备列表"""
        devices = get_connected_devices(self.adb_path)
        self.device_combobox['values'] = devices
        if devices:
            self.device_combobox.current(0)
        else:
            self.device_var.set("")

    def update_status(self, message):
        self.status_queue.put(message)

    def check_status_queue(self):
        try:
            while True:
                message = self.status_queue.get_nowait()
                self.status_text.config(state=tk.NORMAL)
                self.status_text.insert(tk.END, message + "\n")
                self.status_text.see(tk.END)
                self.status_text.config(state=tk.DISABLED)
                self.status_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_status_queue)

    def start_script(self):
        if self.running:
            return
        try:
            self.num = int(self.num_entry.get())
        except:
            self.num = 9999
        try:
            self.count1 = int(self.count1_entry.get())
        except:
            self.count1 = 4
        # 获取选中的设备
        self.selected_device = self.device_var.get()
        self.running = True
        self.update_status(f"开始挂机 - 计划挂机次数: {self.num}, 收集间隔: {self.count1}, 设备: {self.selected_device}")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.run_script)
        self.thread.daemon = True
        self.thread.start()
    
    def stop_script(self):
        if not self.running:
            return
        self.running = False
        self.update_status("正在停止挂机...")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def run_script(self):
        count = 1
        a = 1  # 进攻次数
        while a < self.num and self.running:
            message = f"第{a}次进攻👻"
            print(message)
            self.update_status(message)
            a += 1
            auto_night_attack(attack1, jineng=self.jineng_var.get(), device=self.selected_device)
            if self.winstar_var.get():
                time.sleep(3)
                tap(*change_xy(724, 670), device=self.selected_device)
                time.sleep(0.2)
            if count == self.count1:
                message = "收集圣水👻"
                print(message)
                self.update_status(message)
                time.sleep(0.8)
                swipe(960, 200, 960, 420, 100, device=self.selected_device)
                time.sleep(0.7)
                x, y = getxy("./pic/dw.png", 0.2, device=self.selected_device)
                x, y = x-39, y+171
                tap(x, y, device=self.selected_device)
                tap(*change_xy(1074, 720), device=self.selected_device)
                tap(*change_xy(1228, 112), device=self.selected_device)
                count = 0
            count += 1
        self.running = False
        self.update_status("挂机已完成或已停止")
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
    
    def on_close(self):
        if self.running:
            self.running = False
            self.update_status("正在停止挂机...")
        self.root.after(500, self.root.destroy)
    
    def run(self):
        self.root.mainloop()
