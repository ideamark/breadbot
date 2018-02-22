#!/usr/bin/python3
import os
import sys
from setuptools import setup


if os.geteuid():
    args = [sys.executable] + sys.argv
    os.execlp('sudo', 'sudo', *args)

if len(sys.argv) <= 1:
    print('Please enter install, uninstall or clean')
    sys.exit(1)

elif sys.argv[1] == 'install':
    os.system('rm -f /etc/bread.cfg')
    os.system('rm -f /usr/local/bin/breadbot')
    os.system('pip3 install -U pip')
    os.system('pip3 install -r requirements.txt')
    setup(
        setup_requires=['pbr>=0.1'],
        pbr=True,)
    from breadbot import core
    log_path = core.common.cfg().get('log_path')
    os.mkdir(log_path)
    data_path = [os.path.join(os.getcwd(), 'data')]
    core.common.cfg().write('data_path', data_path)
    os.system('breadbot import')

elif sys.argv[1] == 'uninstall':
    from breadbot import data
    data.database.dataBase().drop_db()
    os.system('pip3 uninstall breadbot')
    os.system('rm -f /etc/bread.cfg')
    os.system('rm -f /usr/local/bin/breadbot')
    sys.exit(0)

elif sys.argv[1] == 'clean':
    exclude = [
        '.git',
        '.gitignore',
        '.tox',
        'bin',
        'breadbot',
        'data',
        'etc',
        'log',
        'tests',
        'LICENSE',
        'NEWS',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        'TODO',
        'tox.ini',
    ]
    fileList = os.listdir('.')
    for f in fileList:
        if f not in exclude:
            os.system('rm -rf %s' % f)
    os.system('find -name "__pycache__"|xargs rm -rf')
    sys.exit(0)
