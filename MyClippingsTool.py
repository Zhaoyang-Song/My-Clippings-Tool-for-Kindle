import re
import sys
import os.path
import shutil
import time
import json
from hashlib import md5

HTML_HEAD = """<!DOCTYPE html>
<html>
	<head>
	<meta charset="utf-8" />
	<title> Kindle 读书笔记 </title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="../style/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
	<link href="../style/css/bootstrap-theme.min.css" rel="stylesheet" type="text/css" />
	<link href="../style/css/custom.css" rel="stylesheet" type="text/css" />
	<!-- 下面是回到顶部组件的样式设置 -->
	<style>
	    .box{
		position:fixed;
		right:10px;
		bottom:15px;
		height:40px;
		width: 40px;    
		text-align:center;
		z-index:999;
		padding-top:20px;    
		background-color: #337AB7;
		opacity:0.4;
		border-radius: 40%;
		overflow: hidden;
	    }
	    .box:hover:before{
		top:50%
	    }
	    .box-in{
		visibility: visible;
		display:inline-block;
		height:28px;
		width: 28px;
		border: 3.4px solid black;
		border-color: white transparent transparent white;
		transform:rotate(45deg);
	    }
	</style>
	<!-- 回到顶部组件样式设置结束 -->
	
	<!-- 下面是主体背景颜色设置，无底纹 -->
  	<style>
		body{
		    background: #f2f2f2;
		}
        </style>
   	<!-- 主体背景颜色设置结束 -->
</head>
<body>
"""

INDEX_TITLE = """
    <!-- 下面是回到顶部组件 -->
    <div id="box" class="box">
        <div class="box-in"></div>
    </div>    
    <script>
    var timer  = null;
    box.onclick = function(){
        cancelAnimationFrame(timer);
        //获取当前毫秒数
        var startTime = +new Date();     
        //获取当前页面的滚动高度
        var b = document.body.scrollTop || document.documentElement.scrollTop;
        var d = 400;
        var c = b;
        timer = requestAnimationFrame(function func(){
            var t = d - Math.max(0,startTime - (+new Date()) + d);
            document.documentElement.scrollTop = document.body.scrollTop = t * (-c) / d + b;
            timer = requestAnimationFrame(func);
            if(t == d){
              cancelAnimationFrame(timer);
            }
        });
    }
    </script>
    </body>
    <!-- 回到顶部组件结束 -->
    
	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Kindle 读书笔记 </small> <span class="badge">更新于 UPDATE </span> <span class="badge"> 共 BOOKS_SUM 本书，SENTENCE_SUM 条笔记</span></h1>
			</div>
		</header>
	<div class="col-md-12">
        <div class="list-group">
"""

BOOK_TITLE = """
    <!-- 下面是回到顶部组件 -->
    <div id="box" class="box">
        <div class="box-in"></div>
    </div>    
    <script>
    var timer  = null;
    box.onclick = function(){
        cancelAnimationFrame(timer);
        //获取当前毫秒数
        var startTime = +new Date();     
        //获取当前页面的滚动高度
        var b = document.body.scrollTop || document.documentElement.scrollTop;
        var d = 400;
        var c = b;
        timer = requestAnimationFrame(function func(){
            var t = d - Math.max(0,startTime - (+new Date()) + d);
            document.documentElement.scrollTop = document.body.scrollTop = t * (-c) / d + b;
            timer = requestAnimationFrame(func);
            if(t == d){
              cancelAnimationFrame(timer);
            }
        });
    }
    </script>
    </body>
    <!-- 回到顶部组件结束 -->

	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span> BookName </small> <span class="badge"></span></h1>
			</div>
		</header>

        <div class="col-md-2">
			<ul class="nav nav-pills nav-stacked go-back">
				<li role="presentation" class="active text-center">
					<a href="../index.html"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span> 返回目录</a>
				</li>
			</ul>
		</div>
"""

MARK_CONTENT = """
    	<div class="col-md-12">
			<article>
				<div class="panel panel-default">
					<div class="panel-body mk88"><p>SENTENCE_TXT
                    </p></div>
					<div class="panel-footer text-right">
						<span class="label label-primary"><span class="glyphicon glyphicon-tag" aria-hidden="true"></span> 标注</span>
						<span class="label label-default"><span class="glyphicon glyphicon-bookmark" aria-hidden="true"></span>SENTENCE_ADDR</span>
						<span class="label label-default"><span class="glyphicon glyphicon-time" aria-hidden="true"></span>SENTENCE_TIME</span>
					</div>
				</div>
			</article>
        </div>
"""

