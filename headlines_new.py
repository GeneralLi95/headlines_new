#from __future__ import unicode_literals
#  __future__  模块是为Python2.x提供的，目的是在2.x中可以导入3.x的用法。
#  本代码直接用3.x写的，因此可以不需要这个模块

import feedparser

from flask import Flask

app = Flask(__name__)

ZHIHU_FEED = "http://www.zhihu.com/rss"


@app.route('/')
def get_news():

    feed = feedparser.parse(ZHIHU_FEED)  #parse 解析 #parser解析器
    first_content = feed['entries'][0]
    html_format = """
    <html><body>
        <h1>知乎头条</h1>
        <b>{0}</b><br/>
        <i>{1}</i><br/>
        <p>{2}</p><br/>
    <body></html>"""
    return html_format.format(first_content.get('title'),
                              first_content.get('published'),
                              first_content.get('summary'))


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
