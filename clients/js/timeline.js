var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {

$.get('../utilities/get_timeline.php', function(d){
    var evts = JSON.parse(d);
    $scope.events = evts.reverse();
    $scope.$apply()
});
});