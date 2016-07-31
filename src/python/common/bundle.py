# coding: utf-8
'''
@author: AilenZou
'''
import logging
import collections
import json


class Bundle(object):
    def __init__(self, attrs):
        # self.__dict__.update(attrs)
        self.items = dict(attrs)

    def has(self, key):
        # return key in self.__dict__
        return key in self.items

    def isEmpty(self):
        # return len(self.__dict__.keys()) == 0
        return len(self.items.keys()) == 0

    def json(self):
        res = {}
        for k, v in self.items.items():
            if isinstance(v, Bundle):
                res[k] = v.json()
            elif isinstance(v, (list, tuple)):
                res[k] = []
                for each in v:
                    if isinstance(each, Bundle):
                        res[k].append(each.json())
                    else:
                        res[k].append(each)
            else:
                res[k] = v
        return res

    def __str__(self):
        return json.dumps(self.json(), ensure_ascii=False)

    def __getitem__(self, item):
        try:
            return self.items[item]
        except:
            raise AttributeError("No `%s` in Bundle" % item)

    def __getattr__(self, item):
        try:
            return self.items[item]
        except:
            raise AttributeError("No `%s` in Bundle" % item)

    @classmethod
    def build(cls, **attrs):
        return cls.build_from_dict(attrs)

    @classmethod
    def build_from_dict(cls, attrs):
        kvs = {}
        for k, v in attrs.items():
            if isinstance(v, dict):
                kvs[k] = cls.build_from_dict(v)
            elif isinstance(v, collections.OrderedDict):
                kvs[k] = cls.build_from_dict(dict(v))
            elif isinstance(v, (tuple, list)):
                kvs[k] = []
                for each in v:
                    if isinstance(each, dict):
                        kvs[k].append(cls.build_from_dict(each))
                    else:
                        kvs[k].append(each)
            else:
                logging.info("%s %s", v, type(v))
                kvs[k] = v
        return cls(kvs)

