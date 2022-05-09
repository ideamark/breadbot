#!/usr/bin/python3
import os
import sys
import platform
from setuptools import setup
import traceback


def check_system():
    return platform.system()


def get_home_dir():
    os_platform = check_system()
    if os_platform == 'Windows':
        return os.environ['USERPROFILE']
    else:
        return os.environ['HOME']


def install():
    try:
        os.system('pip3 install -U pip')
        os.system('pip3 install --user -r requirements.txt')
        setup(
            setup_requires=['pbr>=0.1'],
            pbr=True,)

        from breadbot.core.common import Cfg
        home_dir = get_home_dir()
        log_path = Cfg().get('local', 'log_path').replace('~', home_dir)
        mem_path = Cfg().get('local', 'mem_path').replace('~', home_dir)
        data_path = Cfg().get('local', 'data_path').replace('~', home_dir)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if not os.path.exists(mem_path):
            os.makedirs(mem_path)
        os.system('git clone https://github.com/ideamark/ideamark.github.io ' + data_path)
        print('Install Success')
    except Exception:
        print(traceback.format_exc())
        print('Install Failed')


def uninstall():
    try:
        home_dir = get_home_dir()
        os.system('pip3 uninstall breadbot')
        os.remove(os.path.join(home_dir, '.breadbot'))
        print('Uninstall Success')
    except Exception:
        print(traceback.format_exc())
        print('Uninstall Failed.')


def clean():
    try:
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
        print('Clean up Success')
    except Exception:
        print(traceback.format_exc())
        print('Clean up Failed')


def menu():
    if len(sys.argv) <= 1:
        print('Please enter install, uninstall or clean')
        sys.exit(1)
    elif sys.argv[1] == 'install':
        install()
        sys.exit(0)
    elif sys.argv[1] == 'uninstall':
        uninstall()
        clean()
        sys.exit(0)
    elif sys.argv[1] == 'clean':
        clean()
        sys.exit(0)


if __name__ == '__main__':
    os_platform = check_system()
    if os_platform == 'Windows':
        print('Windows is not supported yet.')
    else:
        menu()
