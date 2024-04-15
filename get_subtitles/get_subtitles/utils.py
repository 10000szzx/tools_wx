import tkinter as tk
import pyautogui


__all__ = ["SWT", "SHT", "SWA", "SHA", "mapXYXY"]


def get_screen_size_by_tk():
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()  # 关闭窗口
    return screen_width, screen_height


def get_screen_size_by_pyautogui():
    return pyautogui.size()


SWT, SHT = get_screen_size_by_tk()
SWA, SHA = get_screen_size_by_pyautogui()


def truncate(number) -> int:
    """去尾"""
    return int(number)


def normalize(number) -> int:
    """归一"""
    if number == int(number):
        return int(number)
    else:
        return int(number) + 1


def mapXYXY(bbox, ratioX=SWT/SWA, ratioY=SHT/SHA):
    x1, y1, x2, y2 = bbox
    return truncate(x1*ratioX), truncate(y1*ratioY), normalize(x2*ratioX), normalize(y2*ratioY)


if __name__ == '__main__':
    print(f"TK: {SWT}x{SHT}")
    print(f"pyautogui: {SWA}x{SHA}")
    print(mapXYXY((500, 500, 800, 600), 1707/2560, 1067/1600))

