/**
 * Created by AilenZou on 2016/8/5.
 */

function routine($scope, $http) {
    $scope.submit = function() {
        var data = {};
        angular.forEach($scope.form, function(value, key) {
            if (key[0] == '$') {//skip
                return;
            }
            if (value.$dirty) {
                // fd.append(key, value.$modelValue);
                data[key] = value.$modelValue;
            }
        });
        console.log(data);
        var req = {
            url: "/mates",
            method: "PUT",
            data: data
        };
        $http(req)
            .then(function(res) {
                console.log(res);
            })
            .catch(function(error) {
                console.log(error);
            })
        ;
    };
}

module.exports = [
    "$scope",
    "$http",
    routine
];
