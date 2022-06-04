import os
import re
import urllib.parse
import urllib.request

from breadbot.core import common


def search_baidu(keyword):
    if not keyword:
        return
    p = {'wd': keyword}
    url = 'http://www.baidu.com/s?' + urllib.parse.urlencode(p)
    return common.url_to_html(url)


def search_corpus(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '+')
    url = 'https://github.com/ideamark/ideamark.github.io/search?q=' + keyword
    return common.url_to_html(url)


def show_homepage():
    url = 'http://breadbot.fun'
    name = 'Breadbot.Fun'
    return common.url_to_html(url, name)

def show_wiki():
    url = 'http://cloud.breadbot.fun:8080/#!wiki/index.md'
    name = 'Wiki'
    return common.url_to_html(url, name)
