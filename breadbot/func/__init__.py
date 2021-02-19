import re

from breadbot.core import common
from . import idea
from . import stardict
from . import teach
from . import web

def response(user, qus):
    ans = ''

    if re.match('^translate .*$', qus):
        content = re.sub('^translate ', '', qus)
        ans = stardict.translate(content)
    elif re.match('^home$', qus):
        ans = web.show_homepage()
    elif re.match('^wiki$', qus):
        ans = web.show_wiki()
    elif re.match('^baidu .*$', qus):
        content = re.sub('^baidu ', '', qus)
        ans = web.search_baidu(content)

    if common.is_super(user):
        if re.match('^idea .*$', qus):
            content = re.sub('^idea ', '', qus)
            ans = idea.Idea().store_idea(user, content)
        elif re.match('^teach .*$', qus):
            content = re.sub('^teach ', '', qus)
            ans = teach.Teach().do_teach(user, content)
        elif re.match('^corpus .*$', qus):
            content = re.sub('^corpus ', '', qus)
            ans = web.search_corpus(content)

    return ans
