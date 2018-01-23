import os
import re

from breadbot.core import misc
from . import manage


def start():
    token = misc.cfg().get('token')
    if not token:
        token = input('Please enter your wechat token: ')
        misc.cfg().write('token', token)

    ip = misc.cfg().get('server_ip')
    if not re.match(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}"
                    r"(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$", ip):
        ip = input('Please enter your server ip: ')
        misc.cfg().write('server_ip', ip)

    ma_path = manage.__file__
    port = '80'
    exeList = ['python3', ma_path, 'runserver', ':'.join([ip, port])]
    exeStr = ' '.join(exeList)
    os.system(exeStr)
