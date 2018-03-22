#from __future__ import unicode_literals
#  __future__  模块是为Python2.x提供的，目的是在2.x中可以导入3.x的用法。
#  本代码直接用3.x写的，因此可以不需要这个模块

import requests
import feedparser   #parse 解析 #parser解析器

from flask import Flask, render_template, request

app = Flask(__name__)

RSS_FEED = {"zhihu": "http://www.zhihu.com/rss",
            "netease": "http://news.163.com/special/00011K6L/rss_newsattitude.xml",
            "songshuhui": "http://songshuhui.net/feed",
            "douban": "http://www.douban.com/feed/review/book"
            }

WEATHERS = {"北京": 101010100,
            "上海": 101020100,
            "广州": 101280101,
            "深圳": 101280601}

@app.route('/')

def home():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEED:
        publication = "songshuhui"
    else:
        publication = query.lower()

    city = request.args.get('city', '北京')

    weather = get_weather(city)
    articles = get_news(publication)

    return render_template('home.html', articles=articles, weather=weather)


def get_news(publication):
    feed = feedparser.parse(RSS_FEED[publication])
    return feed['entries']


def get_weather(city):
    code = WEATHERS.get(city, 101010100)
    url = "http://www.weather.com.cn/data/sk/{0}.html".format(code)

    r = requests.get(url)
    r.encoding = 'utf-8'

    data = r.json()['weatherinfo']
    return dict(city=data['city'], temperature=data['temp'], description=data['WD'])



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)


