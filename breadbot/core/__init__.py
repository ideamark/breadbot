import random
import re

from . import chat
from . import common
from . import memory
from . import www
from breadbot.data import teach


def response(user, in_str):
    in_str = common.init_input(in_str)
    res = ''

    if re.match('^next$', in_str):
        res = memory.Memory(user).get_longstr_mem()
    elif re.match('^translate .*$', in_str):
        content = re.sub('^translate ', '', in_str)
        res = www.translate(content)
    elif re.match('^help$', in_str.lower()):
        res = common.show_help(user)
    elif re.match('^readme$', in_str.lower()):
        res = www.show_readme()
    elif re.match('^(home|home page)$', in_str):
        res = www.show_homepage()
    elif re.search('[\u4e00-\u9fa5]', in_str):
        res_list = [
            'I speak English only.',
            'Speak English please.',
            'English, please.']
        res = random.choice(res_list)

    if common.is_super(user):
        if re.match('^teach .*$', in_str):
            content = re.sub('^teach ', '', in_str)
            res = teach.Teach().do_teach(user, content)
        elif re.match('^public ip$', in_str):
            res = www.get_public_ip()
        elif re.match('^corpus .*$', in_str):
            content = re.sub('^corpus ', '', in_str)
            res = www.corpus_search(content)

    if not res:
        res = chat.Chat().response(user, in_str)
    memory.Memory(user).save_dialog(in_str, res)
    res = memory.Memory(user).check_longstr(res)
    return res
