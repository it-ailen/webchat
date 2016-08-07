/**
 * Created by AilenZou on 2016/8/7.
 */

"use strict";

function get_url_param(searchStr, name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = searchStr.substr(1).match(reg);
    if (r != null) return r[2];
    return null;
}


module.exports = {
    get_url_param: get_url_param
};