#!/usr/bin/env python3
from breadbot.core import common
import os

LOG = common.ConsoleLog()

class CountQues(object):

    def __init__(self):
        self.data_path_list = common.get_yml_path_list()

    def do_count(self):
        count = 0
        for data_path in self.data_path_list:
            with open(data_path, 'r') as fp:
                content = fp.read()
                count += content.count('- que:\n')

        LOG.info('Total ques: %s' % count)
