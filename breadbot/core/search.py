import os
import re
import urllib.parse
import urllib.request


def baiduSearch(keyword):
    if not keyword:
        return
    p = {'wd': keyword}
    return "http://www.baidu.com/s?" + urllib.parse.urlencode(p)


def wikiSearch(keyword):
    if not keyword:
        return
    keyword = keyword.replace(' ', '_')
    return 'https://en.m.wikipedia.org/wiki/' + keyword


def translate(word):
    if not word:
        return
    if re.match(u'.*[\u4e00-\u9fa5].*', word):
        return "https://translate.google.cn/m/translate#zh-CN/en/" + urllib.parse.quote(word)
    elif ' ' in word:
        return "https://translate.google.cn/m/translate#en/zh-CN/" + urllib.parse.quote(word)
    else:
        reses = os.popen('sdcv -n ' + word).readlines()
        if not reses:
            return 'You may not have installed sdcv, please install it first'
        if not re.match(u'^Found 1 items.*', reses[0]):
            return "https://translate.google.cn/m/translate#en/zh-CN/" + urllib.parse.quote(word)
        res = ''
        for i in range(4, len(reses)):
            res += reses[i]
        res = re.sub(u'\[.+\]', '', res)
        res = res.replace('\n', '')
        res = res.replace('//', '\r')
        return res


def get_public_ip():
    reg = 'fk="\d+\.\d+\.\d+\.\d+" '
    url = 'http://www.baidu.com/s?wd=gongwangip'
    result = re.search(reg, str(urllib.request.urlopen(url).read())).group(0)
    result = re.search('\d+\.\d+\.\d+\.\d+', result).group(0)
    return result
