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
    C_ENV_AUTO_RESPONSE = "AUTO_RESPONSE"
    C_ENV_DB_FILE = "DB_FILE"

    def __init__(self, configFile=None):
        self._configMgr = config.ConfigMgr(configFile)
        self.do_check()

    def do_check(self):
        self._configMgr.get("app_id")
        self._configMgr.get("secret")
        self._configMgr.setdefault("port", os.environ.get(self.C_ENV_PORT, 80))
        self._configMgr.set("token", os.environ[self.C_ENV_TOKEN])
        if os.environ.get(self.C_ENV_WEBCHAT_MENU_CONF, None) is None:
            raise config.ConfigError("Missing environment: %s" % self.C_ENV_WEBCHAT_MENU_CONF)
        self._configMgr.set("menu",
                            config.ConfigMgr.parse(os.environ[self.C_ENV_WEBCHAT_MENU_CONF]))
        if os.environ.get(self.C_ENV_AUTO_RESPONSE, None) is None:
            raise config.ConfigError("Missing environment: %s" % self.C_ENV_AUTO_RESPONSE)
        self._configMgr.set("auto_response",
                            config.ConfigMgr.parse(os.environ[self.C_ENV_AUTO_RESPONSE]))
        if os.environ.get(self.C_ENV_DB_FILE, None) is None:
            raise config.ConfigError("Missing environment: %s" % self.C_ENV_DB_FILE)
        self._configMgr.set("db_file",
                            os.environ[self.C_ENV_DB_FILE])
        self._configMgr.setdefault("mongo", {
            "host": "localhost",
            "port": 27017
        })

    def get(self, key):
        return self._configMgr.get(key)
