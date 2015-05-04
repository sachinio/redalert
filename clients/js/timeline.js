var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {
    $scope.show = 10;
    var maxScrollTop = 0;

    var refresh = function () {
        $.get('../utilities/get_timeline.php', function (d) {
            var events = JSON.parse(d);
            $scope.events = process(events.reverse());
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

    var process = function(events){
        var expression = new RegExp(
            "(^|[ \t\r\n])((ftp|http|https|gopher|mailto|news|nntp|telnet|wais|file|prospero|aim|webcal):(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-]))"
            ,"g"
        );

        for(var i=0;i<events.length;i++){
            var uri = events[i].content.match(expression);
            if(uri){
                events[i].uri = uri;

                console.log(uri);
            }
        }

        return events;
    }
});