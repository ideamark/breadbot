#!/usr/bin/env python3
import os
import sys
import yaml

from breadbot.core import common


class checkData(object):

    def __init__(self):
        pass

    def _error(self, err, msg):
        print('\n[Error] %s' % msg)
        raise Exception(err)

    def do_check(self, dataPaths=[]):
        try:
            dataPaths = common.path_parser(dataPaths)
            for dataPath in dataPaths:
                if os.path.splitext(dataPath)[-1] != '.yml':
                    continue
                print('Checking %s...' % dataPath)
                if not os.path.exists(dataPath):
                    self._error('', 'wrong data path')

                with open(dataPath, 'r') as f:
                    qas = yaml.load(f.read())['qas']

                for qa in qas:
                    if not qa:
                        self._error(qa, 'qa is none')
                    for value in qa.values():
                        if not value:
                            self._error(qa, 'value is none')
                        else:
                            for item in value:
                                if type(item) is dict:
                                    self._error(qa, 'item is dict')
                                if not item:
                                    self._error(qa, 'item is none')
                print('\nCheck Passed!')

        except Exception as e:
            print(e)
