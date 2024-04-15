## 爬虫 —— 古诗文网

> 用于从古诗文网下载网文

分三种运行方式：

1. 修改 `run.py` 文件中的代码，然后运行该文件：

```python
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

```

2. 以命令行的方式运行 `run_cli.py` 命令，需要输入路径参数，使用 `-url` 选项进行参数传递：

```shell
python -m run_cli.py -url "https://so.gushiwen.cn/guwen/book_c6a0e66fd254.aspx"
```

3. 运行 `run_qt.py` 文件，以窗口形式进行参数输入：

![image-20240415114649291](.\images\image-20240415114649291.png)