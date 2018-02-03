#!/usr/bin/env python3
from breadbot.core.common import cfg
import os


class CountQues(object):

    def __init__(self):
        self.dataPaths = cfg().get('data_path')

    def action(self):
        count = 0
        for dataPath in self.dataPaths:
            for root, dirs, files in os.walk(dataPath):
                if not files:
                    continue
                for f in files:
                    if f.split('.')[-1] != 'yml':
                        continue
                    filePath = os.path.join(root, f)
                    with open(filePath, 'r') as fp:
                        content = fp.read()
                        count += content.count('- que:\n')

        print('Count: %s' % count)


if __name__ == '__main__':
    CountQues().action()
