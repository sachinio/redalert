var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {
    $scope.show = 10;

    var refresh = function () {
        $.get('../utilities/get_timeline.php', function (d) {
            var evts = JSON.parse(d);
            $scope.events = evts.reverse();
            $scope.$apply()
        });
    }

    /*$(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() > $(document).height()) {
            console.log('loading more');
            if($scope.events.length >= $scope.show + 10){
                $scope.show += 10;
            }
            else if($scope.events.length >= $scope.total){
                $scope.show = $scope.events.length;
            }else{
                console.log('ignoring')
            }

            $scope.$apply();
        }
    });*/

    refresh();
    setInterval(refresh, 2000);
});