from googletrans import Translator
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


def translate(word):
    if not word:
        return
    translator = Translator(service_urls=['translate.google.com.cn'])
    lang = translator.detect([word])[0].lang
    if lang == 'en':
        return translator.translate(word, dest='zh-cn').text
    else:
        return translator.translate(word, dest='en').text


def show_homepage():
    url = 'https://ideamark.github.io'
    name = 'Home Page'
    return common.url_to_html(url, name)
