var timeoutId = 0;
var angleV = 80;
var angle = 80;
var isCamOn = false;

var makeServoCall = function(a,s){
    $.get("../camera/servo_cmd.php?angle="+a+"&sno="+s, function(output){
        console.log('servo_cmd output: '+ output);
    });
};

var makeCamCall = function(state){
    $.get("../camera/cam_cmd.php?on="+state, function(output){
        console.log('cam_cmd output: '+ output);
    });
}

var center = function(){
    angle = 80;
    angleV = 80;
    send(1,1);
    send(0,1);
}

var record = function(){
    var state = $('#record').attr('record');
    var cmd;
    if(state === 'false'){
        $('#record').attr('record','true');
        $('#record').text('Stop Recording');
        cmd = "ca 1";
    }else{
        $('#record').attr('record','false');
        $('#record').text('Start Recording');
        cmd = "ca 0";
    }

    $.get("../camera/pipe_cmd.php?cmd="+cmd,function(){
        console.log("written to PIPE");
    });
}

var send = function(s,p){
    var a = 0;
    if(s === 1){
        if(p==1) {
            a = angleV += 10;
        }else{
            a = angleV -= 10;
        }
    }else{
        if(p==1) {
            a = angle += 10;
        }else{
            a = angle -= 10;
        }
    }

    a = Math.max(s===1?10:0, a);
    a = Math.min(s===1?170:180, a);

    makeServoCall(a,s);
}

var toggleCam = function () {
    var checked = $('.camButton').attr('checked');
    if(checked){
        $('.camButton').attr('checked', false);
        clearTimeout(timeoutId);
        isCamOn = false;
        makeCamCall(0);
    }else{
        $('.camButton').attr('checked', true);
        isCamOn = true;
        makeCamCall(1);
        getPic();
    }
}

var getPic = function(){
    if(isCamOn) {
        $("#cam").attr("src", "../../ram/cam.jpg?" + new Date().getTime());
        timeoutId =  setTimeout(getPic,parseInt($('#slider').val()));
    }
}

center();
