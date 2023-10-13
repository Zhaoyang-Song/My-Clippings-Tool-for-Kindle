import re
from bs4 import BeautifulSoup
import json
from pathlib import Path
from collections import deque

# 将root改成您存放html文件的目录
root = Path("../books")

# 扫描html文件
def scanfile(path: Path, content) -> dict:
    # 使用BeautifulSoup解析HTML内容
    htmlcontent = BeautifulSoup(content, 'html.parser')

    # 将p, h2, h3, h4的内容，去除符号之后作为搜索内容
    textlist = "".join(
        map(lambda p: re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", p.get_text()),
            htmlcontent.find_all(name=['p']))
    )

    # 以h1或者文件名作为标题
    title = htmlcontent.find(name="h1")  # 查找HTML中的h1标签
    title = title.get_text() if title else path.stem  # 如果h1标签存在，使用h1标签的文本作为标题，否则使用文件名
    return {
        "title": title,
        "path": path.relative_to(root).__str__(),  # 获取文件路径相对于根目录的字符串表示
        "text": textlist
    }

if __name__ == "__main__":
    j = []  # 创建一个空列表j，用于存储扫描结果
    target = deque([root])  # 创建一个双向队列，初始值包含根目录路径

    # 递归的遍历文件夹下所有的html文件
    while len(target) > 0:  # 当队列不为空时
        file = target.pop()  # 从队列中取出一个路径
        if file.is_dir():  # 如果是目录
            target.extend(file.iterdir())  # 将目录下的所有子路径添加到队列中
        elif file.is_file() and file.suffix == ".html":  # 如果是文件且扩展名为.html
            j.append(scanfile(file, file.read_bytes()))  # 调用scanfile函数，将扫描结果添加到列表j中

    # 将最后的扫描结果和search.js输出到searcher.js
    # html文件中应该包含searcher.js
    with open("search_script/searcher.js", "w", encoding="utf-8") as output:
        with open("search_script/search.js", "r", encoding="utf-8") as input:
            # 将扫描结果j转化为JSON字符串并写入searcher.js
            output.write("let SearchResult = '" + json.dumps(j) + "';\n")
            # 将search.js的内容写入searcher.js
            output.write(input.read())