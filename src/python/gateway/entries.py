# coding: utf-8
import weixinhandlers

entries = [
    (r"^/webchat/?$", weixinhandlers.WebChatHandler),
]