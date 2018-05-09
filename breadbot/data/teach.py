import os
from breadbot.core import common


class Teach(object):

    def __init__(self):
        self.splitSym = ':'
        self.teach_file = 'teach.yml'

    def do_teach(self, user, inStr):
        if not common.is_super(user):
            return
        if not inStr:
            return
        if self.splitSym not in inStr:
            return
        data_path = common.cfg().get('local', 'data_paths')[0]
        file_path = os.path.join(data_path, self.teach_file)
        f = open(file_path, 'a')
        que = inStr.split(self.splitSym)[0]
        ans_list = inStr.split(self.splitSym)[1:]
        ans = self.splitSym.join(ans_list)
        que = common.init_input(que)
        ans = common.init_input(ans)
        text = '\n- que:\n  - %s\n  ans:\n  - %s\n' % (que, ans)
        f.write(text)
        f.close()
        return 'OK, I learned.'
