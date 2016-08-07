/**
 * Created by AilenZou on 2016/8/7.
 */
"use strict";

require("angular");


var app = angular.module("activities.list", [
]);

app
    .controller("activities.list", require("./c/activities/list"))
;



module.exports = app;
