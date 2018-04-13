import os
import re

from breadbot.core import common
from . import manage


def start():
    token = common.cfg().get('wechat', 'token')
    if not token:
        token = input('Please enter your wechat token: ')
        common.cfg().write('wechat', 'token', token)

    ip = input('Please enter your IP: ')
    common.cfg().write('wechat', 'allowed_ips', ip)

    ma_path = manage.__file__
    port = '80'
    exeList = ['python3', ma_path, 'runserver', ':'.join([ip, port])]
    exeStr = ' '.join(exeList)
    os.system(exeStr)
