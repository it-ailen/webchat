/**
 * Created by AilenZou on 2016/8/4.
 */
"use strict";

require("angular");
// require("mobile-angular-ui");
require("angular-route");

require("./partial/register.html");


var app = angular.module("mates.register", [
    // "mobile-angular-ui",
    // "mobile-angular-ui.gestures",
    "ngRoute"
]);

app
    .controller("form.controller", require("./c/register/form-ctrl"))
;


app
    .config(function ($routeProvider) {
        $routeProvider
            .when("/",
                {
                    controller: "form.controller",
                    templateUrl: "partial/register.html"
                })
        ;
    })
;


module.exports = app;
