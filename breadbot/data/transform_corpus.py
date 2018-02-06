#!/usr/bin/env python3
import os
import sys

from breadbot.core import common


class transformCorpus(object):

    def __init__(self):
        pass

    def do_transform(self, filePaths=[]):
        filePaths = common.path_parser(filePaths)
        for filePath in filePaths:
            fr = open(filePath, 'r')
            text = fr.read()
            fr.close()
            list1 = text.split('\n\n\n')
            list2 = []
            for item in list1:
                subItem1 = item.split('\n\n')
                subItem2 = [subItem1[0].split('\n'), subItem1[-1].split('\n')]
                list2.append(subItem2)
            fname = str(f).replace('.txt', '.yml')
            fw = open(os.path.join(dir, fname), 'w')
            fw.write('tag:\n- dia\n\nqas:\n')
            for item in list2:
                fw.write('\n- que:\n')
                for que in item[0]:
                    fw.write('  - %s\n' % que)
                fw.write('  ans:\n')
                for ans in item[-1]:
                    fw.write('  - %s\n' % ans)
            fw.close()
