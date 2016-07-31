# coding: utf-8
import common
import logging
from lxml import etree
import time


class UnknownHello(Exception):
    def __init__(self, key):
        self.key = key


class ClientAgent(object):
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr

    def wrap_xml(self, **tags):
        root = etree.Element("xml")
        for k, v in tags.items():
            sub = etree.SubElement(root, k)
            sub.text = v
        return etree.tostring(root)

    def handle_message(self, msg):
        msgType = "text"
        content = ""
        if msg.MsgType == "text":
            content = "You said: " + msg.Content
        else:
            logging.warn("Unhandled message type: %s", msg.MsgType)
            logging.warn("%s", msg)
            content = "Unsupported type of message: %s" % msg.MsgType
        return self.wrap_xml(FromUserName=etree.CDATA(msg.ToUserName),
                             ToUserName=etree.CDATA(msg.FromUserName),
                             CreateTime=str(long(time.time())),
                             MsgType=etree.CDATA(msgType),
                             Content=etree.CDATA(content))

    def parse_xml_msg(self, src):
        tree = etree.fromstring(src)
        msg = {}
        for e in tree.findall(".*"):
            msg[e.tag] = e.text
        return common.Bundle.build_from_dict(msg)

    def handle_event(self, event):
        clicks = {
            "WEBCHAT_MENU_news": {

            }
        }
        conn = self.dbMgr.get_connection()
        if event.Event == "subscribe":
            sql = "INSERT INTO `webchat_client`(`userId`, `subscribeTime`) " \
                  " VALUES(?, ?)"
            conn.execute(sql, (event.FromUserName, event.CreateTime))
            conn.commit()
            content = u"您好！欢迎订阅SJTU四川校友会"
            return self.wrap_xml(FromUserName=etree.CDATA(event.ToUserName),
                                 ToUserName=etree.CDATA(event.FromUserName),
                                 CreateTime=str(long(time.time())),
                                 MsgType=etree.CDATA("text"),
                                 Content=etree.CDATA(content))
        elif event.Event == "unsubscribe":
            sql = "DELETE FROM `webchat_client` WHERE `userId`=?"
            conn.execute(sql, (event.FromUserName))
            conn.commit()
        elif event.Event == "CLICK":
            # 自定义菜单事件
            logging.info("Got CLICK.%s from %s",
                         event.EventKey,
                         event.FromUserName)
            if event.EventKey == "WEBCHAT_MENU_news":
                pass
            else:
                logging.warn("Undefined event key: %s", event.EventKey)
        else:
            logging.warn("Unhandled message: %s", event.json())
