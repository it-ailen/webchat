/**
 * Created by AilenZou on 2016/8/4.
 */
"use strict";

require("angular");
require("angular-route");

require("./partial/console/activities/list.html");


var app = angular.module("console", [
    "ngRoute"
]);

app
    .controller("activities.list", require("./c/console/activities_list"))
;


app
    .config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when("/activities/list",
                {
                    controller: "activities.list",
                    templateUrl: "partial/console/activities/list.html"
                })
            .when("/", {
                redirectTo: "/activities/list"
            })
        ;
    })
;


module.exports = app;
