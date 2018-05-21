import random
import re

from . import common
from . import dialog
from . import memory
from . import search
from breadbot.data import teach


class Chat(object):

    def __init__(self):
        pass

    def response(self, user, in_str):
        in_str = common.init_input(in_str)
        res = ''

        if re.match('^n$', in_str):
            res = memory.Memory(user).get_longstr_mem()
        elif common.is_super(user):
            if re.match('^s .*$', in_str):
                content = re.sub('^s ', '', in_str)
                res = search.translate(content)
            elif re.match('^d .*$', in_str):
                content = re.sub('^d ', '', in_str)
                res = search.baidu_search(content)
            elif re.match('^w .*$', in_str):
                content = re.sub('^w ', '', in_str)
                res = search.wiki_search(content)
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
                res = search.baidu_search(in_str)
        else:
            if re.search('[\u4e00-\u9fa5]', in_str):
                res_list = [
                    'I speak English only.',
                    'Speak English please.',
                    'English, please.']
                return random.choice(res_list)
        if not res:
            res = dialog.response(user, in_str)
        memory.Memory(user).save_dialog(in_str, res)
        res = memory.Memory(user).check_longstr(res)
        return res
