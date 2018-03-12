import os

from . import import_data
from breadbot.core import common


class Teach(object):

    def __init__(self):
        self.splitSym = ';'
        self.new_dia = 'new_dia.yml'
        self.new_klg = 'new_klg.yml'

    def do_teach(self, tag, user, inStr):
        if not common.is_super(user):
            return
        if not inStr:
            return
        if self.splitSym not in inStr:
            return
        data_path = common.cfg().get('data_path')[0]
        if tag == 'dia':
            file_path = os.path.join(data_path, self.new_dia)
        elif tag == 'klg':
            file_path = os.path.join(data_path, self.new_klg)
        else:
            return
        f = open(file_path, 'a')
        que = inStr.split(self.splitSym)[0]
        ans = inStr.split(self.splitSym)[1]
        que = common.init_input(que)
        ans = common.init_input(ans)
        text = '\n- que:\n  - %s\n  ans:\n  - %s\n' % (que, ans)
        f.write(text)
        f.close()
        import_data.importData().do_import([file_path])
        return 'OK, I learned.'
