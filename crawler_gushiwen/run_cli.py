"""
用于从古诗文网中下载古书，输入为古书的目录页链接
"""
import re

import argparse
from run import *


def check_link_format(link):
    pattern = r"https://so\.gushiwen\.cn/guwen/book_[0-9a-z]+\.aspx"
    if re.match(pattern, link):
        return True
    else:
        return False


def download_book(url):
    x = get_urls(url)
    book_name = get_name(url)
    ifdir(book_name)
    for idx, row in tqdm(x.iterrows(), total=len(x)):
        savepath = os.path.join(book_name, f"{idx:0>3}_{row['name']}.md")
        text = get_text(row)
        append_to_file(text, savepath)


def main(args):
    url = args.url
    if url == "notInput":
        print("本程序用于下载古诗文网上的古籍，通过古籍目录页链接来获取古籍内容\n使用 `-url ` 参数接收网页链接")
    elif check_link_format(url):
        download_book(url)
    else:
        print("输入参数错误，请检查后重新输入，一般链接格式为：`https://so.gushiwen.cn/guwen/book_[XXXXXXXXXXXX].aspx`")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="示例程序 - 传递参数")

    # 添加参数
    # url = "https://so.gushiwen.cn/guwen/book_db8fe8b5a11f.aspx"
    # parser.add_argument("-url", type=str, default=url, help="输入网页链接")

    parser.add_argument("-url", type=str, default="notInput", help="输入网页链接")

    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数，并将参数传递给它
    main(args)
