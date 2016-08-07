# coding: utf-8

import tornado.web
import tornado.escape
import error_code
import json
import logging


class CustomHTTPError(tornado.web.HTTPError):
    def __init__(self, status_code, error_code, cause=None, log_message=None, *args, **kwargs):
        super(CustomHTTPError, self).__init__(status_code, log_message, *args, **kwargs)
        self.error_code = error_code
        self.cause = cause


class BaseHandler(tornado.web.RequestHandler):
    C_KEY_ERROR = "error"
    C_KEY_CAUSE = "cause"

    def _encode(self, data):
        res = {}
        for k, v in data.items():
            if isinstance(k, unicode):
                k = k.encode("utf-8")
            if isinstance(v, unicode):
                v = v.encode("utf-8")
            elif isinstance(v, dict):
                v = self._encode(v)
            res[k] = v
        return res

    def prepare(self):
        try:
            jsonData = tornado.escape.json_decode(self.request.body)
        except:
            logging.exception("Invalid json body")
            return
        self.request.arguments.update(self._encode(jsonData))

    def write_error(self, status_code, **kwargs):
        if "exc_info" in kwargs:
            _, err, _ = kwargs["exc_info"]
            if isinstance(err, CustomHTTPError):
                res = {
                    self.C_KEY_ERROR: err.error_code,
                    self.C_KEY_CAUSE: err.cause,
                }
            elif isinstance(err, tornado.web.MissingArgumentError):
                res = {
                    self.C_KEY_ERROR: error_code.C_EC_ARG_MISSING,
                    self.C_KEY_CAUSE: err.log_message,
                }
            elif isinstance(err, tornado.web.HTTPError):
                res = {
                    self.C_KEY_ERROR: error_code.C_EC_UNKNOWN,
                    self.C_KEY_CAUSE: err.log_message,
                }
            else:
                res = {
                    self.C_KEY_ERROR: error_code.C_EC_UNKNOWN,
                    self.C_KEY_CAUSE: "Unknown",
                }
            self.write(res)
            return
        super(BaseHandler, self).write_error(status_code, **kwargs)

    def write(self, trunk):
        data = trunk
        if isinstance(trunk, (list, tuple)):
            data = json.dumps(trunk, ensure_ascii=False)
        super(BaseHandler, self).write(data)

    _CUSTOM_ARG_DEFAULT = []

    def get_bool_argument(self, name, default=_CUSTOM_ARG_DEFAULT):
        args = self.get_arguments(name)
        if not args:
            if default is self._CUSTOM_ARG_DEFAULT:
                raise tornado.web.MissingArgumentError(name)
            if default is not None and not isinstance(default, bool):
                raise TypeError("Default must be boolean.")
            return default
        value = args[0].lower()
        if value == "null":
            return None
        elif value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise CustomHTTPError(400,
                                  error_code.C_EC_ARG_TYPE_WRONG,
                                  cause="Type of `%s` must be boolean" % name)

    def get_long_argument(self, name, default=_CUSTOM_ARG_DEFAULT):
        args = self.get_arguments(name)
        if not args:
            if default is self._CUSTOM_ARG_DEFAULT:
                raise tornado.web.MissingArgumentError(name)
            return default
        try:
            if args[0].lower() == "null":
                return None
            return long(args[0])
        except (ValueError, TypeError):
            raise CustomHTTPError(400,
                                  error_code.C_EC_ARG_TYPE_WRONG,
                                  cause="Type of `%s` must be long" % name)