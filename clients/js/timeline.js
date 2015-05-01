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
        var top = $(window).scrollTop();

        if(top + $(window).height() > $(document).height() - 100) {
            if($scope.events.length >= $scope.show){
                if(top > maxScrollTop) {
                    maxScrollTop = top;
                    $scope.show += 10;
                    $scope.$apply();
                }
            }
        }
    });

    refresh();
});