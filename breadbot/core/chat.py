import os
import random
import re
import string

from . import common
from . import memory
from breadbot.func import teach
from breadbot.func import web


class Chat(object):
    def __init__(self, db):
        self.db = db

    def __search_ans(self, user, qus):
        is_super = common.is_super(user)
        qus = re.sub(r'[^\w\s]', '', qus)
        qus = qus.lower()
        ans_type = self.db.type(qus)
        if ans_type == 'set':
            ans = self.db.srandmember(qus, 1)[0]
        elif ans_type == 'string':
            ans = self.db.get(qus)
        else:
            ans = None
        return ans

    @common.time_limit(3)
    def __response(self, user, qus):
        qus = common.que_init(qus)
        ans = self.__search_ans(user, qus)
        if not ans:
            ans = self.__search_ans(user, qus)
        if not ans:
            ans = common.dont_know()
        return ans

    def response(self, user, qus):
        qus = common.init_input(qus)
        ans = ''

        if re.match('^next|n$', qus):
            ans = memory.Memory(user).get_longstr_mem()
        elif re.match('^translate .*$', qus):
            content = re.sub('^translate ', '', qus)
            ans = web.translate(content)
        elif re.match('^help$', qus.lower()):
            ans = common.show_help(user)
        elif re.match('^home$', qus):
            ans = web.show_homepage()
        elif re.search('[\u4e00-\u9fa5]', qus):
            ans = '中文暂不支持，请用英文'
            '''
            en_str = web.translate(qus)
            ans = self.__response(user, en_str)
            ans = web.translate(ans)
            '''

        if common.is_super(user):
            if re.match('^teach .*$', qus):
                content = re.sub('^teach ', '', qus)
                ans = teach.Teach().do_teach(user, content)
            elif re.match('^corpus .*$', qus):
                content = re.sub('^corpus ', '', qus)
                ans = web.corpus_search(content)

        if not ans:
            ans = self.__response(user, qus)
        memory.Memory(user).save_dialog(qus, ans)
        ans = memory.Memory(user).check_longstr(ans)
        return ans
