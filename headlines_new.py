#from __future__ import unicode_literals
#  __future__  模块是为Python2.x提供的，目的是在2.x中可以导入3.x的用法。
#  本代码直接用3.x写的，因此可以不需要这个模块

import feedparser   #parse 解析 #parser解析器

from flask import Flask

app = Flask(__name__)

RSS_FEED = {"zhihu": "http://www.zhihu.com/rss",
            "netease": "http://news.163.com/special/00011K6L/rss_newsattitude.xml",
            "songshuhui": "http://songshuhui.net/feed",
            "ifeng": "http://news.ifeng.com/rss/index.xml"
            }


@app.route('/')

@app.route('/<publication>')
def get_news(publication = "songshuhui"):
    feed =feedparser.parse(RSS_FEED[publication])
    first_content = feed['entries'][0]
    html_format = """
    <html><body>
        <h1>头条</h1>
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
