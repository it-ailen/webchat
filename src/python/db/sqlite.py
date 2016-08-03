# coding: utf-8
from .sql import Connection
import sqlite3
import logging


class Sqlite3Connection(Connection):
    def __init__(self, path, *args, **kwargs):
        self.conn = sqlite3.connect(path, *args, **kwargs)

    def execute(self, sql, *args, **kwargs):
        logging.info("%s, %s", sql, args)
        return self.conn.execute(sql, *args, **kwargs)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
