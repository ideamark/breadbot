#!/usr/bin/env python3
import os
import re
import shutil
import sys
from breadbot.core import common

LOG = common.ConsoleLog()

class TransformCorpus(object):

    def __init__(self):
        pass

    def do_transform(self, file_path_list=[]):
        file_path_list = common.expand_path(file_path_list)
        for file_path in file_path_list:
            LOG.info('Transforming %s' % file_path)
            text = ''
            with open(file_path, 'r') as fp:
                text = fp.read()
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

            list1 = text.split('\n\n\n')
            list2 = []
            for item in list1:
                sub_item1 = item.split('\n\n')
                sub_item2 = [sub_item1[0].split('\n'), sub_item1[-1].split('\n')]
                list2.append(sub_item2)

            yml_path = file_path + '.yml'
            with open(yml_path, 'w') as fp:
                for item in list2:
                    fp.write('\n- que:\n')
                    for que in item[0]:
                        if not que:
                            continue
                        fp.write('  - %s\n' % que)
                    fp.write('  ans:\n')
                    for ans in item[-1]:
                        if not ans:
                            continue
                        fp.write('  - %s\n' % ans)
