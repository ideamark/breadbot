import random
import re
from pymongo import MongoClient

from . import data
from . import dia
from . import klg
from . import memory
from . import common
from . import search
from . import teach


class chat(object):

    def __init__(self):
        self.db = self._open_db()

    def _open_db(self):
        db_name = common.cfg().get('db_name')
        db_ip = common.cfg().get('db_ip')
        db_port = common.cfg().get('db_port')
        client = MongoClient(db_ip, db_port)
        return client[db_name]

    @common.time_limit(5)
    def response(self, user, inStr):
        inStr = common.init_input(inStr)
        res = ''

        if re.match('^n$', inStr):
            res = memory.longStr(user).read_mem()

        if common.is_super(user):
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
            elif re.match('^t .*$', inStr):
                content = re.sub('^t ', '', inStr)
                res = teach.response(user, content)
            elif re.search('[\u4e00-\u9fa5]', inStr):
                res = search.baiduSearch(inStr)
            elif klg.DO_YOU_MEAN in str(memory.dialogue(user).get_dia()[-1].values()):
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
        if not res:
            res = common.dontKnow()
        memory.dialogue(user).insert_dia(inStr, res)
        res = memory.longStr(user).check_long_str(res)
        return res
