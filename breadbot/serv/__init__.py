import os
import re

from breadbot.core import common
from . import manage


def start():
    token = common.Cfg().get('wechat', 'token')
    if not token:
        token = input('Please enter your wechat token: ')
        common.Cfg().write('wechat', 'token', token)

    host_ip = common.Cfg().get('wechat', 'host_ip')
    if not host_ip:
        host_ip = input('Please enter host IP: ')
        common.Cfg().write('wechat', 'host_ip', host_ip)

    port = common.Cfg().get('wechat', 'port')
    ma_path = manage.__file__
    exe_list = ['python3', ma_path, 'runserver',
                ':'.join([host_ip, port])]
    exe_str = ' '.join(exe_list)
    os.system(exe_str)
