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

    def handle_text(self, msg):
        response = """
            <xml>
                <ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
                <FromUserName><![CDATA[%(FromUserName)s]]></FromUserName>
                <CreateTime>%(CreateTime)s</CreateTime>
                <MsgType><![CDATA[%(MsgType)s]]></MsgType>
                <Content><![CDATA[%(Content)s]]></Content>
            </xml>
        """
        return response % {
            "ToUserName": msg.FromUserName,
            "FromUserName": msg.ToUserName,
            "CreateTime": long(time.time()),
            "MsgType": "text",
            "Content": "You said: " + msg.Content
        }

    def parse_xml_msg(self, src):
        tree = etree.fromstring(src)
        msg = {}
        for e in tree.findall(".*"):
            msg[e.tag] = e.text
        return common.Bundle.build_from_dict(msg)

    def handle_event(self, event):
        root = etree.Element("xml")
        sub = etree.SubElement(root, "FromUserName")
        sub.text = etree.CDATA(event.ToUserName)
        sub = etree.SubElement(root, "ToUserName")
        sub.text = etree.CDATA(event.FromUserName)
        sub = etree.SubElement(root, "CreateTime")
        sub.text = str(long(time.time()))

        conn = self.dbMgr.get_connection()
        if event.Event == "subscribe":
            sql = "INSERT INTO `webchat_client`(`userId`, `subscribeTime`) " \
                  " VALUES(?, ?)"
            conn.execute(sql, (event.FromUserName, event.CreateTime))
            conn.commit()
            return "您好！欢迎订阅SJTU四川校友会"
        elif event.Event == "unsubcribe":
            sql = "DELETE FROM `webchat_client` WHERE `userId`=?"
            conn.execute(sql, (event.FromUserName))
            conn.commit()
        elif event.Event == "CLICK":
            # 自定义菜单事件
            logging.info("Got CLICK.%s from %s",
                         event.EventKey,
                         event.FromUserName)
        else:
            logging.warn("Unhandled message: %s", event.json())
