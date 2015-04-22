var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {

    var refresh = function(){
        $.get('../utilities/get_timeline.php', function(d){
            var evts = JSON.parse(d);
            $scope.events = evts.reverse();
            $scope.$apply()
        });
    }

    refresh();
    setInterval(refresh, 2000);
});