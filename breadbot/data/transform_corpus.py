#!/usr/bin/env python3
import os
import re
import shutil
import sys
from breadbot.core import common

LOG = common.console_log()

class transformCorpus(object):

    def __init__(self):
        outDir = 'output'
        if os.path.basename(os.getcwd()) == outDir:
            self.outPath = os.getcwd()
        else:
            self.outPath = os.path.join(os.getcwd(), outDir)
        if not os.path.exists(self.outPath):
            LOG.info('Create %s' % self.outPath)
            os.makedirs(self.outPath)

    def do_transform(self, filePaths=[]):
        filePaths = common.path_parser(filePaths)
        newFilePaths = []

        # Copy file
        for filePath in filePaths:
            fileName = os.path.basename(filePath)
            newFilePath = os.path.join(self.outPath, fileName)
            if not os.path.exists(newFilePath):
                LOG.info('Copy %s' % filePath)
                shutil.copyfile(filePath, newFilePath)
            newFilePaths.append(newFilePath)

        # Initilization
        for filePath in newFilePaths:
            LOG.info('Initializing %s...' % filePath)
            text = ''
            with open(filePath, 'r') as fr:
                text = fr.read()
            if not text:
                raise Exception('empty file!')
            text = re.sub(r'[^\u000A-\u007E]', '', text)
            text = re.sub(r'#*', '', text)
            text = re.sub(r':', ',', text)
            text = re.sub(r'//*', r'/', text)
            text = re.sub(r'!!*', '!', text)
            text = re.sub(r',,*', ',', text)
            text = re.sub(r'::*', ':', text)
            text = re.sub(r';;*', ';', text)
            text = re.sub(r'\?\?*', '?', text)
            text = re.sub(r'\(\(*', '(', text)
            text = re.sub(r'\)\)*', ')', text)
            text = re.sub(r'\(.*\)', '', text)
            text = re.sub(r'\[\[*', '[', text)
            text = re.sub(r'\]\]*', ']', text)
            text = re.sub(r'\[.*\]', '', text)
            text = re.sub(r'\{\{*', '{', text)
            text = re.sub(r'\}\}*', '}', text)
            text = re.sub(r'{.*}', '', text)
            text = re.sub(r'\<\<*', '<', text)
            text = re.sub(r'\>\>*', '>', text)
            text = re.sub(r'<.*>', '', text)
            text = re.sub(r'  *', ' ', text)
            text = re.sub(r'^ *', '', text)
            text = re.sub(r' *$', '', text)
            text = re.sub(r'\? ', r'?\n', text)
            text = re.sub(r'! ', r'!\n', text)
            text = re.sub(r'\. ', r'.\n', text)
            text = re.sub(r'&.*;', '', text)
            text = re.sub(r'\n\n*\n', '\n', text)
            text = re.sub(r'.{140,9999}\n', '', text)
            text = re.sub(r'\n[^a-zA-Z]*\n', r'\n', text)
            text = re.sub(r'\n[^a-zA-Z0-9]*', r'\n', text)
            text = re.sub(r'(.*\?\n)(.*[^\?]\n)', r'\1\n\2', text)
            text = re.sub(r'(.*[^\?]\n)(.*\?\n)', r'\1\n\n\2', text)
            with open(filePath, 'w') as fw:
                fw.write(text)

        # Transform
        for filePath in newFilePaths:
            LOG.info('Transforming %s...' % filePath)
            with open(filePath, 'r') as fr:
                text = fr.read()
            list1 = text.split('\n\n\n')
            list2 = []
            for item in list1:
                subItem1 = item.split('\n\n')
                subItem2 = [subItem1[0].split('\n'), subItem1[-1].split('\n')]
                list2.append(subItem2)
            ymlName = os.path.splitext(filePath)[0] + '.yml'
            with open(os.path.join(self.outPath, ymlName), 'w') as fw:
                fw.write('tag:\n- dia\n\nqas:\n')
                for item in list2:
                    fw.write('\n- que:\n')
                    for que in item[0]:
                        if not que:
                            continue
                        fw.write('  - %s\n' % que)
                    fw.write('  ans:\n')
                    for ans in item[-1]:
                        if not ans:
                            continue
                        fw.write('  - %s\n' % ans)
