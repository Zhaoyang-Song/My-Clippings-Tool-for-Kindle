let SearchResult = '[{"title": " README  ", "path": "c47c7c7383225ab55ff591cb59c41e6b.html", "text": "AtooltoconvertMyClippingstxtfromyourKindleintoHTMLfilesManageyourKindleclippingsmoreeasilyTheindexhtmlfilegeneratedafterrunningisthefirstlevelindexofallhtmlfilesandcanbeopenedbybrowsertoviewtheconversionresults"}, {"title": " \u4e2d\u6587\u663e\u793a Chinese Display  ", "path": "848b3e79d57bb7289823297f3b96c134.html", "text": "\u751f\u5e74\u4e0d\u6ee1\u767e\u5e38\u6000\u5343\u5c81\u5fe7\u663c\u77ed\u82e6\u591c\u957f\u4f55\u4e0d\u79c9\u70db\u6e38\u4e3a\u4e50\u5f53\u53ca\u65f6\u4f55\u80fd\u5f85\u6765\u5179\u611a\u8005\u7231\u60dc\u8d39\u4f46\u4e3a\u540e\u4e16\u55e4\u4ed9\u4eba\u738b\u5b50\u4e54\u96be\u53ef\u4e0e\u7b49\u671f"}, {"title": " !!! NOTE !!!  ", "path": "60a1c42aeb6d132d565f51c739dc922a.html", "text": "BackupyourMyClippingstxtregularlyretainingsomebackwardcopiestopreventmisuse"}]';
obj = JSON.parse(SearchResult);

function check() {
    return false;
}

function maxfor(arr) {
    var len = arr.length;
    var max = -Infinity;
    while (len--) {
        if (arr[len] > max) {
            max = arr[len];
        }
    }
    return max;
}

let input = document.getElementById('input')
let result = document.getElementById('resultlist')
let button = document.getElementById('searchbutton')

input.addEventListener("focus", e => {
    result.id = 'active'
    result.style.overflow = 'auto'
    result.style.padding = '3px'
})
input.addEventListener("blur", e => {
    result.id = 'resultlist'
    result.style.overflow = 'hidden'
    result.style.padding = '0'
})

function searchtext() {
    result.innerHTML = input.value;
    if (input.value == '') {
        result.innerHTML = '<i>- 搜索 Search -</i><hr>' + '<p align="center">输入搜索内容 Enter search content</p><hr>'
    }

    // 标题搜索
    resultcount = 0;
    resultstr = '';
    var resulttitlecache = new Array()
    for (i = 0; i < obj.length; i++) {
        if (obj[i]['title'].includes(input.value) == true) {
            resulttitlecache.unshift(obj[i]['title'])
            resultcount++;
        }
    }

    // 标题搜索结果展示
    if (resultcount !== 0 && resultcount !== obj.length) {
        for (i = 0; i < resulttitlecache.length; i++) {
            for (j = 0; j < obj.length; j++) {
                if (obj[j]['title'] == resulttitlecache[i]) {
                    titlesearchresult = '<h4><a href="' + '../books/' + obj[j]["path"] + '" class="resulttitle">' + obj[j]['title'].replace(new RegExp(input.value, 'g'), '<mark>' + input.value + '</mark>') + '</a></h4><em>- 标题匹配 Title match</em><p class="showbox">' + obj[j]['text'].substring(0, 100) + '</p>'
                    resultstr = titlesearchresult + '<hr>' + resultstr
                }
            }
            result.innerHTML = '<i>"' + input.value + '"</i><hr>' + resultstr;
        }
    }

    // 正文搜索
    var resulttextcache = new Array()
    for (i = 0; i < obj.length; i++) {
        if (obj[i]['text'].includes(input.value) == true) {
            resulttextcache.unshift(obj[i]['text'])
            resultcount++;
        }
    }

    // 正文搜索结果计数
    var targetname = new Array()
    var targetscore = new Array()
    if (resulttextcache.length !== 0 && input.value !== '') {
        for (i = 0; i < resulttextcache.length; i++) {
            for (j = 0; j < obj.length; j++) {
                if (obj[j]['text'] == resulttextcache[i]) {
                    targetname.unshift(obj[j]['title'])
                    targetscore.unshift(obj[j]['text'].match(RegExp(input.value, 'gim')).length)
                }
            }
        }
    }

    //排序相关选项
    var targetscorecache = targetscore.concat([]);
    var resultfortext = '';
    var textsearchresult = ''
    targetscorecache.sort(function (a, b) {
        return b - a
    })
    for (i = 0; i < targetscorecache.length; i++) {
        for (j = 0; j < targetscore.length; j++) {
            if (targetscorecache[i] == targetscore[j]) {
                console.log('文章排序:' + targetname[j])
                for (k = 0; k < obj.length; k++) {
                    if (obj[k]['title'] == targetname[j]) {
                        // 确认选区
                        textorder = obj[k]['text'].indexOf(input.value) - 15;
                        while (textorder < 0) {
                            textorder++
                        }

                        resultfortext = '<h4><a href="' + '../books/' +  obj[k]["path"] + '" class="resulttitle">' + obj[k]['title'] + '</a></h4><em>- 结果数 Number of results：' + targetscorecache[i] + '</em><p class="showbox">...' + obj[k]['text'].substring(textorder, textorder + 100).replace(new RegExp(input.value, 'g'), '<mark>' + input.value + '</mark>') + '</p>'
                        textsearchresult = textsearchresult + '<hr>' + resultfortext;
                    }
                }
            }
        }
    }

    // 无效结果安排
    if (resultcount !== obj.length) {
        if (resultcount == 0) {
            result.innerHTML = '<i>"' + input.value + '"</i><hr><p align="center">没有找到结果<br/>No results found</p>'
        }
    }
    // 整合
    result.innerHTML = result.innerHTML.substring(0, result.innerHTML.length - 4) + textsearchresult.substring(0, textsearchresult.length - 4)
}