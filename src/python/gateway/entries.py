# coding: utf-8
import weixinhandlers

entries = [
    (r"^/weixin/auth/?$", weixinhandlers.AuthHandler),
]