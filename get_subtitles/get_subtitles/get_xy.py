import tkinter as tk
from tkinter import Toplevel, Canvas

__all__ = ["get_XYXY", "get_XYWH"]


class SelectAreaApp:
    def __init__(self, root):
        self.sy = None
        self.sx = None
        self.root = root
        self.rect = None
        self.coordinates = None

        self.top = Toplevel(root)
        self.top.attributes('-fullscreen', True)
        self.top.attributes('-alpha', 0.3)  # 半透明覆盖层
        self.canvas = Canvas(self.top, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_move_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def on_button_press(self, event):
        self.sx = self.canvas.canvasx(event.x)
        self.sy = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.sx, self.sy, self.sx, self.sy, outline='red', width=3)

    def on_move_press(self, event):
        ex, ey = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.sx, self.sy, ex, ey)

    def on_button_release(self, event):
        ex, ey = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.coordinates = (min(self.sx, ex), min(self.sy, ey), max(self.sx, ex), max(self.sy, ey))
        self.top.quit()  # 退出top级别的事件循环

    def get_xyxy(self):
        return self.coordinates

    def get_xywh(self):
        x1, y1, x2, y2 = self.coordinates
        return x1, y1, x2 - x1, y2 - y1


def get_XYXY():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    app = SelectAreaApp(root)
    root.mainloop()  # 开始事件循环
    xyxy = app.get_xyxy()
    app.top.destroy()  # 销毁窗口
    app.root.quit()  # 退出事件循环
    return xyxy
    # return app.get_xyxy()


def get_XYWH():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    app = SelectAreaApp(root)
    root.mainloop()  # 开始事件循环
    xywh = app.get_xywh()
    app.top.destroy()  # 销毁窗口
    app.root.quit()  # 退出事件循环
    return xywh


if __name__ == "__main__":
    selected_coordinates = get_XYXY()

    if selected_coordinates:
        print("Selected Area Coordinates:", selected_coordinates)
