#!/usr/bin/env python3
import datetime
from urllib.parse import urljoin

from flask import Flask
from flask import request
from flask import render_template
from werkzeug.contrib.atom import AtomFeed
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/feed')
def feed():
    feed = AtomFeed('Beijing People\'s Art Theatre Performances',
            feed_url=request.url,
            url=request.url_root,
            author={'name': 'typd', 'email': 'othertang@gmail.com'})
    list = get_performance_list()
    for title, link, content in list:
        feed.add(title, content, url=link, updated=datetime.datetime.now())
    return feed.get_response()

def get_performance_list():
    url = 'http://www.bjry.com/bjry/yczx/ycxx/index.shtml'
    base = 'http://www.bjry.com/'
    bs = requests.get(url).content
    html = bs.decode('gb2312')
    soup = BeautifulSoup(html)
    ul = soup.find(id="ycxx_disnone")
    script = ul.script
    str = script.get_text()
    str = get_middle(str, 'var str="', '|";')
    item_strs = str.split('|')
    items = []
    for item_str in item_strs:
        title = get_middle(item_str, '<b>', '</b>')
        link = get_middle(item_str, 'href=\'', '\'>')
        link = urljoin(base, link)
        item_soup = BeautifulSoup(item_str)
        items.append((title, link, item_soup.get_text()))
    return items

def get_middle(str, start, end):
    start_index = str.find(start)
    end_index = str[start_index + len(start):].find(end)
    return str[start_index + len(start):start_index + len(start) + end_index]

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
