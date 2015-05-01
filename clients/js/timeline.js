var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {
    $scope.show = 10;
    var maxScrollTop = 0;

    var refresh = function () {
        $.get('../utilities/get_timeline.php', function (d) {
            var events = JSON.parse(d);
            $scope.events = events.reverse();
            $scope.$apply();
        }).always(function(){
            setTimeout(refresh, 2000);
        })
    };

    $(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
            if($scope.events.length >= $scope.show){
                if($(window).scrollTop() > maxScrollTop) {
                    maxScrollTop = $(window).scrollTop();
                    $scope.show += 10;
                }
            }
        }
    });

    refresh();
});