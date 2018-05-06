#!/usr/bin/python3
import os
import sys
from setuptools import setup


data_path = os.path.join(os.getcwd(), 'data')
log_path = '/var/log/breadbot'
basic_corpus_path = os.path.join(os.getcwd(), 'data/corpus/basic_dialogues')
bread_cfg_path = '/etc/bread.cfg'
bread_bin_path = '/use/local/bin/breadbot'


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
    from breadbot import data
    from breadbot import core
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    core.common.cfg().write('local', 'data_paths', data_path)
    core.common.cfg().write('local', 'log_path', log_path)
    os.system('git clone https://github.com/ideamark/ideamark.github.io "data"')
    data.import_data.importData().do_import(basic_corpus_path)

elif sys.argv[1] == 'uninstall':
    if os.path.exists(bread_cfg_path):
        from breadbot import data
        data.database.dataBase().drop_db()
        os.remove(bread_cfg_path)
    if os.path.exists(bread_bin_path):
        os.remove(bread_bin_path)
    os.system('pip3 uninstall breadbot')
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
