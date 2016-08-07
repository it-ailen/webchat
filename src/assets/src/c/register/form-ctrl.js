/**
 * Created by AilenZou on 2016/8/5.
 */

"use strict";

function get_url_param(searchStr, name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = searchStr.substr(1).match(reg);
    if (r != null) return r[2];
    return null;
}

function routine($scope, $http, $location) {
    console.log(location)
    $scope.error = null;
    $scope.status = "normal";
    // var query = $location.search();
    // console.log($location.path());
    // console.log(query);
    // console.log(query.webChatId);
    var webChatId = get_url_param(location.search, "webChatId");
    console.log("webChatId=" + webChatId);
    $scope.submit = function() {
        $scope.error = null;
        var fd = new FormData();
        fd.append("webchat_id", webChatId);
        angular.forEach($scope.form, function(value, key) {
            if (key[0] == '$') {//skip
                return;
            }
            console.log("key: " + key);
            fd.append(key, value.$modelValue);
        });
        var req = {
            url: "/mates",
            method: "PUT",
            data: fd,
            headers: {"Content-Type": undefined}
        };
        $http(req)
            .then(function(res) {
                console.log(res);
                $scope.status = "success";
            })
            .catch(function(error) {
                console.log(error);
                var body = error.data;
                $scope.error = (body && (body.cause || body.error)) || "unknown";
            })
        ;
    };
}

// module.exports = [
//     "$scope",
//     "$http",
//     "$location",
//     routine
// ];
module.exports = routine;
