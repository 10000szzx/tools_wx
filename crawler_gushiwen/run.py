"""
用于从古诗文网中下载古书，输入为古书的目录页链接
"""
import os
import warnings

warnings.filterwarnings("ignore", message="The NumPy module was reloaded")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# 书籍目录路径，获取章节名称列表与其对应的链接
def get_urls(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保正确的编码

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找class="bookcont"的<div>标签
    bookcont_divs = soup.find_all('div', class_='bookcont')
    # print(bookcont_divs)
    # 遍历每个找到的<div class="bookcont">标签
    urls = pd.DataFrame(columns=["name", "url"])
    for div in bookcont_divs:
        # 在当前<div>标签内查找所有的<p>标签
        p_tags = div.find_all('a')
        # 遍历找到的每个<p>标签
        for p in p_tags:
            urls.loc[len(urls), :] = [p.get_text(strip=True), p["href"]]
    urls["url"] = "https://so.gushiwen.cn" + urls["url"]

    return urls


def get_text(item):
    name = item["name"]
    url = item["url"]
    # 使用requests获取网页内容
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保正确的编码

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有的<div class="contson">标签
    contson_divs = soup.find_all('div', class_='contson')

    res = f"## {name}\n\n\n"
    # 打印找到的内容
    for div in contson_divs:
        # 在当前<div>标签内查找所有的<p>标签
        p_tags = div.find_all('p')
        if p_tags:
            # 遍历找到的每个<p>标签
            for p in p_tags:
                # 打印每个<p>标签的文本内容，并去除前后空白
                res += p.get_text(strip=True)
                res += "\n\n"
        else:
            res += div.get_text(strip=True)
            res += "\n\n"
    return res


def append_to_file(content, file_path):
    """将字符串或字符串列表追加到文件中。

    参数:
    - file_path: 字符串，目标文件的路径。
    - content: 字符串或字符串列表，要追加到文件的内容。
    """
    # 确定content是单个字符串还是字符串列表
    if isinstance(content, list):
        # 以追加模式打开文件
        with open(file_path, 'a', encoding='utf-8') as file:
            # 遍历列表，每个元素后加换行符然后写入
            for line in content:
                file.write(line + '\n\n')
    elif isinstance(content, str):
        # 以追加模式打开文件
        with open(file_path, 'a', encoding='utf-8') as file:
            # 直接追加字符串
            file.write(content)
    else:
        # 如果content既不是字符串也不是列表，抛出异常
        raise ValueError("Content must be a string or a list of strings.")


def ifdir(dir_path):
    """
    如果指定的文件路径不存在，则创建文件；如果已存在，则不执行任何操作。
    """
    # 检查文件是否存在
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def get_name(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 根据网页的编码设置，可能需要调整

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有具有指定style属性的<span>标签
    span_text = soup.find_all('span', style='font-size:20px; line-height:22px; height:22px;')[0].text
    return span_text


if __name__ == '__main__':
    ################ TODO 修改 url 参数后运行程序 ####################
    # url = "https://so.gushiwen.cn/guwen/book_1bd76a1c3d01.aspx"  # 论语
    # url = "https://so.gushiwen.cn/guwen/book_7723bfd24ca1.aspx"  # 史记
    url = "https://so.gushiwen.cn/guwen/book_c6a0e66fd254.aspx"  # 汉书

    x = get_urls(url)
    book_name = get_name(url)
    ifdir(book_name)
    for idx, row in tqdm(x.iterrows(), total=len(x)):
        savepath = os.path.join(book_name, f"{idx:0>3}_{row['name']}.md")
        text = get_text(row)
        append_to_file(text, savepath)
