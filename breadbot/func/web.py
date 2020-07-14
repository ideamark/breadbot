import os
import re
import urllib.parse
import urllib.request

from breadbot.core import common
#from google.cloud import translate as google_trans


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


'''
def translate(in_str):
    if not in_str:
        return
    trans_client = google_trans.Client()
    lang = trans_client.detect_language(in_str)['language']
    if lang == 'en':
        trans = trans_client.translate(
            in_str, target_language='zh')
        return trans['translatedText']
    else:
        trans = trans_client.translate(
            in_str, target_language='en')
        return trans['translatedText']
'''


def show_homepage():
    url = 'http://breadbot.fun'
    name = 'Breadbot.Fun'
    return common.url_to_html(url, name)

def show_wiki():
    url = 'http://cloud.breadbot.fun:8080/#!wiki/index.md'
    name = 'Wiki'
    return common.url_to_html(url, name)
