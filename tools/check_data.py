#!/usr/bin/env python3
import os
import sys
import yaml


def error(err, msg):
    print(err)
    print('\n[Error] %s' % msg)
    exit(1)


if len(sys.argv) <= 1:
    error('', 'please enter file path')
filePath = sys.argv[1]
if not os.path.exists(filePath):
    error('', 'wrong file path')

with open(filePath, 'r') as f:
    qas = yaml.load(f.read())['QA']

for qa in qas:
    if not qa:
        error(qa, 'qa is none')
    for value in qa.values():
        if not value:
            error(qa, 'value is none')
        else:
            for item in value:
                if type(item) == dict:
                    error(qa, 'item is dict')
                if not item:
                    error(qa, 'item is none')
print('\nCheck Passed!')
