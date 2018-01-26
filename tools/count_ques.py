#!/usr/bin/env python3
from breadbot.core.common import cfg
import os

quesCount = 0
dataPaths = cfg().get('data_path')

for dataPath in dataPaths:
    for root, dirs, files in os.walk(dataPath):
        if not files:
            continue
        for f in files:
            if f.split('.')[-1] != 'yml':
                continue
            filePath = os.path.join(root, f)
            with open(filePath, 'r') as fp:
                content = fp.read()
                quesCount += content.count('- que:\n')

print(quesCount)
