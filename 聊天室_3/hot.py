import requests
from pyquery import PyQuery as pq
import datetime
import time
def WeiBo_Spider():
    # 微博热搜网址
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'

    headers={
    'user-agent':'Mozilla/5.0 '
                 '(Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' 
                 'Chrome/92.0.4515.107 Safari/537.36'
    ,'cookie': 'SUB=_2AkMVXbshf8NxqwFRmP0dxGvla4pyyADEieKjAUr6JRMxHR'
               'l-yT8Xqk4_tRB6Pt2Vzn847yXzFTKaiuQAK0SbKmYuEU6G; SUBP=0033WrSX'
               'qPxfM72-Ws9jqgMF55529P9D9WhGAV2Xr9IPZApw8Qg9WsXc; _s_tentry'
               '=passport.weibo.com; Apache=208493768202.0982.16442460'
               '63693; SINAGLOBAL=208493768202.0982.1644246063693; U'
               'LV=1644246063701:1:1:1:208493768202.0982.1644246063693:'
    ,
        "sec-ch-ua-mobile": "?0"
    ,
        "sec-ch-ua": '" Not A;Brand";v = "99", "Chromium";v = "102", "Google Chrome";v = "102"'
    ,
        "Referer": "https://s.weibo.com/"
    ,
        "sec-ch-ua-platform": "Windows"
    }


    # 请求微博热搜网址 获取其文本数据
    resp = requests.get(url,headers=headers)
    res = resp.text
    # print(res)

    # 数据初始化
    doc = pq(res)
    # 通过类选择器提取热搜信息
    td = doc('.td-02 a').items()
    time_ = time.strftime("%Y-%m-%d %H:%M:%S")

    time_ = list(time_)

    time_[10] = "--"
    time_ = ''.join(time_)
    print("当前时间是:",time_)

    # 遍历数据
    for x in td:

        # 获取热搜文字
        title = x.text()

    #
        # 获取热搜链接 并拼接成完整链接
        href = 'https://s.weibo.com' + x.attr('href')
        # 将文字和链接合并在一个content变量中
        content = title + '\n' + href + '\n\n'

        # 获取今日日期，并转换为字符串的形式。以此日期命名建立文件路径
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        # 将文件保存以日期命名的txt文件 以追加的方式写入 编码为utf-8
        f = open(date + '.txt', 'a', encoding='utf-8')
        # 将热搜内容写入
        f.write(content)
        # 关闭写入
        f.close()
        # 显示当前时间
        print(title)
        print(href)

WeiBo_Spider()