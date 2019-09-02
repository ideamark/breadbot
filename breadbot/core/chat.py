import Levenshtein as Leven
import os
import random
import re
import string

from . import common


class Chat(object):
    def __init__(self, db):
        self.db = db

    @common.time_limit(3)
    def response(self, user, qus):
        qus = common.que_init(qus)
        ans = self.__search_ans(user, qus)
        if not ans:
            ans = self.__search_ans(user, qus)
        if not ans:
            ans = common.dont_know()
        return ans

    def __search_ans(self, user, qus):
        # is_super = common.is_super(user)
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
