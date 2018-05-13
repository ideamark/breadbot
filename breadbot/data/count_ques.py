#!/usr/bin/env python3
from breadbot.core import common
import os

LOG = common.consoleLog()

class countQues(object):

    def __init__(self):
        data_paths = common.cfg().get('local', 'data_paths')
        self.data_path_list = common.expand_path(data_paths)

    def do_count(self):
        count = 0
        for data_path in self.data_path_list:
            if os.path.splitext(data_path)[-1] != '.yml':
                continue
            with open(data_path, 'r') as fp:
                content = fp.read()
                count += content.count('- que:\n')

        LOG.info('Total ques: %s' % count)
