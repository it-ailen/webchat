# coding: utf-8
import weixinhandlers
import tornado.web
import os
import logging

curDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(curDir))

print "path::::", os.path.join(srcDir, "assets")

# class FileWrapperHandler(tornado.web.StaticFileHandler):
#     def get(self, path, include_body=True):
#         logging.debug("path: %s", path)
#         return super(FileWrapperHandler, self).get(path, include_body=include_body)

entries = [
    (r"^/webchat/?$", weixinhandlers.WebChatHandler),
    (r"^/webchat/menu/?$", weixinhandlers.WebChatMenuHandler),

    (r"^/mates/?$", weixinhandlers.MatesHandler),

    (r"^/assets/(.+)", tornado.web.StaticFileHandler, {
        "path": os.path.join(srcDir, "assets")
    })
]