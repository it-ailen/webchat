# coding: utf-8

from http import BaseHandler, CustomHTTPError, error_code
import hashlib
import env
import logging
import requests
import json


class WebChatBaseHandler(BaseHandler):
    C_WEIXIN_CGI = "https://api.weixin.qq.com/cgi-bin"

    C_GRANT_TYPE_CLIENT = "client_credential"

    def check_signature(self, signature, timestamp, nonce, token):
        L = [token, timestamp, nonce]
        L.sort()
        s = L[0] + L[1] + L[2]
        return hashlib.sha1(s).hexdigest() == signature

    def fetch_access_token(self, type=C_GRANT_TYPE_CLIENT):
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


class WebChatMenuHandler(WebChatBaseHandler):
    def post(self):
        accessToken = self.fetch_access_token()
        menu = env.configMgr.get("menu")
        logging.info(menu)
        data = json.dumps(menu, ensure_ascii=False)
        try:
            resp = requests.post(self.C_WEIXIN_CGI + "/menu/create?access_toke=" + accessToken,
                                 data=data)
            res = resp.json()
            if res["errcode"] != 0:
                raise Exception("Wrong response from WebChat: %s" % resp.body)
        except:
            logging.exception("Fail to create menu")
            raise CustomHTTPError(503,
                                  error_code.C_EC_UNKNOWN,
                                  cause="WebChat has gone")
