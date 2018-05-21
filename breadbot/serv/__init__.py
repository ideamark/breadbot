import os
import re

from breadbot.core import common
from . import manage


def start():
    token = common.Cfg().get('wechat', 'token')
    if not token:
        token = input('Please enter your wechat token: ')
        common.Cfg().write('wechat', 'token', token)

    public_ip = common.Cfg().get('wechat', 'public_ip')
    if not public_ip:
        public_ip = input('Please enter public IP: ')
        common.Cfg().write('wechat', 'public_ip', public_ip)

    ma_path = manage.__file__
    port = '80'
    exe_list = ['python3', ma_path, 'runserver',
               ':'.join([public_ip, port])]
    exe_str = ' '.join(exe_list)
    os.system(exe_str)
