var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {
    $scope.total = 10;

    var refresh = function () {
        $.get('../utilities/get_timeline.php', function (d) {
            var evts = JSON.parse(d);
            $scope.events = evts.reverse();
            $scope.$apply()
        });
    }

    $(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() > $(document).height()) {
            console.log('loading more');
            if($scope.events.length >= $scope.total + 10){
                $scope.total += 10;
            }
            else if($scope.events.length >= $scope.total){
                $scope.total = $scope.events.length;
            }else{
                console.log('ignoring')
            }
        }
    });

    refresh();
    setInterval(refresh, 2000);
});