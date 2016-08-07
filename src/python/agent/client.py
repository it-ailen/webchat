# coding: utf-8
import common
import logging
from lxml import etree
import time
from pymongo import MongoClient


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
    C_WELCOME_words = """
        感谢关注上海交大四川校友会。
        回复以下命令:
        [注册] 注册校友信息
        [活动] 查看近期活动
    """
    C_ARM_wrong_msg = """
        亲，您说什么？
        %s
    """ % C_WELCOME_words

    C_AUTO_RESPONSE_register = u"注册"
    C_AUTO_RESPONSE_activity = u"活动"

    C_STATUS_normal = "normal"
    C_STATUS_unsubscribed = "unsubscribed"

    C_HOST = "test.hrmesworld.com"

    C_PAGE_AUTH_AND_REGISTER = "http://%s/assets/mates/register.html" % C_HOST
    C_PAGE_ACTIVITIES_LIST = "http://%s/assets/activities/list.html" % C_HOST

    def __init__(self, mongoConf):
        self._mongoConf = mongoConf
        self._reconnect_to_db()

    def _reconnect_to_db(self):
        self._mongoClient = MongoClient(**self._mongoConf)
        self._db = self._mongoClient.clients

    def wrap_xml(self, **tags):
        root = etree.Element("xml")
        for k, v in tags.items():
            sub = etree.SubElement(root, k)
            sub.text = v
        return etree.tostring(root)

    def _auto_reply_assistant(self, msg):
        logging.debug("get msg: %s", msg.Content)
        if msg.Content == self.C_AUTO_RESPONSE_register:
            content = """
                尊敬的校友，欢迎您，请进入<a href="%s?webChatId=%s">此页面进行注册</a>
            """ % (self.C_PAGE_AUTH_AND_REGISTER, msg.FromUserName)
        elif msg.Content == self.C_AUTO_RESPONSE_activity:
            content = """
                <a href="%s?webChatId=%s">活动列表</a>
            """ % (self.C_PAGE_ACTIVITIES_LIST, msg.FromUserName)
        else:
            content = self.C_ARM_wrong_msg
        return self.C_PATERN_text_msg % {
            "FromUserName": msg.ToUserName,
            "ToUserName": msg.FromUserName,
            "CreateTime": long(time.time()),
            "Content": content,
        }

    def handle_message(self, msg):
        msgType = "text"
        if msg.MsgType == "text":
            return self._auto_reply_assistant(msg)
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
        # conn = self.dbMgr.get_connection()
        tbl = self._db.clients
        if event.Event == "subscribe":
            # sql = "INSERT INTO `webchat_client`(`userId`, `subscribeTime`) " \
            #       " VALUES(?, ?)"
            # conn.execute(sql, (event.FromUserName, event.CreateTime))
            # conn.commit()
            oldInfo = tbl.find_one(filter={
                "webChatId": event.FromUserName
            })
            if oldInfo:
                if oldInfo.get("status", "normal") == self.C_STATUS_unsubscribed:
                    self._db.update({
                        "webChatId": event.FromUserName
                    }, {
                        "$set": {
                            "status": self.C_STATUS_normal
                        }
                    })
            else:
                tbl.insert_one({
                    "webChatId": event.FromUserName,
                    "subscribedTime": event.CreateTime
                })
            # oauthPattern = "https://open.weixin.qq.com/connect/oauth2/authorize?" \
            #                "appid=%(appid)s&redirect_uri=%(redirect_uri)s&" \
            #                "response_type=code&scope=%(scope)s&state=STATE#wechat_redirect" % {
            #     "appid": appid,
            #     "redirect_uri": self.C_PAGE_AUTH_AND_REGISTER,
            #     "scope": "snsapi_userinfo"
            # }
            # content = """您好！欢迎订阅SJTU四川校友会, <a href="%s">认证</a>""" % oauthPattern
            content = self.C_WELCOME_words
            logging.info(content)
            return self.C_PATERN_text_msg % {
                "FromUserName": event.ToUserName,
                "ToUserName": event.FromUserName,
                "CreateTime": long(time.time()),
                "Content": content,
            }
        elif event.Event == "unsubscribe":
            # sql = "DELETE FROM `webchat_client` WHERE `userId`=\"%s\"" % event.FromUserName
            # logging.info("%s - %d - %s", event.FromUserName, len(event.FromUserName), type(event.FromUserName))
            # conn.execute(sql)
            # conn.commit()
            tbl.update({
                "webChatId": event.FromUserName
            }, {
                "$set": {
                    "status": self.C_STATUS_unsubscribed
                }
            })
        else:
            logging.warn("Unhandled message: %s", event.json())

    def mate_register(self, meta):
        tbl = self._db.mates
        tbl.insert_one(meta)

