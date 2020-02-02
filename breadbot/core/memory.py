import json
import os
import re

from . import common


class Memory(object):

    def __init__(self, user):
        self.max_words = 800
        self.next_symble = '....'
        self.max_dialogs = 3
        self.user = user
        log_path = common.Cfg().get('local', 'mem_path')
        mem_name = '%s.log' % self.user
        self.mem_path = os.path.join(log_path, mem_name)
        self.__create_data()

    def __create_data(self):
        if not os.path.exists(self.mem_path):
            data = {
                'dialog': [],
                'long_str': {
                    'cur_block': 0,
                    'block_count': 0,
                    'content': []
                }
            }
            with open(self.mem_path, 'w') as fp:
                json.dump(data, fp, indent=4)

    def __get_data(self):
        try:
            with open(self.mem_path, 'r') as fp:
                return json.load(fp)
        except Exception:
            self.__del_data()
            self.__create_data()
            with open(self.mem_path, 'r') as fp:
                return json.load(fp)

    def __del_data(self):
        if os.path.exists(self.mem_path):
            os.remove(self.mem_path)

    def __save_data(self, data):
        with open(self.mem_path, 'w') as fp:
            json.dump(data, fp, indent=4)

    def __split_longstr(self, in_str):
        in_str = str(in_str).encode('unicode-escape').decode()
        data = self.__get_data()
        block_count = len(in_str) // self.max_words
        if len(in_str) % self.max_words != 0:
            block_count += 1
        data['long_str']['block_count'] = block_count
        data['long_str']['cur_block'] = 1
        content = [
            in_str[i:i + self.max_words]
            for i in range(0, len(in_str), self.max_words)]
        data['long_str']['content'] = content
        self.__save_data(data)

    def get_longstr_mem(self):
        data = self.__get_data()
        in_str_list = data['long_str']['content']
        cur_block = int(data['long_str']['cur_block'])
        block_count = int(data['long_str']['block_count'])
        res = 'no more'
        if cur_block <= block_count and in_str_list:
            res = in_str_list[cur_block - 1] + self.next_symble
            data['long_str']['cur_block'] = str(cur_block + 1)
            if cur_block == block_count:
                res = res.replace(self.next_symble, '')
            res = res.replace(r'\n', '\n')
            res = res.replace(r'\r', '\r')
        self.__save_data(data)
        return res

    def check_longstr(self, in_str):
        in_str = str(in_str)
        if len(in_str) <= self.max_words or self.next_symble in in_str:
            return in_str
        elif 'http://' in in_str or 'https://' in in_str:
            return in_str
        elif re.match(u'[\u4e00-\u9fa5]+', in_str):
            return in_str
        else:
            self.__split_longstr(in_str)
            return self.get_longstr_mem()

    def save_dialog(self, in_str, res):
        in_str = str(in_str).encode('unicode-escape').decode()
        if in_str == 'n' or in_str == 'next':
            return
        res = str(res).encode('unicode-escape').decode()
        data = self.__get_data()
        dialog_list = data['dialog']
        if len(dialog_list) >= self.max_dialogs:
            dialog_list.pop(0)
        dialog_list.append({'que': in_str, 'ans': res})
        data['dialog'] = dialog_list
        self.__save_data(data)

    def get_dialog(self):
        data = self.__get_data()
        return data['dialog']
