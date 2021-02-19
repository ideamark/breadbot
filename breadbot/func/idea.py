import os
import time
from breadbot.core import common


class Idea(object):

    def __init__(self):
        self.store_file = 'ideas.md'

    def store_idea(self, user, idea_str):
        if not common.is_super(user):
            return
        if not idea_str:
            return
        data_path = common.Cfg().get('local', 'data_paths')[0]
        file_path = os.path.join(data_path, self.store_file)
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        text = '* %s %s\n' % (time_str, idea_str)
        with open(file_path, 'a') as fp:
            fp.write(text)
        return 'OK, idea is stored.'


if __name__ == '__main__':
    Idea().store_idea('localuser', 'I think sunny is nice.')
