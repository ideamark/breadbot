#!/usr/bin/env python3
import os
import sys
import yaml

from breadbot.core import common

LOG = common.consoleLog()

class checkData(object):

    def __init__(self):
        pass

    def _error(self, err, msg):
        LOG.error('[Error] %s' % msg)
        raise Exception(err)

    def do_check(self, data_path_list=[]):
        try:
            if not data_path_list:
                data_path_list = common.cfg().get('local', 'data_paths')
            data_path_list = common.expand_path(data_path_list)
            for data_path in data_path_list:
                if os.path.splitext(data_path)[-1] != '.yml':
                    continue
                print('')
                LOG.info('Checking %s' % data_path)
                if not os.path.exists(data_path):
                    self._error('', 'wrong data path')

                with open(data_path, 'r') as f:
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
