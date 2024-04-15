import logging
import sys
import threading
import tkinter as tk

from get_subtitles import draw_frame_line, get_XYXY, ScreenRecorderApp, mapXYXY
logging.getLogger("PIL").setLevel(logging.ERROR)

# from get_subtitles.draw_frame_bbox import draw_frame_line
# from get_subtitles.get_xy import get_XYXY
# from get_subtitles.record import ScreenRecorderApp
# from get_subtitles.utils import mapXYXY

# TO DO 两个库对屏幕尺寸的识别不一致，需要进行坐标映射
# DONE 做完映射后，现在两个尺寸又一致了，TMD，FK，TMD****
# DONE 引入 pyautogui 时应该会修改屏幕映射，如果在后边使用 tk ，tk就能正确识别了，因为 tk 不改变底层，只会从系统层调用参数，凸(艹皿艹 )


def on_close(root, stop_event, threads):
    """关闭窗口时执行的操作，包括停止线程和销毁窗口"""
    stop_event.set()  # 通知线程停止
    for thread in threads:
        thread.join()  # 等待线程结束
    root.destroy()  # 销毁窗口
    root.update()
    sys.exit()      # 销毁主程序，会错误退出，但退出了……


def run():
    # 绘制录制区域
    selected_coordinates = get_XYXY()
    selected_coordinates_ = mapXYXY(selected_coordinates)
    # 可视化录制区域，一个录制提示框线
    stop_event = threading.Event()
    tk_thread = threading.Thread(target=draw_frame_line, args=(selected_coordinates_, (15, 15, 25, 25), stop_event))
    tk_thread.daemon = True  # 将线程设置为守护线程
    tk_thread.start()
    # 启动录制控件，可以开始录制，结束录制，显示录制时间，控制录制帧率
    root = tk.Tk()
    app = ScreenRecorderApp(root, bbox=selected_coordinates, position='DR')
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, stop_event, [tk_thread]))
    root.mainloop()


if __name__ == "__main__":
    run()
