#!/usr/bin/env python3
import os
import sys
import yaml


class CheckData(object):

    def __init__(self):
        pass

    def _error(self, err, msg):
        print(err)
        print('\n[Error] %s' % msg)
        exit(1)

    def action(self):
        if len(sys.argv) <= 1:
            _error('', 'please enter file path')
        filePath = sys.argv[1]
        if not os.path.exists(filePath):
            _error('', 'wrong file path')

        with open(filePath, 'r') as f:
            qas = yaml.load(f.read())['qas']

        for qa in qas:
            if not qa:
                _error(qa, 'qa is none')
            for value in qa.values():
                if not value:
                    _error(qa, 'value is none')
                else:
                    for item in value:
                        if type(item) == dict:
                            _error(qa, 'item is dict')
                        if not item:
                            _error(qa, 'item is none')
        print('\nCheck Passed!')


if __name__ == '__main__':
    CheckData().action()
