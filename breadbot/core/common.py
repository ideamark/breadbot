from configobj import ConfigObj
import os
import random
import re
import string
from threading import Thread
import time


def show_help(user):
    text = \
        'translate xxx (translate dialogs)\n' \
        'page (show home pages)\n' \
        'next (turn to next page)\n'
    if is_super(user):
        text += \
            '--------\n' \
            'corpus xxx (search corpus)\n' \
            'teach xxx (teach a dialogue)\n' \
            'public ip (get public ip)\n'
    return text


def url_to_html(url, text='Link'):
    return '<a href="%s">%s</a>' % (url, text)


def time_limit(secs):
    def dec(function):
        def dec2(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self):
                    Thread.__init__(self)
                    self.result = dont_know()

                def run(self):
                    self.result = function(*args, **kwargs)

            t = TimeLimited()
            t.start()
            t.join(secs)
            return t.result
        return dec2
    return dec


def init_input(in_str):
    in_str = re.sub('\s', ' ', in_str)
    in_str = re.sub('  ', ' ', in_str)
    in_str = re.sub('  ', ' ', in_str)
    in_str = in_str.lower()
    in_str = in_str.strip()
    return in_str


def expand_abbrev(in_str):
    if "'" not in in_str:
        return in_str
    in_str = re.sub("'m", ' am', in_str)
    in_str = re.sub("'s", ' is', in_str)
    in_str = re.sub("'re", ' are', in_str)
    in_str = re.sub("'ll", ' will', in_str)
    return in_str


def que_init(in_str):
    in_str = expand_abbrev(in_str)
    in_str = re.sub('[%s]+' % string.punctuation, '', in_str)
    in_str = in_str.lower()
    return in_str


def is_super(user):
    super_user_list = Cfg().get('wechat', 'super_users')
    if super_user_list and type(super_user_list) is list:
        for super_user in super_user_list:
            if user == super_user:
                return True
    return False


def dont_know():
    not_list = [
        "Well...",
        "Hmm...",
        "Let's talk about sth. others",
        "Let's change a topic",
        "Sorry, I don't know",
        "My IQ is not enough",
        "I'm still under construction",
        "You'd better in English",
        "Let me see..."]
    res = random.choice(not_list)
    return res


class ChatLog(object):
    def __init__(self):
        self.log_dir = os.path.join(
            Cfg().get('local', 'log_path'),
            'chat.log')

    def write(self, in_str):
        cur_time = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
        text = cur_time + in_str
        f = open(self.log_dir, 'a')
        f.write(text + '\n')
        f.close()
        return text


class ConsoleLog(object):
    def __init__(self):
        self.log_dir = os.path.join(
            Cfg().get('local', 'log_path'),
            'console.log')

    def __write(self, tag, in_str):
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        text = '%s [%s] %s' % (cur_time, tag, in_str)
        f = open(self.log_dir, 'a')
        f.write(text + '\n')
        f.close()
        return text

    def info(self, in_str):
        print(in_str)
        self.__write('INFO', in_str)

    def warn(self, in_str):
        print(in_str)
        self.__write('WARN', in_str)

    def error(self, in_str):
        print(in_str)
        self.__write('ERROR', in_str)

    def debug(self, in_str):
        self.__write('DEBUG', in_str)


class Cfg(object):
    def __init__(self):
        self.cfg = ConfigObj('/etc/bread.cfg')

    def get(self, ctype, value):
        res = self.cfg[ctype][value]
        if (ctype, value) == ('local', 'data_paths') or \
            (ctype, value) == ('wechat', 'allowed_ips') or \
                (ctype, value) == ('wechat', 'super_users'):
            if type(res) is not list:
                res = [res]
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


def expand_path(path_list=[]):
    expand_path_list = []
    for path in path_list:
        if not os.path.isdir(path):
            expand_path_list.append(path)
            continue
        for root, dirs, files in os.walk(path):
            if not files:
                continue
            for filename in files:
                if not filename:
                    continue
                file_path = os.path.join(root, filename)
                expand_path_list.append(file_path)
    return expand_path_list


def get_yml_path_list(path_list=[]):
    if not path_list:
        path_list = Cfg().get('local', 'data_paths')
    path_list = expand_path(path_list)
    yml_path_list = []
    for path in path_list:
        if not os.path.exists(path):
            continue
        elif os.path.splitext(path)[-1] != '.yml':
            continue
        yml_path_list.append(path)
    return yml_path_list
