import os
import random
import re
import string

from . import common
from . import memory
from breadbot import func


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
            #ans = common.dont_know()
            ans = func.web.search_baidu(qus)
        return ans

    def response(self, user, qus):
        qus = common.init_input(qus)
        ans = ''

        if re.match('^next|n$', qus):
            ans = memory.Memory(user).get_longstr_mem()
        elif re.match('^help$', qus.lower()):
            ans = common.show_help(user)
        else:
            ans = func.response(user, qus)

        if not ans:
            ans = self.__response(user, qus)
        memory.Memory(user).save_dialog(qus, ans)
        ans = memory.Memory(user).check_longstr(ans)
        return ans