ITEM_CONTENT = """          <a href="HTML_URL" class="list-group-item"><span class="glyphicon glyphicon-book" aria-hidden="true"></span> HTML_FILE_NAME <span class="glyphicon glyphicon-tag" aria-hidden="true">SENTENCE_COUNT</span></a>
"""

FOOTER_CONTENT = """
        </div>
    </div>
</body>
</html>
"""

DELIMITER = u"==========\n"
all_books = []
all_marks = []


def get_book_index(book_name):
    """get book's index"""
    for i in range(len(all_books)):
        if all_books[i]["name"] == book_name:
            return i
    return -1


def render_clippings(file_name):
    global all_marks
    global all_books
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("\n\n", "\n")
    all_marks = content.split(DELIMITER)
    for i in range(len(all_marks)):
        mark = all_marks[i].split("\n")
        if len(mark) == 4:
            book_url = md5(mark[0].encode("utf-8")).hexdigest()
            book_info = re.split(r"[()<>|\[\]（）《》【】｜]\s*", mark[0])
            book_name = book_info[0] if str(book_info[0]) != "" else (mark[0])
            book_author = book_info[-2] if len(book_info) > 1 else ""
            mark_info = mark[1].split("|")
            mark_time = mark_info[1]
            mark_address = mark_info[0].strip("- ")
            mark_content = mark[2]
            book_index = get_book_index(book_name)
            if book_index == -1:
                all_books.append(
                    {
                        "name": book_name,
                        "author": book_author,
                        "url": book_url,
                        "nums": 0,
                        "marks": [],
                    }
                )
            all_books[book_index]["marks"].append(
                {"time": mark_time, "address": mark_address, "content": mark_content}
            )
            all_books[book_index]["nums"] += 1
    all_books.sort(key=lambda x: x["nums"], reverse=True)
    try:
        json_str = json.dumps(all_books, indent=2, ensure_ascii=False)
        with open("clippings.json", "w") as f:
            f.write(json_str)
        return 1
    except:
        return 0


def render_index_html():
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_HEAD.replace("../", ""))
        f.write(
            INDEX_TITLE.replace("SENTENCE_SUM", str(len(all_marks)))
            .replace("UPDATE", time.strftime("%Y-%m-%d %H:%M", time.localtime()))
            .replace("BOOKS_SUM", str(len(all_books)))
        )
        for book in all_books:
            f.write(
                ITEM_CONTENT.replace("HTML_URL", "books/" + book["url"] + ".html")
                    .replace("HTML_FILE_NAME", book["name"] + "（" + book["author"] + "）")
                    .replace("SENTENCE_COUNT", str(book["nums"]))
            )
        f.write(FOOTER_CONTENT)

def render_books_html():
    if os.path.exists("books"):
        shutil.rmtree("books")
    os.mkdir("books")
    for i in range(len(all_books)):
        book_url = all_books[i]["url"]
        book_name = all_books[i]["name"]
        book_author = all_books[i]["author"]
        with open("books/" + book_url + ".html", "w", encoding="utf-8") as f:
            f.write(HTML_HEAD)
            f.write(
                BOOK_TITLE.replace("BookName", book_name + "（" + book_author + "）")
            )
            for j in range(len(all_books[i]["marks"])):
                mark = all_books[i]["marks"][j]
                f.write(
                    MARK_CONTENT.replace("SENTENCE_TXT", mark["content"])
                    .replace("SENTENCE_ADDR", mark["address"])
                    .replace("SENTENCE_TIME", mark["time"])
                )
            f.write(FOOTER_CONTENT)


def render_date_json():
    all_dates = {}
    for i in range(len(all_marks)):
        mark = all_marks[i].split("\n")
        if len(mark) == 4:
            date = re.split(r"[年月日]\s*",mark[1].split("|")[1].split(" ")[2])
            month = date[1] if len(date[1]) == 2 else "0" + date[1]
            day = date[2] if len(date[2]) == 2 else "0" + date[2]
            date = date[0] + "-" + month + "-" + day
            if date not in all_dates:
                all_dates[date] = 0
            all_dates[date] += 1
    try:
        json_str = json.dumps(all_dates, indent=2, ensure_ascii=False)
        with open("date.json", "w") as f:
            f.write(json_str)
        return 1
    except:
        return 0


if __name__ == "__main__":
    file_path = "My Clippings.txt" if len(sys.argv) == 1 else sys.argv[1]
    render_clippings(file_path)
    render_index_html()
    render_books_html()
    render_date_json()
    print("书籍总数：", len(all_books))
    print("笔记总数：", len(all_marks))
