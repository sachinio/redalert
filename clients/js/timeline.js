var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {
    $scope.show = 10;
    var maxScrollTop = 0;

    var refresh = function () {
        $.get('../utilities/get_timeline.php', function (d) {
            var evts = JSON.parse(d);
            $scope.events = evts.reverse();
            $scope.$apply()
        });
    };

    $(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
            if($scope.events.length >= $scope.show){
                if($(window).scrollTop() > maxScrollTop) {
                    maxScrollTop = $(window).scrollTop();
                    $scope.show += 10;
                    $scope.$apply();
                    console.log('loading more');
                }
            }
            else{
                console.log('ignoring')
            }
        }
    });

    refresh();
    setInterval(refresh, 2000);
});