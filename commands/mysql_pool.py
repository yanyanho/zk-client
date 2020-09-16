import pymysql

from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

from commands.constants import DATABASE_DEFAULT_ADDRESS, DATABASE_DEFAULT_PORT, DATABASE_DEFAULT_USER, \
    DATABASE_DEFAULT_PASSWORD, DATABASE_DEFAULT_DATABASE

charset = 'utf8'

class MysqlPool(PooledDB):
    __instance = None
    __pool = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            # cls.__instance = object.__new__(cls)
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """创建链接池"""
        PooledDB.__init__(self, pymysql, maxconnections=50, mincached=0, maxcached=0, maxshared=0, blocking=True,
                          host=DATABASE_DEFAULT_ADDRESS, port=DATABASE_DEFAULT_PORT ,user=DATABASE_DEFAULT_USER, password=DATABASE_DEFAULT_PASSWORD, database=DATABASE_DEFAULT_DATABASE, charset=charset, cursorclass=DictCursor)

    def conn(self):
        _conn = self.connection()
        return _conn