from googletrans import Translator
import os
import re
import urllib.parse
import urllib.request


def baidu_search(keyword):
    if not keyword:
        return
    p = {'wd': keyword}
    return 'http://www.baidu.com/s?' + urllib.parse.urlencode(p)


def google_search(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '+')
    return 'https://www.google.com/search?q=' + keyword


def wiki_search(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '_')
    return 'https://en.m.wikipedia.org/wiki/' + keyword


def corpus_search(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '+')
    return 'https://github.com/ideamark/ideamark.github.io/search?q=' + keyword


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
