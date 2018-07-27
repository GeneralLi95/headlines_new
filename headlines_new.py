# from __future__ import unicode_literals
#  __future__  模块是为Python2.x提供的，目的是在2.x中可以导入3.x的用法。
#  本代码直接用3.x写的，因此可以不需要这个模块

import datetime
import requests
import feedparser  # parse 解析 #parser解析器

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

DEFAULTS = {'city': '北京',
            'publication': 'songshuhui'}

RSS_FEED = {"zhihu": "http://www.zhihu.com/rss",
            "netease": "http://news.163.com/special/00011K6L/rss_newsattitude.xml",
            "songshuhui": "http://songshuhui.net/feed",
            "douban": "http://www.douban.com/feed/review/book"
            }

WEATHERS = {"北京": 101010100,
            "上海": 101020100,
            "广州": 101280101,
            "深圳": 101280601}


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]  # 这是当前两个if 条件都不符合时return默认值。


# cookie   web 浏览器创建的存储在和用户本地终端的文件，其中包含用户的个人信息，可提高浏览器加载速度。


@app.route('/')
def home():
    publication = get_value_with_fallback('publication')
    city = get_value_with_fallback('city')

    weather = get_weather(city)
    articles = get_news(publication)

    response = make_response(render_template('home.html', articles=articles, weather=weather))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('publication', publication, expires=expires)
    response.set_cookie('city', city, expires=expires)

    return response


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
    app.run(host='0.0.0.0', port=5000)
