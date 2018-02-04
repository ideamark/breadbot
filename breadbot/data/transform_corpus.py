#!/usr/bin/env python3
import os
import sys


class transformCorpus(object):

    def __init__(self):
        pass

    def action(self, pathList=[]):
        if not pathList:
            print('Please enter file paths')
            return None
        for i in range(len(pathList)):
            if pathList[i][-1] == '*':
                pathList[i] == pathList[i][:-2]
            if os.path.isdir(pathList[i]):
                newPaths = os.listdir(pathList[i])
                for j in range(len(newPaths)):
                    newPaths[j] = os.path.join(pathList[i], newPaths[j])
                pathList += newPaths
        self.transform(pathList)

    def transform(self, pathList):
        for filePath in pathList:
            if not os.path.exists(filePath):
                print('%s not exists, passed!' % filePath)
                continue
            print(filePath)
            continue
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


if __name__ == '__main__':
    transformCorpus().action(sys.argv[1:])
