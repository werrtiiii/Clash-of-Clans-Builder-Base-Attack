import cv2
import pyautogui as pa
import time
import win32gui
import ctypes
import win32ui
import win32con
import numpy as np
import subprocess

def capture_screenshot(adb_path):
    """使用 ADB 获取屏幕截图并返回 OpenCV 图像对象"""
    result = subprocess.run(
        [adb_path, 'exec-out', 'screencap', '-p'],
        stdout=subprocess.PIPE
    )
    screenshot_data = result.stdout

    # 将二进制数据转换为 NumPy 数组
    np_img = np.frombuffer(screenshot_data, dtype=np.uint8)

    # 使用 OpenCV 解码图像
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    return img

def getxy(img_model_path, threshold):
    adb_path = r'.\platform-tools\adb.exe'
    img=capture_screenshot(adb_path)
    img_m = cv2.imread(img_model_path)
    height, width, _ = img_m.shape
    result = cv2.matchTemplate(img, img_m, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if min_val > threshold:
        return 0
    up_left = min_loc
    low_right = (up_left[0] + width, up_left[1] + height)
    avg = (int((up_left[0] + low_right[0]) / 2), int((up_left[1] + low_right[1]) / 2))
    
    return avg

def tap(x, y, device=None, adb_path='platform-tools/adb'):
    """
    发送点击事件到指定坐标
    :param x: 横坐标
    :param y: 纵坐标
    :param device: 设备序列号（可选）
    :param adb_path: ADB路径（可选）
    """
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['shell', 'input', 'tap', str(x), str(y)]
    subprocess.run(cmd, check=True)

def swipe(x1, y1, x2, y2, duration=300, device=None, adb_path='platform-tools/adb'):
    """
    发送滑动事件
    :param x1: 起始横坐标
    :param y1: 起始纵坐标
    :param x2: 结束横坐标
    :param y2: 结束纵坐标
    :param duration: 滑动持续时间（毫秒，默认300）
    :param device: 设备序列号（可选）
    :param adb_path: ADB路径（可选）
    """
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)]
    subprocess.run(cmd, check=True)

def long_press(x, y, duration=1000, device=None, adb_path='platform-tools/adb'):
    """
    发送长按事件到指定坐标
    :param x: 横坐标
    :param y: 纵坐标
    :param duration: 长按持续时间（毫秒，默认1000）
    :param device: 设备序列号（可选）
    :param adb_path: ADB路径（可选）
    """
    cmd = [adb_path]
    if device:
        cmd += ['-s', device]
    cmd += ['shell', 'input', 'swipe', str(x), str(y), str(x), str(y), str(duration)]
    subprocess.run(cmd, check=True)

def change_xy(x,y):
    return int(x/1470*1920),int((y-34)/826*1080)

def tapking():
    x,y=change_xy(150,770)
    tap(x,y)

def tapsend():
    x,y=change_xy(1162,444)
    tap(x,y)

def attack1():
    time.sleep(0.4)
    swipe(960, 540, 400, 540, 100)
    kingt=0
    if getxy("./pic/king3.png",0.2)!=0 or getxy("./pic/king.png",0.2)!=0:
        kingt=1
        print("king!!!👻")
        tapking()
        tapsend()
        tapking()
        time.sleep(2)
    tap(*change_xy(276,778))
    long_press(*change_xy(1162,444),2000)
    print("放技能👻")
    for i in range(0,10):
        tap(*change_xy(154+116*i,768))
    time.sleep(2)
    while 1:
        if (getxy("./pic/next.png",0.2)!=0)or(getxy("./pic/back_home.png",0.2)!=0):
            break
        if kingt:
            tapking()
        time.sleep(2)
    if getxy("./pic/next.png",0.3)!=0:
        print("第二阶段进攻👻")
        time.sleep(0.3)
        swipe(960, 540, 400, 540, 100)
        time.sleep(1)
        kingt=0
        if getxy("./pic/king3.png",0.3)!=0 or getxy("./pic/king.png",0.3)!=0:
            kingt=1
            tapking()
            print("king!!!👻")
            tapsend()
            tapking()
            time.sleep(2)
        tap(*getxy("./pic/nvwu.png",0.3))
        long_press(*change_xy(1162,444),2000)
        print("放技能👻")
        for i in range(0,11):
            tap(*change_xy(154+116*i,768))
        while 1:
            if (getxy("./pic/back_home.png",0.2)!=0):
                break
            if kingt:
                tapking()
            time.sleep(2)

def auto_night_attack(attack_plan):
    time.sleep(1)
    tap(*change_xy(86,756))
    tap(*change_xy(1084,584))
    time.sleep(1)
    t1=time.time()
    te=0
    while 1:
        t2=time.time()
        if t2-t1>4:
            te=1
            break
        if getxy("./pic/next.png",0.2)!=0:
            print("开始进攻👻")
            break
    if te:
        time.sleep(0.4)
        tap(*change_xy(728,756))
        time.sleep(1)
    elif te==0:
        time.sleep(0.4)
        attack_plan() #进攻方案
        while getxy("./pic/back_home.png",0.2)==0:
            time.sleep(0.6)
        tap(*change_xy(726,732))


if __name__ == '__main__':
    count=0
    a=1
    while 1:
        print(f"第{a}次进攻👻")
        a=a+1
        auto_night_attack(attack1)
        time.sleep(3)
        tap(*change_xy(724,670))
        time.sleep(0.2)
        if count==3:
            print("收集圣水👻")
            time.sleep(1.5)
            swipe(960, 540, 960, 710, 100)
            time.sleep(0.7)
            x,y=getxy("./pic/dw.png",0.3)
            x,y=x-39,y+171
            tap(x,y)
            tap(*change_xy(1074,720))
            tap(*change_xy(1228,112))
            count=0
        count=count+1