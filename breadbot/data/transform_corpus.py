#!/usr/bin/env python3
import os
import re
import shutil
import sys
from breadbot.core import common

LOG = common.ConsoleLog()

class TransformCorpus(object):

    def __init__(self):
        out_dir = 'output'
        if os.path.basename(os.getcwd()) == out_dir:
            self.out_path = os.getcwd()
        else:
            self.out_path = os.path.join(os.getcwd(), out_dir)
        if not os.path.exists(self.out_path):
            LOG.info('Create %s' % self.out_path)
            os.makedirs(self.out_path)

    def do_transform(self, file_path_list=[]):
        file_path_list = common.expand_path(file_path_list)
        new_file_path_list = []

        # Copy file
        for file_path in file_path_list:
            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(self.out_path, file_name)
            if not os.path.exists(new_file_path):
                LOG.info('Copy %s' % file_path)
                shutil.copyfile(file_path, new_file_path)
            new_file_path_list.append(new_file_path)

        # Initilization
        for file_path in new_file_path_list:
            LOG.info('Initializing %s' % file_path)
            text = ''
            with open(file_path, 'r') as fr:
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
            with open(file_path, 'w') as fw:
                fw.write(text)

        # Transform
        for file_path in new_file_path_list:
            LOG.info('Transforming %s' % file_path)
            with open(file_path, 'r') as fr:
                text = fr.read()
            list1 = text.split('\n\n\n')
            list2 = []
            for item in list1:
                sub_item1 = item.split('\n\n')
                sub_item2 = [sub_item1[0].split('\n'), sub_item1[-1].split('\n')]
                list2.append(sub_item2)
            yml_name = os.path.splitext(file_path)[0] + '.yml'
            with open(os.path.join(self.out_path, yml_name), 'w') as fw:
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
