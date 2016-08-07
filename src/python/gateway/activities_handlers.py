# coding: utf-8

from http import BaseHandler, CustomHTTPError, error_code
import logging
import env
import data_view
import datetime


class ActivitiesHandler(BaseHandler):
    def get(self):
        al = env.clientAgent.activities_get()
        self.write([data_view.formalize_activity(a) for a in al])

    def post(self):
        title = self.get_argument("title")
        content = self.get_argument("content")
        cover = self.get_argument("cover")
        apply_begin = self.get_long_argument("apply_begin")
        apply_deadline = self.get_long_argument("apply_deadline")
        activity_time = self.get_long_argument("activity_time")
        try:
            apply_begin = datetime.datetime.utcfromtimestamp(apply_begin / 1000)
            apply_deadline = datetime.datetime.utcfromtimestamp(apply_deadline / 1000)
            activity_time = datetime.datetime.utcfromtimestamp(activity_time / 1000)
        except:
            raise CustomHTTPError(400,
                                  error_code.C_EC_INVALID_ARGS,
                                  cause="Invalid timestamp.")
        address = self.get_argument("address")
        args = {
            "title": title,
            "content": content,
            "cover": cover,
            "apply_begin": apply_begin,
            "apply_deadline": apply_deadline,
            "activity_time": activity_time,
            "address": address
        }
        actId = env.clientAgent.activities_create(args)
        self.write({
            "id": str(actId)
        })
