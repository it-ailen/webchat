# coding: utf-8
'''
Created on 2016年4月13日

@author: AilenZou
'''
import os
import config


class ConfigureMgr(object):
    C_ENV_PORT = "PORT"
    C_ENV_TOKEN = "TOKEN"

    def __init__(self, configFile=None):
        self._configMgr = config.ConfigMgr(configFile)
        self.do_check()

    def do_check(self):
        self._configMgr.setdefault("port", os.environ.get(self.C_ENV_PORT, 80))
        self._configMgr.set("token", os.environ[self.C_ENV_TOKEN])


    def get(self, key):
        return self._configMgr.get(key)
