#!/usr/bin/env python3
import os
import re
import yaml
from pymongo import MongoClient
from breadbot.core import common

LOG = common.consoleLog()

class importData(object):

    def __init__(self):
        self.db = self._open_db()

    def do_import(self, data_path_list=[]):
        LOG.info('Start import data')
        self.all_flag = False
        if not data_path_list:
            data_path_list = common.cfg().get('local', 'data_paths')
            self.all_flag = True
        if type(data_path_list) is not list:
            data_path_list = [data_path_list]
        self.data_path_list = data_path_list
        redund_list = \
            self._get_redund_list()
        self._clean_old_db_data(redund_list)
        changed_list = \
            self._get_changed_list()
        self._clean_old_db_data(changed_list)
        self._import_db_data(changed_list)

    def _open_db(self):
        db_name = common.cfg().get('mongodb', 'db_name')
        ip = common.cfg().get('mongodb', 'db_ip')
        port = common.cfg().get('mongodb', 'db_port')
        client = MongoClient(ip, port)
        return client[db_name]

    def _clean_old_db_data(self, data_path_list):
        for data_path in data_path_list:
            if not data_path:
                continue
            else:
                coll = self._get_coll_name(data_path)
                LOG.info('clean %s' % coll)
                self.db[coll].drop()

    def _get_coll_name(self, data_path):
        return re.sub('[^a-zA-Z0-9]', '_', data_path)

    def _read_data_file(self, data_path):
        with open(data_path, 'r') as f:
            read_str = f.read()
            read_str = re.sub(r'\n +\n', '\n\n', read_str)
        return read_str

    def _get_modify_time(self, data_path):
        return os.stat(data_path).st_mtime

    def _get_cur_list(self):
        cur_list = []
        for data_path in self.data_path_list:
            if not os.path.exists(data_path):
                continue
            for root, dirs, files in os.walk(data_path):
                for File in files:
                    if os.path.splitext(File)[1] != '.yml':
                        continue
                    data_path = os.path.join(root, File)
                    cur_list.append(data_path)
        return cur_list

    def _get_old_list(self):
        colls = self.db.collection_names()
        old_list = []
        for coll in colls:
            if coll[-4:] != '_yml':
                continue
            db_data = self.db[coll].find_one()
            if db_data:
                data_path = db_data['path']
                if data_path:
                    old_list.append(data_path)
        return old_list

    def _get_changed_list(self):
        cur_list = self._get_cur_list()
        old_list = self._get_old_list()
        changed_list = []
        if not self.all_flag:
            return cur_list
        for data_path in cur_list:
            coll = self._get_coll_name(data_path)
            db_data = self.db[coll].find_one()
            if db_data:
                old_mtime = db_data['mtime']
            new_mtime = self._get_modify_time(data_path)
            if data_path not in old_list:
                changed_list.append(data_path)
            elif old_mtime != new_mtime:
                changed_list.append(data_path)
        changed_list = list(set(changed_list))
        return changed_list

    def _get_redund_list(self):
        cur_list = self._get_cur_list()
        old_list = self._get_old_list()
        redund_list = []
        if not self.all_flag:
            return cur_list
        for data_path in old_list:
            if data_path not in cur_list:
                redund_list.append(data_path)
        redund_list = list(set(redund_list))
        return redund_list

    def _import_db_data(self, changed_list):
        try:
            for data_path in changed_list:
                coll = self._get_coll_name(data_path)
                LOG.info('import %s' % data_path)
                db_coll = self.db[coll]
                read_str = self._read_data_file(data_path)
                data = yaml.load(read_str)
                data['path'] = data_path
                data['mtime'] = self._get_modify_time(data_path)
                db_coll.insert(data)
                db_coll.create_index('tag')
                db_coll.create_index('que')
            LOG.info('All Complete!')
        except Exception as e:
            LOG.error(e)
            LOG.error('Import Failed!')
