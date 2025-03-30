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

def get_connected_devices(adb_path):
    """通过 adb devices 获取连接的设备列表"""
    result = subprocess.run([adb_path, "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    lines = result.stdout.splitlines()
    devices = []
    for line in lines[1:]:
        if line.strip() and "device" in line:
            dev = line.split()[0]
            devices.append(dev)
    return devices if devices else [""]  # 若无设备，可返回空字符串，使用默认设备

def capture_screenshot(adb_path, device=None):
    """使用 ADB 获取屏幕截图并返回 OpenCV 图像对象"""
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['exec-out', 'screencap', '-p']
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    screenshot_data = result.stdout

    np_img = np.frombuffer(screenshot_data, dtype=np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    return img

def getxy(img_model_path, threshold, device=None, adb_path=r'platform-tools\adb.exe'):
    """在截图中寻找模板图片，并返回中心点坐标"""
    img = capture_screenshot(adb_path, device)
    img_m = cv2.imread(img_model_path)
    height, width, _ = img_m.shape
    result = cv2.matchTemplate(img, img_m, cv2.TM_SQDIFF_NORMED)
    min_val, _, min_loc, _ = cv2.minMaxLoc(result)
    if min_val > threshold:
        return 0
    up_left = min_loc
    low_right = (up_left[0] + width, up_left[1] + height)
    avg = (int((up_left[0] + low_right[0]) / 2), int((up_left[1] + low_right[1]) / 2))
    return avg

def tap(x, y, device=None, adb_path=r'platform-tools\adb.exe'):
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['shell', 'input', 'tap', str(x), str(y)]
    subprocess.run(cmd, check=True,creationflags=subprocess.CREATE_NO_WINDOW)

def swipe(x1, y1, x2, y2, duration=300, device=None, adb_path=r'platform-tools\adb.exe'):
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)]
    subprocess.run(cmd, check=True,creationflags=subprocess.CREATE_NO_WINDOW)

def long_press(x, y, duration=1000, device=None, adb_path=r'platform-tools\adb.exe'):
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['shell', 'input', 'swipe', str(x), str(y), str(x), str(y), str(duration)]
    subprocess.run(cmd, check=True,creationflags=subprocess.CREATE_NO_WINDOW)

def change_xy(x, y):
    """将相对坐标转换为屏幕坐标（具体转换公式根据设备分辨率设定）"""
    return int(x/1470*1920), int((y-34)/826*1080)

def tapking(device=None):
    x, y = change_xy(150, 770)
    tap(x, y, device=device)

def tapsend(device=None):
    x, y = change_xy(1162, 444)
    tap(x, y, device=device)

def attack1(jineng, device=None):
    swipe(960, 540, 400, 540, 100, device=device)
    kingt = 0
    if getxy("./pic/king3.png", 0.2, device=device) != 0 or getxy("./pic/king.png", 0.2, device=device) != 0:
        kingt = 1
        print("king!!!👻")
        tapking(device=device)
        tapsend(device=device)
        tapking(device=device)
        time.sleep(2)
    tap(*change_xy(276, 778), device=device)
    long_press(*change_xy(1162, 444), 2000, device=device)
    if jineng:
        print("放技能👻")
        for i in range(10):
            tap(*change_xy(154+116*i, 768), device=device)
    time.sleep(2)
    while True:
        if (getxy("./pic/next.png", 0.2, device=device) != 0) or (getxy("./pic/back_home.png", 0.2, device=device) != 0):
            break
        if kingt:
            tapking(device=device)
        time.sleep(2)
    if getxy("./pic/next.png", 0.3, device=device) != 0:
        print("第二阶段进攻👻")
        time.sleep(0.3)
        swipe(960, 540, 400, 540, 100, device=device)
        time.sleep(0.5)
        kingt = 0
        if getxy("./pic/king3.png", 0.2, device=device) != 0 or getxy("./pic/king.png", 0.2, device=device) != 0:
            kingt = 1
            tapking(device=device)
            print("king!!!👻")
            tapsend(device=device)
            tapking(device=device)
            time.sleep(2)
        tap(*getxy("./pic/nvwu.png", 0.3, device=device),device=device)
        long_press(*change_xy(1162, 444), 2000, device=device)
        if jineng:
            print("放技能👻")
            for i in range(10):
                tap(*change_xy(154+116*i, 768), device=device)
        while True:
            if getxy(img_model_path="./pic/back_home.png", threshold=0.2, device=device) != 0:
                break
            if kingt:
                tapking(device=device)
            time.sleep(2)

def auto_night_attack(attack_plan, jineng, device=None):
    tap(*change_xy(86, 756), device=device)
    tap(*change_xy(1084, 584), device=device)
    time.sleep(1)
    t1 = time.time()
    te = 0
    while True:
        t2 = time.time()
        if t2 - t1 > 4:
            te = 1
            break
        if getxy("./pic/next.png", 0.2, device=device) != 0:
            print("开始进攻👻")
            break
    if te:
        time.sleep(0.4)
        tap(*change_xy(728, 756), device=device)
        time.sleep(1)
    elif te == 0:
        time.sleep(0.4)
        attack_plan(jineng=jineng, device=device)
        while getxy("./pic/back_home.png", 0.2, device=device) == 0:
            time.sleep(0.6)
        tap(*change_xy(726, 732), device=device)
    time.sleep(1)
