#!/usr/bin/env python3
import os
import re
import sys
import yaml

from breadbot.core import misc


class sameQue(object):

    def __init__(self, dataPath=None):
        if not dataPath:
            dataPath = misc.cfg().get('data_path')
        if not dataPath:
            print('[Error] data path not found')
            sys.exit(1)
        logPath = './same-que.log'
        self.show_same(dataPath, logPath)

    def _init(self, inStr):
        inStr = str(inStr)
        inStr = inStr.lower()
        newStr = []
        for chr in inStr:
            if re.match(r'[a-z0-9 ]', chr):
                newStr.append(chr)
        outStr = ''.join(newStr)
        outStr = outStr.strip()
        return outStr

    def show_same(self, dataPath, logPath):
        allQueList = []
        outDict = {}
        for root, dirs, files in os.walk(dataPath):
            for file in files:
                print('reading %s...' % file)
                if not re.match(r'^.*\.yml$', file):
                    continue
                filePath = os.path.join(root, file)
                f = open(filePath, 'r')
                readStr = f.read()
                data = yaml.load(readStr)
                for qas in data['QA']:
                    for que in qas['que']:
                        que = self._init(que)
                        allQueList.append(que)
                f.close()

        for que in allQueList:
            count = allQueList.count(que)
            if count > 1:
                print(que, count)
                outDict[que] = count

        print('creating log...')
        f = open(logPath, 'w')
        for que in outDict.keys():
            count = outDict[que]
            files = os.popen(r'grep -R "\- %s$" %s/*' % (que, dataPath))
            filePath = ''.join(files)
            f.write('- "%s" %d\n%s\n' % (que, count, filePath))
        f.close()


if __name__ == '__main__':
    sameQue()
