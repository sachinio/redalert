var timelineApp = angular.module('timelineApp', []);

timelineApp.controller('TimelineCtrl', function ($scope) {

$.get('../utilities/get_timeline.php', function(d){
    var evts = JSON.parse(d);
    $scope.events = evts;
    $scope.$apply()
});

 /*$scope.events = [
    {
        'title': 'Build break!',
        'content': 'Pedram broke the build',
        'timeStamp': 'April 24th 2015',
        'icon': 'fa-ambulance',
        'iconBackground': 'danger',
        'by':'Mona'
    },
    {
        'title': 'Exec review',
        'content': 'Satya just saw the new branding and he loved it!!!',
        'timeStamp': 'April 23th 2015',
        'icon': 'fa-bullhorn',
        'iconBackground': 'info',
        'by': 'Diego'
    },
    {
        'title': 'Team Meeting @ 3pm',
        'content': 'Make sure you attend!',
        'timeStamp': 'April 22th 2015',
        'icon': 'fa-users',
        'iconBackground': 'info',
        'img':'http://www.online-image-editor.com//styles/2014/images/example_image.png',
        'by':'Nick'
    },
    {
        'title': 'Awesome D3 video',
        'content': 'watch @ www.youtube.com',
        'timeStamp': 'April 21th 2015',
        'icon': 'fa-graduation-cap',
        'iconBackground': 'success',
        'by':'Nick'
    },
  ]*/
});