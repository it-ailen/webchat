# coding: utf-8

from http import BaseHandler, CustomHTTPError, error_code
import hashlib
import logging
import requests
import time
import re
import env
import datetime


matcher = re.compile(r"<!\[([^\[\]]+)\[([^\[\]]+)\]\]>")

class WebChatBaseHandler(BaseHandler):
    C_WEIXIN_CGI = "https://api.weixin.qq.com/cgi-bin"

    C_GRANT_TYPE_CLIENT = "client_credential"

    accessTokens = {}

    def check_signature(self, signature, timestamp, nonce, token):
        L = [token, timestamp, nonce]
        L.sort()
        s = L[0] + L[1] + L[2]
        return hashlib.sha1(s).hexdigest() == signature

    def fetch_access_token(self, type=C_GRANT_TYPE_CLIENT):
        now = long(time.time())
        if WebChatBaseHandler.accessTokens.get(type, None) is not None:
            oldToken = WebChatBaseHandler.accessTokens[type]
            if oldToken["expired_time"] < now:
                return oldToken["access_token"]
        appId = env.configMgr.get("app_id")
        secret = env.configMgr.get("secret")
        data = {
            "appid": appId,
            "secret": secret,
            "grant_type": type
        }
        try:
            resp = requests.get(self.C_WEIXIN_CGI + "/token",
                                params=data)
            res = resp.json()
            WebChatBaseHandler.accessTokens[type] = {
                "access_token": res["access_token"],
                "expired_time": res["expires_in"] + now - 300 # 余300s
            }
            logging.info("access_token: %s", res["access_token"])
            return res["access_token"]
        except:
            logging.exception("WeiXin error")
            raise CustomHTTPError(503,
                                  error_code.C_EC_UNKNOWN,
                                  cause="Weixin has gone")


class WebChatHandler(WebChatBaseHandler):
    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        if self.check_signature(signature, timestamp, nonce, env.configMgr.get("token")):
            self.write(echostr)
        else:
            raise CustomHTTPError(403,
                                  error_code.C_EC_CHECK_FAILED,
                                  cause="Wrong request from WebChat")

    def post(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        if not self.check_signature(signature, timestamp, nonce, env.configMgr.get("token")):
            raise CustomHTTPError(403,
                                  error_code.C_EC_CHECK_FAILED,
                                  cause="Wrong request from WebChat")
        logging.info("args: %s", self.request.body)
        msg = env.clientAgent.parse_xml_msg(self.request.body)
        if msg.MsgType == "event":
            res = env.clientAgent.handle_event(msg, env.configMgr.get("app_id"))
            if res is not None:
                self.write(res)
        else:
            res = env.clientAgent.handle_message(msg)
            self.write(res)


class WebChatMenuHandler(WebChatBaseHandler):
    def post(self):
        accessToken = self.fetch_access_token()
        menu = env.configMgr.get("menu")
        logging.info(menu)
        try:
            url = self.C_WEIXIN_CGI + "/menu/create?access_token=" + accessToken
            logging.info("url: %s", url)
            resp = requests.post(url,
                                 json=menu)
            res = resp.json()
            if res["errcode"] != 0:
                raise Exception("Wrong response from WebChat: %s" % resp.text)
        except:
            logging.exception("Fail to create menu")
            raise CustomHTTPError(503,
                                  error_code.C_EC_UNKNOWN,
                                  cause="WebChat has gone")

    def get(self):
        accessToken = self.fetch_access_token()


class MatesHandler(WebChatBaseHandler):
    def put(self):
        logging.info(self.request.arguments)
        args = {
            "name": self.get_argument("name"),
            "phone": self.get_argument("phone"),
            "college": self.get_argument("college"),
            "degree": self.get_argument("degree"),
        }
        startTime = self.get_argument("start_time")
        endTime = self.get_argument("end_time")
        logging.debug("start_time: %s", startTime)
        try:
            startTime = datetime.datetime.strptime(startTime, "%Y/%m")
            endTime = datetime.datetime.strptime(endTime, "%Y/%m")
        except:
            logging.exception("Format error")
            raise CustomHTTPError(400,
                                  error_code.C_EC_INVALID_ARGS,
                                  cause="Invalid format of time, must be with format 'yyyy/mm'")
        if startTime >= endTime:
            raise CustomHTTPError(400,
                                  error_code.C_EC_INVALID_ARGS,
                                  cause="Invalid range of time")
        args["startTime"] = startTime
        args["endTime"] = endTime
        args["webchatId"] = self.get_argument("webchat_id")
        env.clientAgent.mate_register(args)
