/**
 * Created by AilenZou on 2016/8/7.
 */

"use strict";

var tools = require("../tools");


function routine($scope, $http, $q) {
    function load(lastId) {
        var defer = $q.defer();
        var req = {
            url: "/activities",
            method: "GET"
        };
        if (lastId) {
            req.params = {
                "last": lastId
            }
        }
        $http(req)
            .then(function(res) {
                for (var i = 0; i < res.data.length; i++) {
                    $scope.activities.push(res.data[i]);
                }
            })
    }
    $scope.activities = [];
    load();
}

module.exports = routine;
