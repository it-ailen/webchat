# coding: utf-8

from http import BaseHandler, CustomHTTPError, error_code
import hashlib
import env


class AuthHandler(BaseHandler):
    def check_signature(self, signature, timestamp, nonce, token):
        L = [token, timestamp, nonce]
        L.sort()
        s = L[0] + L[1] + L[2]
        return hashlib.sha1(s).hexdigest() == signature

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
                                  cause="Invalid request from fake WeiXin")