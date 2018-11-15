import goslate
import os
import re
import urllib.parse
import urllib.request
from breadbot.core import common


def baidu_search(keyword):
    if not keyword:
        return
    p = {'wd': keyword}
    url = 'http://www.baidu.com/s?' + urllib.parse.urlencode(p)
    return common.url_to_html(url)


def corpus_search(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '+')
    url = 'https://github.com/ideamark/ideamark.github.io/search?q=' + keyword
    return common.url_to_html(url)


def translate(in_str):
    if not in_str:
        return
    gs = goslate.Goslate()
    lang = gs.detect(in_str)
    if lang == 'en':
        return gs.translate(in_str, 'zh')
    else:
        return gs.translate(in_str, 'en')


def show_homepage():
    url = 'http://breadbot.fun'
    name = 'Breadbot.Fun'
    return common.url_to_html(url, name)
