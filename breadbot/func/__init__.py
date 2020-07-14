import re

from breadbot.core import common
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

    if common.is_super(user):
        if re.match('^teach .*$', qus):
            content = re.sub('^teach ', '', qus)
            ans = teach.Teach().do_teach(user, content)
        elif re.match('^corpus .*$', qus):
            content = re.sub('^corpus ', '', qus)
            ans = web.corpus_search(content)

    return ans
