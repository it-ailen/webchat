# coding: utf-8
import common
import logging
from lxml import etree


class UnknownHello(Exception):
    def __init__(self, key):
        self.key = key


class ClientAgent(object):
    def __init__(self, autoResponse):
        self.auto = common.Bundle.build_from_dict(autoResponse)

    def handle_text(self, *msgs):
        if msgs[0] == "?":
            return self.list_all_auto_response()
        lastLevel = self.auto
        for msg in msgs:
            try:
                lastLevel = lastLevel[msg]
            except:
                raise UnknownHello(msg)
        text = u""
        if lastLevel.type == "directory":
            if lastLevel.has("text"):
                text += lastLevel.text
            for k, v in lastLevel.directory.items.items():
                text += k
        elif lastLevel.type == "text":
            return lastLevel.text

    def list_all_auto_response(self):
        textPieces = []
        for k, v in self.auto.items.items():
            if isinstance(k, unicode):
                textPieces.append(k.encode("utf-8"))
            else:
                textPieces.append(k)
            if v.has("text"):
                if isinstance(v.text, unicode):
                    textPieces.append(v.text.encode("utf-8"))
                else:
                    textPieces.append(v.text)
            textPieces.append("\n")
        return "".join(textPieces)

    def parse_xml_msg(self, src):
        data = etree.fromstring(src)
        logging.info(data)
        logging.info("ToUserName: %s", data.find("ToUserName").text)
        msg = {
            "ToUserName": data.find("ToUserName").text,
            "FromUserName": data.find("FromUserName").text,
            "CreateTime": long(data.find("CreateTime").text),
            "MsgType": data.find("MsgType").text,
            "Content": data.find("Content").text,
            "MsgId": data.find("MsgId").text
        }
        return common.Bundle.build(**msg)


