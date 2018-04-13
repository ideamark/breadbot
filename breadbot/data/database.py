#!/usr/bin/env python3
from pymongo import MongoClient

from breadbot.core import common


class dataBase(object):

    def __init__(self):
        pass

    def drop_db(self):
        db_name = common.cfg().get('mongodb', 'db_name')
        ip = common.cfg().get('mongodb', 'db_ip')
        port = common.cfg().get('mongodb', 'db_port')
        client = MongoClient(ip, port)
        client.drop_database(db_name)
        print('\n Drop Database Done.')

