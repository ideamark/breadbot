#!/usr/bin/env python3
import os
import re
import yaml
from pymongo import MongoClient

from breadbot.core import misc

SPLIT_SYMBLE = ' '


class Data(object):

    def __init__(self, dataPaths=[]):
        self.all_flag = False
        if not dataPaths:
            dataPaths = misc.cfg().get('data_path')
            self.all_flag = True
        self.dataPaths = dataPaths
        self.dataLogPath = self._get_data_log_path()
        self.db = self._open_db()

    def import_data(self):
        changedList = \
            self._get_changed_list()
        self._clean_old_db_data(changedList)
        self._import_db_data(changedList)

    def drop_db(self):
        db_name = misc.cfg().get('db_name')
        ip = misc.cfg().get('db_ip')
        port = misc.cfg().get('db_port')
        client = MongoClient(ip, port)
        client.drop_database(db_name)
        data_log = os.path.join(
            misc.cfg().get('log_path'),
            'data.log')
        if os.path.exists(data_log):
            os.remove(data_log)
        print('\n Drop Database Done.')

    def _open_db(self):
        db_name = misc.cfg().get('db_name')
        ip = misc.cfg().get('db_ip')
        port = misc.cfg().get('db_port')
        client = MongoClient(ip, port)
        return client[db_name]

    def _clean_old_db_data(self, changedList):
        for dataPath in changedList:
            if not dataPath:
                continue
            else:
                pathName = self._get_path_name(dataPath)
                print('clean %s...' % pathName)
                self.db[pathName].drop()
        for dataPath in changedList:
            path = dataPath.split(SPLIT_SYMBLE)[0]
            if not os.path.exists(path):
                changedList.remove(dataPath)

    def _get_data_log_path(self):
        dataLogPath = os.path.join(misc.cfg().get('log_path'), 'data.log')
        return dataLogPath

    def _get_path_name(self, dataPath):
        return re.sub('[^a-zA-Z0-9]', '_', dataPath)

    def _read_data_file(self, dataPath):
        with open(dataPath, 'r') as f:
            readStr = f.read()
            readStr = re.sub(r'\n +\n', '\n\n', readStr)
        return readStr

    def _get_data_list(self, root, files):
        dataList = []
        for file in files:
            if not re.match(r'^.*\.yml$', file):
                continue
            dataPath = os.path.join(root, file)
            editTime = os.stat(dataPath).st_mtime
            info = '%s %s' % (dataPath, str(editTime))
            dataList.append(info)
        return dataList

    def _get_cur_list(self):
        curList = []
        for dataPath in self.dataPaths:
            if not os.path.exists(dataPath):
                continue
            for root, dirs, files in os.walk(dataPath):
                dataList = self._get_data_list(root, files)
                curList += dataList
        return curList

    def _get_old_list(self):
        if os.path.exists(self.dataLogPath):
            with open(self.dataLogPath, 'r') as log:
                oldList = log.read().split('\n')
            return oldList
        else:
            return []

    def _get_changed_list(self):
        if not self.all_flag:
            return self.dataPaths
        curList = self._get_cur_list()
        oldList = self._get_old_list()
        changedList = []
        for dataPath in curList:
            if dataPath not in oldList:
                dataPath = dataPath.split(SPLIT_SYMBLE)[0]
                changedList.append(dataPath)
        for dataPath in oldList:
            if dataPath not in curList:
                dataPath = dataPath.split(SPLIT_SYMBLE)[0]
                changedList.append(dataPath)
        changedList = list(set(changedList))
        return changedList

    def _save_data_info(self, dataPath):
        editTime = os.stat(dataPath).st_mtime
        if not os.path.exists(self.dataLogPath):
            with open(self.dataLogPath, 'w') as log:
                pass
        with open(self.dataLogPath, 'r') as log:
            old_list = log.read().split('\n')
            cur_list = self._get_cur_list()
            for i in range(len(cur_list)):
                cur_list[i] = cur_list[i].split(' ')[0]
            for item in old_list:
                file_name = item.split(' ')[0]
                if file_name not in cur_list:
                    old_list.remove(item)
        with open(self.dataLogPath, 'w') as log:
            if not old_list:
                log.write('%s %s' % (dataPath, editTime))
            else:
                new_list = []
                has_replace = False
                for item in old_list:
                    if dataPath == item.split(' ')[0]:
                        new_list.append('%s %s' % (dataPath, editTime))
                        has_replace = True
                    elif not item:
                        continue
                    else:
                        new_list.append(item)
                if not has_replace:
                    new_list.append('%s %s' % (dataPath, editTime))
                log.write('\n'.join(new_list))

    def _import_db_data(self, changedList):
        try:
            for dataPath in changedList:
                pathName = self._get_path_name(dataPath)
                print('import %s...' % dataPath)
                coll = self.db[pathName]
                readStr = self._read_data_file(dataPath)
                data = yaml.load(readStr)
                coll.insert(data)
                coll.create_index('tag')
                coll.create_index('que')
                self._save_data_info(dataPath)
            print('\n All Complete!')
        except Exception as e:
            print(e)
            print('\n Import Failed!')
