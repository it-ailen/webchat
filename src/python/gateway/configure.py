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
    C_ENV_WEBCHAT_MENU_CONF = "MENU_CONF"

    def __init__(self, configFile=None):
        self._configMgr = config.ConfigMgr(configFile)
        self.do_check()

    def do_check(self):
        self._configMgr.setdefault("port", os.environ.get(self.C_ENV_PORT, 80))
        self._configMgr.set("token", os.environ[self.C_ENV_TOKEN])
        if os.environ.get(self.C_ENV_WEBCHAT_MENU_CONF, None) is None:
            raise config.ConfigError("Missing environment: %s" % self.C_ENV_WEBCHAT_MENU_CONF)
        self._configMgr.set("menu",
                            config.ConfigMgr.parse(os.environ[self.C_ENV_WEBCHAT_MENU_CONF]))


    def get(self, key):
        return self._configMgr.get(key)
