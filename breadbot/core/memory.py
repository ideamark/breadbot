import os
from pymongo import MongoClient
import re

from . import common

MEM_COLL = 'breadbot_memory_'


class _Coll(object):
    def __init__(self):
        pass

    @staticmethod
    def get_mem_coll(user):
        db_name = common.cfg().get('mongodb', 'db_name')
        ip = common.cfg().get('mongodb', 'db_ip')
        port = common.cfg().get('mongodb', 'db_port')
        client = MongoClient(ip, port)
        db = client[db_name]
        colls = db.collection_names()
        mem_coll = '%s%s' % (MEM_COLL, user)
        coll = db[mem_coll]
        if mem_coll not in colls or not coll.find_one():
            data = {
                'dialogue': [],
                'long_str': {
                    'cur_block': 0,
                    'block_count': 0,
                    'content': []
                }
            }
            coll.insert(data)
        return coll

    @staticmethod
    def insert_to_coll(coll, data):
        coll.remove({})
        coll.insert(data)


class longStr(object):

    def __init__(self, user):
        self.max_words = 140
        self.next_symble = r'....'
        self.mem_coll = _Coll.get_mem_coll(user)
        self.mem_data = self.mem_coll.find_one()

    def _split_str(self, text):
        text = str(text)
        block_count = len(text) // self.max_words
        if len(text) % self.max_words != 0:
            block_count += 1
        self.mem_data['long_str']['block_count'] = block_count
        self.mem_data['long_str']['cur_block'] = 1
        text = text.encode('unicode-escape').decode()
        content = [
            text[i:i + self.max_words]
            for i in range(0, len(text), self.max_words)]
        self.mem_data['long_str']['content'] = content
        _Coll.insert_to_coll(self.mem_coll, self.mem_data)

    def read_mem(self):
        text_list = self.mem_data['long_str']['content']
        cur_block = int(self.mem_data['long_str']['cur_block'])
        block_count = int(self.mem_data['long_str']['block_count'])
        if cur_block <= block_count and text_list:
            res = text_list[cur_block - 1] + self.next_symble
            self.mem_data['long_str']['cur_block'] = str(cur_block + 1)
            _Coll.insert_to_coll(self.mem_coll, self.mem_data)
            if cur_block == block_count:
                res = res.replace(self.next_symble, '')
        else:
            res = 'no more'
        res = res.replace(r'\n', '\n')
        res = res.replace(r'\r', '\r')
        return res

    def check_long_str(self, text):
        text = str(text)
        if len(text) <= self.max_words or self.next_symble in text:
            return text
        elif 'http://' in text or 'https://' in text:
            return text
        elif re.match(u'[\u4e00-\u9fa5]+', text):
            return text
        else:
            self._split_str(text)
            return self.read_mem()


class dialogue(object):

    def __init__(self, user):
        self.max_len = 3
        self.mem_coll = _Coll.get_mem_coll(user)
        self.mem_data = self.mem_coll.find_one()

    def insert_dia(self, in_str, res):
        if in_str == 'n' or in_str == 'next':
            return
        in_str = str(in_str)
        res = str(res)
        dia_list = self.mem_data['dialogue']
        if len(dia_list) >= self.max_len:
            dia_list.pop(0)
        in_str = in_str.encode('unicode-escape').decode()
        res = res.encode('unicode-escape').decode()
        dia_list.append({'que': in_str, 'ans': res})
        self.mem_data['dialogue'] = dia_list
        _Coll.insert_to_coll(self.mem_coll, self.mem_data)

    def get_dia(self):
        dias = self.mem_data['dialogue']
        if not dias:
            return []
        new_dia_list = []
        for dia in dias:
            new_dia_list.append({dia['que']: dia['ans']})
        return new_dia_list

    def erase_dia(self):
        self.mem_data['dialogue'] = []
        _Coll.insert_to_coll(self.mem_coll, self.mem_data)
