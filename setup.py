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
    os.system('pip3 install -U pip')
    os.system('pip3 install -r requirements.txt')
    setup(
        setup_requires=['pbr>=0.1'],
        pbr=True,)
    from breadbot.core.common import Cfg
    log_path = Cfg().get('local', 'log_path')
    mem_path = Cfg().get('local', 'mem_path')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    if not os.path.exists(mem_path):
        os.mkdir(mem_path)
    data_path = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_path):
        Cfg().write('local', 'data_paths', data_path)
        os.system('git clone https://github.com/ideamark/ideamark.github.io "data"')
        os.system('chmod -R 777 data')
    print('Install success!')
    sys.exit(0)

elif sys.argv[1] == 'uninstall':
    from breadbot.core.common import Cfg
    cfg_path = Cfg().get('local', 'cfg_path')
    bin_path = Cfg().get('local', 'bin_path')
    if os.path.exists(cfg_path):
        os.remove(cfg_path)
    if os.path.exists(bin_path):
        os.remove(bin_path)
    os.system('pip3 uninstall breadbot')
    print('Uninstall success!')
    sys.exit(0)

elif sys.argv[1] == 'clean':
    exclude = [
        '.eggs',
        'AUTHORS',
        'breadbot.egg-info',
        'build',
        'ChangeLog'
    ]
    file_list = os.listdir('.')
    for f in file_list:
        if f in exclude:
            os.system('rm -rf %s' % f)
    os.system('find -name "__pycache__"|xargs rm -rf')
    print('Clean up success!')
    sys.exit(0)
