/**
 * Created by AilenZou on 2016/8/7.
 */


function routine($scope, $q, $http) {
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
