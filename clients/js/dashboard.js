var missile = function(cmd,val) {
    var input = $('#alturl').val();
    var suffix = input === '' ? '../' : input;
    $.get(suffix+"hardware/missile/missile_cmd.php?cmd=" + cmd + "&val=" + val, function(d){
        console.log(d);
    });
};

var send = function () {
    var address = $("#address option:selected").val();
    var cmd = $("#cmd option:selected").val();
    var del = $('#del').val();
    var bri = $('#bri').val();
    var rgb = $('#rgb').val();
    var tout = $('#tout').val();

    var R = hexToR(rgb);
    var G = hexToG(rgb);
    var B = hexToB(rgb);

    rgb = R + ',' + G + ',' + B;
    run(address, cmd, del, bri, rgb, tout);
};

var run = function (addr, cmd, del, bri, rgb, tout) {
    var getCmd = "../hardware/lights/lights_cmd.php?cmd=" + cmd + "&del=" + del + "&bri="
        + bri + "&rgb=" + rgb + "&tout=" + tout + '&addr="' + addr + '"';
    console.log('sending command');
    $.get(getCmd, function (d) {
        console.log(d);
    });
};

var pTimeout = 0;

var party = function () {
    var bri = '30';
    run('00 00 00 00 00 00 FF FF', 'P', '50', bri, '255,100,0', '0');

    $.get('../hardware/sound/play_sound_cmd.php?name=/var/www/git/redalert/assets/sounds/gfdr.mp3', function (d) {
        console.log(d);
    });

    clearTimeout(pTimeout);
    pTimeout = setTimeout(function () {
        run('00 00 00 00 00 00 FF FF', 'D', '40', bri, '255,100,0', '0');
    }, 14500);
};

var stop = function () {
    clearTimeout(pTimeout);
    $.get('../hardware/sound/kill_player_cmd.php');
    run('00 00 00 00 00 00 FF FF', 'O', '50', '0', '255,100,0', '1');
};

function hexToR(h) {
    return parseInt((cutHex(h)).substring(0, 2), 16)
}
function hexToG(h) {
    return parseInt((cutHex(h)).substring(2, 4), 16)
}
function hexToB(h) {
    return parseInt((cutHex(h)).substring(4, 6), 16)
}
function cutHex(h) {
    return (h.charAt(0) == "#") ? h.substring(1, 7) : h
}