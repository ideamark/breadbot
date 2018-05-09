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

    def response(self, user, in_str):
        in_str = common.init_input(in_str)
        res = ''

        if re.match('^n$', in_str):
            res = memory.longStr(user).read_mem()
        elif common.is_super(user):
            mem_dias = memory.dialogue(user).get_dia()
            if re.match('^s .*$', in_str):
                content = re.sub('^s ', '', in_str)
                res = search.translate(content)
            elif re.match('^d .*$', in_str):
                content = re.sub('^d ', '', in_str)
                res = klg.response(self.db, user, content)
                if not res:
                    res = search.baiduSearch(content)
            elif re.match('^w .*$', in_str):
                content = re.sub('^w ', '', in_str)
                res = search.wikiSearch(content)
            elif re.match('^help$', in_str.lower()):
                res = common.show_help()
            elif re.match('^readme$', in_str.lower()):
                res = common.show_readme()
            elif re.match('^(home|home page)$', in_str):
                res = common.show_homepage()
            elif re.match('^t .*$', in_str):
                content = re.sub('^t ', '', in_str)
                res = teach.Teach().do_teach(user, content)
            elif re.search('[\u4e00-\u9fa5]', in_str):
                res = search.baiduSearch(in_str)
            elif mem_dias and klg.DO_YOU_MEAN in str(mem_dias[-1].values()):
                res = klg.response(self.db, user, in_str)
        else:
            if re.search('[\u4e00-\u9fa5]', in_str):
                res_list = [
                    'I speak English only.',
                    'Speak English please.',
                    'English, please.']
                return random.choice(res_list)
        if not res:
            res = dia.response(self.db, user, in_str)
        memory.dialogue(user).insert_dia(in_str, res)
        res = memory.longStr(user).check_long_str(res)
        return res
