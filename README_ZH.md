**中文 | [English](README.md)**

基于 Python3 编写。用于将 Kindle 标注笔记文件 `My Clippings.txt` 转换成 `HTML` 文件

[在这里可以预览此脚本的生成效果](https://zhaoyang-song.github.io/My-Clippings-Tool-for-Kindle/)

## 使用说明

将 `My Clippings.txt` 文件拉至该脚本的根目录下后运行 `run.bat`

也可以手动在根目录运行：

```bash
python MyClippingsTool.py
```

```bash
python search_main/search.py
```

运行后生成的 `index.html` 文件是所有 `html` 文件的第一层索引，浏览器打开可浏览转换结果

> **注意：管理好自己的 `My Clippings.txt` 文件备份以防止误操作**

## 特性变化

- **2022年6月5日**：改进页面布局，增加回到顶部功能组件
- **2022年6月7日**：去除页面底纹
- **2022年6月19日**：优化页面的书籍条目展示
- **2023年10月14日**：增加静态网页搜索功能，支持搜索HTML页面内的笔记内容

## 致谢

- [cyang812/kindleNote](https://github.com/cyang812/kindleNote)
- [muzi502/kindle](https://github.com/muzi502/kindle)
- [Clippings Fere](https://bookfere.com/tools#ClippingsFere)