var send = function(){
    var addr = $("#addr option:selected").val();
    var cmd = $("#cmd option:selected").val();
    var del = $('#del').val();
    var bri = $('#bri').val();
    var rgb = $('#rgb').val();
    var tout = $('#tout').val();

    R = hexToR(rgb);
    G = hexToG(rgb);
    B = hexToB(rgb);

    rgb = R+','+G+','+B;
    run(addr,cmd,del,bri,rgb,tout);
}

var run = function(addr, cmd, del, bri, rgb, tout) {
    var getCmd = "../../lights/lights_cmd.php?cmd=" + cmd + "&del=" + del + "&bri="
            + bri + "&rgb=" + rgb + "&tout=" + tout+ "&addr=" + addr;
    console.log(addr+' '+cmd+' '+del+' '+bri+' '+rgb+' '+tout);
    $.get(getCmd, function(d){
        console.log(d);
    });
}

function hexToR(h) {return parseInt((cutHex(h)).substring(0,2),16)}
function hexToG(h) {return parseInt((cutHex(h)).substring(2,4),16)}
function hexToB(h) {return parseInt((cutHex(h)).substring(4,6),16)}
function cutHex(h) {return (h.charAt(0)=="#") ? h.substring(1,7):h}