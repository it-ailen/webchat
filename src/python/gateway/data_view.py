# coding: utf-8


def formalize_activity(act):
    res = act
    res["detail_link"] = "/assets/activities/detail.html?id=%s" % act._id
    return res