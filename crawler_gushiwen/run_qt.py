# TODO 控制台输出部分还是没有实现，并没有将所有的标准输出流显示在前台
import time

from PyQt5.QtCore import Qt

from run import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit
import io

from run_cli import check_link_format


class QTextEditLogger(io.TextIOBase):
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.append(message)


def download_book(url):
    x = get_urls(url)
    book_name = get_name(url)
    ifdir(book_name)
    for idx, row in x.iterrows():
        savepath = os.path.join(book_name, f"{idx:0>3}_{row['name']}.md")
        text = get_text(row)
        append_to_file(text, savepath)
        print(f"[{idx} / {len(x)}]: {row['name']} V", end=" ")
        time.sleep(1)
    print("下载完毕", end=" ")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口大小
        self.setFixedSize(800, 400)

        # 将窗口移动到屏幕中心
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        # 设置窗口标题
        self.setWindowTitle("古诗文网古籍下载器")

        layout = QVBoxLayout()

        # 添加描述文字
        description_label = QLabel("- 基于古诗文网 [  https://so.gushiwen.cn/guwen/  ] 古籍目录页链接下载古籍文本\n- 请输入网页链接并点击按钮开始下载:")
        description_label.setTextInteractionFlags(description_label.textInteractionFlags() | Qt.TextSelectableByMouse)

        layout.addWidget(description_label)

        # 添加输入框
        self.input_box = QLineEdit()
        layout.addWidget(self.input_box)

        # 添加运行按钮
        self.start_button = QPushButton("开始下载")
        self.start_button.clicked.connect(self.run)
        layout.addWidget(self.start_button)

        # 添加输出文本框
        output_label = QLabel("")
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet(
            "background-color: black; color: lightgrey;"
        )  # 设置输出文本框的背景色为黑色，文字颜色为浅灰色
        layout.addWidget(self.output_text)

        # 设置布局
        self.setLayout(layout)

        # 重定向标准输出流到 QTextEdit
        sys.stdout = QTextEditLogger(self.output_text)

    def run(self):
        # 获取输入框内容
        input_text = self.input_box.text()

        url = input_text
        if url == "":
            print("本程序用于下载古诗文网上的古籍，通过古籍目录页链接来获取古籍内容\n请输入网页链接")
        elif check_link_format(url):
            download_book(url)
        else:
            print(
                "输入参数错误，请检查后重新输入，一般链接格式为：`https://so.gushiwen.cn/guwen/book_[XXXXXXXXXXXX].aspx`")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
