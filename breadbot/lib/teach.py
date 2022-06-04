import os
from breadbot.core import common


class Teach(object):

    def __init__(self):
        self.split_sym = ':'
        self.teach_file = 'teach.md'

    def do_teach(self, user, in_str):
        if not common.is_super(user):
            return
        if not in_str:
            return
        if self.split_sym not in in_str:
            return
        data_path = common.Cfg().get('local', 'data_paths')[0]
        file_path = os.path.join(data_path, self.teach_file)
        f = open(file_path, 'a')
        que = in_str.split(self.split_sym)[0]
        ans_list = in_str.split(self.split_sym)[1:]
        ans = self.split_sym.join(ans_list)
        que = common.init_input(que)
        ans = common.init_input(ans)
        text = '## %s\n%s\n\n' % (que, ans)
        f.write(text)
        f.close()
        return 'OK, I learned.'


if __name__ == '__main__':
    Teach().do_teach('localuser', 'how to teach?:Just do teach func')
