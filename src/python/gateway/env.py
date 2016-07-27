# coding: utf-8

import configure
import logging

configMgr = None


def init(configFile=None):
    global configMgr
    configMgr = configure.ConfigureMgr(configFile)

def finish():
    logging.info("Finish now")