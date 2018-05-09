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


def show_help():
    return(
        ' d ....search knowledge\n'
        ' s ....search dictionary\n'
        ' w ....search wikipedia\n'
        ' n ....turn to next page\n'
        ' t ....teach a dialogue\n')


def show_readme():
    return 'https://github.com/ideamark/breadbot/blob/master/README.md'


def show_homepage():
    return 'https://ideamark.github.io'


def que_init(in_str):
    in_str = expand_abbrev(in_str)
    in_str = re.sub('[%s]+' % string.punctuation, '', in_str)
    in_str = in_str.lower()
    return in_str


def is_super(name):
    super_users = cfg().get('wechat', 'super_users')
    if super_users and type(super_users) is list:
        for user in super_users:
            if user == name:
                return True
    return False


def dont_know():
    not_list = [
        "Well...",
        "What?",
        "Parden?",
        "...",
        "Hmm..."]
    res = random.choice(not_list)
    return res


class chatLog(object):
    def __init__(self):
        self.log_dir = os.path.join(
            cfg().get('local', 'log_path'),
            'chat.log')

    def write(self, in_str):
        cur_time = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
        text = cur_time + in_str
        f = open(self.log_dir, 'a')
        f.write(text + '\n')
        f.close()
        return text


class consoleLog(object):
    def __init__(self):
        self.log_dir = os.path.join(
            cfg().get('local', 'log_path'),
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
        print(in_str)
        self.__write('DEBUG', in_str)


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


def path_parser(file_path_list=[]):
    if not file_path_list:
        print('Please enter file paths')
        return []

    for path in file_path_list:
        if path[-1] == '*':
            path = path[:-1]
        if not os.path.exists(path):
            file_path_list.remove(path)
        if os.path.isdir(path):
            file_path_list.remove(path)
            files = os.listdir(path)
            for f in files:
                f_path = os.path.join(path, f)
                if not os.path.exists(f_path):
                    continue
                if os.path.isfile(f_path) and \
                        f[-4:] == '.yml':
                    file_path_list.append(f_path)

    return file_path_list
