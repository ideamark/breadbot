from googletrans import Translator
import os
import re
import urllib.parse
import urllib.request
from . import common


def baidu_search(keyword):
    if not keyword:
        return
    p = {'wd': keyword}
    url = 'http://www.baidu.com/s?' + urllib.parse.urlencode(p)
    return common.url_to_html(url)


def google_search(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '+')
    url = 'https://www.google.com/search?q=' + keyword
    return common.url_to_html(url)


def wiki_search(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '_')
    url = 'https://en.m.wikipedia.org/wiki/' + keyword
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


def get_public_ip():
    reg = 'fk="\d+\.\d+\.\d+\.\d+" '
    url = 'http://www.baidu.com/s?wd=gongwangip'
    result = re.search(reg, str(urllib.request.urlopen(url).read())).group(0)
    result = re.search('\d+\.\d+\.\d+\.\d+', result).group(0)
    return result


def show_readme():
    url = 'https://github.com/ideamark/breadbot/blob/master/README.md'
    return common.url_to_html(url, 'Readme')


def show_homepage():
    url = 'https://ideamark.github.io'
    return common.url_to_html(url, 'Home Page')
