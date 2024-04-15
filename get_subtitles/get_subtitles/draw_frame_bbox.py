import tkinter as tk
from .utils import mapXYXY


__all__ = ["draw_frame_line", "check_stop"]


def check_stop(root, stop_event):
    """检查是否应该停止并销毁Tk窗口。"""
    if stop_event.is_set():
        root.destroy()  # 销毁窗口
    else:
        root.after(100, check_stop, root, stop_event)  # 每100毫秒检查一次，继续传递参数


def create_overlay(root, bbox, point=(15, 15, 25, 25)):
    """
    创建一个覆盖层，仅显示框线和左上角的闪烁红点
    :param root: Tkinter 的根窗口
    :param bbox: 录制区域的坐标 (x1, y1, x2, y2)
    :param point: 闪烁点的大小与位置，(长, 宽, x, y)
    """
    # 创建一个新窗口
    overlay = tk.Toplevel(root)
    overlay.attributes('-alpha', 1.0)  # 设置窗口完全不透明
    overlay.attributes('-topmost', True)  # 置于顶层
    overlay.overrideredirect(True)  # 隐藏窗口的标题栏和边框
    overlay.attributes('-transparentcolor', 'black')  # 设置黑色为透明色

    # 设置窗口的大小和位置
    overlay.geometry(f"{bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}+{bbox[0]}+{bbox[1]}")

    # 创建一个画布，背景色设置为透明的黑色
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_rectangle(1, 1, bbox[2]-bbox[0]-1, bbox[3]-bbox[1]-1, outline='red', width=2)  # 绘制边框

    # 在左上角添加一个闪烁的红点
    blinking_dot = canvas.create_oval(
        point[0], point[1],     # 左上角坐标
        point[2], point[3],     # 右下角坐标
        fill='red'
    )  # 在指定框线内绘制一个椭圆

    def blink():
        current_color = canvas.itemcget(blinking_dot, "fill")
        new_color = 'red' if current_color == '' else ''  # 交替闪烁
        canvas.itemconfig(blinking_dot, fill=new_color)
        overlay.after(1000, blink)  # 每1000毫秒调用一次blink函数

    blink()  # 开始闪烁
    return overlay


def draw_frame_line(recording_bbox, point):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    overlay = create_overlay(root, recording_bbox, point)

    root.mainloop()  # 开始事件循环


def draw_frame_line(recording_bbox, point, stop_event):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    overlay = create_overlay(root, recording_bbox, point)

    # 使用独立的check_stop函数开始周期性检查
    root.after(100, check_stop, root, stop_event)  # 启动周期检查

    root.mainloop()  # 开始事件循环


if __name__ == "__main__":
    # recording_bbox = (333, 333, 533, 400)
    recording_bbox = (500, 500, 800, 600)
    recording_bbox = mapXYXY(recording_bbox)
    draw_frame_line(recording_bbox, (10, 10, 25, 25))
