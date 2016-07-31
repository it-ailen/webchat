# coding: utf-8

import configure
import logging
import agent
import hjson

configMgr = None
clientAgent = None


def init(configFile=None):
    global configMgr
    global clientAgent
    configMgr = configure.ConfigureMgr(configFile)
    clientAgent = agent.ClientAgent(configMgr.get("auto_response"))

def finish():
    logging.info("Finish now")