# coding: utf-8
import common
import logging
from lxml import etree
import time


class UnknownHello(Exception):
    def __init__(self, key):
        self.key = key


class ClientAgent(object):
    C_PATERN_text_msg = """
        <xml>
            <FromUserName><![CDATA[%(FromUserName)s]]></FromUserName>
            <ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
            <CreateTime>%(CreateTime)s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%(Content)s]]></Content>
        </xml>
    """

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

    def handle_event(self, event, appid):
        conn = self.dbMgr.get_connection()
        if event.Event == "subscribe":
            sql = "INSERT INTO `webchat_client`(`userId`, `subscribeTime`) " \
                  " VALUES(?, ?)"
            conn.execute(sql, (event.FromUserName, event.CreateTime))
            conn.commit()
            oauthPattern = "https://open.weixin.qq.com/connect/oauth2/authorize?" \
                           "appid=%(appid)s&redirect_uri=%(redirect_uri)s&" \
                           "response_type=code&scope=SCOPE&state=STATE#wechat_redirect" % {
                "appid": appid,
                "redirect_uri": "http://test.hrmesworld.com/mates/register.html"
            }
            content = """您好！欢迎订阅SJTU四川校友会, <a href="%s">认证</a>""" % oauthPattern
            logging.info(content)
            # return self.wrap_xml(FromUserName=etree.CDATA(event.ToUserName),
            #                      ToUserName=etree.CDATA(event.FromUserName),
            #                      CreateTime=str(long(time.time())),
            #                      MsgType=etree.CDATA("text"),
            #                      Content=etree.CDATA(content))
            return self.C_PATERN_text_msg % {
                "FromUserName": event.ToUserName,
                "ToUserName": event.FromUserName,
                "CreateTime": long(time.time()),
                "Content": content,
            }
        elif event.Event == "unsubscribe":
            sql = "DELETE FROM `webchat_client` WHERE `userId`=\"%s\"" % event.FromUserName
            logging.info("%s - %d - %s", event.FromUserName, len(event.FromUserName), type(event.FromUserName))
            conn.execute(sql)
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
