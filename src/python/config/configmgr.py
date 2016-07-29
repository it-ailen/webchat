# coding: utf-8
'''
Created on 2015年10月14日

@author: AilenZou
'''
import yaml
import hjson
import json


class ConfigError(Exception):
    pass


class ConfigMgr(object):
    def __init__(self, configFile=None):
        if configFile:
            self.__config = ConfigMgr.parse(configFile)
        else:
            self.__config = {}

    @classmethod
    def parse(cls, configFile):
        if configFile and configFile.endswith("yaml"):
            with open(configFile, 'r') as s:
                return yaml.load(s)
        elif configFile and configFile.endswith("hjson"):
            with open(configFile, "r") as s:
                return hjson.load(s)
        elif configFile and configFile.endswith("json"):
            with open(configFile, "r") as s:
                return json.load(s)
        else:
            raise ConfigError("Unsupported configg")


    C_CONFIG_DEFAULT = "configure_default"

    def get(self, key, default=C_CONFIG_DEFAULT):
        """
            Get the configuration value of the key.
            @param key: key of the configuration.
            @param default: default value of the key if there is no value. You must
                            set this default value if the configuration is optional.
            @raise ConfigError: raise ConfigError when the value of key is missing
                                and no default value specified.
        """
        value = self.__config.get(key, default)
        if value is self.C_CONFIG_DEFAULT:
            raise ConfigError("Configuration %s missing." % key)
        return value

    def all(self):
        return self.__config

    def setdefault(self, key, default):
        return self.__config.setdefault(key, default)

    def set(self, key, value):
        self.__config[key] = value

    @classmethod
    def time_config_parse(cls, val):
        if val.endswith("s"):
            try:
                sec = int(val[:len(val) - 1])
            except:
                raise ConfigError("Invalid format of time configuration")
        elif val.endswith("m"):
            try:
                sec = int(val[:len(val) - 1]) * 60
            except:
                raise ConfigError("Invalid format of time configuration")
        elif val.endswith("h"):
            try:
                sec = int(val[:len(val) - 1]) * 60 * 60
            except:
                raise ConfigError("Invalid format of time configuration")
        else:
            raise ConfigError("Invalid format of time configuration")
        return sec * 1000
