import logging
import time
import tkinter as tk
from threading import Thread
from tkinter import filedialog

import cv2
import numpy as np
from PIL import ImageGrab

from .utils import mapXYXY

logging.getLogger("PIL").setLevel(logging.ERROR)


class ScreenRecorderApp:
    def __init__(self, master, bbox, position='UL', frame_rate=10):
        self.master = master
        self.bbox = bbox
        self.position = position
        self.frame_rate = frame_rate
        self.running = False
        self.start_time = None
        self.thread = None

        self.setup_gui()
        self.master.attributes('-topmost', True)

    def setup_gui(self):
        self.master.title("Screen Recorder Control")
        self.position_window()

        # 创建左侧和右侧的框架
        self.left_frame = tk.Frame(self.master, padx=10, pady=10)
        self.right_frame = tk.Frame(self.master, padx=10, pady=10)

        # 时间显示在左侧
        # self.time_label = tk.Label(self.left_frame, text="00:00:00", font=('Helvetica', 16))
        self.time_label = tk.Label(self.left_frame, text="00:00.000", font=('Helvetica', 16))
        self.time_label.pack(anchor='w')

        # 帧率输入在时间显示下方，水平排列
        frame_rate_frame = tk.Frame(self.left_frame)
        frame_rate_label = tk.Label(frame_rate_frame, text="录制帧率(fps):")
        frame_rate_label.pack(side=tk.LEFT)
        self.frame_rate_entry = tk.Entry(frame_rate_frame, width=5)
        self.frame_rate_entry.insert(tk.END, str(self.frame_rate))
        self.frame_rate_entry.pack(side=tk.LEFT)
        frame_rate_frame.pack(anchor='w')

        # 开始和停止按钮在右侧
        self.start_button = tk.Button(self.right_frame, text="开始录制", command=self.start_recording)
        self.start_button.pack(fill=tk.X)

        self.stop_button = tk.Button(self.right_frame, text="结束录制", command=self.stop_recording,
                                     state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X)

        # 分布框架
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def position_window(self):
        x1, y1, x2, y2 = self.bbox
        width = 450
        height = 100

        positions = {
            'UL': (x1 - 10, y1 - height - 52),
            'UR': (x2 - width - 10, y1 - height - 52),
            'LU': (x1 - width - 15, y1),
            'LD': (x1 - width - 15, y2 - height - 52),
            'RU': (x2 - 5, y1 - 5),
            'RD': (x2 - 5, y2 - height - 45),
            'DL': (x1 - 10, y2),
            'DR': (x2 - width - 10, y2),
        }

        x, y = positions.get(self.position, (100, 100))  # Default position if not found
        x, y = int(x), int(y)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def start_recording(self):
        self.filepath = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        if not self.filepath:
            return

        self.frame_rate = int(self.frame_rate_entry.get())
        self.start_time = time.time()
        self.running = True
        self.thread = Thread(target=self.record_screen)
        self.thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_time()  # 启动时间更新

    def stop_recording(self):
        self.running = False
        self.thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        # self.stop_event.set()

    def record_screen(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        bbox = mapXYXY(self.bbox)
        # bbox = self.bbox
        self.out = cv2.VideoWriter(self.filepath, fourcc, self.frame_rate, (bbox[2] - bbox[0], bbox[3] - bbox[1]))

        # while self.running:
        #     img = ImageGrab.grab(bbox=bbox)
        #     img_np = np.array(img)
        #     frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        #     self.out.write(frame)

        # 计算每帧之间的时间间隔
        interval = 1 / self.frame_rate
        while self.running:
            start_time = time.time()  # 记录当前时间
            img = ImageGrab.grab(bbox=bbox)
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            self.out.write(frame)
            # 计算处理帧和保存所需的时间
            elapsed_time = time.time() - start_time
            # 等待直到达到间隔时间
            time.sleep(max(0, interval - elapsed_time))

        self.out.release()

    def update_time(self):
        # if self.running:
        #     elapsed_time = int(time.time() - self.start_time)
        #     time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        #     self.time_label.config(text=time_str)
        #     # 继续每秒调用自己来更新时间
        #     self.master.after(1000, self.update_time)
        if self.running:
            elapsed_time = time.time() - self.start_time  # 获取精确到小数的时间差
            # 将时间差格式化为小时:分钟:秒:毫秒
            # 其中毫秒取整数部分后三位
            milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
            time_str = time.strftime('%M:%S', time.gmtime(elapsed_time)) + f'.{milliseconds:03d}'
            self.time_label.config(text=time_str)
            # 继续每10毫秒调用自己来更新时间
            self.master.after(10, self.update_time)


if __name__ == '__main__':
    root = tk.Tk()
    app = ScreenRecorderApp(root, bbox=(500, 500, 800, 600), position='DR')
    root.mainloop()
