#!/usr/bin/env python3
import os
import sys
import yaml

from breadbot.core import common

LOG = common.console_log()

class checkData(object):

    def __init__(self):
        pass

    def _error(self, err, msg):
        LOG.error('[Error] %s' % msg)
        raise Exception(err)

    def do_check(self, dataPaths=[]):
        try:
            dataPaths = common.path_parser(dataPaths)
            for dataPath in dataPaths:
                if os.path.splitext(dataPath)[-1] != '.yml':
                    continue
                print('')
                LOG.info('Checking %s...' % dataPath)
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
                LOG.info('Check Passed!')

        except Exception as e:
            LOG.error(e)
