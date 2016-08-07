# coding: utf-8

import configure
import logging
import agent
import db
import data

configMgr = None
clientAgent = None
# dbManager = None

# dbConn = None


def init(configFile=None):
    global configMgr
    global clientAgent
    # global dbManager
    # global dbConn
    configMgr = configure.ConfigureMgr(configFile)
    # dbConn = db.sqlite.Sqlite3Connection(configMgr.get("db_file"))
    # dbManager = data.Manager(dbConn)
    clientAgent = agent.ClientAgent(configMgr.get("mongo"))

def finish():
    # global dbConn
    logging.info("Finish now")
    # dbConn.close()