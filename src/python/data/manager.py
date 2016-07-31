# coding: utf-8


class Manager(object):
    def __init__(self, sqlConnection):
        self.conn = sqlConnection

    def get_connection(self):
        return self.conn

    def close(self):
        self.conn.close()