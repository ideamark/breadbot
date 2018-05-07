from configobj import ConfigObj
import os
import random
import re
import string
from threading import Thread
import time


def time_limit(secs):
    def dec(function):
        def dec2(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self):
                    Thread.__init__(self)
                    self.result = dontKnow()

                def run(self):
                    self.result = function(*args, **kwargs)

            t = TimeLimited()
            t.start()
            t.join(secs)
            return t.result
        return dec2
    return dec


def init_input(inStr):
    inStr = re.sub('\s', ' ', inStr)
    inStr = re.sub('  ', ' ', inStr)
    inStr = re.sub('  ', ' ', inStr)
    inStr = inStr.strip()
    return inStr


def expand_abbrev(inStr):
    if "'" not in inStr:
        return inStr
    inStr = re.sub("'m", ' am', inStr)
    inStr = re.sub("'s", ' is', inStr)
    inStr = re.sub("'re", ' are', inStr)
    inStr = re.sub("'ll", ' will', inStr)
    return inStr


def show_help():
    return(
        '- d ....search knowledge\n'
        '- s ....search dictionary\n'
        '- w ....search wikipedia\n'
        '- n ....turn to next page\n'
        '- t ....teach a dialogue\n')


def show_readme():
    return 'https://github.com/ideamark/breadbot/blob/master/README.md'


def show_homepage():
    return 'http://ideamark.github.io'


def que_init(inStr):
    inStr = expand_abbrev(inStr)
    inStr = re.sub('[%s]+' % string.punctuation, '', inStr)
    inStr = inStr.lower()
    return inStr


def is_super(name):
    super_users = cfg().get('wechat', 'super_users')
    if super_users and type(super_users) is list:
        for user in super_users:
            if user == name:
                return True
    return False


def dontKnow():
    notList = [
        "Well...",
        "What?",
        "Parden?",
        "...",
        "Hmm..."]
    res = random.choice(notList)
    return res


class log(object):
    def __init__(self):
        self.logDir = os.path.join(
            cfg().get('local', 'log_path'), 'dia.log')

    def write(self, inStr):
        curTime = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
        text = curTime + inStr
        f = open(self.logDir, 'a')
        f.write(text + '\n')
        f.close()
        return text

    def print(self, inStr):
        curTime = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
        print(curTime + str(inStr))


class cfg(object):
    def __init__(self):
        self.cfg = ConfigObj('/etc/bread.cfg')

    def get(self, ctype, value):
        res = self.cfg[ctype][value]
        if (ctype, value) == ('local', 'data_paths') or \
            (ctype, value) == ('wechat', 'allowed_ips') or \
                (ctype, value) == ('wechat', 'super_users'):
            if type(res) is not list:
                res = [res]
        elif ctype == 'mongodb' and value == 'db_port':
            res = int(res)
        return res

    def write(self, ctype, value, key):
        if (ctype, value) == ('local', 'data_paths') or \
            (ctype, value) == ('wechat', 'allowed_ips') or \
                (ctype, value) == ('wechat', 'super_users'):
            if type(key) is not list:
                key = [key]
            old_key = self.get(ctype, value)
            key = old_key + key
            key = list(set(key))
        self.cfg[ctype][value] = key
        self.cfg.write()


def path_parser(filePaths=[]):
    if not filePaths:
        print('Please enter file paths')
        return []

    for path in filePaths:
        if path[-1] == '*':
            path = path[:-1]
        if not os.path.exists(path):
            filePaths.remove(path)
        if os.path.isdir(path):
            filePaths.remove(path)
            files = os.listdir(path)
            for f in files:
                fPath = os.path.join(path, f)
                if not os.path.exists(fPath):
                    continue
                if os.path.isfile(fPath) and \
                        f[-4:] == '.yml':
                    filePaths.append(fPath)

    return filePaths
