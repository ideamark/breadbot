import random
import re
from pymongo import MongoClient

from . import common
from . import dia
from . import klg
from . import memory
from . import search
from breadbot.data import teach


class chat(object):

    def __init__(self):
        self.db = self._open_db()

    def _open_db(self):
        db_name = common.cfg().get('mongodb', 'db_name')
        db_ip = common.cfg().get('mongodb', 'db_ip')
        db_port = common.cfg().get('mongodb', 'db_port')
        client = MongoClient(db_ip, db_port)
        return client[db_name]

    def response(self, user, inStr):
        inStr = common.init_input(inStr)
        res = ''

        if re.match('^n$', inStr):
            res = memory.longStr(user).read_mem()
        elif common.is_super(user):
            mem_dias = memory.dialogue(user).get_dia()
            if re.match('^s .*$', inStr):
                content = re.sub('^s ', '', inStr)
                res = search.translate(content)
            elif re.match('^d .*$', inStr):
                content = re.sub('^d ', '', inStr)
                res = klg.response(self.db, user, content)
                if not res:
                    res = search.baiduSearch(content)
            elif re.match('^w .*$', inStr):
                content = re.sub('^w ', '', inStr)
                res = search.wikiSearch(content)
            elif re.match('^help$', inStr.lower()):
                res = common.show_help()
            elif re.match('^readme$', inStr.lower()):
                res = common.show_readme()
            elif re.match('^(home|home page)$', inStr):
                res = common.show_homepage()
            elif re.match('^t .*$', inStr):
                content = re.sub('^t ', '', inStr)
                res = teach.Teach().do_teach(user, content)
            elif re.search('[\u4e00-\u9fa5]', inStr):
                res = search.baiduSearch(inStr)
            elif mem_dias and klg.DO_YOU_MEAN in str(mem_dias[-1].values()):
                res = klg.response(self.db, user, inStr)
        else:
            if re.search('[\u4e00-\u9fa5]', inStr):
                resList = [
                    'I speak English only.',
                    'Speak English please.',
                    'English, please.']
                return random.choice(resList)
        if not res:
            res = dia.response(self.db, user, inStr)
        memory.dialogue(user).insert_dia(inStr, res)
        res = memory.longStr(user).check_long_str(res)
        return res
