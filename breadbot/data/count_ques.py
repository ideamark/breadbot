#!/usr/bin/env python3
from breadbot.core import common
from breadbot.core.common import cfg
import os

LOG = common.consoleLog()

class countQues(object):

    def __init__(self):
        self.data_path_list = cfg().get('local', 'data_paths')

    def do_count(self):
        count = 0
        for data_path in self.data_path_list:
            for root, dirs, files in os.walk(data_path):
                if not files:
                    continue
                for f in files:
                    if f.split('.')[-1] != 'yml':
                        continue
                    file_path = os.path.join(root, f)
                    with open(file_path, 'r') as fp:
                        content = fp.read()
                        count += content.count('- que:\n')

        LOG.info('Total ques: %s' % count)
